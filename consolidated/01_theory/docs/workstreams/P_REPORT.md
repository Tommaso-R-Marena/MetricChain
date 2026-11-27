# Workstream P — chains: envelopes from pair-distance profiles (transport envelopes)

Directory: `scratch:ws/P/`
(all scripts, outputs `out_*.txt`, this report; nothing in the repository was modified; no Lean).
Scope: idealised synthetic chains only (fixed bond length and angle, three rotameric torsion states,
made-up bead-type sequences and energies); no biological sequences, no design.

Status tags: **[P]** proved here (complete paper proof), **[P+cite]** proved from a cited theorem,
**[N]** numerical (own Python code, commands in §7), **[C]** conjecture / heuristic.
"Known" = I can name the standard result it is; "new" = apparently not stated before (after the
searches of §4), never a claim of depth.

Contents: 0 setting · 1 verdicts · 2 statements and proofs · 3 numerics · 4 prior art and search log ·
5 not settled · 6 next steps · 7 files, commands, outputs.

---

## 0. Setting and conventions

* Chain: beads `0..N−1`, `N = n+3`, `n` torsions with states `t, g⁺, g⁻` (`180°, ±60°`).  Two geometries:
  **dia** = diamond-lattice chain (tetrahedral angle, bond vector `(1,1,1)`; all squared distances are
  integers: bonded 3, 1–3 pairs 8, 1–4 pairs 19 (`t`) / 11 (`g`)); **gen** = generic chain (`b = 1`,
  `θ = 111°`; 1–4 squared distances 6.433 (`t`) / 3.819 (`g`); irrational, generically distinct
  distances).  Excluded volume: **dia** self-avoiding; **gen** hard core `s_pq ≥ 3.0` for `q−p ≥ 3`
  (this removes the `g⁺g⁻` sequences, whose 1–5 squared distance is 2.92).  "Phantom" = the full
  product domain `3ⁿ`.
* Pairs: `𝒫 = {(p,q): q−p ≥ 3}` (pairs with `q−p ≤ 2` have conformation-independent distances and
  would only add a constant).  `s_pq(x)` squared distance, `s̃ = min(s, S_c)`.  Type pair of a pair:
  the unordered pair of bead types, `t ∈ [T]`, `T ≤ A(A+1)/2` for an alphabet of size `A`.
* Class `P_L`: `g_φ(x) = Σ_{(p,q)∈𝒫} φ_{t(p,q)}(s_pq(x))`, each `φ_t` `L`-Lipschitz on `[0,∞)`, `φ_t = 0` on
  `[S_c,∞)`.  Profile `N^x_t(s) = #{(p,q) of type t : s_pq(x) ≤ s}`, `0 ≤ s < S_c`, an element of
  `𝓛 = L¹([0,S_c)×[T])`, `‖u‖₁ = Σ_t ∫₀^{S_c}|u_t|`; `⟨ψ,u⟩ = Σ_t∫ψ_t u_t`.  `K_N = {N^x : x ∈ X_N}`.
* **z-condition**: every conformation has at most `zN/2` pairs of `𝒫` inside the cutoff (true with
  excluded volume, `z ≤` a packing number; false for phantom chains as `N → ∞`).
* Formats compared (same instance `E = f + g`, `g ∈ P_L`):
  **H** weighted torsion-Hamming envelope `Σ_i c_i[x_i≠y_i]` with constants valid for `P_L`;
  **P** the profile envelope `d_P(x,y) = L‖N^x − N^y‖₁` and its first-order class
  `Lip(d_P) = {g : g(x) − g(y) ≤ d_P(x,y)}`; **S** the class `P_L` itself ("span certificates").
  `N^H_cov, N^P_cov, N^S_cov` are the covering numbers that equal the certificate size up to `+1`
  (theory report Thm 11.4 for H, P; Theorem 4 below for S).
* Known part in the numerics: `f = e·#gauche`, `e = 1` (minimiser all-trans); `β = 1` for `ln Z`.
  Cutoffs: **dia** `S_c = 12` (distances 3, 8, 11 below the cutoff: `D = 3`) and `S_c = 28` (`D = 7`);
  **gen** `S_c = 16`.

---
## 1. Verdicts in one paragraph

**P1 confirmed** (two-line proof; the identity checked in exact integer arithmetic on all `3ⁿ`
conformations, `n ≤ 10`); it is the configurational energy equation after one integration by parts.
**P2 confirmed**; equivalent closed form: `d_P(x,y) = L Σ_t ‖sort(s̃^x_t) − sort(s̃^y_t)‖_{ℓ¹}`, the
1-Wasserstein distance between the multisets of truncated squared distances (Kantorovich–Rubinstein
duality in one dimension).  **P3: the formula is confirmed** (LP duality; primal = dual as an
identity of rationals on 288 lattice instances and to `10⁻¹⁰` on 12 960 instances), **but its
parenthesis is corrected**: the bracket half-width is *at most* `L·dist₁(N^y, span)`, with equality
at the zero data; in general the two one-sided slacks are *asymmetric weighted* `L¹` distances to the
span, with weights `L ∓ φ*′`, and the bracket can collapse to a point although `N^y` is not in the
span (explicit instance).  **P4: (a) confirmed and sharpened** — no logarithm,
`ln N^P_cov(ε₁N) ≤ 1.39·T·⌈4zLS_c/ε₁⌉` for every instance; but the bound is astronomically loose
(216 nats against a measured 2.5 in the simplest model), and at enumerable sizes (`N ≤ 16`) the
normalised entropy still grows with `N` in every model except the three-feature lattice one, where
it saturates (`m(δ=1) = 10–12` for `N = 13…16`; sampled families up to `N = 960`: 15–18).
**(b) confirmed with exponent 2**: `N^S_cov(ε₁N) ≤ (8(1+κ)TzLS_c/ε₁)²` (greedy theorem in `L²` plus
Cauchy–Schwarz); measured greedy widths decay like `4/m` per bead, and lower bounds are linear in
the number of features.  **(c) the last sentence of P4 is refuted as stated**: on a lattice the
first-order class of `d_P` is *polynomial* in `N` at every accuracy, including `ε = 0`
(`N^P_cov ≤ #profiles ≤ C(zN/2+DT, DT)`), and off-lattice it is at most stretched-exponential,
`exp(O(√(TλN ln n)))`, for a gapped site-additive known part at the zero residual; what one *sees*
off-lattice for `n ≤ 10` at `L = e` is growth by a factor 1.5–1.9 per torsion.  The span certificate
is polynomial, as claimed (`≤ rank`; `≤ (16TzLS_cN/ε)²`).  **P5 corrected**: the metric is right and
the first-order format is exponential (proved on the product domain), but in the span format
pair-specific residuals cost between `n − 2ε/(Lδ₁₄)` (proved) and the rank `O(N²)` — polynomial, not
exponential; the governing quantity is the **number of independent features** (type pairs ×
resolvable distances): span cost ∝ features, first-order cost ∝ exp(features), and the chain length
enters only through the number of features.  **Measured on the same instances** (`f = #gauche`,
zero residual, `L = e`, exact certification of the minimum): at `n = 12` on the lattice, H needs
`≥ 2.2·10⁵` of the 422 825 conformations (×2.9–3.0 per torsion, also at the extensive accuracy `N/2`),
P needs 21 (≈ +2 per torsion), S needs 2 (never more than the rank 3); off-lattice at `n = 10`: H
`≥ 5 539` of 8 115, P 318, S between 3 and 10; for `ln Z` (`ε = 0.01`, lattice `n = 8`): H all 5 849, P
between 10 and 69, S exactly 3.  **Most important negative finding**: the chain-length independence
is a property of the *exactly* pair-additive, transferable class, not of chains.  With a remainder
`r` in a first-order class `η·d₀` the two slacks add (Corollary 15:
`σ_sum ≥ σ_span,aff + s_{ηd₀}`, hence `N^{sum}_cov ≥ max(N^S_cov, N^{ηd₀}_cov)`), the exact bracket acquires
a Kantorovich–Rubinstein term that is at least `η·d₀(y, A)`, and with `d₀` a torsion-Hamming
envelope this reinstates the exponential cost of D42 in proportion to `η` (measured: the
certificate of a 683-state chain grows from 2 to 20 as `η` goes from 0 to the remainder's own
sharpness threshold).  Second negative finding: with a purely torsional known part no format has
a chain-length-independent *one-evaluation* threshold (a hairpin of 3 gauche torsions changes the
profile by an amount `∝ N`); the formats differ in what happens beyond that threshold.

---
## 2. Precise statements, with proofs or counterexamples

### 2.1 The three identities (P1–P3)

**Proposition 1 (P1) [P; known].**  For `g_φ ∈ P_L` and every `x`:
`g_φ(x) = −⟨φ′, N^x⟩ = −Σ_t ∫₀^{S_c} φ_t′(s) N^x_t(s) ds`.  The map `φ ↦ ψ = φ′` is a bijection of the
radial functions of the class onto `{ψ ∈ L^∞([0,S_c)×[T]) : ‖ψ‖_∞ ≤ L}`; hence
`P_L = {x ↦ −⟨ψ, N^x⟩ : ‖ψ‖_∞ ≤ L}`, the image of an `L^∞` ball under a linear map.

*Proof.*  A Lipschitz `φ_t` is absolutely continuous with `|φ_t′| ≤ L` a.e. and `φ_t(S_c) = 0`, so for
`s₀ < S_c`: `φ_t(s₀) = −∫_{s₀}^{S_c} φ_t′ = −∫₀^{S_c} φ_t′(s)·1[s₀ ≤ s] ds`, and `φ_t(s₀) = 0` for
`s₀ ≥ S_c`.  Sum over the pairs of type `t`: `Σ 1[s_pq ≤ s] = N^x_t(s)`.  Conversely every measurable
`ψ` with `‖ψ‖_∞ ≤ L` is `φ′` for `φ_t(s) = −∫_s^{S_c} ψ_t`. ∎

**Proposition 2 (P2) [P; Kantorovich–Rubinstein duality in one dimension].**
`d_P(x,y) := sup_{g∈P_L}(g(x) − g(y)) = L‖N^x − N^y‖₁`, attained at `ψ = −L·sgn(N^x − N^y)`.
Moreover, with `q^x_t ∈ ℝ^{P_t}` the sorted vector of the truncated squared distances `s̃_pq(x)` of
the `P_t` pairs of type `t`,

    d_P(x,y) = L Σ_t ‖q^x_t − q^y_t‖_{ℓ¹} = L · min_π Σ_{(p,q)} |s̃_pq(x) − s̃_{π(p,q)}(y)|  ≤  L Σ_{(p,q)} |s̃_pq(x) − s̃_pq(y)|,

the minimum over the bijections `π` of `𝒫` that preserve the type pair.  `d_P` is a pseudometric,
invariant under rigid motions and reflections (and, for palindromic type sequences, chain
reversal); it vanishes exactly between conformations with equal profiles ("homometric" ones).

*Proof.*  The first formula is the duality `(L¹)* = L^∞`.  For the second: both conformations have
the same number `P_t` of pairs of each type (fixed sequence), the profile is the counting
distribution function of the multiset `{s̃_pq}` restricted to `[0,S_c)`, and for two multisets of
equal size on the line `∫|F − G| = ‖sort − sort‖_{ℓ¹}` = the optimal matching cost (the quantile
form of `W₁`). ∎  So "free boundary at the cutoff" is the same as "truncate the distances at the
cutoff".  The right-hand inequality compares with the envelope of the pair-specific class of P5
(identity matching).

**Proposition 3 (P3; conditioning) [P; optimal recovery = LP duality].**  Let `g = g_{ψ*}` be
evaluated at `a₁,…,a_m`, `v_i = g(a_i)`.  For every `y`,

    U_A(y) := sup{ g′(y) : g′ ∈ P_L, g′(a_i) = v_i }  =  min_{λ∈ℝ^m} [ λ·v + L ‖N^y − Σ_i λ_i N^{a_i}‖₁ ],
    Lo_A(y) := inf{ … }                                  =  max_{λ∈ℝ^m} [ λ·v − L ‖N^y − Σ_i λ_i N^{a_i}‖₁ ],

both attained (`λ` is unconstrained; `λ = e_i` is McShane's bound, `λ = 0` the a-priori bound
`L‖N^y‖₁`).  In terms of the true slopes, with `V_A = span{N^{a_i}}`,

    σ⁺_A(y) := U_A(y) − g(y)  = min_{u∈V_A} ∫ [ (L+ψ*)(N^y−u)₊ + (L−ψ*)(N^y−u)₋ ],
    σ⁻_A(y) := g(y) − Lo_A(y) = min_{u∈V_A} ∫ [ (L−ψ*)(N^y−u)₊ + (L+ψ*)(N^y−u)₋ ]

(integrals over `[0,S_c)×[T]`).  Consequently, if `|ψ*| ≤ κL`,
`(1−κ)L·dist₁(N^y,V_A) ≤ σ^±_A(y) ≤ (1+κ)L·dist₁(N^y,V_A)`, and always

    U_A(y) − Lo_A(y)  ≤  2L·dist₁(N^y, V_A),   with equality if ψ* = 0 (zero data).

