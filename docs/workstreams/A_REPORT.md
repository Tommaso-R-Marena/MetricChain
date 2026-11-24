# Workstream A — the randomised exponent of `ln Z`: a two-measure isoperimetric problem

Directory: `<session scratch>/ws/A/`
(all scripts and outputs referred to below are in this directory; I modified nothing in the
repository — it was read at the state of 2026-11-24 ≈19:15 UTC and was being edited by others
while this work ran).  Status labels: **[K]** known (cited), **[R]** routine, **[N]** apparently new,
**[P]** paper proof by me, not machine-checked, **[V*]** machine-checked in my scratch file
`lean/WorkstreamA.lean` (Lean 4.31 + the repository's Mathlib via `lake env lean`; standard axioms
only; not part of the repository), **[num]** numerical evidence only.

---

## 1. Verdicts

**The main conjecture is false for alphabets of size ≥ 3 and true for two-state sites, and the
exact single-letter exponent is now known for every alphabet.**  On a product instance
`X = Sⁿ` (single-site Gibbs measure `π`, single-site slack `s`) the randomised query exponent of
`ln Z` at accuracy `nε₁ + o(n)` is

    R^gen_β(ε₁) = max_{0≤t≤β} [ −ln val(K_t) − t ε₁/β ],      K_t(a, φ) = exp(−t[φ(a) − Λ(φ)/β]),

where `a` ranges over the letters, `φ` over the **vertices of the Lipschitz polytope** of the
site, `Lip(S,s) = {φ : φ(a) − φ(b) ≤ s(a,b)}` modulo constants, `Λ(φ) = −ln Σ_a π(a) e^{−βφ(a)}`
is the soft gap of the "centre" `φ`, and `val` is the value of the matrix game (sampler chooses a
letter law `Q`, adversary a vertex).  The report's `R^rand_β` is the same expression with the
vertices replaced by the `|S|` distance functions `s(·,b)` (the single dips).  (Theorem A: lower
bound for every `n` and every algorithm; matching upper bound by an explicit *universal* sampler —
the uniform mixture over type classes — via the inherently-typical-subset method of
Ahlswede–Yang–Zhang; paper proof, corroborated numerically.)  Consequences: (i) for `|S| = 2` the
Lipschitz polytope is a segment whose two vertices are the two distance functions, so
`R^gen = R^rand`: **single dips are extremal at the exponential scale on every binary product
instance** (biased cube, arbitrary additive residual, asymmetric slack), with a closed form;
(ii) for `|S| ≥ 3` the polytope has further vertices ("dips centred at a subset of states"; for the
Hamming envelope: one for every proper nonempty subset `B ⊂ S`) and they win at intermediate and
high temperature: flat 4-state site at `βc = 1`: `0.02914 > 0.02841`; flat 8-state site:
`0.0309` against `0.0194`; three-state site with energies `(0,0,2)`, `β = c = 1`: `0.0290` against
`0.0247`; the ratio `R^gen/R^rand` is unbounded (`→ k²/(4(k−1))` for flat `k`-state sites as
`βc → 0`).  This is `DEAD_ENDS` D34 ("unions of shallow dips") surviving the product limit: the
extremal perturbations are unions of dips whose centres fill a *box* `∏ B_i`.  (iii) The
accuracy threshold conjectured in the report (`ε₁^crit`, a game over dips) is correct for binary
sites and too small in general; the true threshold is `ε₁^thr = β·min_Q max_φ [E_Q φ − Λ(φ)/β]`
(game over Lipschitz vertices), and it is **sharp for every alphabet and every `n`**: above it a
*dimension-free* two-reference sandwich gives `O(1)` random evaluations (Theorem B; its core is
machine-checked in a scratch file), below it the
cost is `exp(n R^gen(ε₁))` with `R^gen(ε₁) > 0`.  (iv) Negative: no *product* sampler `Qⁿ` attains
the exponent on a biased site (e.g. `0.1655` against `0.1541`), so the result is not a corollary
of the known isoperimetric exponent for two fixed product measures (Yu 2024), and tensorisation
alone cannot prove it; at finite `n` dips are not extremal even on the uniform cube (exact
`FC/FC_dip` up to `2.1` for `n ≤ 6`), only at the exponential scale.

---

## 2. Statements, proofs, counterexamples

### 2.0 Setting and the combinatorial form

*Site.*  `S` finite, `k = |S| ≥ 2`; `π` a probability vector on `S` with full support; `s : S×S →
[0,∞)` a quasi-metric (`s(a,a) = 0`, triangle inequality, not necessarily symmetric);
`s_max = max s`; `β > 0`.  For an additive instance with Hamming envelope constant `c`, known part
`φ_site` and residual `γ`: `π ∝ e^{−β(φ_site+γ)}`, `s(a,b) = c[a≠b] − γ(a) + γ(b)`.
Convention as in the brief: in `s(a,b)` the first argument is the letter of the *evaluated* point,
the second the letter of the centre.

*Product.*  `X_n = Sⁿ`, `πⁿ`, `s_n(x,y) = Σ_i s(x_i,y_i)`.

*Perturbation profiles.*  `g' = g − h` is admissible iff `h(y) − h(x) ≤ s_n(x,y)` for all `x,y`,
and then `Z(f+g')/Z(f+g) = E_{πⁿ} e^{βh}` **[K]** (repository: `dip_eq_sub`, `sum_exp_dip`).
For `D ⊂ X_n` the largest admissible profile vanishing off `D` is
`h_D(y) = min_{x∉D} s_n(x,y)`.  A set is *sensitive at level `ε`* if `ln E e^{βh_D} > ε`;
`𝒟_n(ε)` is the family of sensitive sets and

    FC_n(ε) = 1 / max_q min_{D ∈ 𝒟_n(ε)} q(D)

its fractional hitting number.  By Theorem 11.22 of the theory report **[K, machine-checked there]**
every randomised `(ε/2, δ)`-correct algorithm makes at least `(1−2δ) FC_n(ε)` evaluations in
expectation at the instance, and the spot-check with a hint needs `⌈ln(1/δ)·FC_n(ε')⌉` samples
(plus `O(ln(1/δ))` samples of `π` for "bumps", below), `ε'` slightly smaller than `ε`.

**Lemma 0 [R].**  (a) If `h` is admissible then so is `h₊`, `supp h₊ ⊂ supp h`,
`E e^{βh₊} ≥ E e^{βh}`; and if `ln E e^{βh} < −ε'` then `π(supp h) > 1 − e^{−ε'}`.  So raising
alternatives are found by sampling `π`, and only nonnegative profiles matter.
(b) (*level sets*) Let `h ≥ 0` be admissible, `h ≤ H`, `E_π e^{βh} ≥ 1 + η`, `J = ⌈βH⌉`.  Then for
some `r ∈ {0, 1/β, …, (J−1)/β}` the set `A = {h > r}` has `π(A) ≥ η e^{−βr−1}/J`, and
`Γ_r(A) := {x : min_{y∈A} s(x,y) ≤ r} ⊂ supp h`.
*Proof.*  (a) is a case distinction; for the second claim `E e^{βh} ≥ E e^{−βh₋} ≥ 1 − π(supp h₋)`.
(b) `E e^{βh} − 1 = ∫_0^H β e^{βρ} π(h>ρ) dρ ≤ Σ_{j<J} e^{j+1} π(h > j/β)`; and `h(x) ≥ h(y) −
s(x,y) > 0` if `h(y) > r ≥ s(x,y)`. ∎

So at the exponential scale the problem is the one stated in the brief: the adversary chooses
`(A, r)` with `π(A) e^{βr} ≳ e^{ε}`, the sampler must hit the slack-`r`-neighbourhood `Γ_r(A)`.
Because the instance is invariant under coordinate permutations, an optimal sampler is a mixture
of uniform distributions on type classes, and for a fixed `D` the best mixed adversary applies a
uniformly random permutation to `D`: *the exponent is `max_D min_types (−n⁻¹ ln density of D in
the type class)`.*

### 2.1 Generalised dips, and a lower bound for every `n`

**Lemma 1 (generalised dips) [R; V*: `genDip_admissible`, `genDip_effect`].**  On any instance let `Φ : X → ℝ` satisfy
`Φ(x) − Φ(y) ≤ s(x,y)` ("`Φ ∈ Lip(X,s)`"; distance functions `s(·,y)` are of this kind) and let
`c ∈ ℝ`.  Then `h = (c − Φ)₊` is an admissible profile, `supp h = {Φ < c}`, and

    E_π e^{βh} ≥ e^{βc − Λ(Φ)},        Λ(Φ) := −ln E_π e^{−βΦ}.

