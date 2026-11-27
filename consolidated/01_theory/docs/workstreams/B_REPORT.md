# Workstream B — beyond product landscapes: chain-structured known parts

Directory: `<session scratch>/ws/B/`
(all scripts `*.py`, all outputs `out_*.txt`; nothing in the repository was touched; no Lean was run).

Status tags: **[T]** theorem with a complete proof given here (standard lemmas cited); **[T*]** proof given, one
step relies on a lemma that is stated with a proof sketch only; **[N]** numerical fact (exact enumeration or LP at
the stated sizes); **[C]** conjecture; **[H]** heuristic; **[K]** known (cited).

---

## 1. Verdicts

*Zero temperature.*  The conjecture of the theory report §12.1(c) is true and its proof needs no "type covering
for Markov types": for a homogeneous finite-range chain with site-additive slack,
`lim n⁻¹ ln N_cov = R* = sup_ν R_ν(e(ν))` over stationary processes (Theorem B.2) — by blocking, the ordinary type
covering lemma on a block alphabet, a convexity estimate that absorbs the `O(1/L)` boundary energies, and a separate
treatment of the low-energy shell.  The one-evaluation criterion becomes a *droplet criterion*: one evaluation
suffices iff every contiguous excitation costs at least `c` per changed site, i.e. iff `c ≤ τ`, the minimum
cost-to-length ratio (a minimum-ratio cycle, a "string tension"); otherwise the cost is exponential (Theorem B.1).
Consequently a chain whose infinite-volume ground state is degenerate (zero-field ferro- or antiferromagnet, any
ground state of period `p ≥ 2`) is **never** sharp: the exponent is positive for every `c > 0` and is `Θ(c/J)`.
The transfer-matrix ("Boltzmann weights") bound of the blueprint is **vacuous exactly on the window
`2h < c ≤ 2(J+h)`** of the Ising chain although certification is exponential there, and it is exact only when the
Gibbs measure of the gap landscape can be de-convolved by a binary symmetric channel — for the Ising chain iff
`cosh(ct/2) ≥ e^{2Jt} cosh(ht)` at the optimal slope (for `h = 0`: `c ≥ 8.23 J`; proved exact for `c ≥ 9.08 J`).
This is the Hajek–Berger/Newman decomposition and, at `h = 0`, Gray's critical distortion; below it the exact
exponent is of the same nature as the rate–distortion function of a binary Markov source beyond its critical
distortion (open since 1970), and the optimal dual weights are *not* finitely correlated.  The right dual is
"pressure minus log joint spectral radius" for matrix-product weights (Proposition B.3); explicit weights of bond
dimension `4–8` certify positive exponents where the Boltzmann bound gives zero.

*Finite temperature.*  The soft gap of a chain is the log-likelihood of a hidden Markov measure (the Gibbs chain
seen through a binary symmetric channel), equivalently the free energy of the chain in a pinning field `±c/2` — a
random-field Ising chain; the three budgets of the report extend to chains by the same blocking argument.
`E_π e^Λ` has no transfer-matrix closed form (it is a negative moment of a product of random matrices) but is
computed to 9 digits by a transfer operator on the projective line; its zero-temperature limit is the entropy of
run-length-limited sequences.  There **is** a threshold phenomenon: the dip bound at the additive instance
`g₀ = θ·M` vanishes exactly at the *chord gap* of the pressure at `θ`, and the sandwich with the reference tilted
to `θ` — a fixed reference, no hint — has width equal to the larger of two Bregman divergences; both are optimised
at the same `θ*`, so **the worst-case accuracy threshold of the class, for algorithms without a hint, is the
largest chord gap of the pressure over the slope interval `[−c, c]`** — a theorem for identical two-state
independent sites (it extends the worst-case statement of Theorem 11.25 from the uniform cube; for the report's
example `e/c = ½`, `β = 1` the value is `0.11383`), and for chains a rigorous lower threshold that is also the
upper one if additive residuals are extremal for the Jensen gap.  (The theory report was updated while this
workstream ran: it now records, from workstream A, that the zero residual is not the worst additive instance —
with the same number `0.11383` — and an instance-wise threshold with an instance-dependent second reference; the
worst-case threshold without a hint is listed there as open, §12.2(c).  See §4.)  That extremality held in every one of about 6 100 exactly enumerated binary
*pairwise* models (chains, trees, cycles, frustrated complete graphs, `n ≤ 5`) and under adversarial search, and
fails with three-body terms; it is stated as a conjecture.

---

## 2. Statements, proofs, counterexamples

### 2.0 Setting

`σ` a finite alphabet, `k = |σ|`; `X_n = σⁿ`; known part
`f_n(y) = Σ_{i≤n} φ(y_i) + Σ_{i<n} ψ(y_i, y_{i+1})` (free boundary; periodic chains are used in some numerics);
envelope `d = c·d_H`; residual `g` additive, `g(y) = Σ γ(y_i)`, `|γ(a) − γ(b)| ≤ κc`, `κ < 1` (the reader may take
`g = 0`).  Then `E = f + g` is again a chain and the slack is site-additive,
`s(a,y) = Σ_i s₁(a_i, y_i)`, `s₁(a,b) = c[a≠b] − γ(a) + γ(b)`, `s₁(a,a) = 0 < s₁(a,b)`.
`gap_n(y) = E_n(y) − min E_n`.  `N_cov(n, ε)` = least `|A|` with: every `y` has `a ∈ A`, `s(a,y) ≤ gap_n(y) + ε`.

Thermodynamic quantities: `e₀ = lim min E_n / n` (minimum mean cycle of the transfer graph;
`|min E_n − n e₀| ≤ C`); for a stationary process `ν` on `σ^ℤ`: `e(ν) = E_ν[φ(Y₀) + γ(Y₀) + ψ(Y₀,Y₁)] − e₀ ≥ 0`
(excitation energy per site), `h(ν)` its entropy rate, `R_ν(D)` its rate–distortion function for the single-letter
distortion `s₁` (nats per site).  `p(t) = lim n⁻¹ ln Σ_y e^{−t·gap_n(y)}` is the pressure of the gap landscape
(log of the top eigenvalue of the transfer matrix `e^{−t(φ+γ+ψ−e₀)}`).

*Ising parametrisation used in all examples:* `σ = {0,1}`, spin `s = 1 − 2y`,
`f = −J Σ s_i s_{i+1} − h Σ s_i`, `g = 0`.  For `J ≥ 0, h ≥ 0`: `gap(y) = 2J·#walls(y) + 2h·#ones(y)`.
`x = e^{−2Jt}`, `z = e^{−2ht}`, `q = e^{−ct}`; `T = [[1, x√z],[x√z, z]]`.

### 2.1 One evaluation: the droplet criterion, and the dichotomy

**Theorem B.1 (droplets; string tension) [T].**  Let `x̂` be a minimiser of `f_n` (chain, any `φ_i, ψ_i`, possibly
inhomogeneous) and `d = c·d_H`.

(a) The single evaluation at `x̂` certifies the minimum exactly (for every residual) iff every *contiguous droplet* is
sharp: for every interval `I` and every `y` with `y_i ≠ x̂_i` on `I`, `y = x̂` off `I`:  `f(y) − f(x̂) ≥ c|I|`.
Equivalently `c ≤ τ_n := min_y gap(y)/d_H(x̂,y)`, and `τ_n` is attained on a contiguous droplet.  The test
`min_y [f(y) − c·d_H(x̂,y)] = f(x̂)` is one min-plus transfer-matrix product, `O(n k²)`.

(b) For a homogeneous chain let `τ = inf` over finite droplets in the infinite ground state of (excess energy)/(length);
`τ` is a minimum cost-to-time ratio cycle in the graph of (phase, state) with reduced edge costs.  If the periodic
ground state is not unique (e.g. period `p ≥ 2`, or two ground cycles), `τ = 0`.