*Proof.*  The profiles of finitely many conformations are step functions on a common finite grid,
so the problem is a finite LP: maximise `−⟨ψ,N^y⟩` over the box `‖ψ‖_∞ ≤ L` subject to
`−⟨ψ,N^{a_i}⟩ = v_i`.  It is feasible (`ψ*`) and bounded, and its dual is
`min_λ λ·v + sup_{‖ψ‖_∞≤L} −⟨ψ, N^y − Σλ_iN^{a_i}⟩ = min_λ λ·v + L‖N^y − Σλ_iN^{a_i}‖₁`.  Insert
`v_i = −⟨ψ*,N^{a_i}⟩` and `g(y) = −⟨ψ*,N^y⟩`: `U − g = min_u [L‖N^y−u‖₁ + ⟨ψ*,N^y−u⟩]`, the first slack
formula; the second follows from the symmetry of the class.  The last line: add the two formulas
with a common `u`. ∎

**Correction to P3 [P + explicit instance].**  The claim "the bracket half-width is the `L¹` distance
from the profile of `y` to the span" holds for the zero data and as an upper bound, not in
general.  Instance (`e1`, exact): phantom diamond chain, `n = 4`, homopolymer, `S_c = 12`, `L = 1`,
`x₁ = (g⁺g⁻g⁺g⁻)` with profile `(1,3,6,10)` on the cells `[0,3),[3,8),[8,11),[11,12)`, `y = (t t t g⁺)`
with profile `(0,0,0,1)`.  If `g(x₁) = 46 = L‖N^{x₁}‖₁` (the extreme value, which forces `ψ ≡ −L`),
the bracket of `g(y)` is the single point `{1}`, while `L·dist₁(N^y, ℝN^{x₁}) = 1`.  Statistics over
random instances (`e1`; 40 instances in each of 324 parameter cells): at `κ = 0` the ratio
half-width/(`L·dist₁`) equals 1 in every instance; at `κ = 0.5` its median is 0.99 but it is `< 1` in
half of the instances (minimum 0.55); at `κ = 1` the minimum is 0.  This is the classical fact that
the radius of information of a linear problem on a balanced convex set is attained at the zero
information; the data-dependent (local) radius is smaller.  For the complexity theory the
correction matters: the object that replaces the slack quasi-metric of the first-order theory is
not `L·dist₁` but the pair of gauges `σ^±`.

### 2.2 Certificates in the span format: coverings by subspaces

Let `𝒢_A(g) = {g′ ∈ P_L : g′ = g on A}`.  *Value certificate*: the numbers `min(f+g′)`, `g′ ∈ 𝒢_A(g)`,
lie in an interval of length `≤ ε`.  *Point certificate*: `min_A E − min_y (f + Lo_A)(y) ≤ ε`.

**Theorem 4 (certificates of `P_L` are covers by subspaces) [P; the analogue of theory report
Thm 11.4, routine once Proposition 3 is written with slacks].**  Put
`N^S_cov(ε) = min{|A| : σ⁻_A(y) ≤ gap(y) + ε for all y}`.  Then

    N^S_cov(ε) ≤ N_value(ε) ≤ N_point(ε) ≤ N^S_cov(ε) + 1,

and `N_value(ε)` is the number of evaluations of the best deterministic (adaptive) algorithm that
returns `min E` within `ε/2` for every member of `P_L`, run on the instance `g` (instance-wise
complexity with a hint).  At the zero residual the cover condition reads
`L·dist₁(N^y, span{N^a}_{a∈A}) ≤ gap_f(y) + ε`: every low-energy profile must lie near the *span*
of the evaluated ones; for a general instance the distance is the asymmetric weighted `L¹` gauge
`σ⁻` with weights `L ∓ ψ*`.

*Proof.*  (i) `inf_{g′} min_y (f+g′)(y) = min_y (f+Lo_A)(y)`.  (ii) `sup_{g′} min(f+g′) ≤ min_A E`
(at `a ∈ A` all `g′` agree with `g`); so point ⟹ value.  (iii) value ⟹ cover: `g ∈ 𝒢_A`, hence
`E* − min_y(f+Lo_A)(y) ≤ ε`, i.e. `E(y) − σ⁻_A(y) ≥ E* − ε` for all `y`.  (iv) a cover that contains a
minimiser has `min_A E = E*` and is a point certificate; adding a point only shrinks `σ⁻`.  The
algorithmic statement is the usual indistinguishability argument: on `g` the algorithm evaluates
some `A`; it behaves identically on every `g′ ∈ 𝒢_A(g)`, so its output is within `ε/2` of all their
minima; conversely "evaluate a smallest value certificate of the hinted `g`, return the midpoint if
the answers agree, else enumerate" is correct on the class. ∎

**Corollary 5 (hierarchy) [P].**  For every instance with `g ∈ P_L`, every `f` and `ε`:
`N^S_cov ≤ N^P_cov ≤ N^H_cov` (for any Hamming envelope valid for `P_L`).
*Proof.*  `σ⁻_A(y) ≤ min_{a∈A} s_P(a,y)` (take `u = N^a` in Proposition 3;
`s_P(a,y) = d_P(a,y) − g(a) + g(y)`), and `d_P ≤ d_H` because `d_P` is the support function of the
class. ∎  The price of the smaller class is that the guarantee holds only for residuals in it
(§2.7).

*Two differences from the first-order theory.*  The upper envelope `U_A` is not a member of the
class (a pointwise supremum of linear functionals), so a value certificate is not characterised
by `min(f+U_A) − min(f+Lo_A) ≤ ε`; the theorem therefore goes through `N^S_cov` and `+1`.  And the
slack does combine across evaluations (a span, not a minimum over centres) — which is the whole
gain.  The greedy rule (add the most violated client) is not optimal: lattice, `n = 6`, `L = 0.2`:
greedy from the minimiser returns 2 points, while one evaluation at another profile class is
already a cover (`out_e4_dia12_A1.txt`, brute force).

### 2.3 Finitely many distances (lattices): `O(1)`, polynomial, exponential

**Theorem 6 [P for (a), (b); (c) from theory report Thm 11.37 and numerics].**  Suppose only `D`
distinct squared distances below `S_c` occur in `X_N` (a lattice chain) and at most `M_N` pairs are
inside the cutoff (`M_N ≤ zN/2`).  For every known part `f`:
(a) **S**: `r = rank(K_N) ≤ DT` evaluations determine every `g ∈ P_L` on all of `X_N`; hence
`N^S_cov(ε) ≤ DT` for every `ε ≥ 0`, every functional (minimum, `ln Z` at any `β`), every `N`.
(b) **P**: for every instance in `Lip(d_P)` and every `ε ≥ 0`:
`N^P_cov(ε) ≤ |K_N| ≤ C(M_N + DT, DT) ≤ (zN/2 + 1)^{DT}` — polynomial in `N`, also for exact
certification.
(c) **H**: every valid weighted-Hamming envelope has `c_i ≥ L·c_i^{sf}`, `c_i^{sf}` the largest
profile change by one torsion; `c_i^{sf}` grows with the distance to the chain end (§3.3; the
zipper of theory report §11.14), so certificates are `3^{n−O(√n)}` (Thm 11.37 on product domains;
measured ×2.9–3.0 per torsion on the self-avoiding domain).

*Proof.*  (a) Choose `a₁..a_r` whose profiles are a basis of `span K_N`; every `N^y` is in the span,
so `σ^±_A(y) = 0` by Proposition 3.  (b) Evaluate one representative per profile.  If `N^a = N^y`
then `d_P(a,y) = d_P(y,a) = 0`, so every admissible `g` has `g(a) = g(y)` and `s_P(a,y) = 0 ≤ gap(y)`.
A profile is determined by its jump counts `J_{t,j} ≥ 0` (`t ≤ T`, `j ≤ D`) with sum `≤ M_N`. ∎

Numbers (**dia**, `S_c = 12`, homopolymer, self-avoiding; `e2`, `e4`): 479 profiles among 1 231 221
conformations at `n = 13`; rank 3.  With the *periodic* two-type sequence the rank is 4, not
`DT = 9`: the diamond lattice is bipartite, pairs at odd sequence separation only have
`s ∈ {3, 11}` and pairs at even separation only `s = 8` — `DT` is only an upper bound.

### 2.4 Extensive accuracy: no dependence on the chain length (P4)

**Lemma (entropy of the profile class) [P; the classical entropy of monotone functions with an
explicit constant].**  Let `𝓜(S,M,T)` be the set of `F = (F_t)_{t≤T}`, `F_t ≥ 0` nondecreasing on
`[0,S)`, `Σ_t F_t(S−) ≤ M`.  For every integer `G ≥ 1` there are at most `4^{TG}` functions such
that every `F ∈ 𝓜` is within `‖·‖₁`-distance `2SM/G` of one of them.  Hence
`ln N_ext(𝓜, δ) ≤ T·ln 4·⌈2SM/δ⌉`.

*Proof.*  Put `J = TG`, `q = M/J`.  Round each `F_t` down to a multiple of `q`: error
`≤ T·S·q = SM/G`.  The rounded function has at most `J` jumps of size `q` in total; move every jump
location up to the next point of `(S/G)ℤ` (a jump moved to `S` disappears): each move changes the
function by `q` on a set of measure `≤ S/G`, in total `≤ J q S/G = SM/G`.  The result is a multiset
of at most `J` elements of the `TG` labelled grid positions: at most `C(TG+J, J) = C(2TG, TG) ≤ 4^{TG}`
possibilities. ∎

**Theorem 7 (P4, first part) [P].**  Under the z-condition, for every `f`, every `g ∈ Lip(d_P)` and
every `ε > 0`: `N^P_cov(ε) ≤ 4^{T⌈4zNLS_c/ε⌉}`.  At extensive accuracy `ε = ε₁N`:

    ln N^P_cov(ε₁N) ≤ T · ln 4 · ⌈4 z L S_c / ε₁⌉      for every N.

*Proof.*  `s_P(a,y) = d_P(a,y) − g(a) + g(y) ≤ 2 d_P(a,y)`.  A maximal `(ε/2L)`-separated subset `A`
of `K_N` is an `(ε/2L)`-net, so `s_P(A,y) ≤ ε ≤ gap(y) + ε`; and
`|A| ≤ N_ext(𝓜(S_c, zN/2, T), ε/4L) ≤ 4^{T⌈2S_c(zN/2)·4L/ε⌉}`. ∎
This is the claim of P4 without the logarithm.  It is a statement about *accuracy relative to the
range of the residual* (`|g| ≤ L·zNS_c/2`), and it is not shared by the Hamming format, whose cost
stays `3^{n−O(√n)}` at every extensive accuracy (Thm 11.37; measured in §3.3).

**Theorem 8 (P4, second part) [P+cite].**  Under the z-condition, for every `m ≥ 1` there are
conformations `a₁..a_m ∈ X_N` (the greedy selection in `L²`) with

    max_{y∈X_N} dist₁(N^y, span{N^{a_i}})  ≤  8 z N S_c T / √m.

Hence for every `f` and every `g = g_{ψ*}` with `|ψ*| ≤ κL`:
`N^S_cov(ε) ≤ ⌈(8(1+κ) T z L S_c N/ε)²⌉`; at `ε = ε₁N` this is `⌈(8(1+κ)TzLS_c/ε₁)²⌉`, independent of
`N`; at fixed `ε` it is `O(N²)`.

*Proof.*  In `ℋ = L²([0,S_c)×[T])` let `P_G` be the averaging projection onto functions constant on
`G` equal cells per type pair (`dim = TG`).  For monotone `F_t` and a cell `I` of length `h = S_c/G`:
`∫_I (F_t − avg)² ≤ h·osc_I(F_t)²`, and `Σ_I osc_I(F_t)² ≤ F_t(S_c−)²`; so
`‖F − P_GF‖₂² ≤ h Σ_t F_t(S_c−)² ≤ hM²`, `M = zN/2`.  Thus `d_n(K_N)_ℋ ≤ M√(2S_cT/n)` for all `n ≥ 1`
(take `G = ⌊n/T⌋` for `n ≥ T`; for `n < T` use `‖F‖₂ ≤ M√S_c`).  By DeVore–Petrova–Wojtaszczyk (2013,
Cor. 3.3(ii), exact greedy, `α = ½`): `σ_m(K_N)_ℋ ≤ 2^{7/2}·M√(2S_cT)·m^{−1/2} = 16M√(S_cT/m)`, where
`σ_m` is the largest `L²` distance of an element of `K_N` to the span of the first `m` greedy elements
(which are elements of `K_N`, i.e. profiles of conformations).  Finally `‖u‖₁ ≤ √(S_cT)‖u‖₂`, and
`σ⁻ ≤ (1+κ)L·dist₁`. ∎
In `L¹` directly the same theory gives the rate `m^{−1/2+β}` (their Cor. 4.2(ii); the Kolmogorov
width of monotone functions in `L¹` is `≍ 1/m`), and their examples show that a loss of `√m` can
occur in Banach spaces; whether the profile sets of chains admit `O(1/ε₁)` evaluations is open.
The measured greedy widths (§3.5) decay like `1/m` (about `4/m` per bead off-lattice), with
constants two to three orders of magnitude below the bound.

### 2.5 Fixed absolute accuracy

**Theorem 9 (stretched-exponential bound for the `d_P` format) [P].**  Assume the z-condition, the
zero residual, and a known part with `gap(y) ≥ e·w(y)`, `w(y)` the number of non-trans torsions
(e.g. `f = Σ_i φ_i(x_i)`, `φ_i(t) = 0`, `φ_i ≥ e` otherwise).  Then for every `ε ≥ 0`

    N^P_cov(ε) ≤ 1 + Σ_{w=1}^{n} min{ C(n,w)(k−1)^w ,  4^{T⌈2zNLS_c/(we+ε)⌉} },
    ln N^P_cov(0) ≤ 1.67 √(T λ N ln(e(k−1)n)) + 1.39 T + ln(n+1),      λ = zLS_c/e.