Hence the queries of every `(ε/2,δ)`-correct randomised algorithm hit `{Φ < r}` with probability
`≥ 1 − 2δ` whenever `βr > Λ(Φ) + ε`.  For `Φ = s(·,y)` this is the dip and the soft gap `Λ(y)` of
Theorem 11.24.  Since `Φ = min_y [Φ(y) + s(·,y)]` for every `Φ ∈ Lip`, `h = max_y (c − Φ(y) −
s(·,y))₊` is a *union of single dips with centre-dependent depths* — the objects of D34.
*Proof.*  `t ↦ t₊` is nondecreasing and 1-Lipschitz, so `h(y) − h(x) ≤ (Φ(x) − Φ(y))₊ ≤ s(x,y)`;
`e^{β(c−Φ)₊} ≥ e^{β(c−Φ)}`. ∎

For a site write `Lip = Lip(S,s)`, `Λ(φ) = −ln Σ_a π(a) e^{−βφ(a)}` and `σ_φ(a) = φ(a) − Λ(φ)/β`
(the normalisation `E_π e^{−βσ_φ} = 1`).

**Proposition 2 (exponential-weights lower bound; every `n`) [N, routine proof; ingredients V*].**  Let `F ⊂ Lip`
be finite, `M` a probability vector on `F`, `t ≥ 0`, and
`ρ_t(M) = max_{a∈S} Σ_{φ∈F} M(φ) e^{−t σ_φ(a)}`.  Then for all `n` and `ε > 0`

    FC_n(ε) ≥ e^{−tε/β} ρ_t(M)^{−n},

so every randomised `(ε/2,δ)`-correct algorithm for `ln Z` makes at least
`(1−2δ) e^{−tε/β} ρ_t(M)^{−n}` evaluations in expectation at the instance.  Minimising over `M`:
`min_M ρ_t(M) = val(K_t^F)`, the value of the matrix game `K_t^F(a,φ) = e^{−tσ_φ(a)}`.
*Proof.*  For `φ⃗ ∈ Fⁿ` let `Φ_φ⃗(x) = Σ_i σ_{φ_i}(x_i)` — additive, in `Lip(X_n, s_n)`, with
`Λ(Φ_φ⃗) = 0` — and `h_φ⃗ = (c − Φ_φ⃗)₊` with `βc = ε' > ε`: sensitive by Lemma 1.  Draw `φ⃗ ∼
M^{⊗n}`.  For each fixed `x`, by Markov's inequality,
`P(x ∈ supp h_φ⃗) = P(Σ_i σ_{φ_i}(x_i) < c) ≤ e^{tc} ∏_i Σ_φ M(φ) e^{−tσ_φ(x_i)} ≤ e^{tε'/β} ρ_t(M)ⁿ`.
For any sampler `q`, `min_D q(D) ≤ E_φ⃗ q(supp h_φ⃗) = Σ_x q(x) P(x ∈ supp h_φ⃗) ≤ e^{tε'/β} ρ_tⁿ`;
let `ε' ↓ ε`.  The algorithmic statement is Theorem 11.22(c) with the weights `M^{⊗n}`. ∎

With `F` = distance functions this is the machine-checked `thermal_product_randomized`; the new
content is that other `φ` are allowed, and which ones matter (next).

*Machine check of the two ingredients* (`lean/WorkstreamA.lean`, products as nested pairs):
every generalised dip `(c − Φ_φ⃗)₊` is admissible for the additive slack (`sumSig_lipschitz`,
`sumS_nonneg`, `genDip_admissible`) and multiplies `Z` by at least `e^{βc}` when the site
functions are normalised (`genDip_product_effect`); and a fixed point `x` lies in the supports
of dips of total `M^{⊗n}`-weight at most `e^{tc}ρⁿ` whenever `Σ_φ M(φ) e^{−tσ_φ(a)} ≤ ρ` for all `a`
(`detect_weight_le`).  The remaining step is the repository's `expected_queries_ge_packing`.

### 2.2 The exponent `R^gen` and its properties

Let `𝒱` be the vertex set of the polytope `Lip ∩ {φ(a₀) = 0}` (finite), `𝒱₀ = {s(·,b) : b ∈ S}`
the distance functions,

    g(φ; Q, t) = −(t/β) Λ(φ) − ln E_Q e^{−tφ},     G(Q,t) = max_{φ ∈ Lip} g(φ; Q, t),
    R^gen_β(ε₁) = max_{0≤t≤β} [ −ln val(K_t) − t ε₁/β ],   K_t = K_t^{𝒱};
    R^rand_β(ε₁) = the same with K_t^{𝒱₀}.

(That the game form of `R^rand` is the report's `max_P R(P; s, (E_P[Λ₁]+ε₁)/β)` is Csiszár's dual
formula; `sl.py` reproduces the report's values `0.0275, 0.154, 0.1882` (`e/c = 1/2`,
`β = 1, 4, 40`) and the cube formula `ln 2 − h(ρ₀)`; `v11_ba_check.py` compares with a
Blahut–Arimoto brute force.)

**Lemma 3 [N].**
(a) `−ln val(K_t^F) = min_Q max_{φ∈F} g(φ;Q,t)` for every finite `F`.
(b) `min_Q G(Q,t) = 0` for `t ≥ β`.
(c) For `0 ≤ t ≤ β` and every `Q`, `G(Q,t) = max_{φ∈𝒱} g(φ;Q,t)`: *the maximum over the Lipschitz
polytope is attained at a vertex.*  (For `t > β` it need not be: `v12_vertex_reduction.py`.)
(d) Hence `sup_{t≥0} [min_Q G(Q,t) − tε₁/β] = R^gen_β(ε₁)` for `ε₁ ≥ 0`; `R^gen_β` is convex,
nonincreasing and continuous on `[0,∞)`, and `R^gen_β(ε₁) > 0` iff
`ε₁ < ε₁^thr := β · min_Q max_{φ∈𝒱} [E_Q φ − Λ(φ)/β]`.
(e) `R^gen_β(ε₁) = max_{M ∈ Δ(𝒱)} R(M; σ, ε₁/β)`: the largest rate–distortion function of a
source on the vertex set, with reproduction alphabet `S` and distortion `σ_φ(a)` — the report's
table with "centres = points, budget `(E_P[Λ₁]+ε₁)/β`, distortion `s`" replaced by "centres =
Lipschitz vertices, budget `(E_M[Λ(φ)]+ε₁)/β`, distortion `φ(a)`".
(f) `R^rand_β ≤ R^gen_β ≤ U_β = ln Σ_b π(b) e^{Λ₁(b)}`.
*Proof.*  (a) `max_φ g = −ln min_φ Σ_a Q(a) K_t(a,φ)`.
(b) `g(φ;π,t) = (t/β) ln E_π e^{−βφ} − ln E_π e^{−tφ} ≤ 0` for `t ≥ β` (monotonicity of `L^p`
norms of `e^{−φ}`), with equality for constants.
(c) Let `t < β` and let `φ*` maximise `g(·;Q,t)` over the polytope, in the relative interior of a
face `F` of dimension `≥ 1`.  The directions of `F` are the functions `ψ` that are constant on the
connected components `C` of its tight graph (at least two components).  Along `φ* + λψ`,
`g' = t(E_{Q_λ}ψ − E_{π_λ}ψ)` and `g'' = t(β Var_{π_λ}ψ − t Var_{Q_λ}ψ)`, where `π_λ ∝ π
e^{−β(φ*+λψ)}`, `Q_λ ∝ Q e^{−t(φ*+λψ)}`.  Stationarity for `ψ = 1_C` gives `π_0(C) = Q_0(C) =: p`,
with `0 < p < 1` because `π` has full support; then `g'' = t(β − t) p(1−p) > 0`, contradicting
maximality.  So the maximum is at a vertex; `t = β` by continuity.
(d) From (b), (c); `F(t) := −ln val(K_t)` satisfies `F(t)/t ↑ min_Q max_φ [E_Qφ − Λ(φ)/β]` as
`t ↓ 0` (each `g(φ;Q,·)` is concave and vanishes at `0`).
(e) `R(M;σ,D) = max_{t≥0} min_Q [−tD + Σ_φ M(φ) g(φ;Q,t)]`; exchange `max_M` and `min_Q` (linear in
`M`, convex in `Q`).
(f) `𝒱₀ ⊂ Lip` and (c).  For the upper bound take `Q̃ ∝ π e^{Λ₁}`: for `φ ∈ Lip`,
`e^{−Λ(φ)} ≥ e^{−βφ(a) − Λ₁(a)}` (because `φ(x) ≤ φ(a) + s(x,a)`), so
`E_Q̃ e^{−tφ} ≥ e^{−U_β + Λ(φ)} E_π e^{−(β+t)φ} ≥ e^{−U_β − tΛ(φ)/β}` (Jensen), i.e.
`g(φ;Q̃,t) ≤ U_β` for all `t`. ∎