(c) *Dichotomy.*  If `c > τ` there is a droplet `u` of length `ℓ` and excess energy `ΔE < cℓ`, and for cells of length
`ℓ' ≥ ℓ + 2` (a multiple of the period)

    N_cov(n, ε) ≥ e^{−tε} · ρ_t^{⌊n/ℓ'⌋ − 2},      ρ_t = 2 / max(1 + e^{−t(cℓ−ΔE)},  e^{−tcℓ} + e^{tΔE})  > 1   for small t > 0,

and the same bound times `(1−2δ)` holds for the expected number of evaluations of every randomised algorithm.
If `c < τ` (and the finitely many boundary droplets are sharp) then `N_cov = 1`; if only boundary droplets fail,
`N_cov` is bounded in `n`.

(d) *Ising chain.*  Ferromagnet (`J ≥ 0`): a droplet of `ℓ` flipped spins costs `4J + 2hℓ` (bulk), `2J + 2hℓ` (at
an end), `2hn` (whole chain), so `τ_n = τ = 2h` for every `n ≥ 2`: **sharp iff `c ≤ 2h`**, whatever `J`.
Antiferromagnet: `τ = 2h − 4|J|` if `h > 2|J|` (ground state all-up), and `τ = 0` if `h ≤ 2|J|` (Néel order).
In particular at `h = 0` no chain is sharp for any `c > 0`, although every single spin flip costs `4J`.

*Proof.*  (a) "One evaluation certifies" is `c·d_H(x̂,y) ≤ f(y) − f(x̂)` for all `y` (Theorem 11.7 of the report,
`single_evaluation_certificate_iff`).  The set `{i : y_i ≠ x̂_i}` is a disjoint union of maximal intervals separated by
at least one unchanged site; with nearest-neighbour interactions the excess energy is the sum of the excess energies
of the single-interval excitations, and so is the Hamming distance; a ratio of sums is at least the least ratio.
(b) A closed walk in the (phase, state) graph that changes at least one site is a periodic configuration; its ratio is
approached by finite droplets (repeat the cycle, close with `O(1)` cost), and conversely a droplet plus the ground
state is a closed walk.  A second ground cycle has zero cost and positive length.
(c) Restrict the covering problem to the `2^m` configurations that carry, independently in each of `m` cells,
either the ground pattern or the droplet (energies add exactly because droplets are separated).  For a centre `a`
let `d₀, d₁` be the distances of its cell content to the ground cell and to the droplet cell, `d₀ + d₁ ≥ ℓ`.  The
exponential-weights bound (Theorem 11.6(b), `card_ge_exp_weights`) with uniform weights on this family factorises
over cells and gives per cell `2 / max_{d₀+d₁≥ℓ} [e^{−tcd₀} + e^{−tcd₁+tΔE}]`; the bracket is decreasing in each
`d` and convex along `d₀+d₁ = ℓ`, so the maximum is at an end point.  Both end-point values are `2` at `t = 0` with
derivative `−(cℓ−ΔE) < 0`.  The randomised statement is Theorem 11.23(b).  If `c < τ`, bulk droplets are sharp with
a margin, boundary droplets of length `> C/(τ−c)` are sharp too, and the finitely many others are covered by
finitely many centres.  (d) is a computation. ∎

*Checks* (`z1_sharpness.py`, `out_z1_sharpness.txt`): definition = droplet criterion = min-plus test, and
`τ_droplet = min_y gap/d_H`, on 3 000 random inhomogeneous chains (`k ∈ {2,3}`, `n ≤ 7`; 1 306 sharp); the
ratio-cycle value against the closed forms for nine Ising parameter sets; `τ_n = 2h` for free ferromagnetic chains
`n = 2..10`; exact `N_cov = 1` in the sharp rows of the ILP table (§3.1).

*What interactions change.*  For independent sites, sharpness is `c ≤` (least single-site excitation).  For a
chain the relevant excitation is a long domain: its two walls cost `4J` once, its bulk costs `2h` per site.  A
chain can have a large single-flip gap `4J + 2h` and still be non-sharp as soon as `c > 2h`.

### 2.2 The exponent

**Theorem B.2 (exact exponent for chains) [T*].**  For a homogeneous nearest-neighbour chain as in §2.0 and
`0 ≤ ε_n = o(n)`,

    lim_{n→∞} n⁻¹ ln N_cov(n, ε_n)  =  R*  :=  sup_ν R_ν(e(ν)),

the supremum over stationary (equivalently: stationary ergodic, or randomly-phased block-i.i.d.) processes.  The
same limit holds for `N_point`, for the fractional covering number, for the one-shot values
`R*_n = max_P R(P; s − gap_n, 0) = max_t V_n(t)` (defined in §2.3), and — with the factor `(1−2δ)` — it is a lower
bound for the expected number of evaluations of every randomised algorithm.

*Proof, lower bound.*  Let `A` be a cover and `a(y) ∈ A` with `s(a(y),y) ≤ gap_n(y) + ε_n`.  For a stationary `ν`
let `Y ~ ν_n`.  `E gap_n(Y) ≤ n e(ν) + C`, so the code `a(·)` has mean distortion at most
`n D_n`, `D_n = e(ν) + (C+ε_n)/n`, and `ln|A| ≥ I(Y; a(Y)) ≥ n R^{(n)}_ν(D_n) ≥ n R_ν(D_n)`: the `n`-th order
rate–distortion function of a stationary source dominates its limit, because `L·R^{(L)}` is subadditive (product
test channels; Gallager 1968, §9.8; Berger 1971, ch. 7) **[K]**.  `R_ν` is convex, hence continuous on `(0,∞)`, and
continuous at `0` by Fano's inequality (`s₁ > 0` off the diagonal), so `liminf n⁻¹ ln N_cov ≥ R_ν(e(ν))`.

*Proof, upper bound.*  Fix a block length `L` and `θ > 0`; `n = mL + r`, `r < L`; block alphabet `B = σ^L` with the
block-additive distortion `s_L`; `F(b)` = internal energy of a block, `G = F − L e₀`.  Then for
`y = (b₁,…,b_m, tail)` with block type `P`:   `gap_n(y) ≥ m(E_P[G] − ‖ψ‖) − C'`.

(i) *Low shell.*  Put every `y` with `gap_n(y) ≤ θn` into `A`.  Their number is at most
`exp(n[tθ + p(t) + o(1)])` for every `t ≥ 0`, hence `exp(n σ(θ) + o(n))`,
`σ(θ) = sup{h(ν) : e(ν) ≤ θ}` (microcanonical entropy; Legendre duality), and `σ(θ) ↓ σ(0)` (upper
semicontinuity of the entropy), `σ(0) = sup{R_ν(0) : e(ν) = 0} ≤ R*`.

(ii) *High shell.*  For each block type `P` put `Δ_P = max(θn, m(E_P[G] − ‖ψ‖) − C')/m`.  By the type covering
lemma on the alphabet `B` (Csiszár–Körner, Lemma 9.1; uniform in the type and the level) **[K]** there is
`A_P ⊂ B^m` covering `T_P` within total distortion `mΔ_P` with `ln|A_P| ≤ m[R(P; s_L, Δ_P) + δ_m]`, `δ_m → 0`.  Take
`A_P × σ^r`.  Every `y` of block type `P` with `gap_n(y) > θn` has `gap_n(y) ≥ mΔ_P` and is covered.

(iii) *Comparison with processes.*  Let `ν_P` be the process of i.i.d. blocks with law `P` and uniformly random
phase (stationary, ergodic).  Then `e(ν_P) ≤ (E_P[G] + ‖ψ‖)/L` and
`R(P; s_L, LD) ≤ L·R_{ν_P}(D)` (condition on the phase, cost `ln L`; given the phase the source is memoryless over
`B` and the standard converse applies; let the number of blocks tend to infinity).  So with `D = Δ_P/L`
and `η = 2‖ψ‖/L + C'/(mL)`:  `D ≥ max(θ, e(ν_P) − η)`.
If `e(ν_P) ≤ θ`:  `R_{ν_P}(D) ≤ R_{ν_P}(θ) ≤ R_{ν_P}(e(ν_P)) ≤ R*` (monotonicity).
If `e(ν_P) > θ`:  by convexity the slope of `R_ν` at distortions `≥ θ` is at most `ln k/θ` in absolute value, so
`R_{ν_P}(D) ≤ R_{ν_P}(e(ν_P)) + η ln k/θ ≤ R* + η ln k/θ`.

(iv) There are at most `(m+1)^{k^L}` block types, so
`limsup n⁻¹ ln N_cov ≤ max(σ(θ), R* + 2‖ψ‖ ln k/(Lθ))`; let `L → ∞`, then `θ → 0`. ∎

*Remarks.*  (1) The step the second referee flagged ("type covering for Markov types with a distortion budget fixed
by the pair marginal") is avoided: the budget of a block type differs from the true budget by `O(1)` per block, and
this is harmless *except near zero distortion*, where the rate–distortion function has unbounded slope — hence the
separate low shell.  (2) Step (iii) is proved in Appendix C.  The tag [T*] is kept only because two textbook ingredients are
cited rather than proved (the type covering lemma, uniform in the type and the level, for the fixed block
alphabet; and `R^{(n)}_ν ≥ R_ν`) and because the proof has not been machine-checked or refereed.
(3) Finite-range interactions and finitely many periodically repeated site types go through verbatim (enlarge the
block).  (4) Nothing here computes `R*`: `sup_ν R_ν` is a multi-letter expression.  §§2.3–2.5 are about that.

**Corollary B.2′ (weak envelope, degenerate ground state) [T].**  For the zero-field Ising chain with `ρ = 2J/c`:

    0.007/ρ  ≤  R*  (for 4ρ ∈ ℕ, 4ρ ≥ 2)        R*  ≤  ln 2 / Δ_max(ρ)  (all ρ),      Δ_max(ρ) = max{Δ ∈ ℕ : (1/Δ) Σ_{k<Δ} min(k, Δ−k) ≤ ρ}  (= 4ρ if 4ρ is an even integer),

so `R* = Θ(c/J)` as `c/J → 0`, with `R* ≤ (ln 2/8)(c/J)(1+o(1))`.  *Upper bound*: quantise domain walls to a grid
of spacing `Δ`; over the `Δ` shifts of the grid the mean displacement of a wall is the displayed average, some shift
is at most average, moving a wall by one bond flips one spin, walls that meet annihilate; this gives
`Δ·2^{n/Δ}` centres (verified by brute force on rings, `z10_grid_cover.py`: valid exactly when the criterion
holds).  *Lower bound*: Theorem B.1(c) with droplets of length `ℓ = 4ρ` (`ΔE = 4J = cℓ/2`), cells `2ℓ`, `ρ_t`
maximised at `e^{4Jt} = 2^{1/3}`.  Better constants: `R* ≥ 0.0549` at `ρ = 2` (free-block LP, §2.3) against
`≤ 0.0866`.  An independent site with excitation energy `e` would be sharp for `c ≤ e`; here no `c` is small enough.

**Remark B.2″ (near the sharpness threshold, `h > 0`) [H].**  With `c = 2h + η`: only configurations whose
domains are longer than `4J/η` are not covered by the ground state, and for them almost the whole domain is within
budget.  The estimate `R ≈ max_w (w/c)(η/2 − 2Jw) ln(1/w)` gives `R* ≍ η² ln(J/η)/(Jc)`: **quadratic** vanishing at
the threshold (independent sites: linear, `0.2785(1 − e/c)`).  Supported only by the droplet lower bound
(`≳ η²/(hJ)`), the trivial upper bound `O((η/J) ln(J/η))`, and the absence of any growth in exact numerics for
`J=1, h=1/4, c=1` up to `n = 14` (`ln N_frac = ln 2`).

### 2.3 Duals and primals: matrix-product weights, soft covering, block brackets

For a finite instance and `t ≥ 0` put `K_t(a,y) = e^{−t s(a,y)}`, `b_t(y) = e^{−t·gap(y)}` and

    V(t) = ln max{ Σ_y u(y) b_t(y) :  u ≥ 0,  Σ_y u(y) K_t(a,y) ≤ 1 ∀a }
         = ln min{ Σ_a m(a)      :  m ≥ 0,  Σ_a m(a) K_t(a,y) ≥ b_t(y) ∀y }          (LP duality).

`V(t)` is the exponential-weights bound of the report optimised over the weights (`v = u·b_t`), so
`ln N_frac ≥ max_t V(t) − tε`, and `max_t V(t) = max_P R(P; s − gap, 0)` (Csiszár's dual).  The second line is a
**soft covering**: cover the Boltzmann factor `e^{−t·gap}` by a nonnegative mixture of slack kernels.  The Boltzmann
choice `u ≡ const` gives `B(t) = ln Σ_y b_t(y) − ln max_a Σ_y K_t(a,y)`.

**Proposition B.3 (pressure minus joint spectral radius) [T for the bound; T* for tightness].**  Let `U_s` (`s ∈ σ`) be nonnegative `D×D`
matrices, `l, r ≥ 0`, `u_n(y) = lᵀ U_{y₁}⋯U_{y_n} r`, and `N_a = Σ_s e^{−t s₁(a,s)} U_s`.  Then for every `n`

    N_cov(n,ε) ≥ e^{−tε} · [Σ_y u_n(y) e^{−t·gap_n(y)}] / [max_a lᵀ N_{a₁}⋯N_{a_n} r],

hence   `R* ≥ ln ρ(𝕋_t) − ln JSR{N_a : a ∈ σ}`, where `𝕋_t` is the `Dk×Dk` transfer matrix of
`u·e^{−t·gap}` and JSR is the joint spectral radius.  `D = 1`, `U_s = 1` is the Boltzmann bound
`p(t) − ln(1+(k−1)e^{−tc})`; `D = 1` with general `U_s` is "Boltzmann with a chemical potential".  The supremum
over `t`, `D` and `U` equals `R*`.

*Proof.*  The displayed inequality is Theorem 11.6(b) with `v = u_n e^{−t·gap}`, since
`Σ_y u_n(y) e^{−t s(a,y)} = lᵀ ∏ N_{a_i} r`.  Tightness: block-product weights are matrix-product weights (a
cyclic counter and the block content), and by the proof of Theorem B.2 together with Theorem 11.9 applied to
blocks, block-product weights with slope `t ≤ ln k/θ` reach `R* − O(1/(Lθ))` on the high shell, while the low shell
is reached by `t → ∞` with weights on ground states. ∎

So the answer to "Markov weights or matrix-valued weights?" is: matrix-product weights, and the price of the
matrices is that the denominator `max_a` becomes a joint spectral radius.  (A warning from the numerics: the
cheap upper bound of the JSR by the nonlinear Perron eigenvalue of `v ↦ max_a N_a v` is far too weak here — with
it the run-length-limited weights below never beat the Boltzmann bound; enumeration of all words of length 14 in a
weighted sup norm is needed.  `z7_rll.py` against `z7c_rll_table.py`.)

**Proposition B.4 (one free block brackets the exponent) [T].**  For the ferromagnetic Ising chain with free
boundary and every block length `L` and slope `t`, with `v(t) = lim V_n(t)/n`:

    (V_L(t) − loss(t))/L  ≤  v(t)  ≤  V_L(t)/L,     loss = 2Jt  (and ln(2/(1+e^{−2Jt})) if h = 0),

and `R* = sup_t v(t)`.  *Proof.*  `gap(y₁y₂) = gap(y₁) + gap(y₂) + 2J[wall at the junction]` and `K_t` is a tensor
product: products of feasible `m` are feasible (upper bound), products of feasible `u` are feasible after the
factor `e^{−2Jt}`; for `h = 0` the flip symmetry of the optimal `u` averages the junction factor to `(1+x)/2`.
`R* = sup_t v(t)`: `R*_n = max_t V_n(t)`, and the maximisers stay bounded because `V_n(t) ≤ ln Σ_y b_t(y)`
(feasible `u` are `≤ 1`), which is small compared with `n` for large `t`. ∎

Rigorous brackets from one block of length 12 (`z8_free_brackets.py`; LP values in floating point; the maximum
over `t` is numerical):

| `(J, h, c)` | Boltzmann `max_t B` | rigorous lower | rigorous upper | estimate (increments of `R*_n`, ring, `n ≤ 14`) | grid upper bound |
|---|---|---|---|---|---|
| (1, 0, 6) | 0.28768 | 0.28922 | 0.31311 | 0.28975 | 0.69315 |
| (1, 0, 4) | 0.18823 | 0.21507 | 0.24166 | 0.21916 | 0.34657 |
| (1, 0, 3) | 0.11193 | 0.16778 | 0.19745 | 0.1757 (not converged) | 0.23105 |
| (1, 0, 2) | 0 | 0.11522 | 0.14718 | 0.124 – 0.126 | 0.17329 |
| (1, 0, 1) | 0 | 0.05486 | 0.09009 | ≥ 0.055 (not converged) | 0.08664 |
| (¼, ¼, 1) | 0 | 0.02486 | 0.04450 | 0.038 – 0.040 | — |
| (1, ¼, 2.5) | 0 | 0.04923 | 0.08982 | 0.076 – 0.081 | — |
| (1, ¼, 4.5) | 0.13711 | 0.13943 | 0.18336 | 0.16727 | — |

So at `c = 6J` (and at `(1, ¼, 4.5)`) the exponent is strictly above the Boltzmann value, and in the window it is
positive where the Boltzmann bound is zero.

**Explicit matrix-product certificates [N, rigorous up to floating point].**  Run-length-limited weights
`u(y) = ω^{#walls(y)}·1[every run of y has length ≥ L]` (bond dimension `2L`); numerator `ln λ`,
`λ^L − λ^{L−1} = ωx`; JSR bounded above by enumerating all words of length 14 (`z7c_rll_table.py`), `J = 1, h = 0`:

| `c/J` | Boltzmann | RLL certificate | `(L, t, ω)` |
|---|---|---|---|
| 4 | 0.18823 | 0.20154 | (2, 0.40, 0.75) |
| 3 | 0.11193 | 0.16094 | (2, 0.45, 0.70) |
| 2 | 0 | 0.10459 | (3, 0.45, 0.50) |
| 1.5 | 0 | 0.07537 | (3, 0.45, 0.45) |
| 1 | 0 | 0.04125 | (4, 0.45, 0.35) |

**Structure of the optimal weights [N]** (`z3_structure.py`, `z5_rank.py`).  On rings of 10 and 12 sites at
`c = 4J` the optimal `u` and the optimal soft-covering measure `m` have the *same support*: exactly the
configurations all of whose runs have length `≥ 2`; at `c = 2J` (ring of 12): runs `≥ 3`.  Domains of length
`≤ 4J/c` can be erased within budget and carry no weight.  On the support `Ku = 1` and `Km = b`, so the value is
`1ᵀ_S K_SS⁻¹ b_S` — a `b`-weighted *magnitude* (in Leinster's sense) of the run-length-limited shift in the
Hamming kernel.  The weights are not of renewal form (`u` depends on the order of the runs: `(2,4,2,4)` against
`(4,2,2,4)`: `0.525` against `0.507`) and not finitely correlated: the singular values of `u` across the middle cut
of a free chain decay like `1, 0.5, 0.18, 0.18, 10⁻², 10⁻³, 10⁻³, 2·10⁻⁴, 10⁻⁴, 3·10⁻⁵, …` without terminating
(`n = 10` and `12`).

### 2.4 When is the transfer-matrix (Boltzmann) bound positive, and when is it exact?

**Theorem B.5 (the vacuous window) [T].**  Ising chain, `J ≥ 0`, `h ≥ 0`, `c > 2h`.  Then
`max_{t≥0} [p(t) − ln(1+e^{−tc})] > 0`  iff  `c > 2(J+h)`.
Hence for `2h < c ≤ 2(J+h)` the Boltzmann bound is zero while `R* > 0` (Theorem B.1).

*Proof.*  `e^{p(t)} = ½[(1+z) + ((1−z)² + 4x²z)^{1/2}]`, so `B(t) > 0 ⟺ x²z > q(1−z) + q²`, i.e.
`F(t) := e^{−(4J+2h)t} − e^{−ct}(1 − e^{−2ht}) − e^{−2ct} > 0`.  If `c ≤ 2(J+h)` then `e^{−(4J+2h)t} ≤ e^{−(2c−2h)t}`
and with `A = e^{−ct}`, `w = e^{2ht}`, `Aw ≤ 1`:  `F ≤ A²w − A + A/w − A² = A(w−1)(Aw−1)/w ≤ 0`.  If
`c > 2(J+h)`: `B(t) = t(c/2 − J − h) + O(t²)`. ∎   (`z9_phase.py`: `max_t B = 0` at `c = 2(J+h)` and `> 0` at
`c = 2(J+h) + 0.05` for eight values of `h/J`.)

Meaning: `c > 2(J+h)` says that a *uniformly random* configuration (mean gap `J + h` per site) is farther than its
budget from every centre.  The window is where only long domains are uncoverable.

**Theorem B.6 (exactness = deconvolution positivity) [T; known in substance, see below].**

(a) (any finite instance with invertible `K_t`)  `V(t) = B(t)` iff `K_t⁻¹ b_t ≥ 0` pointwise, i.e. iff the
Boltzmann factor is a nonnegative mixture of slack kernels; for the Hamming envelope: iff the Gibbs measure of the
gap landscape at inverse temperature `t` is the output of a memoryless symmetric channel with crossover
`q/(1+(k−1)q)` per wrong letter.

(b) (Ising chain)  `(K_t⁻¹ b_t)(a) ∝ Tr ∏_i (D_{a_i} T)` on a ring (`lᵀ D_{a₁} T D_{a₂} ⋯ D_{a_n} l` on a free
chain), `D₀ = diag(1,−q)`, `D₁ = diag(−q,1)`.  It is nonnegative for **all** words of **all** lengths iff

    x² z (1+q)² ≥ q (1+z)²,     i.e.     cosh(ct/2) ≥ e^{2Jt} cosh(ht);

if the inequality fails, the alternating word `0101…` becomes negative first (at length `≈ π/θ`, `θ` the argument
of the complex eigenvalue of `D₀TD₁T`).

(c) At large `t` the condition reads `c > 4J + 2h` (the single-flip energy); it fails for all `t > 0` if `c ≤ 4J`.

*Proof.*  (a) `u ≡ const > 0` is optimal iff there is a dual `m ≥ 0` with `Km ≥ b` and complementary slackness,
which forces `Km = b`.  (b) The Möbius maps `ξ ↦ (w − zqξ)/(1 − wqξ)` and `ξ ↦ (zξ − qw)/(wξ − q)` (`w = x√z`,
`ξ` the ratio of the two components) induced by `TD₀`, `TD₁` are decreasing; an interval of ratios inside the
positivity domain `[q/w, w/(zq)]` invariant under both exists iff the increasing map obtained by composing them has
a real fixed point there, i.e. iff `D₀TD₁T` has real positive eigenvalues: `tr² ≥ 4 det` with
`tr = x²z(1+q²) − q(1+z²)`, `det = q²z²(1−x²)²`.  With an invariant cone all products map the cone into itself, so
traces and the boundary contractions are nonnegative; without it the alternating product rotates (or has two
negative eigenvalues). ∎

*Checks* (`z4_positivity.py`): (a) on 48 (instance, `t`) pairs, `V − B < 10⁻⁷ ⟺ min_a (K⁻¹b)(a) ≥ 0`; (b) on 397
random `(x,z,q)`: condition true ⇒ all words of length `≤ 14` nonnegative (ring and free chain, 62 cases);
condition false ⇒ a negative word at the predicted length (335 cases), the first one alternating in all 335.

*Prior art.*  (a)–(b) are the **Hajek–Berger (1987) decomposition** of a binary Markov random field as the
mod-2 sum of a field and white noise, which is what makes the Shannon lower bound of its rate–distortion function
exact; Newman (1987) relates the largest noise weight `δ_c` to zero-free regions of the partition function; for
`h = 0` the condition is `4D(1−D) ≤ x²`, `D = q/(1+q)`, i.e. **Gray's critical distortion**
`D_c = ½(1 − (1 − (q_G/p_G)²)^{1/2})` of the binary symmetric Markov source (Gray 1970) **[K; the formula is quoted
from memory, re-derived and checked here]**.  The closed form with a field is the same computation; I could read
only the abstracts of Hajek–Berger and Newman and do not claim it is new.  What is specific here is the *use*: the
criterion decides whether the transfer-matrix bound on the certificate size is the truth.

**Corollary B.7 (zero field: where the closed form is the exponent) [T for (i), (iii); N for (ii)].**
`ρ = 2J/c`, `B(x) = ln(1+x) − ln(1+x^{1/ρ})`.

(i) `R* ≤ max( sup_{positive t} B, sup_{non-positive t} 2 ln[(1+√q)/(1+q)] )`; the second function is at most
`2 × 0.18823 = 0.37645` (at `q = 3 − 2√2`).  Therefore, for `ρ ≤ ρ₁ = 0.22037` (`c ≥ 9.076 J`),

    R* = max_{0<x<1} [ ln(1+x) − ln(1+x^{c/2J}) ]      (= the exponent of independent *bonds* with excitation 2J).

(ii) Positivity holds at the Boltzmann optimum iff `ρ ≤ ρ_pos = 0.24307` (`c ≥ 8.228 J`); for
`ρ₁ < ρ ≤ ρ_pos` the same formula is supported by the one-shot values (`c = 9J`: increments `0.37479` against
`0.37479`) but not proved.

(iii) For `ρ > ρ_pos`, `V(t*) > B(t*)` on every sufficiently long ring, and for `ρ ≥ ½` (`c ≤ 4J`) the
Boltzmann weights are optimal for **no** `t > 0`.  `R* > max B` strictly: rigorous at `c = 6J, 4J, 3J`
(table in §2.3).  At `c = 8J` the two differ only in the sixth digit.

With a field the positivity boundary at the optimum is `c_pos(h)`: `8.23, 8.40, 8.56, 8.98, 9.58, 10.65, 12.63,
16.49` for `h/J = 0, 0.05, 0.1, 0.25, 0.5, 1, 2, 4` (`z9_phase.py`); at `J=1, h=¼, c=10` the increments of `R*_n`
equal the Boltzmann value `0.33942` to five digits.

*Proof of (i).*  Where positivity fails, replace `x` by `x' = 2√q/(1+q) ≥ x`: `b' ≥ b_t` pointwise and
`K_t⁻¹ b' ≥ 0`, so `m = K_t⁻¹ b'` is feasible for the soft covering and
`V_n(t) ≤ ln Σ_a m(a) = ln Z'_n − n ln(1+q) ≤ n[ln(1+x') − ln(1+q)] + ln 2`.  With `R* = lim max_t V_n(t)/n`
this gives the bound; for `ρ ≤ ρ₁`, `max B ≥ 0.37645`. ∎

**The picture for the Ising chain (units `J = 1`).**

| regime | `c` | status |
|---|---|---|
| sharp | `c ≤ 2h` | `N_cov = 1` |
| exponential, Boltzmann bound vacuous | `2h < c ≤ 2(1+h)` | `R* > 0`; only long domains matter |
| exponential, Boltzmann positive but not exact | `2(1+h) < c < c_pos(h)` | `R* >` Boltzmann |
| exponential, Boltzmann exact | `c ≥ c_pos(h)` (proved for `h=0`, `c ≥ 9.08`) | closed form |

The statement "two-state sites: Boltzmann weights are always optimal" of the product theory (report, after
Theorem 11.9) does **not** survive a coupling: it needs `c ≳ 8J`.

**Negative result on closed forms [N + K].**  In the non-positive regime the exponent is `sup_ν R_ν(e(ν))` over
processes beyond their critical distortion.  For `h = 0` and Markov `ν` this is the rate–distortion function of the
binary symmetric Markov source above `D_c`, unknown since Gray (1970) (bounds: Berger 1977; Jalali–Weissman 2007).
The supremum over `ν` could in principle be easier than a single `R_ν`; the non-terminating Schmidt spectrum of the
optimal weights (§2.3) is evidence that it is not given by a finite transfer matrix.

### 2.5 Finite temperature: the soft gap of a chain, and the three budgets

`π` = Gibbs measure of `E` at inverse temperature `β`; here `q = e^{−βc}`, `T_β` = transfer matrix of `e^{−βE}`,
`λ(T_β)` its top eigenvalue.

**Proposition B.8 (soft gap = hidden-Markov log-likelihood = pinned free energy) [T].**
For site-additive slack, `e^{−Λ(y)} = Σ_a π(a) ∏_i e^{−β s₁(a_i,y_i)}`.  Hence:

(i) For `g = 0` and the Hamming envelope, `e^{−Λ(y)} = (1+(k−1)q)ⁿ · π̃(y)`, where `π̃` is the law of a sample of `π`
observed through the memoryless symmetric channel with crossover `q/(1+(k−1)q)` per wrong letter:
`Λ(y) = −ln π̃(y) − n ln(1+(k−1)q)`.  For a chain, `π̃` is a hidden Markov measure and

    e^{−Λ(y)} = lᵀ ∏_i (Q_{y_i} T_β) r / Z,      Q_s = diag(e^{−β s₁(a,s)})_a ,

computable in `O(nk²)` for each `y` — a ratio of two transfer-matrix partition functions, the numerator with the
`y`-dependent pinning potential `s₁(·, y_i)`.  For the Ising chain the pinning is a field of magnitude `c/2` with
signs prescribed by `y`: `Λ(y)/β` is the free-energy cost of that field configuration (for random `y`, the free
energy of a random-field Ising chain).

(ii) `min_y Λ(y) = n[ln λ(T_β) − ln JSR{Q_s T_β}] + O(1)`; for the Ising ferromagnet the minimiser is a constant
word, for the antiferromagnet the alternating word **[N]** (rings of 14, seven parameter sets, also with a field).

(iii) For a stationary `ν`, `Λ̄(ν) := lim n⁻¹ E_ν Λ = h(ν) + d(ν‖π̃) − ln(1+(k−1)q)` (a cross-entropy rate; a
Lyapunov exponent of the matrix products `Q_{y_i}T_β` driven by `ν`), continuous in `ν`.

(iv) `Σ_y e^{−τΛ(y)}` is a finite transfer matrix only for integer `τ ≥ 1` (`τ = 1`: `(1+(k−1)q)ⁿ` exactly;
`τ = 2`: a two-replica `k²×k²` matrix with weights `1+q²` / `2q` on equal / unequal replica letters).  For
non-integer `τ`, and for `E_π e^{Λ} = (1+(k−1)q)^{−n} Σ_y π(y)/π̃(y)` (a moment of order `−1`), there is none; they
are spectral radii of transfer operators on the projective line,

    (L_τ F)(p) = Σ_s ν(p,s)^τ F(φ(p,s)),        (M F)(a,p) = Σ_s T_β(a,s) ν(p,s)^{−1} F(s, φ(p,s)),

where `(1−p, p) Q_s T_β = ν(p,s)·(1−φ, φ)`.

*Proof.*  Definitions and `K = ⊗ K_site`; (iii) is the subadditive ergodic theorem for positive matrices. ∎
*Checks* (`f1_softgap.py`, `softgap_ops.py`): enumeration against `2×2` products to `10⁻¹⁵`; `Σ π̃ = 1`;
`0 ≤ Λ ≤ −ln π`; operator values against the exact two-replica matrix to 9 digits (four parameter sets, including
`βJ = 3`), against enumeration increments (`n ≤ 20`), and `P_Λ(1) = ln(1+q)` to `10⁻¹⁵`.  The operator is
discretised by Chebyshev interpolation in the log-odds coordinate on the invariant interval; in the raw coordinate
`p` it does not converge at low temperature (recorded dead end).

**Theorem B.9 (three budgets for chains) [T*].**  Homogeneous chain as in §2.0.  Per site:

| problem | budget of a process `ν` | exponent | status |
|---|---|---|---|
| minimum, all algorithms | `e(ν)` | `R* = sup_ν R_ν(e(ν))` | Theorem B.2 |
| `ln Z`, deterministic | `d(ν‖π)/β = e(ν) − h(ν)/β + p(β)/β` (free-energy gap of `ν`) | `R_β = sup_ν R_ν(d(ν‖π)/β)` | lower bound [T] (one-shot Hölder converse of the report on the `n`-block + converse of §2.2); upper bound: Merhav's construction on block types, sketch only |
| `ln Z`, randomised, dip bound, accuracy `nε₁` | `(Λ̄(ν) + ε₁)/β` | `R^rand_β(ε₁) = sup_ν R_ν((Λ̄(ν)+ε₁)/β)` | this is the exact exponent of the best dip-packing bound (proof of B.2 with radii `(Λ+ε)/β`; `Λ` is additive over blocks up to `O(1)` per block) |
| spot-check with the report's hint distribution | — | `U_β = lim n⁻¹ ln E_π e^Λ = sup_ν [Λ̄(ν) − d(ν‖π)]` | Prop. B.8(iv) |

Bracket for the randomised exponent at an additive chain instance: `R^rand_β ≤ exponent ≤ min(R_β, U_β)`.
Uniform-weight (transfer-matrix) versions: `R_β ≥ max_t {((β+t)/β)[p(τβ) − τ p(β)] − ln(1+(k−1)e^{−tc})}`,
`τ = t/(β+t)` (closed form; tends to the thermodynamic entropy `s(β)` as `t → ∞`), and
`R^rand_β(ε₁) ≥ sup_t [P_Λ(t/β) − tε₁/β − ln(1+(k−1)e^{−tc})]` with the Rényi-type pressure `P_Λ(τ) = ln ρ(L_τ) − τ ln λ(T_β)`.
At `t = β` the latter is exactly `0` (`K_β⁻¹ π̃^{1} ∝ π ≥ 0`: the uniform weights are optimal there and the bound is trivial).

Numbers, per site (`f2_exponents.py`; `R^rand` from LP increments on rings `n ≤ 12`, the rest thermodynamic):

| `(J, h, β, c)` | `R^rand_β(0)` LP | `R^rand_β(0)` uniform weights | `U_β` | entropy `s(β)` | `R_β ≥` |
|---|---|---|---|---|---|
| (0, 0, 1, 1) cube | 0.02914 (closed form 0.02914) | 0.02913 | 0.37989 | 0.69315 | 0.69315 |
| (0.25, 0, 1, 1) | 0.02880 | 0.02878 | 0.36964 | 0.66285 | 0.66579 |
| (0.5, 0, 1, 1) | 0.0316 | 0.02777 | 0.34191 | 0.58220 | 0.59412 |
| (1, 0, 1, 1) | not converged (0.029, 0.046) | 0.02427 | 0.26754 | 0.36533 | 0.39670 |
| (0.5, 0, 1, 2) | 0.0915 | 0.08819 | 0.51181 | 0.58220 | 0.60540 |
| (0.5, 0, 2, 1) | ≈ 0.096 – 0.101 | 0.07027 | 0.41149 | 0.36533 | 0.43006 |
| (0.5, 0.25, 1, 1) | 0.0233 | 0.02055 | 0.30207 | 0.45418 | 0.49130 |
| (−0.5, 0, 1, 1) | 0.0316 (= ferromagnet, by the sublattice gauge) | 0.02777 | 0.34191 | 0.58220 | 0.59412 |

As at zero temperature, uniform weights stop being optimal once the coupling is appreciable.  The gap between
`R^rand` and `U_β` is as wide as on the cube (where the lower one is the truth, by Harper's theorem): `E_π e^Λ` is
a general but loose upper bound.

**Zero-temperature limit of the spot-check exponent [T for the limit; N for the count].**
`lim_{β→∞} E_π e^Λ = Σ_{y stable} 1/mult(y)`, `y` *stable* iff `gap(y) ≤ gap(a) + c·d_H(a,y)` for all `a` (the
contact set: `y` is a minimiser of `f + g` for some admissible `g`).  For the zero-field ferromagnetic chain and
generic `c`, `y` is stable iff all its (interior) runs have length `≥ L₀ = ⌈4J/c⌉`, so
`U_∞ = ln(largest root of z^{L₀} = z^{L₀−1} + 1)`: `ln 2, 0.4812, 0.3823, 0.3223` for `L₀ = 1, 2, 3, 4`
(`f7_zeroT_limit.py`: 4096, 324, 92, 62 stable configurations on a ring of 12 for `c/J = 5, 3, 1.5, 1.1`, and
`E_π e^Λ = 4066, 326, 90, 60` at `β = 6`).  Compare `R* ≈ 0.176` at `c = 3J`: at low temperature the covering
exponent is far below the sampling exponent, and `U_∞ ≈ ln(L₀)/L₀` against `R* ≍ 1/L₀` for small `c/J`.

### 2.6 Is there an accuracy threshold as on the cube?  Yes: the largest chord gap of the pressure

Binary alphabet; `M(y)` = number of ones.  For a slope `θ ∈ [−c, c]` let `E_θ = f + θM`, `π_θ` its Gibbs measure,

    P(θ) = lim n⁻¹ ln Σ_y e^{−β E_θ(y)}        (convex, |P′| ≤ β),
    G(θ) = [(c+θ) P(c) + (c−θ) P(−c)] / (2c) − P(θ)        (chord gap; concave, ≥ 0),
    D(θ′; θ) = P(θ′) − P(θ) − (θ′−θ) P′(θ)                (Bregman divergence),
    ε₁* = max_{|θ|≤c} G(θ) = G(θ*),   P′(θ*) = [P(c) − P(−c)]/(2c).

The additive residuals `θM` are exactly the uniform fields the envelope cannot exclude: for the Ising chain
`P(θ) = p_field(h + θ/2) − βθ/2`, `p_field(h′) = ln[e^{K} cosh βh′ + (e^{2K} sinh² βh′ + e^{−2K})^{1/2}]`, `K = βJ`,
and `ε₁*` is the largest chord gap of the pressure over the field interval `[h − c/2, h + c/2]`.  For independent
sites with excitation `e`: `P(θ) = ln(1 + e^{−β(e+θ)})`.

**Theorem B.10 (dip threshold at the instance `g₀ = θM`) [T for independent sites; T* for chains].**
If `ε₁ < G(θ)` there is `κ > 0` such that every randomised algorithm that is `(nε₁/2, δ)`-correct for `ln Z` on the
whole class makes at least `(1−2δ) e^{κn}` evaluations in expectation on the instance `g₀ = θM`.
For independent sites and for ferromagnetic chains [N for the latter] `G(θ)` is exactly where the dip bound stops
being exponential.  At the zero residual: `G(0) = ½[P(c) + P(−c)] − P(0)`, a second difference of the pressure
(this is the `ε₁^crit` of the report); for a spin-flip symmetric chain

    G(0) = p_field(c/2) − p_field(0) = ln[cosh(u/2) + (sinh²(u/2) + e^{−4βJ})^{1/2}] − ln(1 + e^{−2βJ}),   u = βc,

`β` times the free energy gained in a field `c/2`; it increases from `ln cosh(u/2)` at `J = 0` to `u/2` as `βJ → ∞`.

*Proof.*  At `g₀` the slack is asymmetric: `s₁(1,0) = c − θ`, `s₁(0,1) = c + θ`.  Let `y` consist of constant
blocks of length `L`, a fraction `μ` of them all-ones (independently).  By Proposition B.8,
`−Λ̄ = (1−μ)[P(c) − P(θ)] + μ[P(−c) − P(θ) − β(c+θ)] + O(1/L)` (on a zero block the pinning turns slope `θ` into
`c`, on a one block into `−c`).  The block process is memoryless over the alphabet `{0^L, 1^L}`; a reproduction
block with `k` ones costs `(1−μ)(c−θ)k + μ(c+θ)(L−k)` on average, linear in `k`, so its zero-rate distortion per
site is `D₀ = min(μ(c+θ), (1−μ)(c−θ))`.  By Theorem 11.24(b) with product weights over blocks (and the dichotomy
argument of Theorem 11.9 for a two-letter source) the bound is exponential iff `(Λ̄ + ε₁)/β < D₀`.  The right-hand
side minus the left is increasing in `μ` up to `μ* = (c−θ)/(2c)` and decreasing after (because `|P′| ≤ β`), and at
`μ*` the condition is `ε₁ < (1−μ*)P(c) + μ*P(−c) − P(θ) = G(θ)`.  Conversely the vanishing point of the dip
exponent is `sup_ν [β D₀(ν) − Λ̄(ν)]` with `D₀(ν) ≤ min_a E_ν s₁(a,Y₀)`, which is
`sup_μ [β min(μ(c+θ),(1−μ)(c−θ)) − Λ̄_min(μ)]`; `Λ̄_min` is linear (phase separation is optimal) for independent
sites, and numerically for ferromagnetic chains. ∎

*A subtlety (recorded dead end).*  The single-centre game value `max_P min_a E_P[βs(a,·) − Λ]` is attained by the
zero-entropy law that mixes the two constant words — for which the packing bound is `2`, not exponential.  The
value is nevertheless the vanishing point of the exponent because block processes with long blocks approach it; the
exponent tends to zero at the threshold.  (For the strongly coupled ferromagnet the threshold is `≈ βc/2` but the
exponent near it is tiny.)

**Theorem B.11 (sandwich with a tilted reference) [T; exact width for independent sites].**
For every admissible `g`, with `g̃ = g − θM`:

    ln Z(f+θM) − β E_{π_θ} g̃  ≤  ln Z(f+g)  ≤  ln Z(f+θM) − β E_{π_θ} g̃ + W_n(θ),
    W_n(θ) = sup_g ln E_{π_θ} e^{−β(g̃ − E_{π_θ} g̃)}  ≥  n·max(D(c;θ), D(−c;θ)) − O(1).

For independent sites `W_n(θ) = n·max(D(c;θ), D(−c;θ))` (tensorisation: the increments of `g̃` lie in
`[−c−θ, c−θ]` and the two-point Jensen gap is convex in the increment).  Moreover
`min_θ max(D(c;θ), D(−c;θ)) = G(θ*) = ε₁*`, attained at `θ = θ*` (the tangent parallel to the chord).
`E_{π_θ} g̃` is estimated from `N` samples of `π_θ` to within `(c+|θ|)(n ln(2/δ)/(2N))^{1/2}` for independent
sites (bounded differences), and within `n(c+|θ|)(ln(2/δ)/(2N))^{1/2}` in general — in both cases `N` does not
grow with `n` when the accuracy is extensive.

**Theorem B.12 (sharp accuracy threshold for identical two-state independent sites) [T].**
`X = {0,1}ⁿ`, `f = e·M`, class of all `c`-Hamming-Lipschitz residuals, `P(θ) = ln(1+e^{−β(e+θ)})`.
(a) If `ε₁ > ε₁*`, a number of random evaluations independent of `n` suffices on every instance (sample `π_{θ*}`,
return the midpoint of the tilted sandwich).
(b) If `ε₁ < ε₁*`, every randomised algorithm that is `(nε₁/2, δ)`-correct on the class makes at least
`(1−2δ)e^{κn}` evaluations on the instance `g₀ = θ*M`.
For `e = 0`: `θ* = 0`, `ε₁* = ln cosh(u/2)` — Theorem 11.25 of the report.  For `e ≠ 0` the hardest instance is not
the zero residual and the best reference is not the Gibbs measure of the known part: for `e/c = ½`, `β = 1`
(the report's example) `G(0) = 0.11367`, untilted width `0.12246`, and `ε₁* = 0.11383` at `θ* = −0.037c`.
In the terms of the updated report (§12.2(c): "the worst-case threshold of a product class for algorithms
*without* a hint … lies between `sup_g ε₁^thr(g)` and the hint-free passive width"): for identical two-state
sites both ends are equal to `ε₁*` — the hint-free width is `ε₁*` once the reference is tilted to `θ*`, and no
instance can have a larger threshold because the tilted sandwich works on every instance.

**For chains:** (b) holds with the chain pressure (Theorem B.10); (a) holds with `ε₁*` replaced by
`W(θ*) = lim W_n(θ*)/n ≥ ε₁*`, and `W(θ*) = ε₁*` iff additive residuals are extremal for the Jensen gap under
`π_{θ*}`:

**Conjecture B.13 (additive extremality for pairwise binary references) [C].**  For every measure
`π ∝ exp(Σ_{i<j} J_ij s_i s_j + Σ h_i s_i)` on `{0,1}ⁿ` (any signs, any graph) and every `θ`, the maximum of
`ln E_π exp(−β(g − θM − E_π[g − θM]))` over the `c`-Hamming-Lipschitz `g` is attained at `g = c Σ_i ε_i y_i`,
`ε ∈ {±1}ⁿ`.

*Evidence.*  The functional is convex, so the maximum is at a vertex of the Lipschitz polytope of the `n`-cube, and
because the cube is bipartite the vertices are exactly `c` times the graph homomorphisms `Q_n → ℤ` (`6, 38, 990,
395 094` for `n = 2,…,5`, pinned): the maximum is computed *exactly* for `n ≤ 5` (`f3_jensen.py`,
`f4_jensen_classes.py`, `f6_class_threshold.py`).  Zero violations in: 39 homogeneous chain cases (ferro, antiferro,
with field, periodic); 400 random inhomogeneous chains; 300 random chains with a random tilt `θ`; 3 000 arbitrary
laws on `{0,1}²`; 300 random trees; 300 stars; 300 ferromagnetic cycles; 300 ferromagnetic complete graphs; 300
frustrated complete graphs; 300 antiferromagnetic odd cycles; 600 chains with next-nearest-neighbour couplings.
Adversarial search (Nelder–Mead on the margin "best non-additive vertex minus best additive vertex") over all
pairwise parameters for `n = 3` (60 starts) and `n = 4` (25 starts): the margin never becomes positive (its
supremum is `0`); the same search with a three-body term finds a violation immediately (margin `0.693`), which is
the known counterexample of the report (`DEAD_ENDS` D25: uniform measure on even-weight strings).  Sequential LP
from 60 random starts for ferromagnetic chains of 6, 7, 8 sites: the magnetisation is the best vertex found.
For product measures the statement is the classical tensorisation **[K]**.

*What it would give.*  (1) The exact worst-case free-energy gap of a binary chain reference (report §12, item 5):
the largest Bregman divergence of the log-partition function over the sign patterns — for a homogeneous
ferromagnetic chain `n·max(D(c;0), D(−c;0))`, two `2×2` eigenvalue problems.  (2) A sharp accuracy threshold
`ε₁*` on chains.
*Dead end for a proof.*  Reduction to one dimension fails: for a law on the line the extremal 1-Lipschitz function
of the one-sided Laplace functional need not be monotone (atoms `−1, 0, 1` with masses `0.01, 0.98, 0.01` and
slope `5`: the tent `−|x|` gives `1.273`, `±x` give `0.902`); on the square the two extra additive functions rescue
the statement.  The Marton/Kontorovich martingale bound is not sharp either (it lets the sign of each increment
depend on the past, which the Lipschitz constraint forbids): `0.399` against the true `0.255` per site at
`βJ = 0.5`, `βc = 1`.

Thresholds per site (`β = 1`; `f5_threshold.py`, `f6_class_threshold.py`; the finite-`n` game values on rings of 10
agree with `G(0)` and `G(θ*)` to 5 digits except at `J = 1`, where `n = 10` is too short):

| `(J, h, c)` | `G(0)` (dip threshold at the zero residual) | untilted width `max(D(±c;0))` | `θ*/c` | `ε₁* = G(θ*) = max(D(±c;θ*))` |
|---|---|---|---|---|
| (0, 0, 1) cube | 0.12011 | 0.12011 | 0 | 0.12011 |
| (0, 0.25, 1) (`e/c = ½`) | 0.11367 | 0.12246 | −0.037 | 0.11383 |
| (0, 1, 1) | 0.05400 | 0.06713 | −0.120 | 0.05479 |
| (0.5, 0, 1) | 0.25517 | 0.25517 | 0 | 0.25517 |
| (0.5, 0.25, 1) | 0.19798 | 0.28303 | −0.184 | 0.20620 |
| (0.5, 0.5, 2) | 0.46929 | 0.81693 | −0.306 | 0.53271 |
| (1, 0.1, 1) | 0.35123 | 0.55203 | −0.147 | 0.36741 |

With a coupling and a field the untilted sandwich is far from the threshold (`0.82` against `0.53`): the reference
must be tilted towards the worst admissible field.

---

## 3. Numerics (what, sizes, results)

All code is in this directory and was written for this workstream (`chainlib.py` is the common library); nothing
from `experiments/` was reused.  Exact = exhaustive enumeration, integer programming (HiGHS through SciPy), or
linear programming with symmetry reduction (orbits of the dihedral group, and of the global flip when `h = 0`).

### 3.1 Exact covering numbers of small free chains (`z6_ncov.py`, ILP; `*` = time limit 40 s, best found / bound)

`N_cov` for `n = 4,…,10`, with the fractional number in brackets:

| `(J, h, c)` | 4 | 5 | 6 | 7 | 8 | 9 | 10 | remark |
|---|---|---|---|---|---|---|---|---|
| (1, 0, 2) | 4 | 4 | 4 | 6 | 7 [6.5] | 8 | 10 | window: Boltzmann bound zero |
| (1, 0, 4) | 8 | 10 | 16 | 19 [18.7] | 24 | 36 | 43 [42] | |
| (1, 0, 1) | 2 | 2 | 4 | 4 | 4 | 4 | 4 | exponent ≈ 0.06: invisible at these sizes |
| (1, ¼, ½) | 1 | 1 | 1 | 1 | 1 | 1 | 1 | sharp (`c ≤ 2h`) |
| (1, ¼, 1) | 2 | 2 | 2 | 2 | 2 | 2 | 3 | non-sharp, domains `> 8` needed |
| (¼, ¼, 1) | 3 | 3 | 3 | 4 | 4 | 5 [4.5] | 6 [5.5] | `c = 2(J+h)`: Boltzmann zero |
| (1, ¼, 4.5) | 8 | 10 | 14 | 17 [16.5] | 23 [22.3] | 29* [27.1] | 38* [34.4] | |
| (−1, 0, 2) | 4 | 4 | 4 | 6 | 7 | 8 | 10 | = ferromagnet (sublattice gauge) |
| (−1, ½, 2) | 5 | 5 | 7 | 6 | 11 | 10 | 16 [15] | Néel order, parity effects |
| (−1, 3, 2) | 1 | 1 | 1 | 1 | 1 | 1 | 1 | sharp (`c ≤ 2h − 4|J|`) |

The greedy cover is up to twice as large (`8` against `4`, `65` against `43`).  `N_frac` and `N_cov` nearly coincide at these sizes.

### 3.2 One-shot values on rings (`z2b_tables.py`; `n = 8, 10, 12, 14`; one row `n = 16`)

`R*_n = max_t V_n(t)`; "incr" = `(R*_n − R*_{n−2})/2` for `n = 10, 12, 14`; the inequalities
`max_t B_n ≤ R*_n ≤ ln N_frac` held in every row.

| `(J, h, c)` | Boltzmann `∞` | incr of `R*_n` | `ln N_frac/n` at `n = 14` |
|---|---|---|---|
| (1, 0, 16) | 0.47468 | 0.47468, 0.47468, 0.47468 (and `n = 16`: 0.47468) | 0.6456 (`n = 16`: 0.6237) |
| (1, 0, 9) | 0.37479 | 0.37478, 0.37479, 0.37479 | 0.5699 |
| (1, 0, 8) | 0.35088 | 0.35086, 0.35088, 0.35088 | 0.4867 |
| (1, 0, 6) | 0.28768 | 0.28964, 0.28973, 0.28975 | 0.4261 |
| (1, 0, 4) | 0.18823 | 0.21934, 0.21917, 0.21916 | 0.2886 |
| (1, 0, 3) | 0.11193 | 0.17484, 0.17533, 0.17565 | 0.2872 |
| (1, 0, 2) | 0 | 0.12315, 0.12605, 0.12411 | 0.1843 |
| (1, 0, 1.5) | 0 | 0.08427, 0.09330, 0.09730 | 0.1843 |
| (1, 0, 1) | 0 | 0.00911, 0.04383, 0.05505 | 0.1165 |
| (1, ¼, 1) | 0 | 0, 0, 0 (`R*_n = 0.18823` for all `n`) | 0.0495 (`N_frac = 2`) |
| (¼, ¼, 1) | 0 | 0.03963, 0.03944, 0.03798 | 0.1355 |
| (¼, ¼, ¾) | 0 | 0, 0.01401, 0.01392 | 0.0954 |
| (1, ¼, 2.5) | 0 | 0.08115, 0.07962, 0.07589 | 0.1686 |
| (1, ¼, 4.5) | 0.13711 | 0.16736, 0.16727, 0.16727 | 0.2841 |
| (1, ¼, 10) | 0.33942 | 0.33942, 0.33942, 0.33942 | 0.5092 |

Reading: the increments of `R*_n` converge very fast where the relevant domains are short and are the best
estimate of `R*`; `ln N_frac/n` is far above (polynomial prefactors and integer radii, as in the report's layer
counts); for small `c` or `c` close to `2h` rings of 14 are too short (domains longer than `4J/(c−2h)` must fit).
In the row `(1, ¼, 1)` the only uncovered pair at these sizes is the fully flipped chain, a single two-state
"super-site" with `e/c = ½`, whence the constant `0.18823` (the number of Theorem 11.9).

### 3.3 Other checks (all passed unless stated)

* `z1_sharpness.py`: §2.1 (3 000 random chains; ratio cycles; finite ferromagnets).
* `z4_positivity.py`: Theorem B.6 (48 + 397 cases) and the three zero-field thresholds
  `ρ_pos = 0.243073`, `ρ₀ = 0.196610` (`q_c ≥ 3 − 2√2`), `ρ₁ = 0.220366`.
* `z9_phase.py`: Theorem B.5 and `c_pos(h)`.
* `z10_grid_cover.py`: domain-wall grid covers are valid exactly when the mean-displacement criterion holds
  (rings of 12, 15, 16; two deliberately invalid cases fail as they should).
* `z3_structure.py`, `z5_rank.py`: supports and Schmidt spectra of the optimal weights.
* `z7_rll.py` (negative: max-operator JSR bound useless), `z7b_probe.py`, `z7c_rll_table.py` (certificates).
* `z8_free_brackets.py`: Proposition B.4 at `L = 12` (1 056 / 2 080 orbits).
* `f1_softgap.py`, `softgap_ops.py`: Proposition B.8.
* `f2_exponents.py`: table of §2.5; cube row reproduces `ln 2 − h(ρ₀) = 0.02914` and `ln cosh(½) = 0.12011`.
* `f3_jensen.py`, `f4_jensen_classes.py`, `f4b_adversarial.py`, `f6_class_threshold.py` (part C): Conjecture B.13.
* `f5_threshold.py`, `f6_class_threshold.py`: finite-`n` game values against `G(0)`, `G(θ*)`; the dip-packing
  bound as a function of the accuracy vanishes at the game value (`0.0316, 0.0128, 0.0033, 0.0008, 0.0001, 0, 0`
  per site at `ε/val = 0, ¼, ½, ¾, 0.9, 1, 1.1` for `J = ½, h = 0, β = c = 1`, `n = 10`).
* `f7_zeroT_limit.py`: zero-temperature limit of `E_π e^Λ`.
* `f8_product_threshold_check.py`: Theorem B.12(a) by exact vertex enumeration (`n = 3, 4, 5`, five parameter
  sets): the exact worst-case width of the tilted sandwich is `n·max(D(c;θ), D(−c;θ))` to `10⁻⁹`, equal to
  `n·ε₁*` at `θ*` (e.g. `0.113832` against the untilted `0.122459` for `e/c = ½`, `β = 1`).

Known numerical weaknesses: rings of at most 14 (one of 16) sites; maxima over `t` by grid plus golden section
(unimodality of `V_n(t)` was observed, not proved); LP values in floating point (HiGHS tolerances `≈ 10⁻⁷`); the
transfer operator for `U_β` loses accuracy for `βJ ≳ 4` (two values at `β = 4` in `out_f7_zeroT_limit.txt` are
visibly wrong and were not used).

---

## 4. Prior art and search log

*Known, and used.*  Type covering (Csiszár–Körner, Lemma 9.1); rate–distortion theory of stationary sources and
the monotonicity `R^{(L)} ≥ R` (Gallager 1968; Berger 1971); Csiszár's dual; Merhav (2011) for the finite-temperature
deterministic exponent — all as in the theory report.  Minimum cost-to-time ratio cycles (Dantzig–Blattner–Rao;
Lawler) for §2.1.  Joint spectral radius (Rota–Strang; Jungers' monograph) for Proposition B.3 — cited from memory.

*Known, and coinciding with part of §2.4.*
* R. M. Gray, "Information rates of autoregressive processes" (IEEE-IT 1970) and "Rate distortion functions for
  finite-state finite-alphabet Markov sources" (IEEE-IT 17, 1971, 127–134): the Shannon lower bound of a Markov
  source is exact below a critical distortion; for the binary symmetric Markov source
  `D_c = ½(1 − (1 − (q/p)²)^{1/2})`.  **Not read**; the 1971 reference was confirmed through the reference list of
  Krishnamachari (2026); the formula is from memory and coincides with my independent derivation (Theorem B.6 at
  `h = 0`).
* T. Berger, "Explicit bounds to R(D) for a binary symmetric Markov source" (IEEE-IT 1977): bounds above `D_c`;
  the function itself is still unknown.  Read: search-result summary only.
* F. Avram and T. Berger, "On critical distortion for Markov sources" (IEEE-IT 1985): lower bounds on the critical
  distortion of general Markov sources.  Read: one-line summary only (authorship from a bibliographic index).
* B. Hajek and T. Berger, "A decomposition theorem for binary Markov random fields", Ann. Probab. 15 (1987)
  1112–1125, and C. M. Newman, "Decomposition of binary random fields and zeros of partition functions", ibid.
  1126–1130: a binary Markov random field is the mod-2 sum of a field and independent white noise of positive
  weight, which gives the exact rate–distortion function at small distortion; the critical weight `δ_c` is related
  to zero-free regions of the partition function.  Read: abstracts (through search summaries; Project Euclid pages
  could not be fetched).  Theorem B.6(a)–(b) is this decomposition for the chain; I do not know whether the closed
  form `cosh(ct/2) ≥ e^{2Jt}cosh(ht)` for the chain in a field is written there.
* S. Jalali and T. Weissman, "New bounds on the rate-distortion function of a binary Markov source" (ISIT 2007):
  bibliographic record only.
* B. Krishnamachari, "A block hierarchy for rate-distortion and dispersion of binary Markov sources",
  arXiv:2603.07435 (2026): block-memoryless approximations of one binary Markov source.  Read: abstract and an
  automatic summary of the HTML.  The blocking device of Theorem B.2 is the same classical one; the statement there
  is about one source at a fixed distortion, not about the supremum over sources with an energy-tied budget.
* A. Kontorovich and K. Ramanan (Ann. Probab. 2008), K. Marton (1996): concentration for Markov chains by the
  martingale/coupling method with constants `1/(1−θ)` — upper bounds on the Jensen gap, not sharp (§2.6).  Read:
  search summary.
* Hidden Markov entropy rates and the random-field Ising chain (Derrida–Hilhorst 1983; Zuk–Kanter–Domany 2005),
  magnitude and maximum diversity (Leinster; Leinster–Meckes): cited from memory as context for Proposition B.8 and
  for the "magnitude" remark; not searched.

*Concurrent internal work.*  The theory report in the repository was revised during this workstream
(read-only check at the end): it now contains, attributed to workstream A, (i) the remark that the zero residual
is not the worst additive instance, with the values `0.11367` and `0.11383` at site difference `−0.037c` (the
same numbers as in §2.6, found independently here); (ii) an instance-wise threshold `ε₁^thr = min_Q γ(Q)` through
a sandwich with a second, instance-dependent reference `Q*` (with a hint); (iii) the refutation of dip
extremality for sites with three or more states (D38).  Not there, as far as I can see: the closed form
(chord gap / second difference of the pressure), the identity `min_θ max(D(c;θ), D(−c;θ)) = max_θ G(θ)` and with
it the hint-free worst-case threshold (their open item §12.2(c)), anything on chains, and Conjecture B.13.
Because of (iii), everything in §§2.5–2.6 is stated for two-state alphabets; for `k ≥ 3` the dip exponent and
the chord-gap threshold are lower bounds only.

*Not found* (seven searches, see the log): the droplet / ratio-cycle criterion for one-evaluation certification;
the exponent theorem with a budget tied to the excitation energy; "pressure minus joint spectral radius" as the
dual of a covering exponent; the chord-gap threshold (Theorems B.10–B.12); extremality of additive residuals for
pairwise binary measures (Conjecture B.13).  The absence of a match after a short search is weak evidence.

*Search log* (all on 2026-11-24; "standard" web search).
1. `Hajek Berger "A decomposition theorem for binary Markov random fields" rate-distortion Ising white noise modulo 2 sum` → the two Annals of Probability papers (abstract-level summary).
2. `Gray 1970 binary symmetric Markov source rate distortion critical distortion D_c Shannon lower bound tight; Berger 1977 explicit bounds; Jalali Weissman new bounds` → Berger 1977 abstract; statement that the function is still open.
3. `Newman "Decomposition of binary random fields and zeros of partition functions" Annals of Probability 1987 Lee-Yang` → abstract-level summary.
4. `Hajek Berger decomposition theorem … critical weight "δ_c" explicit formula Gray … "critical distortion"` → Avram–Berger 1985; Krishnamachari 2026.
5. `Jalali Weissman "New bounds on the rate-distortion function of a binary Markov source" ISIT 2007 …` → bibliographic record.
6. `"critical distortion" binary Markov source asymmetric transition probabilities explicit formula …` → no explicit asymmetric formula found.
7. `exact worst-case Laplace transform Lipschitz function Hamming distance Ising model Markov chain extremal function additive magnetization …` → Kontorovich–Ramanan; Bobkov–Houdré–Tetali (subgaussian constant); nothing on exact extremal functions.
Fetches: Project Euclid pages of Hajek–Berger and Newman (empty); arXiv:2603.07435 abstract and HTML (summaries);
arXiv cs/0610143 (turned out to be Sahai–Mitter on unstable processes — irrelevant).

---

## 5. What is not settled

1. **Theorem B.2 is [T*].**  The proof is complete modulo two textbook lemmas (Appendix C has the one step that
   is not in the textbooks), but it has not been refereed or machine-checked.  The finite-temperature analogues
   (Theorem B.9, rows 2–3) are stated with less detail: the upper bound for the deterministic exponent is only
   the remark that Merhav's construction can be run on block types.
2. **No formula for `R*` in the non-positive regime** (`c < c_pos`), in particular in the window
   `2h < c ≤ 2(J+h)` and for small `c/J`.  Known: rigorous brackets (§2.3), the scaling `Θ(c/J)` at `h = 0`,
   constants `0.0549 ≤ R* ≤ 0.0866` at `c = J`.  The limit constant `κ = lim R*·J/c` (a continuum problem: cover
   telegraph signals within an `L¹` distance equal to the number of jumps) is between `0.0035` and `0.0866`
   rigorously and probably near `0.06`.  The quadratic law of Remark B.2″ is heuristic.
3. **Exactness of the Boltzmann formula for `8.23 ≤ c/J < 9.08`** (`h = 0`) and for `c ≥ c_pos(h)`, `h > 0`: needs
   `V(t) ≤ B(t*)` in the non-positive range of `t`; my domination argument is too crude there.  Unimodality of
   `t ↦ V(t)` would settle it; it was observed in every computation.
4. **Conjecture B.13** (additive extremality) — and with it the upper half of the threshold on chains and the
   exact worst-case free-energy gap of a chain reference.  Exact evidence stops at `n = 5`.
5. **The randomised exponent itself** on chains (as on product spaces): the bracket
   `R^rand_β ≤ exponent ≤ min(R_β, U_β)` is wide (`0.03` against `0.34` at `βJ = ½`, `βc = 1`); on the cube the
   lower end is the truth by Harper's theorem; an isoperimetric statement for Gibbs chains is missing.
6. **Instance-wise thresholds.**  Theorem B.12 is about the class (worst instance `θ*M`).  At the zero residual
   with `e ≠ 0`, accuracies between `G(0)` and `ε₁*` are neither excluded by dips nor reached by the tilted
   sandwich with a guarantee on that instance alone.
7. **`k > 2` states and inhomogeneous chains** for §§2.4–2.6: the deconvolution criterion becomes an invariant
   cone problem in `ℝ^k` (no closed form expected); the threshold becomes a chord gap over a polytope of slopes,
   and single dips are no longer extremal even for independent sites (D38 of the updated dead-ends list), so the
   finite-temperature statements here are lower bounds only for `k ≥ 3`.
8. **Two dimensions.**  Everything in §2.1 has an obvious analogue (droplets with perimeter cost), but the low
   shell of Theorem B.2 and the sharpness criterion change character when the ground state is ordered
   (`τ` is then the bulk field again, while domain walls cost perimeter, not `O(1)`).

---

## 6. The three most promising next steps

1. **Prove (or refute at `n = 6`) Conjecture B.13.**  It is the cleanest statement found here, it is about the
   report's open item 5, and it would turn Theorem B.12 into a sharp threshold theorem for chains (and trees) with
   a two-line transfer-matrix formula, `ε₁* = max chord gap of the pressure over the fields h ± c/2`.  Routes:
   (i) the exact recursion `Φ_n(g) = Φ_{n−1}(ĝ) + E ln ψ(p(y_{n−1}), βΔ_n)` obtained by integrating out a leaf, with
   an inductive class for `ĝ`; (ii) the Hubbard–Stratonovich representation of a pairwise measure as a mixture of
   product measures (the three-body counterexample shows that pairwise structure must enter); (iii) exact
   enumeration at `n = 6` by a layered search over the `3.3·10¹⁰` homomorphisms `Q₆ → ℤ` with pruning.
   Independently of the conjecture, **Theorem B.12 should go into the theory report**: it replaces the cube-only
   worst-case threshold by one for all identical two-state product landscapes, with the tilted reference as the
   (hint-free) algorithm and the tilted additive instance as the lower bound, and it answers the open item
   §12.2(c) of the updated report for two-state sites.  Its proof is ten lines on top of Theorems 11.21 and
   11.24 and is a natural candidate for machine-checking (`f8_product_threshold_check.py` is the harness test).
2. **Machine-check the one-shot statements**: Theorem B.1(a),(c) (droplet criterion and the cell bound — a direct
   application of `card_ge_exp_weights`), Theorem B.5 (an elementary inequality), Proposition B.3 (the
   matrix-product form of the exponential-weights bound) and the product half of B.6(a).  Then write Theorem B.2
   out in full; the result is the "step beyond product landscapes" both referees asked for, and the vacuous window
   (Theorem B.5) is the honest correction to blueprint §6.6 Step 2: for a chain the planning estimate must not use
   Boltzmann weights unless `c ≳ 8J`.
3. **The weak-envelope constant and better primal constructions.**  Compute `κ = lim_{c/J→0} R* J/c` (continuum
   telegraph covering), and replace the grid quantiser by entropy-coded wall positions; on the dual side optimise
   matrix-product weights of bond dimension `≤ 16` with a certified JSR bound (invariant polytope algorithm).
   This would give a usable planning formula for chains in the regime that matters in the application (envelope
   constant small compared with the couplings), where today only the bracket `[0.055, 0.087]·(c/J)` at `c = J` is
   available.

---

## Appendix A. Dead ends and negative results (for `DEAD_ENDS.md`, if adopted)

* **B-D1.** "For two-state chains with zero residual the Boltzmann (transfer-matrix) weights are optimal, as for
  two-state sites" — false below `c ≈ 8.23J` (`h = 0`); vacuous for `2h < c ≤ 2(J+h)`; never optimal at any slope
  for `c ≤ 4J`.
* **B-D2.** "The optimal dual weights are Markov / of renewal form / a finite matrix product" — refuted
  numerically (order dependence of run weights; non-terminating Schmidt spectrum).
* **B-D3.** "Run-length-limited weights with the max-operator bound on the joint spectral radius" — gives nothing
  (never beats Boltzmann); the weights are fine, the JSR bound is not; enumeration of words is needed.
* **B-D4.** "The dip threshold is the single-centre game value because one mixed centre covers" — the maximiser is
  a zero-entropy law for which the packing bound is 2; correct only as a limit of block processes.
* **B-D5.** "The zero residual is the hardest instance for the accuracy threshold" (implicit in the `ε₁^crit` of
  the version of the report I was given; the updated report corrects it independently) — false without spin-flip
  symmetry; the hardest additive instance is `θ*M` and the matching hint-free reference is `π_{θ*}`.
* **B-D6.** "Additive extremality follows from a one-dimensional monotone rearrangement" — false (tent beats the
  identity for a three-atom law); "it follows from the martingale method" — the martingale bound is not sharp.
* **B-D7.** Chebyshev discretisation of the projective transfer operator in the coordinate `p` — fails at low
  temperature; the log-odds coordinate on the invariant interval works.
* **B-D8.** A closed form for the exponent in the non-positive regime — not found; tied to Gray's open problem.

## Appendix B. Files

`chainlib.py` (library) · `z1_sharpness.py` · `z2_tables.py`, `z2b_tables.py` · `z3_structure.py` · `z4_positivity.py`
· `z5_rank.py` · `z6_ncov.py` · `z7_rll.py`, `z7b_probe.py`, `z7c_rll_table.py` · `z8_free_brackets.py` ·
`z9_phase.py` · `z10_grid_cover.py` · `f1_softgap.py` · `softgap_ops.py` · `f2_exponents.py` · `f3_jensen.py` ·
`f4_jensen_classes.py` · `f4b_adversarial.py` · `f5_threshold.py` · `f6_class_threshold.py` · `f7_zeroT_limit.py` ·
`f8_product_threshold_check.py`;
outputs `out_<script>.txt` (and `out_z2b_h0_c16_n16.txt` for the single `n = 16` row; `out_z2_tables_n12.txt` is an
earlier, superseded run); `cache/` holds the orbit/distance tensors; `untrusted_pdf1/` holds one fetched PDF that
turned out to be irrelevant.

## Appendix C. Step (iii) of Theorem B.2

**Lemma C.1.**  Let `P` be a law on `B = σ^L`, `s_L` the block-additive distortion, and `ν_P` the stationary process
obtained from i.i.d. blocks with law `P` by a uniformly random phase.  Then `R(P; s_L, LD) ≤ L·R_{ν_P}(D)` for
every `D ≥ 0`.

*Proof.*  Let `(Y^N, A^N)` attain the `N`-th order rate–distortion function of `ν_P` at level `D`, and let
`Φ ∈ {0,…,L−1}` be the phase.  `I(Y^N; A^N | Φ) ≤ I(Y^N, Φ; A^N) ≤ I(Y^N; A^N) + H(Φ)`, so
`I(Y^N; A^N) ≥ I(Y^N; A^N | Φ) − ln L`.  Given `Φ = φ`, `Y^N` contains `m_φ ≥ ⌊N/L⌋ − 1 =: m` complete blocks
`B₁,…,B_{m_φ}`, i.i.d. with law `P`; with `Â_j` the part of `A^N` aligned with `B_j` and
`d_{j,φ} = E[s_L(Â_j, B_j) | Φ = φ]`,

    I(Y^N; A^N | Φ = φ) ≥ Σ_j I(B_j; Â_j | Φ = φ) ≥ Σ_j R(P; s_L, d_{j,φ}) ≥ m · R(P; s_L, N D_φ / m),

by independence of the blocks, the definition of `R(P; ·)`, and its convexity and monotonicity
(`N D_φ := E[s(A^N,Y^N) | Φ = φ] ≥ Σ_j d_{j,φ}`).  Averaging over `φ` and using convexity once more,
`I(Y^N; A^N) ≥ m·R(P; s_L, ND/m) − ln L`.  Divide by `N` and let `N → ∞`: `m/N → 1/L`, `ND/m ↓ LD`, and
`R(P; s_L, ·)` is continuous on `[0, ∞)` (convex on `(0,∞)`; at `0` by Fano's inequality, since `s₁ > 0` off the
diagonal). ∎

The other two estimates used in (iii) are `e(ν_P) = L⁻¹[E_P F + E_{P⊗P} ψ(last, first)] − e₀ ≤ (E_P[G] + ‖ψ‖)/L` and
`gap_n(y) ≥ Σ_j F(b_j) − m‖ψ‖ − (tail) − (n e₀ + C) = m(E_P[G] − ‖ψ‖) − C′` (with `ψ` normalised so that
`0 ≤ ψ ≤ ‖ψ‖`).