*Proof.*  The conformations with exactly `w` excitations number at most `C(n,w)(k−1)^w` and have
gap `≥ we`.  A maximal `((we+ε)/L)`-separated subset of their profiles covers them within slack
`we+ε` and has at most `N_ext(𝓜, (we+ε)/2L) ≤ 4^{T⌈2S_c(zN/2)·2L/(we+ε)⌉}` elements.  For the second
line use `C(n,w)(k−1)^w ≤ e^{wA}`, `A = ln(e(k−1)n)`, and `min(wA, B/w) ≤ √(AB)` with
`B = 2 ln 4·TλN`. ∎
(The mechanism of theory report Thm 11.38 for the RMSD envelope.  The bound is vacuous at
enumerable sizes: with `z = 24`, `S_c = 12`, `L = e` it beats `n ln 3` only for `N` of order `10⁴`.)

**Correction to the last sentence of P4.**  "At fixed absolute accuracy the first-order class is
exponential in `N`" is
(i) **false on lattices** — polynomial, Theorem 6(b); measured with three distances below the
cutoff: 21 evaluations at `n = 12`, `L = e`, growing by about 2 per torsion (§3.3); with seven
distances the polynomial regime is not yet visible at `n ≤ 9` (49, 102, 191, 386, 720 — the
number of profile classes itself still grows ×2.3 per torsion there);
(ii) **not exponential for a gapped additive known part at the zero residual off-lattice** —
Theorem 9;
(iii) **plausibly true off-lattice when the known part has no gaps** [C]: for `f ≡ 0` the covering
number of the generic chain's profile set at fixed absolute radius grows ×1.5–2.0 per torsion for
`n ≤ 13` (`out_e2_gen16_A1.txt`, columns `m_abs`); a block-mixture heuristic gives
`ln N ≳ cN/ln N`;
(iv) at the sizes one can enumerate, with `L = e`, the generic chain shows
`N^P_cov = 27, 48, 92, 137, 215, 318` for `n = 5..10` — 90 % of all profile classes at `n = 5`, 23 %
at `n = 10`; Theorem 9 says nothing yet at these sizes.

### 2.6 Lower bounds: how many evaluations are necessary (task 4)

**Theorem 10 (worst-case brackets = inner Kolmogorov widths; adaption does not help) [P; the
classical zero-information argument of optimal recovery].**  Let
`δ_m(K_N) = min_{a₁..a_m∈X_N} max_y dist₁(N^y, span{N^{a_i}})` and `d_m(K_N)` the Kolmogorov `m`-width
of `K_N` in `𝓛`.
(i) For every deterministic adaptive scheme with `m` evaluations there are `g ∈ P_L` and `y` whose
bracket has half-width `≥ L·δ_m(K_N) ≥ L·d_m(K_N)`; the span bracket with the best `m` points attains
`L·δ_m`, with greedy points `L·σ_m`.
(ii) `m` arbitrary linear measurements of `g` (linear functionals of the vector `(g(x))_x`, not only
point evaluations) still leave a half-width `≥ L·d_m(K_N)`.
(iii) At the zero residual, with a known part: `N^S_cov(ε) ≥ max_{G≥0} min{m : d_m(K_G) ≤ (G+ε)/L}`,
`K_G = {N^y : gap_f(y) ≤ G}`.

*Proof.*  On `g = 0` the scheme sees zeros and queries a fixed sequence `a₁..a_m`; the consistent
set contains `{ψ : ‖ψ‖_∞ ≤ L, ψ ⊥ N^{a_i}}`, and the supremum of `−⟨ψ,N^y⟩` over it is
`L·dist₁(N^y, span)` (`(𝓛/V)* = V^⊥`).  (ii) A linear functional of `(g_ψ(x))_x` is `−⟨ψ,u⟩` with
`u ∈ span K_N`; same argument with `span{u_i}`.  (iii) Theorem 4 at `ψ* = 0`, restricted to the
clients of gap `≤ G`; the evaluated points need not have small gap, hence `d_m`, not `δ_m`. ∎

**Lemma 11 (computable lower bounds for `d_m`) [P].**  Write elements of `K` as vectors with
`‖u‖₁ = Σ_f|u_f|` (cell widths multiplied in).
(a) *Bernstein bound.*  For `u₀..u_m ∈ K`: `d_m(K) ≥ s_* := min_{c≠0} ‖Σ_j c_ju_j‖₁/‖c‖₁`
(`s_*` is computed exactly by `2^m` LPs).
(b) *Eigenvalue bound.*  For every probability `μ` on `K`:
`d_m(K)² ≥ Σ_{j>m} λ_j(Σ_y μ_y u_y u_yᵀ)` (eigenvalues in decreasing order).
(c) *Box bound.*  If `K ⊇ {F₀ + Σ_{t∈I} c_t e_t : c_t ∈ {0,..,n_t}}` with disjointly supported `e_t`,
`‖e_t‖₁ = δ_t`, then `d_m(K) ≥ ½ ·` (sum of the `|I| − m` smallest `n_tδ_t`).

*Proof.*  (a) The absolutely convex hull of `{u_j}` contains the ball of radius `s_*` of their
`(m+1)`-dimensional span, and the `m`-width of such a ball is its radius (Tikhomirov).  (b)
`max_y dist₁² ≥ Σ_y μ_y dist₂² ≥` the tail eigenvalue sum (`‖·‖₁ ≥ ‖·‖₂` for vectors; optimality of
principal components).  (c) `aco(K) ⊇ ½(K−K) ⊇ ½·Π_t[−n_tδ_t, n_tδ_t]` in the coordinates of the `e_t`
(an `ℓ¹` space; since the supports are disjoint there is a norm-one projection of `𝓛` onto
`span{e_t}`, so only subspaces `V` of that span need be considered).  For such a `V` of dimension
`m`, the polytope `[−1,1]^I ∩ V^⊥` has a vertex `ψ`,
at which at least `|I| − m` coordinates are `±1`; then
`max_{x∈box}⟨ψ,x⟩ = Σ_t n_tδ_t|ψ_t| ≥` the sum of the `|I|−m` smallest `n_tδ_t`. ∎
(The vertex argument is also the three-line proof of `d_m(B_∞^n, ℓ₁^n) = n − m`.)

**Proposition 12 (span certificates need one evaluation per independent feature) [P on the
product domain].**  Phantom chain, `S_c > s_g`, `δ₁₄ = min(s_t,S_c) − s_g`, every pair its own type
(the class of P5).  Then `d_m(K_N) ≥ δ₁₄(n−m)/2`.  Consequently, at the zero residual with `f ≡ 0`,
a uniform bracket `ε` needs `m ≥ n − 2ε/(Lδ₁₄)` evaluations — linear in `N` even at extensive
accuracy `ε₁N < Lδ₁₄n/2` — while `rank K_N` evaluations always suffice.

*Proof.*  The component of `N^x` on the type pair of the 1–4 pair of torsion `i` is the single step
`1[s ≥ s̃_{14}(x_i)]`, which depends on `x_i ∈ {t, g}` only.  The coordinate projection onto these `n`
components is an `L¹` contraction that maps subspaces to subspaces, and it maps `K_N` onto a
combinatorial cube; apply Lemma 11(c) with `n_t = 1`, `δ_t = δ₁₄`. ∎  For typed classes the same
argument gives `d_m ≥ (δ₁₄/2)·`(sum of the `T₁₄−m` smallest numbers of 1–4 pairs per type pair) on
any sub-family of conformations whose other pairs stay outside the cutoff; so the span cost is
of the order of the number of type pairs when these are balanced.

*When is the span certificate optimal?*  (1) For given points the LP bracket of Proposition 3 is
exact: nothing consistent with the class is excluded.  (2) Against the worst case over the class
(equivalently, at the zero residual) the best `m` points give exactly `L·δ_m`, no adaptive
deterministic scheme does better, and arbitrary linear information could at most improve `δ_m` to
`d_m`; numerically `d_m` and the greedy `σ_m` are within a factor 2–4 for `m ≤ 8` (§3.5).
(3) Instance-wise the greedy choice of points is not optimal (§2.2), and randomised algorithms
are not covered by any of the above (§5).

### 2.7 Robustness: pair-additive plus a remainder (task 5)

Let `h = g + r`, `g ∈ P_L`, and let `h` be evaluated at `A = {a_i}`, `v_i = h(a_i)`, `y ∉ A`.

**Theorem 13 (sup-norm remainder `|r| ≤ η`) [P].**

    sup{ h(y) } = η + min_λ [ λ·v + η‖λ‖₁ + L‖N^y − Σ_i λ_i N^{a_i}‖₁ ]

— an `ℓ¹`-penalised `L¹` regression.  At the zero data the half-width is
`η + min_λ[η‖λ‖₁ + L‖N^y − Σλ_iN^{a_i}‖₁] ≥ η`, and it is `≤ η(1+‖λ‖₁) + L·misfit(λ)` for every `λ`.

**Theorem 14 (first-order remainder `r(x) − r(x′) ≤ η d₀(x,x′)`, `d₀` a metric) [P].**

    sup{ h(y) } = min_{Σλ_i = 1} [ λ·v + L‖N^y − Σ_i λ_i N^{a_i}‖₁ + η·KR_{d₀}(δ_y − Σ_i λ_i δ_{a_i}) ],

`KR_{d₀}(μ) = sup{Σ_xμ_x ρ(x) : ρ 1-Lipschitz} =` the least cost of shipping `μ₊` to `μ₋` at unit cost
`d₀`.  Usable bounds, valid for every `λ` with `Σλ_i = 1`:

    d₀(y, A)  ≤  KR_{d₀}(δ_y − Σ_i λ_i δ_{a_i})  ≤  Σ_i |λ_i| d₀(y, a_i).

*Proofs.*  Both are LP duals (finite: `ψ` on the cells, the remainder at `y` and at the `a_i`; a
Lipschitz function on these points extends to `X`).  Lagrangian of the equality constraints with
multipliers `λ`: the supremum over `ψ` gives `L‖N^y − Σλ_iN^{a_i}‖₁`; in Theorem 13 the supremum over
`|r(a_i)| ≤ η` gives `η|λ_i|` and `r(y) = η`; in Theorem 14 the supremum over the Lipschitz `r` of
`r(y) − Σλ_ir(a_i)` is `+∞` unless `Σλ_i = 1` (constants are admissible) and is `η·KR` otherwise
(Kantorovich–Rubinstein duality on a finite metric space).  Upper bound:
`δ_y − Σλ_iδ_{a_i} = Σ_iλ_i(δ_y − δ_{a_i})` and `KR` is a seminorm.  Lower bound: `ρ(x) = d₀(x, A)` is
1-Lipschitz, vanishes on `A`, and equals `d₀(y,A)` at `y`. ∎

**Corollary 15 (the remainder is paid at first-order prices, and the two slacks add) [P].**  For
the class `P_L + Lip(ηd₀)`, an instance `h = g + r`, evaluations on `A` and `y ∉ A`, the lower slack
`σ⁻_sum(y) = h(y) − inf{h′(y)}` satisfies

    σ⁻_sum(y)  ≥  σ⁻_{S,aff}(y) + s_{ηd₀}(A, y),

where `σ⁻_{S,aff}` is the span slack of `g` with the constraint `Σλ_i = 1` (a gauge distance to the
*affine* hull of the evaluated profiles; `≥ σ⁻_A(y)`) and `s_{ηd₀}(A,y) = min_a[ηd₀(a,y) − r(a) + r(y)]`
is the first-order slack of `r`.  Hence every cover for the sum class satisfies
`σ⁻_{S,aff}(y) + s_{ηd₀}(A,y) ≤ gap(y) + ε` for all `y`, and in particular

    N^{sum}_cov(ε; f, g+r)  ≥  max{ N^S_cov(ε; f+r, g),  N^{ηd₀}_cov(ε; f+g, r) },

the second number being the ordinary first-order covering number for the envelope `ηd₀`.
*Proof.*  By Theorem 14 applied to the lower end,
`σ⁻_sum(y) = min_{Σλ=1} { [g(y) − λ·g(A) + L‖N^y − Σλ_iN^{a_i}‖₁] + [r(y) − λ·r(A) + η·KR_{d₀}(δ_y − Σλ_iδ_{a_i})] }`.
The minimum of the first bracket alone is `σ⁻_{S,aff}(y)`; the minimum of the second alone is the
lower slack of `r` in the class `Lip(ηd₀)` given its values on `A` (the same duality for the
first-order class), i.e. the McShane slack. ∎
At the zero data this reads `σ_sum(y) ≥ L·dist₁(N^y, aff{N^a}) + η·d₀(y,A)`: the gap of `y` must pay
for both.  Numbers (`e6b`, lattice `n = 6`, `L = 0.2`, `d₀` = torsion Hamming with unit constants,
`e = 1`): the remainder alone needs one evaluation for every `η ≤ 1` and the pair-additive part
alone two, yet the sum class needs 2, 2, 7, 20 evaluations at `η = 0.25, 0.5, 0.75, 1` — the maximum
in the display is only a lower bound.