**Closed forms.**
* *Two-state sites* (`s₀₁ = s(0,1)`, `s₁₀ = s(1,0)`): `𝒱 = 𝒱₀` and, whenever the 2×2 game has
  no saddle point (generic),

      R^gen = R^rand = max_{0≤t≤β} { ln[(1−e^{−t s₀₁}) e^{−tΛ₁(0)/β} + (1−e^{−t s₁₀}) e^{−tΛ₁(1)/β}]
                                     − ln(1 − e^{−t(s₀₁+s₁₀)}) − tε₁/β };

  for the biased cube (`s₀₁ = s₁₀ = c`, `u = βc`):
  `max_t { ln[(π₀+π₁e^{−u})^{t/β} + (π₁+π₀e^{−u})^{t/β}] − ln(1+e^{−tc}) − tε₁/β }`, threshold
  `ε₁^thr = ½[u + ln(π₀+π₁e^{−u}) + ln(π₁+π₀e^{−u})]` (`= ln cosh(u/2)` for the uniform cube; `0.1137`
  for `e/c = ½`, `β = 1`, the report's `ε₁^crit`).
* *Hamming envelope, any additive residual `γ`*: `ψ = φ + γ` is 1-Lipschitz for `c` times the
  uniform metric, so the vertices are `φ_B = c·1[a ∉ B] − γ`, one for each nonempty proper
  `B ⊂ S` (`2^k − 2` vertices; the singletons are the dips), and
  `e^{−Λ(φ_B)} = [Z₁^f(B) + e^{−βc} Z₁^f(Bᶜ)]/Z₁`, `Z₁^f(B) = Σ_{a∈B} e^{−βφ_site(a)}`.  The
  generalised dip with site functions `φ_{B_i}` is `h(x) = c·(R − #{i : x_i ∉ B_i})₊` (for `γ = 0`):
  **a dip centred at the box `∏ B_i`**, i.e. the union of the equally deep dips at all points of
  the box.  (For a generic metric on `k` points the Lipschitz polytope has `C(2k−2, k−1)`
  vertices, Gordon–Petrov 2017.)
* *Flat `k`-state site* (`π` uniform, `s = c[a≠b]`): by symmetry `Q` uniform is optimal and

      R^gen_β(ε₁) = max_{1≤m≤k−1} D( ρ_m ‖ 1 − m/k )₊ ,    ρ_m = [ε₁ − ln(m/k + (1−m/k)e^{−u})]/u,

  (`D` the binary relative entropy, `0` if `ρ_m ≥ 1−m/k`); the report's `R^rand` is the term
  `m = 1`.  For `u → 0`: `D ≈ u² θ(1−θ)/8` with `θ = m/k`, so `R^gen/R^rand → k²/(4(k−1))`
  (`k` even).

### 2.3 Theorem A: the exact exponent

**Theorem A [N; P].**  Let `(S,π,s)` be a site, `β > 0`, and `ε_n > 0` with `ε_n/n → ε₁ ∈ [0,∞)`
and `n⁻¹ ln(1/ε_n) → 0`.  Then

    lim_{n→∞} n⁻¹ ln FC_n(ε_n) = R^gen_β(ε₁).

More precisely: (i) `FC_n(ε) ≥ e^{−tε/β} val(K_t)^{−n}` for all `n`, `t ≥ 0`, `ε > 0`; (ii) the
*universal sampler* `q_n = ½ πⁿ + ½ · (uniform mixture, over the type classes of Sⁿ, of the uniform
distributions on them)` — whose second half depends neither on `β` nor on `s` — satisfies
`min_{D∈𝒟_n(ε_n)} q_n(D) ≥ exp(−n R^gen_β(ε₁) − o(n))`.
Consequently, for fixed `δ ∈ (0,½)`, the least expected number of evaluations at the additive
instance, among randomised algorithms that are `(ε_n/2, δ)`-correct for `ln Z` on the whole
admissible class, is `exp(n R^gen_β(ε₁) + o(n))`.

*Remarks on the statement.*  The hypothesis `ln(1/ε_n) = o(n)` is necessary for the same reason as
in Theorem 11.15 (D29): for exponentially small `ε` single points become sensitive.  For the
algorithmic statement the upper bound is the spot-check of Theorem 11.22(d) with hint `g`, output
`ln Z(g) + ε_n/2 − ε'` with `ε' = min(1, ε_n/2)`: undetected alternatives then have
`ln Z(g') − ln Z(g) ∈ [−ε', ε_n − ε']`; lowerings by more than `ε_n − ε'` are in `𝒟_n(ε_n − ε')`,
raisings by more than `ε'` differ from `g` on Gibbs weight `≥ 1 − e^{−ε'}` (Lemma 0a); the same
hedging device was being added to the repository while this was written
(`QueryRefinements.lean`, `hedgedSpotCheck_correct`; seen read-only).  On additive
instances the hint costs `n(k−1)+1` evaluations (star + additive interpolant, exactly as in
"learn-then-cover", Theorem 11.23(ii): the interpolant of an admissible residual is admissible for
the Hamming envelope, and if it does not have the expected form the algorithm falls back to full
evaluation).

*Proof of (i).*  Proposition 2 with `F = 𝒱` and an optimal column strategy `M`. ∎

The proof of (ii) needs two ingredients.

**Proposition 4 (the auxiliary variable collapses to a matrix game) [N; the dualisation
technique is K].**  Let `𝒰` be a finite set and `P_{UX}` a law on `𝒰×S` with conditional laws
`μ_u = P_{X|U=u}`; `α := D(P_{X|U}‖π|P_U) = Σ_u P(u) KL(μ_u‖π)`.  For `ρ ≥ 0` let

    V(P_{UX}; ρ) = min { I(X';U) : kernels P_{X'|XU} with E s(X',X) ≤ ρ }.

Then for all `ε₁ ≥ 0`, `δ ≥ 0`:
(i) `V(P_{UX}; (α+ε₁)/β) ≤ R^gen_β(ε₁)`;
(ii) `V(P_{UX}; max((α+ε₁)/β − δ, 0)) ≤ R^gen_β(ε₁) + 2βδ`;
(iii) `sup_{P_{UX}} V(P_{UX}; (α+ε₁)/β) = R^gen_β(ε₁)`, attained by `U = φ ∈ 𝒱` distributed
according to a maximiser `M` of `R(M;σ,ε₁/β)` and `μ_φ ∝ π e^{−βφ}` (a generalised dip).
*Proof.*  (i) Let `ρ = (α+ε₁)/β > 0` (if `ρ = 0` then `μ_u ≡ π` and `V = 0`).  With
`W_s(ν,μ) = min_{couplings} E s(X',X)` and `I(X';U) = min_Q Σ_u P(u) KL(ν_u‖Q)`,

    V = min_Q min { Σ_u P(u) KL(ν_u‖Q) : Σ_u P(u) W_s(ν_u, μ_u) ≤ ρ }
      = min_Q sup_{t≥0} Φ(Q,t),     Φ(Q,t) = Σ_u P(u) 𝒦(μ_u,Q,t) − tρ,
      𝒦(μ,Q,t) = min_ν [KL(ν‖Q) + t W_s(ν,μ)]

(Lagrangian duality for a convex programme; Slater's condition holds at `ν_u = μ_u` for `Q` of
full support, and the infimum over such `Q` equals the minimum over all `Q` by convexity).  `Φ`
is convex and lower semicontinuous in `Q` (partial minimisation of a jointly convex function) and
**concave in `t`** (a minimum of affine functions), and `Q` ranges over a compact convex set: by
Sion's theorem `V = sup_t min_Q Φ(Q,t)`.  By Kantorovich duality for a quasi-metric cost,
`W_s(ν,μ) = max_{φ∈Lip} [E_ν φ − E_μ φ]`; exchanging `min_ν` and `max_φ` (Sion) and using
`min_ν [KL(ν‖Q) + tE_ν φ] = −ln E_Q e^{−tφ}`,

    𝒦(μ,Q,t) = max_{φ∈Lip} [ −ln E_Q e^{−tφ} − t E_μ φ ].

Therefore, with `ρ = (Σ_u P(u) KL(μ_u‖π) + ε₁)/β`,

    Φ(Q,t) = Σ_u P(u) [ 𝒦(μ_u,Q,t) − (t/β) KL(μ_u‖π) ] − tε₁/β
           ≤ max_μ max_φ [ −ln E_Q e^{−tφ} − tE_μφ − (t/β) KL(μ‖π) ] − tε₁/β
           = max_φ [ −ln E_Q e^{−tφ} − (t/β)Λ(φ) ] − tε₁/β = G(Q,t) − tε₁/β

(Gibbs variational principle in `μ`; the maximiser is `μ ∝ π e^{−βφ}`).  Hence
`V ≤ sup_t [min_Q G(Q,t) − tε₁/β] = R^gen_β(ε₁)` by Lemma 3(d).
(ii) `ρ ↦ V(P_{UX};ρ)` is convex and nonincreasing with `V(·;0) ≤ I(X;U) ≤ α` (identity kernel;
`I(X;U) = min_Q Σ P(u) KL(μ_u‖Q) ≤ α`).  Let `ρ* = (α+ε₁)/β`.  If `ρ* ≥ 2δ`, convexity gives
`V(ρ*−δ) ≤ V(ρ*) + δ·V(0)/(ρ*−δ) ≤ R^gen + δ α/(ρ*−δ) ≤ R^gen + 2βδ` (as `α ≤ βρ*`).  If
`ρ* < 2δ` then `V(0) ≤ α ≤ βρ* < 2βδ`.
(iii) "`≤`" is (i).  For the stated `P_{UX}`: `α = Σ_φ M(φ)[Λ(φ) − βE_{μ_φ}φ]`, and every feasible
kernel has `Σ_φ M(φ)[E_{ν_φ}φ − E_{μ_φ}φ] ≤ Σ_φ M(φ) W_s(ν_φ,μ_φ) ≤ (α+ε₁)/β`, i.e.
`E σ_U(X') ≤ ε₁/β`; hence `V ≥ R(M;σ,ε₁/β) = R^gen_β(ε₁)` by Lemma 3(e). ∎

(`v1_single_letter_AZ.py` checks (i) and (iii) by a primal minimisation over kernels: `V` of the
tilted law equals `R^gen` to `10⁻¹²`, and no `P_{UX}` with a larger value was found.)

**Lemma 5 (inherently typical subsets, weighted form) [K: Ahlswede–Yang–Zhang 1997; this
version, with a rounding-up quantiser, has a short proof].**  Let `A ⊂ Sⁿ` be nonempty,
`m ≥ 1`, `α_B := −n⁻¹ ln πⁿ(B)`.  There are a finite set `𝒰_m ⊂ Δ(S)` with `|𝒰_m| ≤ (m+1)^k`
(depending only on `m, k`), maps `u_i : S^{i−1} → 𝒰_m`, a subset `Ã ⊂ A` and a law `P_{UX}` on
`𝒰_m × S` such that
(1) every `x ∈ Ã` has joint type `P_{UX}` with its label sequence `(u_i(x^{i−1}))_{i≤n}`;
(2) `πⁿ(Ã) ≥ πⁿ(A) (n+1)^{−k(m+1)^k}`;
(3) `α_A − k/m ≤ α := D(P_{X|U}‖π|P_U) ≤ α_Ã`.
*Proof.*  Let `P_A = πⁿ(·|A)` with conditional laws `p_i(·|x^{i−1})`, and
`u_i(x^{i−1})(a) = ⌈m p_i(a|x^{i−1})⌉ / Σ_b ⌈m p_i(b|x^{i−1})⌉`, so that `u_i ≥ p_i · m/(m+k)`
pointwise and `u_i` takes at most `(m+1)^k` values.  Let `Ã` be the most `P_A`-probable class of
the partition of `A` by the joint type of `((u_i(x^{i−1}), x_i))_i`: (1), (2).  For `x ∈ Ã`:
`πⁿ(x)/πⁿ(A) = ∏_i p_i(x_i|x^{i−1}) ≤ (1+k/m)ⁿ ∏_i u_i(x^{i−1})(x_i)`; taking logarithms and
using (1), `α_A ≤ k/m + Σ_{u,a} P_{UX}(u,a) ln(u(a)/π(a)) = k/m + α − D(P_{X|U}‖U|P_U) ≤ k/m + α`.
For the other inequality let `Xⁿ ∼ πⁿ(·|Ã)`, `U_i = u_i(X^{i−1})`, `I` uniform on `[n]` and
independent, `V = (I, X^{I−1})`.  By (1) the pair `(U_I, X_I)` has law `P_{UX}`, and by the chain
rule

    α_Ã = n⁻¹ D(P_{Xⁿ}‖πⁿ) = D(P_{X_I|V}‖π|P_V) = α + I(X_I; V | U_I) ≥ α.   ∎

(`v7_typical_subset.py` checks (2), (3) by brute force on 180 random and structured sets.)  The
proof also gives the identity used below:

    I(X_I; V | U_I) = α_Ã − α ≤ η_{m,n} := k/m + k(m+1)^k ln(n+1)/n.                      (★)

*Proof of Theorem A(ii).*  Fix `D ∈ 𝒟_n(ε_n)`, `D ≠ X_n`, `h = h_D ≤ n s_max`, `η = e^{ε_n} − 1`.
*Step 1.*  Lemma 0(b) gives `r = j/β` and `A = {h > r}` with `πⁿ(A) ≥ η e^{−βr−1}/J`,
`J ≤ ⌈βn s_max⌉`, `Γ_r(A) ⊂ D`.  If `j = 0` then `πⁿ(D) ≥ η/(eJ)` and the `π`-half of `q_n` hits
`D` with probability `e^{−o(n)}`.  Otherwise, with `ε_{1,n} := n⁻¹[ln η − 1 − ln J] → ε₁`,

    r/n ≥ (α_A + ε_{1,n})/β.

*Step 2.*  Apply Lemma 5 with `m = m_n → ∞` so slowly that `η_{m_n,n} → 0`: `Ã`, `P_{UX}`, `α`,
with `α ≤ α_Ã ≤ α_A + k(m+1)^k ln(n+1)/n`.
*Step 3.*  Let `δ = n^{−1/4}`, `κ_n = (|ε₁ − ε_{1,n}| + η_{m,n})/β`, `δ' = δ + κ_n`.  By
Proposition 4(ii) there is a kernel `W(x'|x,u)` with `E s(X',X) ≤ max((α+ε₁)/β − δ', 0) ≤
max(r/n − δ, 0)` and `I(X';U) ≤ R^gen_β(ε₁) + 2βδ'`.
*Step 4.*  Let `Xⁿ ∼ πⁿ(·|Ã)` and, given `Xⁿ = x`, draw the `X'_i ∼ W(·|x_i, u_i(x^{i−1}))`
independently.  For every `x ∈ Ã` the conditional mean of `s_n(X'ⁿ, x)` is `n E s(X',X)` — it
depends on `x` only through the joint type, which is constant on `Ã`; this is what the lemma is
for.  By Hoeffding's inequality (or trivially if the bound is `0`),
`P(X'ⁿ ∈ Γ_r(Ã)) ≥ 1 − e^{−2nδ²/s_max²} =: 1 − θ_n`.
*Step 5.*  Let `Q = P_{X'}` (the `X'`-marginal of `P_{UX} × W`), `V = (I, X^{I−1})`.  Since
`X'^{i−1} — X^{i−1} — X'_i` is a Markov chain,

    n⁻¹ D(P_{X'ⁿ}‖Qⁿ) = n⁻¹ Σ_i [ I(X'_i; X'^{i−1}) + D(P_{X'_i}‖Q) ]
                      ≤ n⁻¹ Σ_i D(P_{X'_i|X^{i−1}}‖Q|P_{X^{i−1}}) = I(X'_I; V)
                      = I(X'_I; U_I) + I(X'_I; V | U_I) ≤ I(X';U) + I(X_I; V | U_I)
                      ≤ R^gen_β(ε₁) + 2βδ' + η_{m,n}

(`(U_I,X_I,X'_I) ∼ P_{UX}×W`, so `Q = P_{X'_I}`; given `U_I`, `V — X_I — X'_I` is Markov; (★)).
*Step 6.*  By the data-processing inequality for the event `Γ = Γ_r(Ã)`,
`(1−θ_n) ln(1/Qⁿ(Γ)) − ln 2 ≤ D(P_{X'ⁿ}‖Qⁿ)`, so `Qⁿ(D) ≥ Qⁿ(Γ) ≥ exp(−n R^gen_β(ε₁) − o(n))`.
*Step 7.*  `Qⁿ` is a mixture over type classes of the uniform distributions on them, so
`max_T (density of D in T) ≥ Qⁿ(D)` and `q_n(D) ≥ ½ (n+1)^{−(k−1)} Qⁿ(D)`.  All `o(n)` terms are
uniform in `D`. ∎

*What the proof is.*  Steps 4–6 are the converse argument of Ahlswede–Zhang (1999) and of the
upper bound in Yu (2024, Theorem 5) for the isoperimetric exponent of two **fixed** product
measures.  Two things are different here and are what makes the answer explicit: the second
measure is chosen *after* the inherent type of the set is known (Step 5 with `Q = P_{X'}`; a fixed
product sampler is strictly worse, §2.6), which turns relative entropies into mutual
informations; and the budget is coupled to the measure of the set (`βρ = α + ε₁`), which makes
the Lagrange multipliers of the two constraints proportional and collapses the optimisation over
the auxiliary variable to a matrix game (Proposition 4).

### 2.4 Corollaries: the conjecture for binary sites, and its failure beyond

**Corollary A1 (binary sites: the main conjecture is true) [N; P].**  If `|S| = 2`, then for every
`π`, every quasi-metric slack (i.e. every additive residual and envelope constant) and every `β`:
`n⁻¹ ln FC_n → R^rand_β(ε₁)`.  Single dips are extremal at the exponential scale; the randomised
exponent of the report's running example (`e/c = ½`) is exactly `0.0275, 0.154, 0.1882` at
`β = 1, 4, 40` (deterministic, from the report: `0.666, 0.482, 0.216`; `U_β = 0.365, 0.630, 0.693`).
*Proof.*  `Lip/ℝ = {φ(0) − φ(1) ∈ [−s(1,0), s(0,1)]}` is a segment with endpoints `s(·,1)` and
`s(·,0)`. ∎

**Corollary A2 (three or more states: the main conjecture is false) [N].**  For `|S| ≥ 3` one can
have `R^gen_β > R^rand_β`; then, by Proposition 2 alone (valid for every `n`; no paper proof of an
upper bound is involved), *every* algorithm needs `exp(n R^gen − o(n)) ≫ exp(n R^rand)` evaluations.
* **Flat four-state site**, `u = βc = 1`, `ε = o(n)` (hand-checkable): dips,
  `ρ₁ = −ln(¼ + ¾e^{−1}) = 0.64263`, `D(ρ₁‖¾) = 0.02841`; boxes of pairs,
  `ρ₂ = −ln(½ + ½e^{−1}) = 0.37989`, `D(ρ₂‖½) = ln 2 − h(ρ₂) = 0.02914` (a product of pairs is
  the binary cube).  Flat 8-state site: `0.01936` (dips) against `0.03093` (boxes of triples) at
  `u = 1`; `0.0994` against `0.1199` (pairs) at `u = 2`.
* **Three states are enough, with the standard Hamming envelope and zero residual**: energies
  `(0,0,2)`, `β = c = 1`: `R^rand = 0.02467`, `R^gen = 0.02903`; energies `(0,2,2)`:
  `0.01640` against `0.02011`.  The optimal adversary mixes a dip coordinate (centre: one state)
  with a box coordinate (centre: the other two states) on about half of the sites each; already
  the period-2 arrangement has exponent `0.02893 > R^rand` (`v9_block_kary.py`).
* 135 of 300 random three-state sites (random `π`, random quasi-metric, `β ∈ [0.3,4]`) have
  `R^gen > R^rand` (largest gap: `0.0926` against `0.0733`).
* The flat three-state site is *not* a counterexample (dips optimal for all `u` scanned in
  `[0.02, 12]`); flat `k`-state sites are counterexamples exactly for `u` below a crossover
  `u_c(k)`: `1.10, 1.79, 2.30, 3.04, 4.65, 7.57` for `k = 4, 5, 6, 8, 16, 64`
  (`kary_crossover.py`).  As `β → ∞` the gap closes on every site tested (`zero_temp.py`), in
  accordance with the zero-temperature theory, where a sensitive perturbation contains a
  sensitive single dip.
* The dip bound can be arbitrarily bad in the exponent: `R^gen/R^rand → k²/(4(k−1))` for the flat
  `k`-state site as `u → 0`.
* At finite `n`, exactly (`kary_finite_n.py`; the instance is vertex-transitive, so the uniform
  sampler is optimal and the hitting numbers are binomial tails): flat 8-state site, `u = 1`,
  `ε = 1`: `ln(N_boxes/N_dips) = 1.7, 11.3, 115, 232` at `n = 100, 10³, 10⁴, 2·10⁴`.

### 2.5 Theorem B: the accuracy threshold, sharp for every alphabet and every `n`

**Theorem B [N; elementary proof; (a) and (c) V*].**  For `Q ∈ Δ(S)` let
`βγ(Q) := max_{φ∈𝒱} [β E_Q φ − Λ(φ)]` (`= max` over all of `Lip`, the functional being convex).
(a) *Two-measure tensorisation.*  For every `n` and every admissible profile `h` on `Sⁿ` (any sign)

    ln E_{πⁿ} e^{βh} ≤ β E_{Qⁿ} h + n βγ(Q).

(b) *Two-reference sandwich.*  For every admissible `g'` and every additive reference `g` with
site data `(π, s)`:  `β E_{πⁿ}[g − g'] ≤ ln Z(f+g') − ln Z(f+g) ≤ β E_{Qⁿ}[g − g'] + n βγ(Q)`.
(c) For every `D ≠ Sⁿ`: `Qⁿ(D) ≥ [ln E e^{βh_D} − n βγ(Q)] / (n β s_max)`.  Hence with
`ε₁^thr = min_Q βγ(Q)` attained at `Q*`:

    FC_n(nε₁) ≤ β s_max / (ε₁ − ε₁^thr)      for all n, whenever ε₁ > ε₁^thr,

and `q = ½πⁿ + ½Q*ⁿ` with `O(ln(1/δ))` samples is a correct spot-check: **the number of
evaluations is bounded independently of `n`**.  With Lemma 3(d): *the cost is bounded for
`ε₁ > ε₁^thr` and exponential, with exponent `R^gen_β(ε₁) > 0`, for `ε₁ < ε₁^thr`.*
(d) `ε₁^thr ≥ ε₁^crit := max_P min_a E_P[βs(a,·) − Λ₁]` (the report's conjectured threshold), with
equality for `|S| = 2` and strict inequality e.g. for the three-state site `(0,0,2)`, `β = c = 1`:
`0.1197` against `0.0947` (at `ε₁ = 0.10`: `R^rand = 0`, `R^gen = 7.8·10⁻⁴`); flat four-state site,
`u = 1`: `0.1201 = ln cosh ½` against `0.1074`.  For accuracies between the two values the
report's conjecture predicts polynomial cost; the cost is exponential.
*Proof.*  (a) For `n = 1` this is the definition of `γ(Q)` (`φ = −h`).  Induction: for
`h(x_1,…,x_n)` let `h̄(x_1..x_{n−1}) = E_{X_n∼Q} h`; it is admissible on `S^{n−1}`, and for fixed
`x^{n−1}` the function `x_n ↦ h` is admissible on `S`, so
`E_{πⁿ} e^{βh} ≤ e^{βγ(Q)} E_{π^{n−1}} e^{βh̄}`.  (b) The lower bound is Jensen.  (c) `0 ≤ h_D ≤
n s_max 1_D`.  (d) `𝒱₀ ⊂ 𝒱`; LP duality. ∎

*Machine check.*  `lean/WorkstreamA.lean` proves, for arbitrary finite sites and real weights
(`π ≥ 0`, `Q ≥ 0`, `ΣQ = 1`, `s(a,a) = 0`): the two-site step (`twoMeasureBound_prod`: if two sites
satisfy `Σ π e^{βh} ≤ exp(β Σ Q h + γ)` for all admissible `h`, their product with the additive
slack satisfies it with `γ + γ'`), the `n`-site statement (`twoMeasureBound_pow`, constant `nγ`;
the product `Sⁿ` is encoded as nested pairs), the hitting bound (c) (`mass_ge_of_twoMeasureBound`)
and their combination (`product_mass_ge`: `Qⁿ(D) ≥ (ε − nγ)/(βH)` for every set `D` supporting an
admissible profile `0 ≤ h ≤ H` with `Σ πⁿ e^{βh} ≥ e^ε`).  Here `γ` is *any* valid single-site
constant; that the best one is the maximum over the Lipschitz vertices (convexity) and the LP
duality in (d) are not formalised.

Part (b) generalises the sandwich of Theorems 11.21/11.25(b) (which is the case `Q = π`, constant
`βγ(π)` = the Jensen gap, `0.1225` in the running example) and answers §12 item 2(c): accuracies
between the game value and the passive width *are* reachable with `O(1)` evaluations at additive
instances, by sampling the second reference `Q*ⁿ` (`ε₁^thr = 0.1137 < 0.1225`, `Q* = (0.6137,
0.3863)` against `π = (0.6225, 0.3775)`).

### 2.6 Product samplers are not optimal (negative)

**Proposition 6 [N].**  For a product sampler `Qⁿ`,
`liminf −n⁻¹ ln min_{D ∈ 𝒟_n(ε_n)} Qⁿ(D) ≥ E(Q) := sup_{t≥0} [G(Q,t) − tε₁/β]` (Chernoff bound for
the generalised dip with the same `φ` on all sites; for dips the centres are constant sequences).
`E_iid := min_Q E(Q) ≥ R^gen`, with strict inequality on biased sites: `e/c = ½`, `β = 4`:
`E_iid = 0.1655` against `R^rand = 0.1541` (by hand: the balanced `Q` solves
`D(ρ₀‖Q₁) = D(ρ₁‖Q₀)`, `ρ_b = Λ₁(b)/u`); `e = 1.5, c = 3, β = 1`: `0.1310` against `0.1258`; equality
on the uniform cube.  So *a mixture over compositions is necessary*: against a product sampler the
adversary centres its dips at `0ⁿ` or `1ⁿ`, whichever is worse, while against the type mixture it
must use centres of an intermediate composition `M*` (`(0.665, 0.335)` in the first example).

### 2.7 Dead ends and negative results (summary)

1. "Single dips are extremal at the exponential scale on product spaces" — **false** for
   `|S| ≥ 3` (Corollary A2); true for `|S| = 2`.
2. "`ε₁^crit` is the polynomial/exponential boundary" — **false** for `|S| ≥ 3` (Theorem B(d)).
3. "A product sampler suffices" — **false** on biased sites (Proposition 6).
4. *Tensorisation alone.*  The two-measure inequality that tensorises exactly,
   `ln E_{Qⁿ} e^{−t T'f} ≥ (t/β) ln E_{πⁿ} e^{−βf} − n G(Q,t)` for all `f` on `Sⁿ`
   (`T'f(x) = min_y [f(y) + s_n(x,y)]`; verified exhaustively in `v4_tensor_ineq.py`), says that
   additive Lipschitz functions maximise `g_n(·; Qⁿ, t)`, but it only yields `E_iid`: it controls
   the Legendre transform of the law of `s_n(·,A)` under one `Qⁿ`, not the minimum over `Q`.
5. *A "weak converse" without typical subsets* (chain rule with `U_i = X^{i−1}` directly) gives
   `D(P_{X'ⁿ}‖Qⁿ) ≤ nR^gen` but `P(X'ⁿ ∈ Γ)` only bounded below by a constant, which loses a
   constant *factor* in the exponent; the typical-subset lemma is what makes the cost constant.
6. *Yu's theorem as a black box* (a net of product samplers, each handled by the fixed-measure
   theorem) gives the bound `sup_α min_Q ψ_Q(α, (α+ε₁)/β)`, which lies between `R^gen` and `E_iid`
   (the sampler may adapt `Q` to `α` but not to the set); I did not evaluate it, and it is not
   needed.
7. *Finite `n`.*  Exact `FC` exceeds `FC_dip` by factors up to `2.1` for `n ≤ 6` even on the
   uniform cube (Harper's extremal sets are not only exact balls): extremality of dips is an
   exponential-scale statement only.
8. Constant-centre dips, and any set containing a constant sequence, are useless against the
   type mixture (exponent `0`); the adversary must use centres of a mixed composition.

### 2.8 Further remarks

* *Zero temperature.*  As `β → ∞` (with `ε/β` fixed) `Λ(φ)/β → min_a [gap(a) + φ(a)]` and a
  generalised dip is sensitive iff one of its constituent dips is; `R^gen − R^rand → 0`
  numerically.  The new vertices are a finite-temperature effect, strongest for `βc ≲ ln k`.
* *Why the deterministic exponent is different.*  `FC` is a *fractional* hitting number of a
  doubly exponential family; the deterministic problem is its integral version (`A` hits every
  sensitive set iff `E_π e^{βs(A,Y)} ≤ e^ε`), and the integrality gap is exponential.
* *Sites of several types* (fractions `λ_j`): the same proof with the site type adjoined to the
  label `U` should give `max_t Σ_j λ_j[−ln val(K_t^{(j)})] − tε₁/β` (common `t`, as in D31).  Not
  written out.
* *Question 2(d) of §12* (no hint, cube class, exponent between `u²/32` and `u²/8`): at the zero
  residual, and at every additive instance, the lower value is attained by an algorithm that is
  correct on the whole class (star + spot-check); the open part is the worst case over
  non-additive instances, which is a different problem.

---

## 3. Numerics

All scripts are plain Python (numpy/scipy; HiGHS for LP/MILP); run as `python3 <script>`.  Outputs
are the `*_out.txt` files.

| script | what | sizes | result |
|---|---|---|---|
| `sl.py` | single-letter formulas: Lipschitz-polytope vertices (brute force), matrix games, `R^rand`, `R^gen`, thresholds, `U_β`, Blahut–Arimoto | `k ≤ 8` | reproduces the report: `R^rand = 0.0275, 0.1541, 0.1882`; `U_β = 0.3647, 0.6304`; `ε₁^crit = 0.1137`; cube `ln 2 − h(ρ₀)` to 5 digits |
| `kary_uniform.py`, `kary_crossover.py` | flat `k`-state sites: dips vs. all vertices | `k ≤ 64`, 4000 values of `u` | `R^gen > R^rand` iff `k ≥ 4` and `u < u_c(k)`; `R^gen` from the game with all `2^k−2` vertices = best box (closed form) |
| `kary_finite_n.py` | the counterexample at finite `n`, exactly (binomial tails in log-space; vertex-transitive, uniform sampler optimal) | `n ≤ 20000`, `k = 4, 8, 16` | `k = 8`, `u = 1`, `n = 2·10⁴`: `n⁻¹ ln N = 0.0196` (dips) vs `0.0311` (boxes), limits `0.0194`, `0.0309`; `N_box/N_dip = e^{232}`; `k = 4`: `e^{14.8}` |
| `fc_exact.py` | **exact `FC`** over *all* sensitive sets: orbit LP + exact MILP best response (constraint generation, certified optimal) | binary `n ≤ 6` (4 parameter sets); flat `k = 3,4` (`n ≤ 3`), `k = 8` (`n ≤ 2`) | binary: `FC/FC_dip ∈ [1, 2.08]`, no trend (e.g. `1, 2, 1.50, 1.12, 1.94` for `n = 2..6`); uniform cube: ratio `2` at `n = 3, 6`; flat 4-state, `u = 1`, `ε = 0.3`: `FC/FC_dip = 1, 1.75, 3.36` for `n = 1, 2, 3`, and box balls are exactly optimal at `n = 2` |
| `fc_ternary.py` | exact `FC` on the three-state counterexample site `(0,0,2)`, `u = 1` | `n ≤ 3` | `ε = 0.3`, `n = 3`: `FC = FC_boxes = 5 > FC_dip = 3.5` (box balls exactly optimal); `ε = 0.1`: `FC/FC_dip = 1, 1.13, 1.21` |
| `fc_orbit_binary.py small` | exact `FC` of the family of all *two-block* sets (conditional type classes with binary `U`, blown up; contains all balls, shells, type neighbourhoods), sensitivity decided exactly | binary `n ≤ 28`, up to 2364 distinct profiles | `FC_2blk/FC_dip`: `1.20, 1.51, 1.05, 1.21, 1.14, 1.06, 1.06, 1.04` for `n = 4..28` (`e=.5, c=1`); similar for 3 other parameter sets — the richer family does not help, as Proposition 4 predicts |
| `fc_orbit_binary.py large` | integer sandwich `L(n) ≤ FC_dip ≤ (n+1)L(n)` in log-space | `n ≤ 800`, 4 parameter sets | `ln L(n) − nR^rand = 2.45, 2.68, 3.03, 3.27` at `n = 100, 200, 400, 800` (`e=.5,c=1`): `≈ ½ ln n + O(1)`, i.e. exponent `R^rand` with a `√n` prefactor; same pattern for the other sets |
| `v1_single_letter_AZ.py` | Proposition 4 by a *primal* convex minimisation over kernels (SLSQP), independent of the dual: `V` for the tilted law, 15 random laws, local ascent in the law | 8 random sites (4 binary, 4 ternary; symmetric and asymmetric `s`; `ε₁ = 0` and `> 0`), `|U| ≤ 4` (`v1_out.txt`, `v1_out_seed1.txt`) | `V(tilted) = R^gen` to `10⁻¹²` in all 8 (one ternary site has `R^gen = 0.0190 = 2.05·R^rand`); no law found with `V > R^gen` (largest excess `5·10⁻¹⁴`) |
| `v4_tensor_ineq.py` | the dimension-free inequalities of §2.7(4) and Theorem B(a),(c): all subsets `A` for `|X| ≤ 16`, 20000 random + all balls otherwise, 3000 random functions each | binary `n ≤ 4`, ternary `n ≤ 3`, 12 random sites, `t/β ∈ [0.05, 1.6]` | no violation; Theorem B(a) tight to `10⁻¹⁵` |
| `v7_typical_subset.py` | Lemma 5 (2), (3) by brute force | 180 (set, `m`) pairs, `n ≤ 12` | no violation |
| `v14_step5_chain.py` | **exact finite-`n` check of Step 5** (the information-theoretic core of the upper bound): for a set `A`, its typical subset `Ã`, labels and joint type from Lemma 5, and an *arbitrary* kernel `W`, the law of `X'ⁿ` is computed by enumeration and `n⁻¹D(P_{X'ⁿ}‖Qⁿ) ≤ I(X';U) + α_Ã − α` is tested, together with the constancy of the conditional mean cost on `Ã` | 40 instances (random sets, balls, threshold sets, a golden-mean set; binary `n ≤ 10`, ternary `n ≤ 6`; `m ≤ 4`) | no violation (smallest slack `−2·10⁻¹⁶`); in several instances `n⁻¹D > I(X';U)`, so the correction `α_Ã − α` is needed; mean-cost deviation `< 10⁻¹⁵` |
| `v8_block_sets.py` | **asymptotic falsification test of Theorem A (binary).**  For a Lipschitz `Φ` on a block `S^b`, the periodic generalised dip has the exact exponent `min_Q b⁻¹ sup_t[(t/β) ln E_{π^b}e^{−βΦ} − ln E_{Q^b}e^{−tΦ}]` against the universal sampler (Cramér).  Tensorisation only bounds it by `E_iid > R^rand`; the theorem demands `≤ R^rand` | all `2^{2^b} − 2` subsets `C` (`Φ = s_b(·,C)`) for `b ≤ 4` (65534 sets) + 6000 random Lipschitz `Φ` per `b`, 4 biased sites | max over all sets and `b ≤ 4`: `0.154070 ≤ 0.154075` (`e=.5,c=1,β=4`; attained by the centre `010`, composition `≈ M*`), `0.1239 ≤ 0.1258`, `0.0692 ≤ 0.0811`, `0.0261 ≤ 0.0275`: **no violation**, and never near `E_iid` |
| `v8b_block_sets_eps.py` | the same at extensive accuracy `ε₁ > 0` | all subsets, `b ≤ 3`, 4 (site, `ε₁`) pairs | e.g. `0.0884 ≤ R^rand(0.2) = 0.0918` (`e=.5,c=1,β=4`): no violation |
| `v9_block_kary.py` | the same for `k = 3, 4`; exhibits explicit counterexamples to the dip conjecture | all 510 subsets of `S²`, all additive vertex functions, 3000 random Lipschitz, `b ≤ 3` | `(0,0,2)`: `b = 2` gives `0.028929 ∈ (R^rand, R^gen] = (0.024665, 0.029032]`; flat 4-state: `0.029139 = R^gen > 0.028405`; no violation of `R^gen` |
| `v10_sft_sets.py` | Markov-structured sets `A` (subshifts of finite type, memory ≤ 2; `d_H(x,A)` via a min-plus transducer, exponent `min_Q sup_t[(t/β) ln λ(π,βc) − ln λ(Q,tc)]` via spectral radii) | the 7 memory-2 subshifts without constant sequences that have a bounded transducer, 2 biased sites | max `0.0411 ≤ R^rand = 0.1541` and `0.0388 ≤ 0.1258`: no violation (these sets are far from extremal); subshifts containing a constant sequence have exponent `0` (the type mixture finds them) |
| `lean/WorkstreamA.lean` (`lean/lean_out.txt`) | Lean 4 check of Lemma 1, of the two ingredients of Proposition 2 and of Theorem B(a), (c), for `n` identical sites (nested-pair products) | 15 theorems, 370 lines, compiles in 15 s | no errors, no `sorry`; `#print axioms`: `propext`, `Classical.choice`, `Quot.sound` only |
| `v12_vertex_reduction.py` | Lemma 3(c) | 3000 random sites, `k ≤ 4`, 400 polytope points each | `t ≤ β`: no interior point beats the vertices (`−5·10⁻¹¹`); `t > β`: it happens in 1115/3000 cases |
| `explore_sl.py` | product sampler vs. universal sampler (binary); scan of random ternary sites; ternary Hamming sites | 6 binary sites, 300 random ternary sites, 10 ternary Hamming sites | §2.4, §2.6 |
| `v13_consistency.py` | consistency with the upper bounds proved in the theory report: `R^rand ≤ R^gen ≤ min(U_β, R_β)` (`R_β` bounded from below by Blahut–Arimoto at 8 sources) | 24 random sites, `k ≤ 4` | no inconsistency in 24/24 (tolerance `10⁻⁶`; with tolerance `10⁻⁹` one case is flagged, `R^rand − R^gen = 7·10⁻⁹`, which is the accuracy of the LP solver — kept as `v13_out_tol1e-9.txt`) |
| `zero_temp.py`, `v11_ba_check.py` | `β → ∞`; game formula vs. Blahut–Arimoto brute force over the source | — | gap closes for `β ≳ 8`; BA agrees to grid accuracy on the 3 binary cases completed (`0.027521` vs `0.027531`; `0.154038` vs `0.154075`; `0.113744` vs `0.113780`); ternary cases not completed |

Caveats on the runs.  The machine was shared (load average 12–18 on 4 cores), so several runs
were cut by time limits: `v1` completed 8 of 14 planned sites, the first version of `v10` was
replaced by a leaner one, the exact MILP was not pushed beyond `n = 6` (binary; `n = 7` did not
finish in 15 minutes), and `v11_ba_check.py` was stopped at its time limit after the three
binary cases (its two ternary cases, which would compare `R^gen` with Blahut–Arimoto on the
active vertices, did not run to completion — for ternary sites the game formula is checked
only through `v1` and `v9`).  Single-letter values are grid + golden-section maximisations over `t`
(the game value at fixed `t` is a linear programme, solved by HiGHS to about `10⁻⁷`); quoted digits
are stable under refinement.

Honest reading of the evidence for the *upper* bound of Theorem A (the only non-elementary step):
exact `FC` is available only for `n ≤ 6`, where exponents cannot be read off; the convincing tests
are `v8`/`v9` (exact asymptotic exponents of 65534 + 510 + thousands of structured adversaries — a
test that a wrong formula, e.g. an `E_iid`-type bound or an error in the minimax step, would
fail), `v1` (the single-letter optimisation) and `v14`/`v7` (the two exact inequalities on which
Steps 2–5 rest, at finite `n`).  They support the statement; they do not replace an independent
check of the proof.

---

## 4. Prior art and search log

What I actually read: the three-page summary of Ahlswede–Zhang (full text, PDF from the Bielefeld
server); for Yu's papers only machine summaries of the arXiv HTML (three passes over
arXiv:2205.07596v3, abstract page of arXiv:2510.04030); search-engine summaries otherwise.

| item | status | source |
|---|---|---|
| Asymptotic vertex isoperimetry in `Xⁿ` for a general distortion: `n⁻¹ log min{|Γ^{dn}A| : |A| ≥ 2^{nR}} → inf_{H(X|U)≥R} sup_{Eρ(X,Y)≤δ} H(Y|U)`; tool: inherently typical subset lemma | **K** | R. Ahlswede, Z. Zhang, "Asymptotical isoperimetric problem", Proc. IEEE ITW 1999 (summary read in full); lemma from R. Ahlswede, E.-H. Yang, Z. Zhang, "Identification via compressed data", IEEE Trans. IT 43 (1997) 48–70 (statement read in the summary: `m ≥ 2^{16|X|²}`, loss `|X|(m+1)^{|X|} log(n+1)/n`, entropy gap `log² m/m`) |
| Isoperimetric exponent for **two fixed product measures**, `−n⁻¹ ln inf{P_Yⁿ(A^{nτ}) : P_Xⁿ(A) ≥ e^{−nα}} → ψ(α,τ) = sup_{Q_{XW}: D(Q_{X|W}‖P_X|Q_W) ≤ α} inf_{Q_{Y|XW}: E c ≤ τ} D(Q_{Y|W}‖P_Y|Q_W)`, `|W| ≤ 2`, with a dual formula by Kantorovich duality | **K** | Lei Yu, "Exact exponents for concentration and isoperimetry in product Polish spaces", arXiv:2205.07596 (v3 2024; listed as IEEE Trans. IT) — Theorems 4, 5, 8 as reported by the summariser; exact hypotheses **not verified by me in the source** |
| Conditional typical sets asymptotically optimal for isoperimetry | **K** | Lei Yu, arXiv:2510.04030 (abstract only) |
| Vertices/faces of the Lipschitz polytope of a finite metric space; generic vertex count `C(2k−2, k−1)` | **K** | J. Gordon, F. Petrov, "Combinatorics of the Lipschitz polytope", Arnold Math. J. 3 (2017), arXiv:1608.06848 (summary) |
| Harper's theorem; stability and approximate versions on the cube | **K** | Harper 1966; Przykucki–Roberts, Jiang–Yehudayoff (summaries) |
| Vertex isoperimetry for the biased cube (Bollobás–Leader) | not retrieved | one search, no relevant hit; nothing is claimed about it |
| The minimax version (second measure chosen by a sampler, non-product), its collapse to a matrix game over Lipschitz vertices, the binary corollary, the threshold of Theorem B, the application to query complexity | **no match found** | the queries below; the application is specific to this project |

Search log (2026-11-24).
1. `Ahlswede Zhang "Asymptotical isoperimetric problem" inherently typical subset lemma Hamming
   space blow-up exponent single-letter` → Bielefeld PDF 149 (read), pointer to Yu.
2. `Lei Yu "Exact exponents for concentration and isoperimetry in product Polish spaces" nonlinear
   transport-entropy inequalities` → arXiv:2205.07596, arXiv:2510.04030.
3. WebFetch of arXiv:2205.07596 (abstract; HTML v3 in three passes: definitions of `E₀`, `ψ`,
   Theorems 4/5/8, Lemma 4) and of arXiv:2510.04030 (abstract).
4. `vertex isoperimetric inequality biased cube p-biased measure Hamming balls optimal down-sets
   Bollobás Leader "fractional set systems" …` → only unbiased-cube results.
5. `"inherently typical subset lemma" universal OR mixture OR "type class" isoperimetric exponent
   minimax …` → no minimax/universal version found.
6. `Lipschitz polytope vertices finite metric space Gordon Petrov …` → Gordon–Petrov.

Classification of my own statements.  Lemma 0, Lemma 1: routine.  Proposition 2: routine proof,
new use (which centres).  Lemma 3(c) (vertex reduction for `t ≤ β`), Proposition 4 (collapse),
Theorem A, Corollaries A1/A2, Theorem B(c,d), Proposition 6: apparently new.  Lemma 5: known
(AYZ), reproved in a convenient form.  Theorem B(a): a standard tensorisation with two measures
(the technique of McDiarmid/Bobkov–Götze-type bounds); its use for a sharp threshold was not
found.  The proof technique of Theorem A(ii) is Ahlswede–Zhang's/Yu's; the dualisation in
Proposition 4 is the technique of Yu's Theorem 8.

---

## 5. What is not settled

1. **Theorem A(ii) is a paper proof.**  It has not been machine-checked or refereed.  The parts
   that are valid for every `n` — Lemma 1, the two ingredients of Proposition 2, Theorem B(a),(c)
   — are machine-checked in a scratch file (not yet connected to the repository's
   `QueryAlgorithm` framework, and with products encoded as nested pairs).  The asymptotic upper
   bound rests on Lemma 5, Sion's theorem and Kantorovich duality.  All claims that the
   conjecture *fails* use only Proposition 2 and the numerical evaluation of single-letter game
   values (for the flat sites: closed forms that can be checked by hand).
2. **Polynomial prefactors.**  The upper bound has an error `exp(o(n))` of the poor kind supplied
   by the typical-subset lemma (`exp(O(n^{1−c_k}))`).  Numerically `FC_dip ≈ √n·e^{nR}` and
   `FC/FC_dip ≤ 2.1` for `n ≤ 6`; whether `FC_n ≤ poly(n) e^{nR^rand}` on binary sites (a weighted
   Harper theorem) is open.
3. Sites of several types, and non-additive/interacting instances (Markov known parts): not
   treated.  For interacting `π` the extremal sets should be conditional *Markov* type classes;
   the relevant tool is the type-graph machinery of Yu–Anantharam–Chen, not read.
4. A structural characterisation of the sites with `R^gen = R^rand` (all binary sites; the flat
   ternary site; flat `k`-state sites for `u ≥ u_c(k)`) is missing.
5. Exponentially small accuracies (`ε_n = e^{−λn}`), as for the deterministic exponent (§12 1(c')).
6. `v10` (Markov-structured sets) covers only mixing subshifts of memory ≤ 2 with bounded
   transducers; periodic ones are covered by `v8`.  Sets with long-range (non-finite-state)
   structure were not tested.
7. Exact hypotheses of Yu's Theorems 5/8 were read only through an automatic summary.

---

## 6. The three most promising next steps

1. **Move the every-`n` statements into the repository and replace the conjecture in the report.**
   (a) Proposition 2 in the game form — a direct generalisation of `thermal_product_randomized`
   from distance functions to arbitrary site-Lipschitz functions; (b) Theorem B(a),(c).  Both
   are checked in `lean/WorkstreamA.lean` for nested-pair products; what remains is to port
   them to the repository's `∀ i, σ i` products, to compose (a) with
   `expected_queries_ge_packing` and (b) with the hedged spot-check.  Together they give a
   machine-checked *sharp threshold for every product landscape* and the corrected lower bound;
   the third row of the table of §11.10 should read "budget `(E_M[Λ(φ)] + ε₁)/β`, centres =
   Lipschitz vertices of the site", and D34 should record that the union-of-dips phenomenon
   persists on product spaces for `|S| ≥ 3`.
2. **Write Theorem A as the theorem of the cluster** — "the randomised query exponent of a free
   energy under a first-order envelope is a matrix game on the Lipschitz polytope of a site, and
   is attained by a temperature-independent universal sampler" — with an independent check of the
   upper-bound proof (it is about 1½ pages), the heterogeneous-site extension, and the polynomial
   prefactor on binary sites.
3. **Interacting known parts.**  Replace types by Markov types: lower bound by generalised dips
   whose site functions follow a stationary process (transfer-matrix pressure instead of
   `ln val`), upper bound by the Markov version of the typical-subset argument.  The first step
   is the Markov analogue of Proposition 4 (is the collapse to a game still valid when `π` is a
   chain?), which can be explored numerically with the transducer code of `v10_sft_sets.py`.