*Reading.*  If `d₀` is a torsion-Hamming envelope with lever-arm constants (the only
general-purpose certified envelope so far, D42), the sum class is exponential in `n` unless `ηc_i`
is below the excitation energies: the pair-additive part buys the factor `η/L`, not a change of
exponent.  The remainder is harmless at extensive accuracy only if it lives in a class with
chain-length-independent constants: small in sup norm (Theorem 13: the accuracy floor is
`η(1+‖λ‖₁)`, and measured `‖λ‖₁` is 1–6 for the homopolymer models, §3.5), or Lipschitz in a profile metric
(`d₀(x,y) = ‖N^x − N^y‖₁`: then Theorems 7–8 apply to the sum), or of higher body order (§2.9).
Note the constraint `Σλ_i = 1` in Theorem 14: when the remainder is defined up to a constant, the
relevant set is the *affine* hull of the evaluated profiles.

### 2.8 Pair-specific residuals (P5)

**Proposition 16 [P on the product domain].**  If every pair has its own radial function, the
envelope is `d_pair(x,y) = L Σ_{pq}|s̃_pq(x) − s̃_pq(y)| ≥ d_P(x,y)` (Proposition 2).
(a) *First-order format: exponential.*  `d_pair(x,y) ≥ Lδ₁₄·d_tg(x,y)`, `d_tg` = number of torsions at
which exactly one of `x, y` is trans.  Hence for `f ≡ 0` at the zero residual on the phantom chain
`N_cov(ε) ≥ 2ⁿ/V(n, ⌊ε/(Lδ₁₄)⌋)` (`V` = Hamming-ball volume), which is
`exp(n[ln 2 − h(ε/(Lδ₁₄n))] − o(n))` for `ε < Lδ₁₄n/2`; and for `f = e·#gauche`:
`N_cov(ε) ≥ max_t e^{−tε}[(1+2e^{−te})/(2+e^{−tLδ₁₄})]ⁿ`, which grows exponentially at every `ε = o(n)`
as soon as `Lδ₁₄ > 2e`.
(b) *Span format: polynomial, at least linear.*  Proposition 12 and the rank.

*Proof of (a).*  The 1–4 pair of torsion `i` contributes `|s̃_t − s_g| = δ₁₄` when exactly one of the
two states is trans.  A `d_pair`-ball of radius `ε` meets at most `V(n, ε/(Lδ₁₄))` of the `2ⁿ`
trans/gauche patterns.  With gaps: theory report Thm 11.6(c) with
`Σ_y e^{−tLδ₁₄ d_tg(a,y)} ≤ (2+e^{−tLδ₁₄})ⁿ` and `Σ_y e^{−te·#g(y)} = (1+2e^{−te})ⁿ`; the ratio exceeds 1
for small `t` iff `2e < Lδ₁₄`. ∎
So the sentence of P5 is right for the format it has in mind, and its conclusion ("the governing
quantity is the number of pair types with many pairs, not the chain length") is right in both
formats, with different laws: **first-order cost is exponential in the number of independent
features, span cost is linear in it**; the chain length enters only through the number of
features (measured dependence on the alphabet: §3.2, §3.5, §3.7).

### 2.9 Three-body terms (task 6, optional)

**Proposition 17 [P for the duality; the entropy statement by the standard quantisation argument,
not written out].**  Let `g(x) = Σ_{p<q<r} φ(s_pq, s_qr, s_pr)` with `φ` symmetric, `L`-Lipschitz in the
`ℓ¹` distance of the sorted squared sides, `φ = 0` when a side reaches `S_c`.  With `μ^x` the
counting measure of the triangles of `x` in `Δ = {0 ≤ s₁ ≤ s₂ ≤ s₃ < S_c}`:

    sup_g (g(x) − g(y)) = L·KR_∂(μ^x − μ^y),      sup{g(y) : g(a_i) = v_i} = min_λ [λ·v + L·KR_∂(μ^y − Σλ_iμ^{a_i})],

where `KR_∂` is the Kantorovich–Rubinstein norm with a reservoir on the face `s₃ = S_c` (mass may be
created or destroyed at cost `S_c − s₃`).  The profile becomes a measure on a 3-dimensional domain;
normalised measures with at most `z₃` triangles per bead have `KR_∂`-entropy
`O((z₃LS_c/ε₁)³ ln(·))` at scale `ε₁/L`, independent of `N`.  So **the complexity depends on the body
order through the dimension of the internal-coordinate space (3 for triangles, `3b−6` for `b ≥ 3`
bodies) and on the number of type tuples, not on `N`**.  There is no distribution-function
formula; the envelope is a transport LP.  (`e7`, diamond lattice: primal = dual for both formulas;
feature counts in §3.7.)

### 2.10 Regimes, in one table

`λ = zLS_c/e`; zero residual and `f = e·#gauche` unless stated; `T` type pairs, `D` distances (lattice).

| format | class | exact / fixed accuracy | extensive accuracy `ε₁N` |
|---|---|---|---|
| **H** | `Lip(Σc_i[·])`, `c_i ≥ L c_i^{sf}`, growing with the lever arm | `3^{n−O(√n)}` (Thm 11.37; measured) | the same |
| **P** | `Lip(d_P)` | lattice: `≤ C(zN/2+DT, DT)` (Thm 6); off-lattice: `≤ exp(1.67√(TλN ln(2en)))` (Thm 9), observed ×1.5–1.9 per torsion for `n ≤ 10` at `L = e` | `≤ 4^{T⌈4zLS_c/ε₁⌉}` (Thm 7) |
| **S** | `P_L` | `≤ rank ≤ DT` (lattice); `≤ (16TzLS_cN/ε)²` (Thm 8) | `≤ (16TzLS_c/ε₁)²`; `≥` width count (Thm 10) |
| pair-specific, first-order | `Lip(d_pair)` | exponential (Prop. 16) | exponential for `ε₁N < Lδ₁₄n/2` |
| pair-specific, span | | `≤ rank = O(N²)` | `≥ n − 2ε₁N/(Lδ₁₄)` (Prop. 12) |
| `P_L + Lip(ηd_H)` | | `≥ max(S, H with constants ηc_i)`; slacks add (Cor. 15) | the same |

---
## 3. Numerical studies (what, sizes, results)

All numbers below are in the output files named; commands and run times are in §7.  Exhaustive =
all `3ⁿ` torsion states were generated and filtered for excluded volume.

### 3.1 P1–P3 on small chains (`e1_verify_P123.py` → `out_e1.txt`; task 1)

Two independent formulations: the *primal* LP uses the definition of the class (values of `φ` on
the occurring squared distances with Lipschitz constraints between neighbours and to the cutoff,
energies as pair sums); the *dual* uses profiles and the `L¹` formulas of P2/P3.  (The
discretisation of `φ` on the occurring distances is exact: a Lipschitz function on a finite set
extends.)

| check | instances | result |
|---|---|---|
| P1, lattice, exact `int64` arithmetic | all `3ⁿ` conformations, `n = 4, 6, 8, 10` (59 049), `A ∈ {1,2,4}`, `S_c ∈ {12,17,28}`; plus 200 conformations per case recomputed pair by pair | identity holds exactly |
| P1, generic chain | all conformations `n = 4, 6, 8`, up to 306 breakpoints | max deviation `1.1·10⁻¹⁴` |
| P2, `sup_g (g(x)−g(y))` by LP vs `L‖N^x−N^y‖₁` | 10 800 random pairs (36 cells: 3 geometry/cutoff choices × `n ∈ {4,6,8,10}` × `A ∈ {1,2,4}`) | max deviation `2.3·10⁻¹³`; maximiser recomputed from pair sums; mirror images have identical profiles; chain reversal is a symmetry only for `A = 1` |
| P3, primal vs dual, floating point | 12 960 instances (324 cells: `n ∈ {6,8,10}`, `A ∈ {1,2,4}`, `m ∈ {1,2,4,6}` evaluations, `κ ∈ {0, ½, 1}`) | max `|primal − dual| = 1.0·10⁻¹⁰`; true value inside the bracket in all; `U ≤` McShane in all, strictly below it in 40–100 % of the instances of a cell |
| P3, exact rationals (own simplex over `Fraction`), lattice | 288 instances (`n ∈ {6,8,10}`, `A ∈ {1,2}`, `m ≤ 4`, `S_c ∈ {12,17,28}`) | primal = dual as rationals, both ends, 288/288; e.g. `Lo = 371/17 ≤ g(y) = 25 ≤ U = 57/2`, half-width `227/68 < L·dist₁ = 84/17` |
| "half-width = `L·dist₁` to span" | same 12 960 instances | ratio = 1 always at `κ = 0`; `< 1` in 51 % of instances at `κ = ½` (min 0.55), in 69 % at `κ = 1` (min 0.00) |

### 3.2 Metric entropy of the profile set (`e2_entropy_exhaustive.py`, `e2b_entropy_sampled.py`; task 2)

Normalised metric `d̄(x,y) = ‖N^x − N^y‖₁/N` (`= d_P/(LN)`).  `m(δ)` = number of points of a
farthest-point traversal needed to bring the covering radius below `δ`; it satisfies
`N_int(δ) ≤ m(δ) ≤ packing(δ) ≤ N_ext(δ/2)`, so `ln m(δ)` is the entropy at scale `δ` up to a factor 2
in the scale.  In terms of certificates: `N^P_cov(ε₁N) ≤ m(ε₁/2L)` for every instance (Theorem 7).

**Exhaustive, self-avoiding diamond chain, `S_c = 12`** (`out_e2_dia12_A*.txt`).  `classes` = distinct
profiles = size of an exact first-order certificate for `f ≡ 0`; `z/2` = largest number of pairs
inside the cutoff per bead; last column: the bound of Theorem 7 on `ln m(1)`.

| `A` | `n` | `N` | conformations | classes | `z/2` | `m(4)` | `m(2)` | `m(1)` | `m(0.5)` | `m(0.25)` | bound on `ln m(1)` |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 8 | 11 | 5 849 | 90 | 2.45 | 2 | 3 | 7 | 14 | 31 | 164 |
| 1 | 10 | 13 | 49 833 | 190 | 2.92 | 3 | 5 | 11 | 25 | 55 | 195 |
| 1 | 11 | 14 | 145 379 | 258 | 3.14 | 3 | 5 | 11 | 26 | 73 | 209 |
| 1 | 12 | 15 | 422 825 | 356 | 3.13 | 3 | 5 | 10 | 34 | 96 | 209 |
| 1 | 13 | 16 | 1 231 221 | 479 | 3.25 | 3 | 5 | 12 | 34 | 88 | 216 |
| 2 (periodic) | 10 | 13 | 49 833 | 430 | 2.92 | 3 | 7 | 21 | 61 | 137 | 586 |
| 2 (periodic) | 12 | 15 | 422 825 | 1 045 | 3.13 | 3 | 8 | 29 | 114 | 311 | 628 |
| 4 (periodic) | 10 | 13 | 49 833 | 6 115 | 2.92 | 8 | 54 | 228 | 751 | 1 423 | 1 955 |
| 4 (periodic) | 12 | 15 | 422 825 | 39 085 | 3.13 | 11 | 96 | 683 | > 3 000 | > 3 000 | 2 093 |

**Exhaustive, other models** (`out_e2_dia28_A1.txt`, `out_e2_gen16_A*.txt`):

| model | `n` | conformations | classes | `z/2` | `m(8)` | `m(4)` | `m(2)` | `m(1)` | `m(0.5)` |
|---|---|---|---|---|---|---|---|---|---|
| dia, `S_c = 28`, `A = 1` | 10 | 49 833 | 4 646 | 4.23 | 7 | 24 | 138 | 628 | 1 779 |
| | 12 | 422 825 | 24 492 | 5.07 | 11 | 44 | 242 | 1 462 | > 3 000 |
| gen, `S_c = 16`, `A = 1` | 10 | 8 115 | 1 360 | 4.23 | 3 | 6 | 19 | 86 | 300 |
| | 12 | 47 141 | 6 137 | 5.20 | 4 | 11 | 40 | 170 | 843 |
| | 13 | 113 587 | 13 012 | 5.69 | 5 | 13 | 42 | 255 | 1 424 |
| gen, `S_c = 16`, `A = 4` (periodic) | 10 | 8 115 | 3 442 | 4.23 | 6 | 40 | 238 | 805 | 1 703 |
| | 12 | 47 141 | 18 656 | 5.20 | 11 | 119 | 740 | > 3 000 | > 3 000 |

Readings.  (1) In the three-feature model (dia, `S_c = 12`, homopolymer) the normalised entropy
**saturates** already at `N ≈ 13`: `m(1) = 11, 11, 10, 12`, `m(0.5) = 25, 26, 34, 34`.  (2) In every
richer model `m(δ)` still grows by 1.4–1.8 per torsion at `N ≤ 16`: the saturation level predicted
by Theorem 7 exists, but it is far above the number of conformations one can enumerate, and the
profile set itself is still expanding (`z/2` grows from 1.3 to 5.7 while the bulk value is 12 for
the lattice at `S_c = 12`).  **At enumerable sizes P4 cannot be seen except in the lowest-
dimensional model.**  (3) The a-priori bound is useless as a number (216 nats against
`ln 12 = 2.5`): it is the entropy of *all* monotone functions; the profile set of a lattice chain
lives in `DT` dimensions.  (4) Alphabet: at fixed `N` the entropy grows quickly with the number of
type pairs (`m(1)`: 11 → 21 → 228 for `T = 1, 3, 10` at `N = 13`), as the factor `T` in Theorem 7 and
the feature-count law of §2.8 suggest.

**Sampled long chains, diamond lattice** (`out_e2b_S12_A1.txt` etc.): for each `N`, about 720
self-avoiding conformations from fixed recipes — chain growth with a contact bias `e^{b_c·#neighbours}`,
`b_c ∈ {0, 0.4, 0.8, 1.2, 1.8, 2.5, 4}` (coil to globule; 60 each), all periodic torsion words of
length `≤ 4`, 300 random mixtures of 2–3 periodic segments, hairpin sheets.

| `S_c`, `A` | `N` | classes | `z/2` | `m(4)` | `m(2)` | `m(1)` | `m(0.5)` | rank |
|---|---|---|---|---|---|---|---|---|
| 12, 1 | 15 | 162 | 3.13 | 2 | 4 | 8 | 21 | 3 |
| | 60 | 624 | 5.37 | 4 | 7 | 15 | 42 | 3 |
| | 120 | 641 | 5.76 | 4 | 7 | 17 | 44 | 3 |
| | 240 | 649 | 6.68 | 4 | 7 | 18 | 49 | 3 |
| | 480 | 660 | 6.89 | 4 | 7 | 17 | 51 | 3 |
| | 960 | 653 | 6.52 | 4 | 7 | 18 | 46 | 3 |
| 12, 2 (periodic) | 60 | 643 | 5.37 | 4 | 7 | 23 | 88 | 4 |
| | 240 | 650 | 6.68 | 4 | 9 | 23 | 65 | 4 |
| | 960 | 654 | 6.52 | 4 | 8 | 27 | 67 | 4 |
| 28, 1 | 60 | 672 | 13.8 | 72 | 207 | 443 | 608 | 7 |
| | 240 | 655 | 19.3 | 82 | 189 | 374 | 553 | 7 |
| | 480 | 668 | 20.7 | 82 | 187 | 347 | 544 | 7 |

For `N ≥ 60` the numbers do not depend on `N` (for `S_c = 12`; for `S_c = 28` the values above ≈ 200
are limited by the sample size).  This supports P4 for these families; it is not a statement
about the whole set `K_N` (a sample of 720 conformations cannot have entropy above `ln 720`).  At
`N = 15` the families reproduce about 70 % of the exhaustive `m(δ)`.
With pseudo-random type sequences (`out_e2b_S12_A2r.txt`, `out_e2b_S12_A4r.txt`; rank 9 and 30 = `DT`)
the sampled `m(δ)` *decreases* with `N` (two types: `m(1) = 130, 123, 81, 54, 38, 25` for
`N = 30 … 960`): in generic conformations the type composition of the pairs inside the cutoff
self-averages, and the families do not contain type-selective conformations.  This is a
limitation of the sample, not evidence about `K_N`; for typed chains only the exhaustive data
below `N = 16` are informative.

**Dependence on the alphabet** (exhaustive, self-avoiding diamond chain, `S_c = 12`; pseudo-random
type sequences with `A` types, `A = N` meaning every bead its own type, i.e. the pair-specific class
of P5; `out_e2_dia12_A{1,2r,4r,8r,99}.txt`).  Entries: `m(4)` / `m(2)`.

| `N` | `A = 1` (`T = 1`) | `A = 2` (`T = 3`) | `A = 4` (`T = 10`) | `A = 8` (`T = 36`) | pair-specific |
|---|---|---|---|---|---|
| 11 | 2 / 3 | 3 / 9 | 6 / 34 | 12 / 48 | 17 / 58 |
| 13 | 3 / 5 | 5 / 18 | 13 / 109 | 42 / 253 | 63 / 299 |
| 15 | 3 / 5 | 6 / 24 | 24 / 321 | 129 / 1 153 | 258 / 1 526 |

At fixed relative scale the entropy has saturated for one type pair, is growing slowly for three,
and for ten or more it is still growing by a factor 2–3 per two torsions at `N = 15`; for the
pair-specific class it grows by ≈ 2 per torsion and never saturates (Proposition 16).  The same
on the generic chain (`out_e2_gen16_A4r.txt`, `out_e2_gen16_A99.txt`, `N = 15`): `m(4) = 11` (`A = 1`),
157 (`A = 4`), 277 (pair-specific).  This is the content of "per type pair" in P4 and of P5: the
saturation level is exponential in the number of type pairs, and the chain length at which the
`N`-independence becomes visible grows with it.

### 3.3 Certificates of the minimum in the three formats (`e4_formats_min.py`; task 3)

Instance: excluded-volume chain, `f = #gauche` (`e = 1`), residual zero (the worst case for the span
format and the reference instance of the theory) or one random member of `κP_L`, `κ = ½`.  Entries
are brackets `[lower, upper]` of the covering number (certificate size up to `+1`):

* **H**: lower = bound valid for *every* valid weighted-Hamming envelope of the class (fractional
  cover / partition bound, theory report Thm 11.6(c), with the single-flip maxima `c^{sf}`, which
  every valid constant vector dominates); upper = greedy/MILP cover with the valid constants of
  smallest sum (an LP over the `2ⁿ−1` sets of changed torsions; computed for `n ≤ 8` (dia), `≤ 9`
  (gen); it coincided with `c^{sf}` on the lattice).  `−` = not computed.
* **P**: LP (fractional cover) and MILP/greedy on profile classes — mostly exact.
* **S**: lower = brute force over all evaluation sets of size 1 (and 2 where affordable) and the
  eigenvalue width bound; upper = min(greedy span cover started at a minimiser, rank).

**Diamond lattice, `S_c = 12`, homopolymer, zero residual** (`out_e4_dia12_A1.txt`; rank of the
profile set 3; valid Hamming constants at `n = 12`: `c/L = (52, 85, 92, 108, 114, 114, 114, 114, 108, 92, 85, 52)`,
central value growing by ≈ 9 per torsion).

| `n` | conformations | profiles | H, `L=1`, `ε=0` | P | S | H, `L=1`, `ε=N/2` | P | S | H, `L=0.2`, `ε=0` | P | S |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | 233 | 22 | 233 | 5 | 2 | 233 | 3 | 1 | [141, 145] | 2 | 1 |
| 6 | 683 | 37 | 683 | 6 | 2 | 683 | 5 | 1 | [483, 487] | 2 | 1 |
| 7 | 2 005 | 57 | [1 027, 2 005] | 10 | 2 | [594, 2 005] | 5 | 1 | [211, 1 929] | 2 | 1 |
| 8 | 5 849 | 90 | [2 955, 5 849] | 10 | 2 | [1 721, 5 849] | 5 | 1 | [594, 5 037] | 2 | 1 |
| 9 | 17 107 | 129 | ≥ 8 569 | 13 | 2 | ≥ 5 107 | 5 | 1 | ≥ 1 733 | 3 | 1 |
| 10 | 49 833 | 190 | ≥ 24 790 | 16 | 2 | ≥ 14 870 | 7 | 1 | ≥ 4 890 | 3 | 1 |
| 11 | 145 379 | 258 | ≥ 74 570 | 19 | 2 | ≥ 45 710 | 7 | 2 | ≥ 14 860 | 4 | 1 |
| 12 | 422 825 | 356 | ≥ 219 000 | 21 | 2 | ≥ 136 200 | 8 | 2 | ≥ 44 180 | 4 | 1 |

(P and S entries are exact: lower = upper.)  At `L = 0.05`: H `≥ 1 285` at `n = 12` (`[33, 38]` at
`n = 6`), P 1–2, S 1.  **Dependence on the chain length**: H ×2.9–3.0 per torsion (lower bound;
`n = 9 → 12`), also at the extensive accuracy `N/2`; P about +2 per torsion at `ε = 0` and +0.5 at
`ε = N/2` (Theorem 6: polynomial; Theorem 7: bounded); S constant (≤ rank).

**Generic chain, `S_c = 16`, homopolymer, zero residual** (`out_e4_gen16_A1.txt`; 21–150 features).

| `n` | conformations | profiles | H, `L=1`, `ε=0` | P | S | H, `L=1`, `ε=N/2` | P | S | H, `L=0.2`, `ε=0` | P | S |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | 99 | 30 | 99 | 27 | [3, 7] | 99 | 9 | [3, 4] | 99 | 5 | 2 |
| 6 | 239 | 60 | 239 | 48 | [3, 7] | 239 | 15 | [3, 5] | 239 | 5 | 2 |
| 7 | 577 | 136 | 577 | 92 | [3, 7] | 577 | 21 | [3, 5] | 577 | 6 | 2 |
| 8 | 1 393 | 291 | [925, 1 393] | 137 | [3, 8] | [617, 1 393] | 34 | [3, 6] | [334, 1 393] | 9 | 3 |
| 9 | 3 363 | 639 | [2 272, 3 363] | 215 | [3, 9] | [1 562, 3 363] | 43 | [2, 6] | [859, 3 363] | 11 | [2, 3] |
| 10 | 8 115 | 1 360 | ≥ 5 539 | [318, 319] | [3, 10] | ≥ 3 897 | [58, 62] | [2, 6] | ≥ 2 187 | 13 | [2, 3] |

Off-lattice at `L = e` the first-order `d_P` format needs between 90 % (`n = 5`) and 23 % (`n = 10`)
of all profile classes and grows ×1.5–1.9 per torsion in this range, while the number of classes
grows ×2.1–2.3 (Theorem 9 is vacuous here); the span format
grows by about one evaluation per two torsions (7 → 10), with the number of features (21 → 150).
At `L = 0.2e` P grows slowly (5 → 13) and S is 2–3.  H is everything or nearly so.

**Other models** (same script).

| model | `n` | H, `L=1`, `ε=0` | P | S | H, `L=0.2`, `ε=0` | P | S |
|---|---|---|---|---|---|---|---|
| dia, `S_c = 28`, `A = 1` (rank 7; `out_e4_dia28_A1_partial.txt`) | 5 | 233 | 49 | [4, 5] | 233 | 12 | 3 |
| | 6 | 683 | 102 | [4, 6] | 683 | 19 | 3 |
| | 7 | [1 588, 2 005] | 191 | [4, 6] | [884, 2 005] | 23 | [3, 4] |
| (`out_e4_dia28_A1_n8_9.txt`) | 8 | [4 640, 5 849] | 386 | [4, 7] | [2 588, 5 849] | 30 | [3, 4] |
| | 9 | ≥ 13 620 | 720 | [4, 7] | ≥ 7 569 | [39, 41] | [3, 4] |
| dia, `S_c = 12`, 2 types periodic (rank 4; `out_e4_dia12_A2.txt`) | 6 | 683 | 11 | [3, 4] | [483, 487] | 2 | 1 |
| | 8 | [2 955, 5 849] | 22 | [3, 4] | [594, 5 037] | 3 | 1 |
| | 10 | ≥ 24 790 | 39 | [3, 4] | ≥ 4 890 | 4 | 1 |
| dia, `S_c = 12`, 2 types pseudo-random (rank 6 at `n = 6`, 9 = `DT` from `n = 7`; `out_e4_dia12_A2r.txt`) | 6 | 683 | 14 | [3, 6] | [483, 487] | 3 | 2 |
| | 8 | [2 961, 5 849] | 55 | [3, 8] | [602, 5 037] | 5 | [2, 4] |
| | 9 | ≥ 8 569 | 71 | [3, 9] | ≥ 1 733 | 6 | [2, 4] |

(For the two-type model the script printed a greedy upper bound 5 for S; the all-trans minimiser
has the zero profile — no pair of `𝒫` inside the cutoff — so it adds nothing to the span, and a
basis of the 4-dimensional profile span is a cover: `S ≤ 4`.  Later versions of the script cap
the upper bound by the rank.)  With more features (7 instead of 3 distances; 3 type pairs instead
of 1) the first-order format grows roughly in proportion to the number of profile classes (at
`n = 8`, `L = 1`: 10 → 55 from one to three type pairs with a generic sequence), the span format
stays below the rank (3 → 9).  Note the lattice with seven distances: `N^P_cov = 49, 102, 191, 386, 720`
for `n = 5..9` at `L = 1` — a factor 2 per torsion.  Theorem 6(b) says this is polynomial in the long
run (`≤ C(zN/2+7, 7)`), but a polynomial of degree 7 is indistinguishable from an exponential at
these sizes (the number of profile classes itself still grows ×2.3 per torsion at `n = 12`).

**Random residual** (`κ = ½`; one random smooth member of `κP_L` per row; `out_e4_dia12_A1_k05.txt`,
lattice `S_c = 12`): `n = 8`: H `[1 197, 5 729]`, P 3, S 1 (`L = 1`); H `[500, 5 519]`, P 4, S 1 (`L = 0.2`);
`n = 11`: H `≥ 4 803`, P 6, S 2 (`L = 1`); H `≥ 1 979`, P 2, S 1 (`L = 0.2`).  Generic chain (`out_e4_gen16_A1_k05.txt`): `n = 8`: H `[295, 1 385]`, P 7,
S `[2, 3]` (`L = 1`); `n = 9`: H `≥ 517`, P 30, S `[2, 6]` (`L = 1`); H `≥ 109`, P 4, S 2 (`L = 0.2`).  The
ordering H ≫ P ≥ S does not depend on the instance being the zero residual (the H lower bounds
are weaker because the partition bound loses the factor `1−κ` in the constants; the P numbers are
smaller than at the zero residual because a smooth random residual enlarges most gaps).

**One-evaluation thresholds** (`e9_thresholds.py`; the largest `L` for which the single evaluation at
the all-trans minimiser is an exact certificate): see §3.7.

### 3.4 Certificates of `ln Z` (`e5_formats_lnZ.py`; `β = 1`; task 3)

Criterion: `ln Z(f + Lo_A) − ln Z(f + U_A) ≤ ε` with the pointwise brackets of the format — exact for
H and P (both envelopes are admissible), sufficient for S.  Upper bounds: greedy.  Lower bounds for
H and P: the larger of the mass bound and the dip bound (every `y` needs an evaluated point within
slack `(Λ(y)+ε)/β`, `Λ` the soft gap; volume/LP bound for that covering problem).  For S with `F = 3`
features the exact bracket of `ln Z` over the consistent potentials was computed (vertex
enumeration for the convex maximum, convex minimisation for the minimum) and the smallest
certificate found by brute force ("exact").

**Diamond lattice, `S_c = 12`, homopolymer, zero residual** (`out_e5_dia12_A1.txt`).

| `n` | `L` | `ε` | H `[LB, UB]` | P `[LB, UB]` | S pointwise (greedy) | S exact minimum |
|---|---|---|---|---|---|---|
| 8 | 1 | 1 | 5 849 (all) | [8, 22] | 3 | 2 |
| 8 | 1 | 0.1 | 5 849 (all) | [10, 48] | 3 | 3 |
| 8 | 1 | 0.01 | 5 849 (all) | [10, 69] | 3 | 3 |
| 8 | 0.2 | 1 | [532, 5 658] | [2, 4] | 2 | 1 |
| 8 | 0.2 | 0.01 | [1 036, 5 847] | [3, 48] | 3 | 2 |
| 8 | 0.05 | 0.01 | [81, 5 624] | [2, 31] | 3 | 2 |
| 10 | 1 | 1 | − | [12, 38] | 3 | 2 |
| 10 | 1 | 0.01 | − | [16, 128] | 3 | 3 |
| 10 | 0.2 | 0.01 | − | [4, 85] | 3 | 3 |

**Generic chain, `S_c = 16`** (`out_e5_gen16_A1.txt`).

| `n` | `L` | `ε` | H `[LB, UB]` | P `[LB, UB]` | S pointwise (greedy) |
|---|---|---|---|---|---|
| 8 | 1 | 1 | 1 393 (all) | [52, 183] | 13 |
| 8 | 1 | 0.01 | 1 393 (all) | [69, 257] | 37 |
| 8 | 0.2 | 0.01 | [1 365, 1 393] | [8, 235] | 27 |
| 8 | 0.05 | 0.01 | [48, 1 371] | [5, 196] | 22 |
| 9 | 1 | 1 | − | [69, 348] | 16 |
| 9 | 1 | 0.01 | − | [93, 546] | 50 |

For `ln Z` the ordering is the same and more pronounced than for the minimum (no gap credit: all
thermally relevant states must be bracketed): H needs essentially every conformation as soon as
`L·c_i` exceeds a few `kT`; P needs a number growing with `n` and with `1/ε`; S needs at most the rank
on the lattice (3, for every `ε`, every `n`), and a few tens off-lattice (the pointwise criterion is
sufficient, not necessary — on the lattice it overshoots the exact minimum by at most 1).

### 3.5 Widths, lower bounds, coefficient norms (`e3_widths_exhaustive.py`, `e3b_widths_sampled.py`; tasks 2 and 4)

All distances per bead (`‖·‖₁/N`).  `σ_m` = greedy (reduced-basis) `L¹` width after `m` evaluations, i.e.
the worst-case half-width`/L` of the span bracket at the zero residual with greedy points; `LB` =
rigorous lower bound on the Kolmogorov width `d_m` (max of the Bernstein and eigenvalue bounds of
Lemma 11), i.e. a lower bound for *any* `m` evaluations and even any `m` linear measurements;
`Leb` = `max_y` / `mean_y` of the smallest `‖λ‖₁` among `L¹`-optimal combinations (the amplification
factor of a sup-norm remainder is `1 + ‖λ‖₁`, Theorem 13).

**Generic chain, `S_c = 16`, homopolymer, exhaustive** (`out_e3_gen16_A1.txt`; `n = 12`: 1 500 of 6 137
profile classes, so `σ_m` is a lower bound for the full set there).

| `m` | 1 | 2 | 4 | 8 | 16 | 32 |
|---|---|---|---|---|---|---|
| `n = 8` (`N = 11`, 291 classes, rank 51): `σ_m` | 3.67 | 2.83 | 0.96 | 0.34 | 0.12 | 0.029 |
| `LB` | 2.14 | 1.47 | 0.53 | 0.085 | 0.012 | 0.002 |
| `Leb` max / mean | 1.0 / 0.6 | 1.1 / 0.7 | 1.8 / 0.9 | 2.6 / 1.4 | 4.6 / 2.3 | 6.0 / 3.1 |
| `n = 10` (`N = 13`, 1 360 classes, rank 140): `σ_m` | 4.79 | 2.76 | 1.47 | 0.52 | 0.22 | 0.090 |
| `LB` | 2.92 | 1.44 | 0.60 | 0.12 | 0.017 | 0.007 |
| `Leb` max / mean | 0.8 / 0.5 | 1.0 / 0.6 | 2.0 / 0.9 | 2.7 / 1.3 | 3.6 / 1.7 | 4.9 / 2.5 |
| `n = 12` (`N = 15`, rank 226): `σ_m` | 5.24 | 3.39 | 1.34 | 0.49 | 0.24 | 0.14 |
| `LB` | 3.07 | 1.78 | 0.52 | 0.12 | 0.014 | 0.006 |
| `Leb` max / mean | 1.0 / 0.5 | 1.0 / 0.6 | 1.6 / 0.8 | 2.5 / 1.4 | 3.2 / 1.9 | 5.0 / 2.7 |

Singular values of the profile matrix (`L²`, relative to the first): `4·10⁻², 2·10⁻², 4·10⁻³, 2·10⁻³,
5·10⁻⁴` at `m = 1, 4, 8, 16, 32` for all three `n`.  Readings: (1) `σ_m ≈ 4/m` per bead for `m ≤ 32`
(`n = 10, 12`) — the rate of the Kolmogorov width of monotone functions, much better than the
`m^{−1/2}` that Theorem 8 can prove, and with a constant about `10³` times smaller than its bound
(`8zS_c/√m ≈ 1 100/√m`).  (2) The rigorous lower bound is within a factor 2–4 of the greedy width
for `m ≤ 8`: with 8 evaluations no scheme brackets every conformation better than `0.12·L` per bead
at `N = 13`, greedy achieves `0.52·L`.  (3) At fixed `m` the widths per bead still increase from
`N = 11` to `13` and are about equal at `13` and `15`; they have not provably saturated.
(4) `‖λ‖₁` stays between 1 and 6: the span brackets are stable.

**Dependence on the number of type pairs** (`n = 8`, `N = 11`; pseudo-random type sequences;
`out_e3_gen16_A2r.txt`, `out_e3_gen16_A4r_n8.txt`):

| `A` (`T`) | features | rank | `σ_4` | `σ_8` | `σ_16` | `σ_32` | `m` needed for `σ_m ≤ 1` |
|---|---|---|---|---|---|---|---|
| 1 (1) | 56 | 51 | 0.96 | 0.34 | 0.12 | 0.03 | 4 |
| 2 (3) | 168 | 69 | 2.68 | 1.55 | 0.53 | 0.13 | ≈ 11 |
| 4 (10) | 504 | 120 | 5.46 | 3.97 | 2.48 | 1.06 | ≈ 33 |

The number of evaluations needed for a given per-bead accuracy grows in proportion to the number
of type pairs (4 : 11 : 33 for `T` = 1 : 3 : 10) — the feature-count law for the span format.

**Lattice** (`out_e3_dia12_A1.txt`, `out_e3_dia28_A1.txt`): the width vanishes at `m =` rank (3 for
`S_c = 12`, 7 for `S_c = 28`).  `S_c = 28`, `n = 12`: `σ_m = 11.8, 4.1, 2.1, 1.6, 0.29` for `m = 1, 2, 3, 4, 6`
against lower bounds `8.2, 2.4, 0.93, 0.55, 0.13`; `Leb ≤ 2.8`.
With four types on the lattice (`S_c = 12`, pseudo-random sequence, `T = 10`; `out_e3_dia12_A4r.txt`): rank
24–25 (of `DT = 30`), `σ_8 = 2.1, 2.0, 2.4` and `σ_16 = 0.67, 0.81, 0.99` per bead for `N = 11, 13, 15`,
`Leb` up to 14 at `m = 24` — eight times the rank of the homopolymer, at similar per-bead scale.

**Long chains (sampled), generic chain** (`out_e3b_gen.txt`): about 330 conformations per `N` (biased
growth from coil to compact, periodic words, mixtures), profiles projected on a grid of 104 cells
(the projection is an `L¹` contraction, so these are lower bounds for the exact widths of the
sample).

| `N` | conformations | max pairs/bead | `σ_1` | `σ_4` | `σ_8` | `σ_16` | `σ_32` | `Leb` max / mean at `m = 32` |
|---|---|---|---|---|---|---|---|---|
| 15 | 341 | 5.2 | 4.85 | 1.51 | 0.50 | 0.25 | 0.10 | 6.1 / 2.9 |
| 30 | 327 | 9.3 | 5.93 | 1.68 | 0.84 | 0.43 | 0.20 | 5.5 / 2.6 |
| 60 | 323 | 11.4 | 7.61 | 1.92 | 0.91 | 0.42 | 0.19 | 4.7 / 2.6 |
| 120 | 315 | 14.0 | 8.90 | 2.07 | 0.81 | 0.35 | 0.17 | 5.6 / 2.7 |
| 240 | 317 | 15.1 | 9.71 | 2.14 | 0.77 | 0.25 | 0.13 | 5.1 / 2.7 |
| 480 | 306 | 15.6 | 10.87 | 2.09 | 0.62 | 0.19 | 0.095 | 5.3 / 3.0 |

For `m ≥ 4` the per-bead widths do not grow with `N` between 30 and 480 (for `m ≥ 12` they decrease
slowly), while `σ_1` follows the densification of the compact family (pairs per bead 5 → 16);
`‖λ‖₁` does not depend on `N` (max ≈ 5, mean ≈ 2.7 at `m = 32`), nor do the relative singular values
(`4·10⁻²`, `10⁻²`, `2·10⁻³`, `2·10⁻⁴` at `m = 1, 4, 8, 32`, slowly decreasing with `N`).  At `N = 15` the
sample agrees with the exhaustive set (`σ_8`: 0.50 against 0.49; `σ_16`: 0.25 against 0.24).  So in
these families the number of evaluations needed for a given per-bead accuracy does not depend on
the chain length — about 8 for `0.8·L` per bead and 32 for `0.2·L` per bead — which is the content
of P4(b); the caveat of §3.2 applies (a sample, not `K_N`).

### 3.6 Robustness (`e6_robust.py`, `e6b_sumclass.py`; task 5)

* **Theorems 13 and 14, primal = dual**: 3 600 instances (`dia` `S_c = 12` and `gen` `S_c = 16`, `n ∈ {6, 8}`,
  `A ∈ {1, 2}`, `m ∈ {2, 5, 10}` evaluations, three values of `η`; remainder uniform in `[−η, η]`,
  respectively site-additive and `η`-Lipschitz in the torsion-Hamming metric): max
  `|primal − dual| = 1.1·10⁻¹²`, the true value inside the bracket in all, hub bound `≥` exact in
  all (median ratio per cell 1.00–1.49), zero-data half-width `≥ η·d_H(y,A)` in all; McShane's
  bracket for the sum envelope is wider than the exact one by a median factor of up to 8.5 (small `η`,
  many evaluations).
* **Size of the brackets against `η`** (`out_e6.txt`, part C; 12 greedy evaluations, zero data, mean
  over 150 other profile classes, `L = 1`):

  | model | `η` | 0 | 0.01 | 0.1 | 0.3 | 1 | 3 |
  |---|---|---|---|---|---|---|---|
  | dia `S_c = 28`, `n = 8` (span = everything) | sup-norm remainder: half-width | 0 | 0.027 | 0.27 | 0.81 | 2.71 | 7.46 |
  | | Hamming-Lipschitz remainder: half-width | 0.45 | 0.50 | 1.02 | 2.15 | 6.08 | 16.8 |
  | | lower bound `η·d_H(y,A)` | 0 | 0.033 | 0.33 | 0.98 | 3.28 | 9.84 |
  | gen `S_c = 16`, `n = 8` | sup-norm remainder: half-width | 0.90 | 0.93 | 1.19 | 1.73 | 3.42 | 7.76 |
  | | Hamming-Lipschitz remainder: half-width | 0.92 | 0.97 | 1.44 | 2.41 | 5.43 | 12.9 |
  | | lower bound `η·d_H(y,A)` | 0 | 0.023 | 0.23 | 0.68 | 2.28 | 6.84 |

  A sup-norm remainder costs `η(1+‖λ‖₁) ≈ 2.7η` (mean `‖λ‖₁ = 1.7`); a Hamming-Lipschitz remainder
  costs about `5.6η` on the lattice (`4.5η` on the generic chain), 1.7–2 times its lower bound
  `η·d_H(y,A)`: the remainder is paid essentially at the price of the nearest evaluated point, and
  the entry at `η = 0` (0.45 instead of 0) is the price of the constraint `Σλ = 1`.
* **Certificates of the minimum for the sum class** (`out_e6b_n6_L02.txt`, `out_e6b_n6_L10.txt`;
  lattice `n = 6`, 683 conformations, `f = #gauche`, zero residual and remainder, `ε = 0`, `d₀` = torsion
  Hamming with unit constants; greedy upper bounds, exact KR term up to 16 points, hub bound
  beyond):

  | `η` | 0 | 0.1 | 0.25 | 0.5 | 0.75 | 1 | 1.5 |
  |---|---|---|---|---|---|---|---|
  | remainder alone, `N^{ηd_H}_cov` | 1 | 1 | 1 | 1 | 1 | 1 | [22, 29] |
  | `L = 0.2`: sum class | 2 | 2 | 2 | 2 | 7 | 20 | ≤ 53 |
  | `L = 0.2`: first-order cover in the sum envelope (McShane) | 3 | 3 | 3 | 5 | 11 | 27 | 53 |
  | `L = 1`: sum class | 3 | 4 | 4 | 5 | 15 | 24 | 75 |
  | `L = 1`: first-order cover in the sum envelope (McShane) | 7 | 10 | 14 | 18 | 36 | 46 | 132 |

  (span part alone: 2 at `L = 0.2`, 3 at `L = 1`).  Below the sharpness threshold of the remainder
  (`η < e/c = 1`) the cost stays near the span cost only while the remainder leaves most of the gap
  unused; it rises to 20–24 at the threshold and joins the Hamming regime beyond — Corollary 15.

### 3.7 Pair-specific classes, three-body features, one-evaluation thresholds

**P5** (`e8_pairspecific.py` → `out_e8.txt`; phantom diamond chain, `S_c = 12`, every pair its own
type, `δ₁₄ = 1`).  The formula `d_pair = L Σ|s̃ − s̃′|`, `d_P(homopolymer) ≤ d_pair` and
`d_pair ≥ Lδ₁₄ d_tg` hold on 2 000 random pairs for each `n = 5..9`.  Covering numbers at the
extensive radius `ρN` (farthest-point numbers) and ranks:

| `n` | distinct truncated distance matrices | `m(0.5N)` pair-specific / typed | `m(0.125N)` pair-specific / typed | rank (span), pair-specific |
|---|---|---|---|---|
| 5 | 93 | 23 / 8 | 56 / 17 | 21 |
| 7 | 727 | 164 / 22 | 433 / 52 | 43 |
| 9 | 5 832 | 1 160 / 55 | 3 571 / 169 | 73 |

The first-order pair-specific format grows ×2.4–2.9 per torsion at fixed relative radius (the
proved bound `2ⁿ/V(n, ⌊r⌋)`, which uses the 1–4 pairs only, gives 51 at `n = 9`, `ρ = 0.125`); the span
format costs the rank, `21, 31, 43, 57, 73` for `n = 5..9` (second differences 2: quadratic in `N`;
the typed homopolymer profile set has rank at most 4 on this domain),
and the greedy widths respect the proved lower bound `(n−m)/2` with a wide margin (e.g. `n = 9`:
`σ_9 = 92` against 0).  So pair-specific residuals are exponential in the first-order format and
polynomial (between linear and quadratic) in the span format.  On the self-avoiding lattice
(`out_e3_dia12_A99.txt`): rank 48 (`n = 8`) and 75 (`n = 10`), and the greedy width per bead after 32
evaluations is 0.98 at `N = 11` but 2.5 at `N = 13` — for pair-specific classes the per-bead width
at a fixed number of evaluations grows with `N`, the opposite of P4.

**Three-body features** (`e7_threebody.py` → `out_e7.txt`; diamond lattice, self-avoiding,
homopolymer): number of features and rank of the feature matrix over all conformations.

| `S_c` | pair distances (rank) | triangle types (rank), `n = 4, 5, 6, 7, 8, 9` |
|---|---|---|
| 12 | 3 (3) | 4, 4, 4, 4, 4, 4 (rank 4) |
| 28 | 7 (7) | 21, 25, 27, 28, 28, 28 (rank 19, 24, 27, 28, 28, 28) |

The number of features saturates in `N` and grows with the body order (7 → 28 at `S_c = 28`).
Duality for the three-body envelope and conditioning formula (Proposition 17): primal = dual on
40 + 40 instances for each of (`S_c = 12`, `n = 7`), (`S_c = 28`, `n = 6`), max deviation `1.7·10⁻¹³`.

**One-evaluation thresholds** (`e9_thresholds.py`; zero residual, `f = #gauche`; largest `L/e` for
which the single evaluation at the all-trans minimiser is an exact certificate):

| `n` | dia `S_c = 12`: `L*_H` | `L*_P` | `L*_S` | gen `S_c = 16`: `L*_H` | `L*_P` | `L*_S` |
|---|---|---|---|---|---|---|
| 5 | 0.036 | 0.103 | 0.103 | 0.030 | 0.054 | 0.094 |
| 7 | 0.021 | 0.063 | 0.063 | 0.013 | 0.033 | 0.085 |
| 9 | 0.013 | 0.053 | 0.053 | 0.0068 | 0.023 | 0.066 |
| 11 | 0.0096 | 0.040 | 0.040 | 0.0043 | 0.018 | 0.055 |
| 12 | 0.0088 | 0.038 | 0.038 | | | |

All three thresholds decrease with `N` when the known part is purely torsional: the critical
conformation for `d_P` on the lattice is a hairpin with 3 gauche torsions whose profile differs from
the all-trans one by `‖ΔN‖₁ = 29 → 80` (`n = 5 → 12`) — an unknown pair potential of slope `L` can
pay for it.  (On the lattice `L*_S = L*_P` because the all-trans profile is zero.)  The formats
differ by constant factors (4 and 13 at `n = 11` off-lattice) in *when one evaluation suffices*;
the difference of exponents is in what happens beyond the threshold (§3.3).

---
## 4. Prior art, with search log

### 4.1 Which of P1–P5 is a known statement in other words

| claim | what it is | verdict |
|---|---|---|
| **P1** | The configurational *energy equation*: a pair-additive energy is the pair potential integrated against the pair-distance histogram; P1 is that identity after one integration by parts (cumulative counts against `φ′`).  In discretised form it is the feature map of the linear ("LP") potentials: energy = Σ (coefficient of a distance bin) × (number of pairs in the bin) — Maiorov–Crippen (1992), Tobi–Shafran–Linial–Elber (2000).  Henderson's theorem (1974) is the statistical-mechanics shadow of the same linearity (the pair potential is determined, up to a constant, by the pair distribution). | **known** (textbook) |
| **P2** | Kantorovich–Rubinstein duality for the one-dimensional measures of (truncated) pair distances: `sup` over `L`-Lipschitz `φ` of `∫φ d(μ^x − μ^y) = L·W₁`; in one dimension `W₁ = ∫|F − G|` = `ℓ¹` distance of sorted samples.  The cutoff condition `φ(S_c) = 0` is the boundary-reservoir variant (optimal transport with a Dirichlet boundary, Figalli–Gigli 2010; "relative" KR norms).  `W₁`/earth-mover distances between radial distribution functions or interatomic-distance histograms are used as structural dissimilarities in materials informatics (several 2021–2026 papers) — as a *score*. | the identity is **known**; its reading as the exact support function (tightest envelope) of the class of unknown `L`-Lipschitz pair potentials was **not found**, and is immediate |
| **P3** | Optimal recovery of a linear functional from linear information on a balanced convex set (Smolyak 1965; Micchelli–Rivlin 1977; Traub–Woźniakowski 1980): the radius of information is attained at the zero information and equals `sup{S(f) : N(f) = 0}` — here `L·dist₁` to the span.  The data-dependent bracket is the "feasible parameter set" interval of set-membership (unknown-but-bounded) estimation (Milanese–Vicino 1991 and that literature), an LP for box-bounded parameters; equivalently the robust counterpart of an LP with box uncertainty (Soyster 1973; Ben-Tal–Nemirovski). | **known**; the parenthesis of P3 confuses the global radius with the local one (§2.1) |
| **P4, entropy** | Metric entropy of bounded monotone functions in `L¹` is `≍ 1/δ` (Birman–Solomyak 1967; van de Geer 2000; Gao–Wellner 2007 for several variables).  Theorem 7 is this with the chain inserted. | known mathematics; application **new, immediate** |
| **P4, span** | Greedy reduced bases against Kolmogorov widths: Binev–Cohen–Dahmen–DeVore–Petrova–Wojtaszczyk (2011), DeVore–Petrova–Wojtaszczyk (2013).  In practice: active learning of linearly parametrised interatomic potentials by D-optimality/MaxVol (Podryabinkin–Shapeev 2017): choose configurations whose feature vectors span the feature space, add a configuration when its "extrapolation grade" `max_i|λ_i|` exceeds a threshold — the same `λ` as in P3, measured in `ℓ^∞` instead of through the `L¹` misfit. | known mathematics and known practice; the certificate statement **new, immediate** |
| **P5** | Counting parameters: a linear class needs at most as many evaluations as features (theory report §11.14, workstream G's G11); pair-specific contact potentials are the perceptron/LP setting of Maiorov–Crippen. | **known**; Proposition 12/16 (linear lower bound for the span format; exponential only in the first-order format) are the precise form |

What I did not find stated, and therefore list as *apparently new* (none is deep; all proofs are a
few lines once the right object is named): Theorem 4 (certificates of a linear class for the
*minimum* with a known part are covers by subspaces, with the asymmetric gauges `σ^±` in place of
the slack); Theorem 6 (constant / polynomial / exponential on lattices in the three formats);
Theorem 9; Proposition 12 and Lemma 11(c); Theorem 14 with its two-sided bound and Corollary 15;
the corrections to P3 and P4.  Theorem 13 is the classical optimal-recovery formula with noisy
information (the `ℓ¹` penalty is the dual of the sup-norm noise) and is certainly known in that
literature, although I did not locate this exact form.

### 4.2 Search log (web search tool; I read result summaries unless stated)

1. `DeVore Petrova Wojtaszczyk "Greedy algorithms for reduced bases in Banach spaces"` — then the
   ar5iv HTML of arXiv:1204.2290 through the fetch tool: statements of Theorem 3.2, Corollary 3.3
   (i)–(iii), Theorem 4.1, Corollary 4.2 and the definition of the weak greedy algorithm were
   extracted (machine-extracted quotations of the full text; I did not read the PDF myself).  Used
   in Theorem 8: Cor. 3.3(ii) "`d_n ≤ C₀n^{−α}` ⟹ `σ_n ≤ 2^{5α+1}γ^{−2}C₀n^{−α}`"; Cor. 4.2(ii) (Banach:
   `n^{−α+1/2+β}`); their remark that the `√n` loss cannot in general be removed.
2. `optimal recovery linear functional Smolyak lemma … Micchelli Rivlin` — summaries (Foucart–Liao
   papers cite Smolyak's thesis for the existence of a linear optimal map on symmetric convex
   sets; Micchelli–Rivlin 1977).  Not read in full.
3. `"adaption does not help" … Bakhvalov Gal Micchelli Traub Wozniakowski` — summaries: Bakhvalov
   for linear functionals, Gal–Micchelli and Traub–Woźniakowski (1980) for operators; radius of
   information at zero.  One summary notes that for *randomised* algorithms adaption can gain a
   factor `n^{1/2}` in some problems — relevant to §5.4.
4. `metric entropy of … bounded monotone functions L1 … van de Geer Birman Solomjak Gao Wellner` —
   summaries only; the `1/δ` law is quoted from memory of van de Geer (2000, Thm 2.4) and
   Birman–Solomyak; **not re-verified in a primary source**, which is why the Lemma of §2.4 is
   proved here with its own constant.
5. `Wasserstein distance between radial distribution functions structural similarity …` —
   summaries (a 2021 paper on local-structure dissimilarity of crystals, a 2023 Digital Discovery
   paper on interatomic-distance representations with earth-mover distance, two generative-model
   papers using `W₁` between distance histograms).  Abstract level.
6. `Maiorov Crippen 1992 contact potential … linear programming` — summary/abstract (J. Mol. Biol.
   227, 876): inequalities "native below decoys" for a potential linear in its parameters.  Cited
   only as the mathematical prior art for linear-in-features potentials; no data used.
7. `Tobi Shafran Linial Elber "On the design and analysis of protein folding potentials"` — summary.
8. `Podryabinkin Shapeev active learning linearly parametrized interatomic potentials D-optimality
   MaxVol extrapolation grade` — summaries (arXiv:1611.09346; follow-ups define the grade).
9. `Kolmogorov n-width transport dominated problems … Ohlberger Rave` — summaries: `d_n ≍ n^{−1/2}`
   in `L²` for families of jumps; consistent with the `1/n` rate in `L¹` used in §2.4 (the `L¹` rate is
   my own two-line estimate, not a quotation).
10. `Soyster 1973 … robust linear programming box uncertainty Ben-Tal Nemirovski` — summaries.
11. `Milanese Vicino "set membership" optimal estimation …` — summaries (Automatica 27 (1991)
    997–1009).
12. `Kloeckner "Wasserstein space" metric entropy …` — summary (critical parameter `d` for the
    Wasserstein space of a `d`-manifold); used only as orientation for Proposition 17.
13. `Henderson theorem 1974 uniqueness pair potential radial distribution function` — summaries.
14. `Kolmogorov width of l_infinity ball in l_1 … Pietsch Stesin` — summaries (the theorem
    `d_n(B_p^N, ℓ_q^N) = (N−n)^{1/q−1/p}`, `q ≤ p`, is stated in recent papers of Vasil'eva with that
    attribution); the case used here has a three-line proof (Lemma 11(c)).
15. `Figalli Gigli "new transportation distance between non-negative measures" …` — summary.
16. `Kantorovich Rubinstein … Lipschitz functions vanishing on boundary …` — summaries
    (relative optimal transport, arXiv:2411.05678; KR norm vs flat norm).

Not searched (out of time): the optimal-recovery literature for *nonlinear* functionals such as a
minimum over a known part (Theorem 4); Lebesgue constants of `L¹` greedy bases; the
statistical-mechanics literature on realisable pair-correlation functions (which is what the
limit set `K_∞` of §5.2 is).

---
## 5. What I did not settle

1. **The true entropy and widths of the profile sets of chains.**  Theorems 7–8 are upper bounds
   through the class of all monotone functions; measured numbers are smaller by orders of
   magnitude.  Open: the limit set `K_∞ = lim K_N/N` (approximately convex by concatenation of
   blocks — not proved with excluded volume, where chain ends can be trapped), its entropy
   (`DT`-dimensional on lattices; off-lattice a `1/δ` law or less?), the rate of the inner widths
   (`1/m`? Theorem 8 gives `m^{−1/2}`), and the size of `N` at which normalised quantities stop
   depending on `N` (not reached at `N ≤ 16` except in the three-feature model).
2. **A limit theorem.**  At extensive accuracy the natural statement is thermodynamic: with
   `e_f(F)` the profile-constrained ground-state energy per bead, `min E/N → min_F [e_f(F) + ĝ(F)]`,
   and certificate sizes should converge to those of this problem on `K_∞` (for `P_L`:
   `ĝ` linear, the minimum is a Legendre transform of `e_f`).  Not attempted.
3. **Fixed absolute accuracy off-lattice.**  For `f ≡ 0` the first-order `d_P` format looks
   exponential (`n ≤ 13`); a proof needs exponentially many profiles pairwise `ε/L` apart (block
   mixtures with generic block profiles: `ln N ≳ cN/ln N` heuristically).  For gapped additive `f` the
   truth lies between polynomial and the `exp(O(√(N ln N)))` of Theorem 9; no lower bound.
4. **Randomised algorithms for linear classes.**  All lower bounds here are for deterministic
   (adaptive) schemes, via the zero residual.  With rich profile sets, group-testing-like
   strategies can localise sparse perturbations with few evaluations, and concentration makes
   minima of many independent unknowns predictable; whether a randomised algorithm can beat the
   width count on worst-case instances of `P_L` is open (the dip construction of the first-order
   theory has no direct analogue: a generic evaluation "sees" every perturbation).
5. **Exact value certificates and exact `ln Z` brackets for `P_L`.**  The value-certificate criterion
   is a max–min over the consistent polytope; for `ln Z` the upper end is a convex maximisation.
   I used point certificates / pointwise brackets (sufficient) and exact vertex enumeration only
   for `F ≤ 4` features.  The gap between the two is visible (`ln Z`, lattice, `n = 8`, `L = 0.2`,
   `ε = 0.01`: pointwise greedy 3, exact minimum 2).
6. **The sum class.**  Corollary 15 is a lower bound (a maximum).  The upper side is a joint
   design problem (span points cheap in the remainder metric need large coefficients); `e6b`
   gives greedy sizes for one small chain only.  No theorem.
7. **Excluded volume in the lower bounds.**  Proposition 12 and Proposition 16(a) are proved on
   the product domain.  With excluded volume the needed sub-families (independent kinks without
   other pairs entering the cutoff) exist only for well-separated kinks; I verified the
   conclusions numerically (`e8` phantom; `e3` self-avoiding widths) but did not prove them.
8. **Valid Hamming constants on non-product domains.**  On the self-avoiding domain validity is a
   system of `2ⁿ − 1` inequalities (one per set of changed torsions); I used the LP-minimal sum of
   constants (it coincided with the single-flip maxima for `n ≤ 8` on the lattice) for upper bounds
   and the single-flip maxima for lower bounds.  Other valid choices could give smaller Hamming
   certificates than the greedy numbers reported, never smaller than the lower bounds.
9. **Three-body classes**: only the duality and a feature count on the lattice; nothing
   off-lattice, no widths in the `KR` norm.
10. **Checking a certificate.**  All counts are evaluations of the residual.  Checking a span
    certificate means minimising a concave function over the consistent polytope `K_v`
    (= one pair-additive ground-state problem per vertex of `K_v`), and checking a `d_P`-certificate
    means minimising `f(y) − L‖N^y − N^a‖₁`, which is not pair-additive.  Not studied.

## 6. The three most promising next steps

1. **Make the linear class a kernel interface, with the remainder in it.**  Replace "constants `c_i`
   per torsion" by "features + box + remainder": certificate = evaluated set, coefficients `λ(y)`
   are not even needed — soundness is weak duality (for *every* `λ` the bound of Theorem 13/14
   holds), so a checker only verifies arithmetic.  The lower bound of the minimum is
   `min_{ψ ∈ vert K_v} min_y E_ψ(y)`: finitely many pair-additive minimisations, i.e. the existing
   pairwise kernels applied to each vertex of the consistent polytope (robust LP with box
   uncertainty).  Machine-check Theorem 4 (cover ⟺ certificate) and the weak-duality halves of
   Theorems 13–14; decide which remainder class (sup-norm `η`, profile-Lipschitz, three-body
   transport) a concrete residual can be certified to satisfy.
2. **Prove the thermodynamic statement for one model.**  For the diamond chain with `D` features:
   existence and convexity of `K_∞` and of the constrained ground-state energy `e_f`, and
   convergence of the normalised certificate sizes in the P and S formats to those of the limit
   problem (a covering / width problem for a convex function on a `DT`-dimensional convex body).
   This would replace the useless constants of Theorems 7–8 by the right ones and say at which
   `N` the chain-length independence sets in.
3. **Settle what a remainder costs, and whether randomisation helps.**  (a) An upper bound for the
   sum class `P_L + Lip(ηd₀)` matching Corollary 15 up to constants, or a proof that the cost is
   genuinely a product; (b) the randomised complexity of `P_L` at the zero residual (is the width
   count a lower bound for Monte Carlo algorithms? the references in §4.2 item 3 suggest that
   adaption-with-randomisation can gain polynomial factors for some linear problems); (c) the
   body-order hierarchy: transport envelopes for 2-, 3-, 4-body profiles with decreasing Lipschitz
   constants, as the chain-specific replacement of the second-order classes of theory report
   §11.7.

---
## 7. Files, commands, outputs

All in `scratch:ws/P/`.
Every command was run from that directory after `ulimit -v 3000000; export OMP_NUM_THREADS=1
OPENBLAS_NUM_THREADS=1` (never more than two processes at once).  Python 3.13, numpy 2.5, scipy 1.18
(HiGHS).  Run times are wall-clock on the shared machine.

Libraries: `plib.py` (builders, profiles, LP brackets of P3 in `λ`- and `ψ`-form, covering tools,
exact rational simplex), `chains.py` (exhaustive enumeration with excluded volume, quantile
representation, profile classes, farthest-point traversal), `formats.py` (Hamming constants,
covers, span oracle and greedy span covers, width lower bound), `widths.py` (greedy `L¹` widths,
Bernstein and eigenvalue lower bounds, coefficient norms), `robust.py` (Theorems 13, 14: primal and
dual LPs), `sampling.py` (growth with excluded volume, periodic words, mixtures, hairpin sheets).

| command (`python3 …`) | output | time | what it establishes |
|---|---|---|---|
| `t0_selftest.py` | (stdout) `ALL SELF-TESTS PASSED` | 1 s | geometry (bond lengths, angles, dihedrals; lattice integrality, `s₁₄ ∈ {19, 11}`), P1 identity, `L¹` = quantile form, exact simplex against HiGHS |
| `e1_verify_P123.py` | `out_e1.txt` | 3 m 57 s | §3.1: P1 exact; P2 max dev `2.3e-13`; P3 `all 324 parameter cells: max |primal - dual| = 1.01e-10`; `288 instances solved exactly … 288 / 288`; half-width/`L·dist₁` statistics; explicit instance |
| `e2_entropy_exhaustive.py dia 12 1 4 13` (also `… 2 4 12`, `… 4 4 12`, `… 2r …`, `… 4r …`, `… 8r …`, `… 99 …`; `dia 28 1 4 12`; `gen 16 {1 4 13, 2 4 12, 4 4 12, 4r 4 12, 99 4 12}`) | `out_e2_<geom><S_c>_A<A>.txt` | 7–55 s each | §3.2 exhaustive tables (`A` with suffix `r` = pseudo-random type sequence, `99` = every bead its own type) |
| `e2b_entropy_sampled.py 12 1 960` (also `12 2`, `12 4 480`, `28 1`, `12 2r`, `12 4r`) | `out_e2b_S<S_c>_A<A>.txt` | 0.5–1.5 m each | §3.2 sampled long chains |
| `e3_widths_exhaustive.py gen 16 1 8 12 2` (also `dia 28 1 8 12 2`, `dia 12 1 8 12 2`, `gen 16 2r 8 10 2`, `gen 16 4r 8 8`, `dia 12 4r 8 12 2`, `dia 12 99 8 10 2`) | `out_e3_<…>.txt` (`gen 16 4r`: `out_e3_gen16_A4r_n8.txt`; the `n = 10` part of that run was stopped) | 12 s – 7 m | §3.5 widths, lower bounds, coefficient norms |
| `e3b_widths_sampled.py 480 104` | `out_e3b_gen.txt` | 2 m 45 s | §3.5 long generic chains |
| `e4_formats_min.py dia 12 1 5 12` | `out_e4_dia12_A1.txt` | 7 m 18 s | §3.3 lattice table |
| `e4_formats_min.py gen 16 1 5 10 0 9` | `out_e4_gen16_A1.txt` | 13 m (≤ 3 m per `n`) | §3.3 generic table |
| `e4_formats_min.py dia 28 1 5 10` (stopped during `n = 7`); `… dia 28 1 8 9` | `out_e4_dia28_A1_partial.txt`; `out_e4_dia28_A1_n8_9.txt` | 9 m; 5 m 41 s | §3.3 other models |
| `e4_formats_min.py dia 12 2 5 10`; `… dia 12 2r 5 10` (stopped during `n = 10`); `… dia 12 1 5 11 0.5`; `… gen 16 1 5 9 0.5 8` | `out_e4_dia12_A2.txt`, `out_e4_dia12_A2r.txt`, `out_e4_dia12_A1_k05.txt`, `out_e4_gen16_A1_k05.txt` | 11 m; 14 m; 3 m; 5 m | §3.3 two types; random residual |
| `e5_formats_lnZ.py dia 12 1 5 10`; `… gen 16 1 5 9 0 8` | `out_e5_dia12_A1.txt`, `out_e5_gen16_A1.txt` | 8 m; 2 m 47 s | §3.4 `ln Z` |
| `e6_robust.py` | `out_e6.txt` | 1 m 28 s | §3.6: Theorems 13–14 primal = dual (max `1.1e-12`), brackets against `η` |
| `e6b_sumclass.py 6 0.2`; `e6b_sumclass.py 6 1.0` | `out_e6b_n6_L02.txt`, `out_e6b_n6_L10.txt` | 20 s; 34 s | §3.6: certificates of the sum class |
| `e7_threebody.py` | `out_e7.txt` | 5 s | §3.7 three-body features and dualities |
| `e8_pairspecific.py` | `out_e8.txt` | 6 s | §3.7 pair-specific classes (P5) |
| `e9_thresholds.py dia 12 5 12`; `… gen 16 5 11` | `out_e9_dia12.txt`, `out_e9_gen16.txt` | 18 s; 34 s | §3.7 one-evaluation thresholds |

Scripts that take arguments have small defaults, so each of them also runs as plain
`python3 <script>` (a reduced case).  `run_batch1..4.sh` are the shell scripts that produced the outputs in sequence; `x_*.py` are
exploratory/profiling scratch scripts, not used for any claim.  Remarks on reproducibility:
(i) the `e4` runs print for `n ≤ 6` exact LP/MILP values for H; beyond, the H lower bound is the
partition bound and the upper bound a greedy cover; (ii) in `out_e4_dia12_A2.txt` and in the first
runs the S upper bound is the greedy value (it may exceed the rank by one because the all-trans
minimiser has the zero profile); the current script caps it by the rank; (iii) three long runs were
stopped by hand (`dia 28` in `e4` at `n = 7`, `dia 12 2r` in `e4` at `n = 10`, `gen 16 4r` in `e3` at `n = 10`) — their completed parts
are in the files named above; (iv) the sizes of the brute-force searches for S are limited by time
(sets of size 1 always; size 2 only for ≤ 200 or ≤ 400 profile classes, with a time limit), so an
S lower bound of 2 or 3 is exact only where the search completed (it did on the lattice
`S_c = 12`, homopolymer).

Scope statement: everything here is synthetic mathematics on model chains; no biological
sequences, no sequence design, no experimental data.
