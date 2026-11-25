# Workstream X — is worst-case envelope uncertainty the right model?

Science division, MetricChain.  Author: independent researcher, workstream X.  Written
2026-11-25.  All scripts, raw outputs and the running notes are in
`experiments/science/ws_X/` (`NOTES.md` is the log).  Labels: **[V]** machine-checked (the Lean
declaration is named), **[P]** paper proof given here, **[K]** known and cited (reading level
given in §4), **[N]** numerical evidence only, **[C]** conjecture, **[H]** heuristic.  Nothing in
this report is machine-checked by me; the only **[V]** statements are the theory division's,
quoted with their declaration names.  *Independent review* means I read and re-derived;
*independent replication* means I re-computed with my own code — I say which.

---

## 1. Verdicts

**The first-order envelope is the wrong class for the non-sharp part of a residual, the right
one for the sharp part, and "worst case versus Bayesian" is not the distinction that matters
most.**  The theory division's exponential price comes from the *geometry* of the class — a
Lipschitz polytope, in which information from evaluations combines by a minimum ("tropical")
— not from the worst-case quantifier.  Replace the polytope by an *ellipsoid* (the ball of a
reproducing-kernel Hilbert space; equivalently, in its Bayesian reading, a Gaussian prior) and
information combines linearly; the uncertainty left at a configuration after evaluating a set
`A` is `B·P_A(x)`, a number that does not depend on the data, and for kernels on the cube
`{0,1}ⁿ` whose Walsh ("ANOVA") spectrum is concentrated on bounded interaction orders it can be
made small with polynomially many evaluations, with a deterministic guarantee.  I prove a
two-sided statement (Theorem 3, Corollary 4): the number of evaluations needed to certify
`min(f+g)` over such an ellipsoid is, up to explicit polynomial factors, the number `M(η)` of
Walsh modes needed to capture all but `η²` of the spectral mass; it is polynomial in `n` **iff**
the interaction-order quantiles of the spectrum are bounded, and otherwise it is exponential
with exponent the binary entropy of the order quantile — for the brief's product covariance
`σ²ρ^{d_H}` with fixed `ρ` the exponent is `h((1−ρ)/2)`, and the polynomial regime is
`ρ = 1 − O(1/n)`.  For `ln Z` the exact interval of values consistent with the data is a
variational formula (Theorem 5), and `ln Z` is strictly cheaper than the minimum: the worst
member of an order-2 ellipsoid is a Curie–Weiss ferromagnet and contributes `O(1)` to `ln Z`
below its critical temperature although it contributes `Θ(n)` to the minimum.  The Bayesian
twin (Theorem 6) has the same designs, a band `z_δ·P_A` instead of `B·P_A`, and one genuinely
probabilistic gain: unlearnable high-order components *self-average* in `ln Z`, so the clean
conjecture "polynomial iff the spectrum decays" is **false** for the value of `ln Z` under a
prior (Proposition 7: a white-noise component of fixed variance costs `O(n)` evaluations in
the annealed regime and essentially `2ⁿ` in the frozen one).  **Negative findings, equally
important:** (i) in the *sharp* regime the envelope paradigm is cheaper than any kernel
paradigm (1 evaluation against about `n`; numerics §3.3), and at the sizes that can be
enumerated (`n ≤ 12`) with oracle-tight envelope constants the two paradigms cost about the
same — the separation is asymptotic, or needs a safety factor on the constants, which every
certified envelope has; (ii) no paradigm can be cheap on a benign subclass *and* remain valid
on the first-order class: that is exactly what the theory division's instance-wise lower
bounds say when read in the other direction (Proposition 8(c), "no free hedging"), so the
assumption that replaces the envelope cannot be verified from polynomially many evaluations
— it has to come from physics; (iii) a Bayesian certificate fails silently on a dip (coverage
9 % on instances that have one, §3.5), a goodness-of-fit test on the same evaluations does not
see it, and conformal recalibration over a population restores marginal coverage only;
(iv) an adversarial remainder that is merely small in the supremum norm is *amplified* by a
regression design (Lebesgue constant up to about `√M`), where a random remainder is averaged
down by `√(M/N)`.  For interacting known parts (direction 3) I define the **LP-funnel slope**
`τ_LP ≤ τ` (Theorem 9): one evaluation certifies `min(f+g)` iff the envelope is below the
funnel slope `τ` (theory division), and the proof of that fact is a polynomial-size dual
certificate, checkable by the existing kernel, exactly when the envelope is below `τ_LP`;
`τ_LP = τ` on trees and for ferromagnetic binary known parts, and fails to equal `τ` in about
half of frustrated instances.  **Recommendation: combine** — keep the envelope/sharpness
machinery for the part of the landscape where the known part dominates, replace the
first-order class for the remainder by a linear-information class (ellipsoid or Gaussian
prior over body-ordered, type-shared features — the form machine-learned interatomic
potentials already have), bound what is outside the class in the supremum norm (an accuracy
floor) and never in a first-order envelope (which brings the exponential price back at any
size of the constant), and state the guarantee as what it is: class-relative or
prior-relative.  Almost every mathematical ingredient here is known in information-based
complexity, kernel interpolation, design of experiments or spin-glass theory; what I did not
find in print is their assembly for the two targets `min` and `ln Z` next to a known part,
with matching lower bounds and a head-to-head comparison with the envelope paradigm.

---

## 2. Statements and proofs

### 2.0 Setting and notation

`X` finite; `f : X → ℝ` known; `g` unknown, observed only through evaluations; targets
`m(g) = min_x (f+g)(x)` and `ℓ_β(g) = ln Σ_x μ(x) e^{−β(f+g)(x)}` for a fixed reference measure
`μ` (counting or uniform).  `π_h ∝ μ e^{−βh}` denotes the Gibbs measure of an energy `h`.

*Kernel classes.*  `K` a symmetric positive semidefinite kernel on `X`, `H_K` its reproducing
kernel Hilbert space, `𝔹(K,B) = {g : ‖g‖_K ≤ B}` the **ball** (an ellipsoid in `ℝ^X`), and
`GP(0,K)` the centred Gaussian field with covariance `K` (the **prior**).  For `A ⊂ X` and data
`y = g|_A`:

    ĝ_A = K_{·A} K_AA⁺ y            (minimum-norm interpolant = posterior mean),
    K_A = K − K_{·A} K_AA⁺ K_{A·}    (conditional kernel = posterior covariance),
    P_A(x) = K_A(x,x)^{1/2}          (power function = posterior standard deviation),
    B_A = (B² − yᵀK_AA⁺y)^{1/2}      (what is left of the radius).

*The cube.*  `X = 𝔽₂ⁿ`, characters `χ_S(x) = (−1)^{Σ_{i∈S} x_i}`, `g = Σ_S ĝ_S χ_S`.  A **spectrum** is
`v : 2^{[n]} → [0,∞)`; it defines the translation-invariant kernel
`K_v(x,y) = Σ_S v_S χ_S(x ⊕ y)`, for which `‖g‖²_v = Σ_S ĝ_S²/v_S` and the prior has independent
coefficients `ĝ_S ~ N(0, v_S)`.  `σ² = Σ_S v_S = K(x,x)`.  The spectrum is *isotropic* if `v_S`
depends on `|S|` only; then `σ_m² = C(n,m) v_m` is the variance carried by interaction order
`m`, and `τ_m² = Σ_{j>m} σ_j²` is the tail beyond order `m`.  Eigenvalue tail:
`T(N) =` the sum of all but the `N` largest values `v_S`; `M(η) = min{M : T(M) ≤ η²}` is the
number of modes needed for tolerance `η`.

*Two remarks that fix the relation to the brief.*  (a) **[P, immediate]** The brief's product
covariance `K(x,y) = σ² ρ^{d_H(x,y)}` is `K_v` with `v_S = σ² a^{n−|S|} b^{|S|}`, `a = (1+ρ)/2`,
`b = (1−ρ)/2` (the 2×2 matrix `[[1,ρ],[ρ,1]]` has eigenvalues `1 ± ρ` on `(1, ±1)`); so the
variance carried by order `m` is `σ²·Binomial(n, b)(m)`.  With general site parameters `ρ_i`
it is the kernel with the product weights `γ_i = (1−ρ_i)/(1+ρ_i)` of information-based
complexity.  For fixed `ρ < 1` the typical interaction order is `n(1−ρ)/2` — extensive.
(b) The theory division's class that is linear in `p` features with coefficients in a box
(theory report Theorem 11.47, `linRes_span_upper` **[V]**) is the `ℓ^∞` sibling of `𝔹(K,B)`:
there the bracket is the weighted `ℓ¹` distance of the feature vector to the span of the
evaluated ones, here it is `B_A P_A`, the `ℓ²` distance in the dual norm.  Both are *linear
information* classes; the first-order class is not.

### 2.1 The certificate for a ball, instance by instance

**Theorem 1 (hypercircle certificate) [(a) K; (b)–(d) P, verified numerically in §3.1].**
Let `g ∈ 𝔹(K,B)` be evaluated on `A`.
(a) The set of members of the ball that agree with the data is `ĝ_A + 𝔹(K_A, B_A)`, and for
every `x` the set of their values at `x` is exactly `[ĝ_A(x) − B_A P_A(x), ĝ_A(x) + B_A P_A(x)]`.
(b) *Minimum.*  The smallest value of `m(g′)` over consistent `g′` is exactly

    LB_A = min_x [ f(x) + ĝ_A(x) − B_A P_A(x) ],

and `m(g) ≤ UB_A := min_{a∈A} (f+g)(a)`; also `m(g′) ≤ min_x [f + ĝ_A + B_A P_A]` for all
consistent `g′`, so the consistent values of the minimum have width at most `2 B_A max_x P_A(x)`.
(c) *Instance-wise complexity.*  If a deterministic algorithm (adaptive or not) returns
`m(g′)` within `ε/2` for every `g′ ∈ 𝔹(K,B)`, then the set `A` it evaluates on `g` satisfies
`LB_A ≥ m(g) − ε`.  Conversely, if `A` satisfies this and contains a minimiser of `f+g`, then
`UB_A − LB_A ≤ ε`, and "evaluate `A`; if the data agree with those of `g` return the midpoint,
otherwise evaluate everything" is correct on the whole ball and makes `|A|` evaluations on `g`.
(d) *At the zero residual:* `A ∋ argmin f` certifies iff

    B · P_A(x) ≤ gap_f(x) + ε        for every x,       gap_f(x) = f(x) − min f.

*Proof.*  (a) `H_K = span{K(·,a)} ⊕ {r ∈ H_K : r|_A = 0}` orthogonally, the second summand is
`H_{K_A}` with the same norm, `ĝ_A` is the projection of `g` on the first, so
`‖g − ĝ_A‖²_{K_A} = ‖g‖² − ‖ĝ_A‖² ≤ B² − yᵀK_AA⁺y`; evaluation at `x` on the second summand is
represented by `K_A(·,x)`, of norm `P_A(x)`, so `|r(x)| ≤ ‖r‖ P_A(x)` with equality for
`r = ± B_A K_A(·,x)/P_A(x)`.  This is the hypercircle inequality of optimal recovery
(Golomb–Weinberger; Micchelli–Rivlin) and, read with `K` as a covariance, the formula for
posterior mean and variance.  (b) `inf_{g′} min_x = min_x inf_{g′}`, and (a).  (c) The member
`g_x = ĝ_A − B_A K_A(·,x)/P_A(x)` agrees with `g` on `A`, so a deterministic algorithm makes the
same evaluations and returns the same output `o` on both; `|o − m(g)| ≤ ε/2` and
`|o − m(g_x)| ≤ ε/2` give `m(g) − m(g_x) ≤ ε`, and `m(g_x) ≤ f(x) + ĝ_A(x) − B_A P_A(x)`.  The
converse is (b); the fallback algorithm is correct because on any `g′` whose data agree with
those of `g` the certified interval contains `m(g′)`.  (d) At `g = 0`: `ĝ_A = 0`, `B_A = B`,
`UB_A = min f`. ∎

*Reading.*  This is the exact counterpart of the theory division's Theorems 11.4 and 11.23(a)
(`isCertificate_iff_cover`, `instance_query_complexity` **[V]**): there a certificate is a
covering of every `y` within **slack distance** `gap(y) + ε`; here it is a design whose **power
function** is below `(gap + ε)/B`.  The slack distance to a set is the minimum of the slack
distances to its points — evaluations do not combine; the power function of a set is the
distance to the *span* of its representers — they do.  Everything that follows is a
consequence of that one difference.  The algorithm that evaluates the minimiser of the lower
bound `f + ĝ_A − B_A P_A` until `UB_A − LB_A ≤ ε` is the ellipsoid's best-first search
(Piyavskii–Shubert); it is the noise-free GP-UCB/"kernelised optimism" algorithm of the
bandit literature (Srinivas et al.; Bull; de Freitas et al.) with the hypercircle radius, and
is what §3.3 runs.

*A bridge to the machine-checked kernels* **[P]**.  If the spectrum is supported on orders
`≤ 2`, then `f + ĝ_A` is a pairwise model whenever `f` is, so
`m(g) ≥ (certified lower bound of the pairwise model f + ĝ_A) − B_A·max_x P_A(x)`, and the first
term is exactly what the theory division's tropical kernel certifies (`verify_sound` **[V]**).
This is the form of their second-order star sandwich (`verify_sound_secondOrder` **[V]**), with
`B_A max P_A` in place of `Σ c_ij`.

### 2.2 Designs on the cube: how many evaluations make the power function small

**Lemma 2 (aliasing on a linear design) [P; verified numerically to 3·10⁻¹⁴, §3.1; known in
substance: Mitchell–Morris–Ylvisaker 1995].**  Let `C ⊂ 𝔽₂ⁿ` be a linear code and
`A = C^⊥` (a "regular fractional factorial"), `N = |A| = 2ⁿ/|C|`.  For a coset `T + C` of
frequencies put `V_T = Σ_{U∈T+C} v_U` and `κ_T(x) = Σ_{U∈T+C} v_U χ_U(x)`.  Then the data `g|_A`
determine exactly the aliased sums `G_T = Σ_{U∈T+C} ĝ_U`, and

    ĝ_A(x) = Σ_T (G_T/V_T) κ_T(x),      K_A(x,y) = K(x,y) − Σ_T κ_T(x) κ_T(y)/V_T,
    P_A(x)² = Σ_T 4 p_T(x) q_T(x) / (p_T(x) + q_T(x))  ≤  4·NL(C),

where `p_T(x)`, `q_T(x)` are the parts of `V_T` on which `χ_U(x)` is `+1`, `−1`, and
`NL(C) = Σ_T (V_T − max_{U∈T+C} v_U)` is the **non-leader mass**: the spectral mass of all
frequencies except the heaviest one in each alias class.

*Proof.*  For `a ∈ A`, `c ∈ C`: `χ_{U+c}(a) = χ_U(a)`, so `g(a) = Σ_T χ_T(a) G_T`; the `N`
functions `a ↦ χ_T(a)` are the characters of the group `A`, hence the data and `(G_T)` determine
each other.  Under the prior the cosets are independent and within a coset one observes the
sum of independent Gaussians: `E[ĝ_U | G_T] = (v_U/V_T) G_T`, conditional covariance
`diag(v) − vvᵀ/V_T`.  Summing over cosets gives the three formulas; with
`κ_T(x) = ±(p_T − q_T)` and `V_T = p_T + q_T` the diagonal is `V_T − (p_T − q_T)²/V_T = 4p_Tq_T/V_T`.
Finally `4pq/(p+q) ≤ 4 min(p,q)`, and the heaviest frequency of the coset lies in one of the
two groups, so `min(p,q) ≤ V_T − max v`.  (The same formulas hold for the ball by Theorem 1(a),
with no probability.) ∎

**Theorem 3 (two-sided design bounds) [P; verified numerically, §3.1–3.2].**  Let `v` be any
spectrum on `𝔽₂ⁿ` and `p(N) = min_{|A|=N} max_x P_A(x)`.
(a) *Lower bound, every design.*  For every `A` with `|A| = N`:
`max_x P_A(x)² ≥ 2^{−n} Σ_x P_A(x)² ≥ T(N)`.
(b) *BCH designs.*  If `C` has minimum distance at least `2m+1`, then `NL(C) ≤ τ_m² :=
Σ_{|U|>m} v_U`, so `max_x P_A(x)² ≤ 4τ_m²`; with the (shortened) binary BCH code of designed
distance `2m+1` the design has `N ≤ 2^{m⌈log₂(n+1)⌉} ≤ (2n)^m` points (`(n+1)^m` if `n+1` is a
power of two).  In particular, if the spectrum is supported on orders `≤ m`, these `N` evaluations
determine `g` exactly.
(c) *Random linear designs.*  For every `M ≥ 1` and every power of two `N₀` there is a linear
design with at most `N₀` points and

    max_x P_A(x)²  ≤  4 [ T(M) + σ² M / N₀ ].

(d) Consequently, for every `η > 0`,   `M(η) ≤ n_p(η) ≤ 16 (σ²/η²) · M(η/√8)`,   where
`n_p(η) = min{N : p(N) ≤ η}`.

*Proof.*  (a) `K_A = K − R` with `R` positive semidefinite of rank at most `N`; by Weyl's
inequality `λ_i(K_A) ≥ λ_{i+N}(K)`, and the eigenvalues of `K` are `2ⁿ v_S`; so
`tr K_A ≥ 2ⁿ T(N)`.  (b) Two distinct frequencies of weight `≤ m` differ by a word of weight
`≤ 2m`, which is not in `C`; so every coset contains at most one frequency of weight `≤ m`, and
`V_T − max v` is at most the mass of the frequencies of weight `> m` in the coset.  The BCH code
of length `2^r − 1` and designed distance `2m+1` has redundancy at most `mr`; shortening keeps
the distance.  (c) Let `H` be an `r × n` matrix with independent uniform entries, `N₀ = 2^r`,
`C = ker H`, `A` the row space.  Fix a total order on frequencies by decreasing `v`.  A frequency
`U` fails to be the first of its coset iff `H(U ⊕ U′) = 0` for some earlier `U′`, an event of
probability at most `rank(U)/N₀`, `rank(U)` the number of earlier frequencies.  Hence
`E[NL] ≤ Σ_U v_U min(1, rank(U)/N₀) ≤ T(M) + σ² M/N₀`, some `H` does at least as well, and Lemma 2
applies.  (d) Lower bound: (a).  Upper bound: (c) with `M = M(η/√8)` and `N₀` the least power of
two above `8σ²M/η²`. ∎

**Corollary 4 (certifying the minimum over a Walsh ellipsoid: tractability and exponent) [P;
the lower bound in (a) is an instance of a known principle, see below].**
Let `comp(ε)` be the least number of evaluations with which a deterministic algorithm returns
`m(g)` within `ε/2` for every `g ∈ 𝔹(K_v, B)` (worst case over the ball).
(a) For `f ≡ 0`:   `n_p(ε/B) ≤ comp(ε) ≤ n_p(ε/2B)`;  for every `f` the upper bound holds, by
a non-adaptive algorithm (evaluate the design, return `min_x (f + ĝ_A)`), and the lower bound
holds in the gap-weighted form of Theorem 1(d).  With Theorem 3:

    M(ε/B)  ≤  comp(ε)  ≤  64 (Bσ/ε)² · M(ε/(2√8·B)).

(b) *Polynomial iff bounded order.*  Let `v = v^{(n)}` be isotropic and nonincreasing in the
order for every `n`, and `m_θ(n) = min{m : τ_m² ≤ θ²σ²}` the order quantile at relative
tolerance `θ`.  Then for fixed `θ = ε/(Bσ) ∈ (0,1)`

    Σ_{j < m_θ} C(n,j)  <  comp(ε)  ≤  (2n)^{m_{θ/4}},

so `comp` is bounded by a polynomial in `n` for every fixed `θ` **iff** `sup_n m_θ(n) < ∞` for
every `θ`; the degree is between `m_θ − 1` and `m_{θ/4}`.
(c) *Exponent.*  If `m_θ(n)/n → α ≤ ½` for every fixed `θ` (the order distribution
concentrates), then `n⁻¹ ln comp(ε) → h(α) = −α ln α − (1−α) ln(1−α)`.  For the product
covariance `σ²ρ^{d_H}` with fixed `ρ ∈ (0,1)`:

    lim n⁻¹ ln comp(ε) = h((1−ρ)/2)        for every fixed ε/(Bσ) ∈ (0,1),

and the cost is polynomial iff `n(1−ρ)` stays bounded; with `ρ = 1 − 2λ/n` the order
distribution is Poisson(`λ`) in the limit and the degree is a Poisson quantile.
(d) For `ε ≥ 2Bσ` no evaluation is needed.

*Proof.*  (a) Upper bound: Theorem 1(b).  Lower bound: Theorem 1(d) with `gap_f = 0` forces
`B P_A ≤ ε` everywhere on the set evaluated at the zero function.  (b) `M(θσ) > Σ_{j<m_θ} C(n,j)`
because the heaviest modes are the low orders and removing fewer leaves more than `θ²σ²`;
upper bound: Theorem 3(b) with `m = m_{θ/4}`, since then `2B·2τ_m ≤ ε`.  If `m_θ(n_k) → ∞`,
`C(n, m_θ − 1) ≥ (n/(m_θ−1))^{m_θ−1}` is superpolynomial.  (c) `Σ_{j≤αn+o(n)} C(n,j) = e^{n h(α)+o(n)}`
for `α ≤ ½`, and the factor `64(Bσ/ε)²` is a constant.  For the product covariance the order
distribution is `Binomial(n, (1−ρ)/2)`, whose quantiles are `n(1−ρ)/2 + O(√n)`.  (d) `B P_∅ = Bσ`. ∎

*What is known here and what is not* (details in §4).  "Global optimisation is as hard as
uniform approximation on convex symmetric classes" is a classical principle of
information-based complexity (Wasilkowski 1984; Novak 1988); (a) is that principle with the
constant 2.  The aliasing structure of Lemma 2 is in the design-of-experiments literature
(Mitchell–Morris–Ylvisaker 1995), and bounds of the type of Theorem 3(b) are the `𝔽₂`
counterpart of lattice algorithms for approximation in weighted Korobov/Walsh spaces
(Kuo–Sloan–Woźniakowski 2006).  Polynomial tractability under finite-order weights is the
theorem of Wasilkowski–Woźniakowski (2004).  I did not find: the two-sided bound of Theorem
3(d) in the supremum norm for arbitrary spectra on `𝔽₂ⁿ` (the random-coding step (c)); the
statement for the minimum next to a known part with the gap-weighted criterion; the exponent
`h((1−ρ)/2)`.  None of this is deep — every step is a few lines once the objects are named.

*How it interpolates between the theory division's two extremes* **[P for the endpoints, H for
the comparison]**.  All variance at order 1: `M = n`, cost `n+1` — their linear class
(Theorem 11.47(c)).  Order at most `m`: cost `≍ n^m`.  Orders up to `αn`: `e^{n h(α)}`.  A flat
spectrum (`α = ½`, the random energy model): `2^{n(1−o(1))}`.  The first-order class is *not*
on this line — it is not an ellipsoid — but its extremal members are: a dip on a Hamming ball
has spectral mass at extensive orders, and to contain a dip of depth 3 an ellipsoid with
bounded effective order needs a radius `10⁹` at `n = 16` where a typical prior draw has norm
`256` and an additive function of the same depth `3.3` (§3.6 **[N]**).  The ellipsoid is cheap
*because* it excludes dips; an ellipsoid large enough to contain the first-order class
inherits every lower bound of the theory division (Proposition 8(b)).

### 2.3 The free energy over a ball: an exact interval, and why it is cheaper than the minimum

**Theorem 5 (consistent interval of `ln Z`) [P; verified numerically on 60 random instances to
`7·10⁻⁷` relative, §3.1].**  In the setting of Theorem 1, let `π̂ = π_{f+ĝ_A}`.  The set of
values `ℓ_β(g′)` over the members `g′` of the ball consistent with the data is the interval
`[ℓ_β(ĝ_A) − L_A, ℓ_β(ĝ_A) + U_A]` with

    U_A = sup_π [ β B_A (πᵀK_Aπ)^{1/2} − KL(π‖π̂) ],        L_A = inf_π [ β B_A (πᵀK_Aπ)^{1/2} + KL(π‖π̂) ],

the supremum and infimum over probability vectors `π` on `X`.  Moreover

    L_A  ≤  β B_A (π̂ᵀK_Aπ̂)^{1/2}  ≤  U_A  ≤  β B_A max_x P_A(x),        U_A ≥ max_x [β B_A P_A(x) + ln π̂(x)].

*Proof.*  For `r ∈ 𝔹(K_A, B_A)`: `ℓ_β(ĝ_A + r) − ℓ_β(ĝ_A) = ln E_π̂ e^{−βr} = sup_π [−β E_π r − KL(π‖π̂)]`
(Gibbs variational principle).  The linear functional `r ↦ E_π r` on `H_{K_A}` has norm
`(πᵀK_Aπ)^{1/2}`.  For `U_A` both operations are suprema and commute.  For `L_A`,
`inf_r sup_π = sup_π inf_r` by Sion's theorem (the function is linear in `r`, concave in `π`,
both domains compact convex), which gives `−L_A = sup_π [−βB_A(πᵀK_Aπ)^{1/2} − KL]`.  The bounds:
`π = π̂` in both; `(πᵀK_Aπ)^{1/2} ≤ Σ_x π(x) P_A(x)` (triangle inequality); point masses. ∎

*Reading.*  The half-width for the minimum is `B_A max_x P_A(x)` — a supremum over
configurations.  For `ln Z` it is `β B_A` times a **Gibbs-averaged** posterior kernel,
`(E_{x,y∼π⊗π} K_A(x,y))^{1/2}`, traded against the entropy cost of concentrating `π`.  The
problem for `U_A` is the maximisation of a convex minus a convex function and has two kinds of
local maxima, a delocalised one (`π` near `π̂`) and a localised one (`π` near a point mass: the
ellipsoid's analogue of a dip); the numerical search of §3.1 found both.  `L_A` is a convex
problem.

**Proposition 5′ (the worst member of an order-2 ellipsoid is a ferromagnet) [lower bound P;
that it is the supremum N, §3.6].**  On the cube with `f ≡ 0`, let the main effects be known
and the remaining class be `{g = Σ_{i<j} ĝ_ij χ_iχ_j : Σ ĝ_ij²/v₂ ≤ B²}` with extensive scaling
`σ₂² = C(n,2)v₂ = n s₂`, `B = b√n`.  The Curie–Weiss member `r = −t Σ_{i<j} χ_iχ_j`,
`t = 2b√s₂/(n−1)`, has norm `B`, so with `J = 2b√s₂`

    U  ≥  ln E_unif exp( (βJ/(n−1)) Σ_{i<j} s_i s_j )  =  { −½ ln(1−βJ) − βJ/2 + o(1),          βJ < 1,
                                                          { n·max_m [βJ m²/2 − I(m)] + O(ln n),  βJ > 1,

`I(m) = ½(1+m)ln(1+m) + ½(1−m)ln(1−m)`, whereas the uncertainty of the *minimum* from the same
class is `B·P = n b√s₂` at every temperature.  Numerically (`n = 8, 10, 12`, seven values of `β`)
no member found by ascent from random, localised and Curie–Weiss starts exceeds the
Curie–Weiss value in the fourth decimal.  *Proof of the inequality.*  `‖r‖² = t² C(n,2)/v₂ = B²`;
the right-hand side is the Curie–Weiss free energy (Hubbard–Stratonovich). ∎

So below the critical temperature of the *worst member of the class*, `n + 1` evaluations
(the main effects) determine `ln Z` to `O(1)` although an extensive pair component is unknown;
above it the `≍ n²` pair coefficients must be learned — still polynomial.  The theory
division's Theorem 11.33 has the same transition for its second-order class (bounded mixed
differences, critical coupling `βc₂n = 4`), with the opposite conclusion above it
(exponential): in their class a droplet can hide, in an ellipsoid of bounded order it cannot.

### 2.4 The Bayesian twin: what a certificate is under a prior

Let `g ~ GP(0,K)` and let `A` be chosen non-adaptively or adaptively (each point a function of
the previous values).  Given the data, `r = g − ĝ_A ~ GP(0,K_A)` — for exact evaluations of a
Gaussian field this holds for adaptively chosen designs as well.  A **Bayesian certificate** is
the triple (prior, design, data) together with an interval whose conditional probability
given the data is at least `1 − δ`; anyone who accepts the prior can recompute it.

**Theorem 6 (credible intervals; variance sandwich; second-moment certificate) [P from
standard tools; coverage and widths measured in §3.4].**  Write `s = max_x P_A(x)`,
`π̂ = π_{f+ĝ_A}`, `a = ln E_π̂ exp(β² P_A²/2) ≤ β²s²/2`, `z_δ = (2 ln(2/δ))^{1/2}`.  Conditionally on
the data:
(i) *Free energy, dimension-free.*  With probability at least `1 − δ`,

    ℓ_β(ĝ_A) − β s z_δ  ≤  ℓ_β(g)  ≤  ℓ_β(ĝ_A) + a + β s z_δ.

(ii) *Minimum.*  With probability at least `1 − δ`,

    min_x [f + ĝ_A − z_X P_A]  ≤  m(g)  ≤  (f+g)(x̂),       z_X = (2 ln(|X|/δ))^{1/2},

`x̂ = argmin(f + ĝ_A)` evaluated in addition (or `≤ (f+ĝ_A)(x̂) + P_A(x̂)(2 ln(1/δ))^{1/2}` without
that evaluation, for `δ` split in two).
(iii) *Variance sandwich.*  With `p*(x) = P(x minimises f+g | data)` and `π̄ = E[π_{f+g} | data]`,

    p*ᵀK_A p*  ≤  Var(m(g) | data)  ≤  Σ_x p*(x) K_A(x,x),
    β² π̄ᵀK_Aπ̄  ≤  Var(ℓ_β(g) | data)  ≤  β² E[π_{f+g}ᵀ K_A π_{f+g} | data].

(iv) *Second-moment certificate.*  With `ν ∝ π̂ e^{β²P_A²/2}` and
`ρ₂ = Σ_{x,y} ν(x)ν(y) e^{β²K_A(x,y)} − 1`, for every `η ∈ (0,1)`,

    | ℓ_β(g) − ℓ_β(ĝ_A) − a |  ≤  −ln(1−η)        with probability at least 1 − ρ₂/η².

*Proof.*  `ℓ_β(g) − ℓ_β(ĝ_A) = ln W`, `W = E_π̂ e^{−βr}`.  (i) `E ln W ≥ −β E_π̂ E r = 0` (Jensen in
`π̂`) and `E ln W ≤ ln EW = a` (Jensen in the prior).  As a function of the standard Gaussian
vector `ξ` with `r = K_A^{1/2}ξ`, `ln W` has gradient `−βK_A^{1/2}π_{f+g}` of norm at most `βs`, so
it deviates from its mean by more than `t` with probability at most `2e^{−t²/2β²s²}`
(Tsirelson–Ibragimov–Sudakov).  (ii) Union bound over `X` for the lower end; the upper end is
an evaluated energy.  (iii) Upper bounds: Gaussian Poincaré inequality with the gradients
`e_{x*}` and `−βπ_{f+g}`.  Lower bounds: Bessel's inequality for the first Wiener chaos,
`Var F(ξ) ≥ |E ∇F|²`, with `E∇` equal to `K_A^{1/2}p*`, `−βK_A^{1/2}π̄` (Stein's identity; `m` is
Lipschitz).  (iv) `EW = e^a`, `EW² = e^{2a}(1+ρ₂)`, Chebyshev. ∎

*Reading.*  (a) The Bayesian band is `z_δ P_A` where the ball's is `B_A P_A`.  For a ball to
contain a typical prior draw one needs `B ≈ (rank K)^{1/2}`, so the Bayesian statement is
narrower by the factor `√rank/z_δ` — a polynomial gain on top of the exponential gain of
leaving the first-order class, and the reason why in §3.3 the ball needs all `M` evaluations
where the prior needs fewer.  (b) (i) has no union bound: at fixed `β` the free energy is
`βs`-Lipschitz in the Gaussian coordinates.  The minimum needs `(2 ln |X|)^{1/2}` in general — a
white posterior attains it.  (c) (iii) says exactly what must be learned: the posterior
covariance *as seen by two independent draws* of the minimiser (of the Gibbs measure).
(iii)–(iv) are small when `K_A` is incoherent across the Gibbs ensemble even if `s` is not
small.  That is the next statement.

**Proposition 7 ("polynomial iff the spectrum decays" is false for the value of `ln Z` under a
prior) [P; measured in §3.4].**  Prior on the cube: `g = a₀ + Σ_i a_i χ_i + τ w`, `a_i ~ N(0, v_i)`
independent, `w` white noise with unit variance at every configuration (the random energy
model as a tail: spectral mass `τ²` spread evenly over all `2ⁿ` modes).  Let `A` be an orthogonal
array of strength 2 with `N` points, `s² = Σ_{i=0}^n (N/τ² + 1/v_i)^{−1} ≤ (n+1)τ²/N`.
(a) *Recovery is exponentially expensive:* for every design with `N` points the average
posterior variance is at least `τ²(1 − N/2ⁿ)` (Theorem 3(a)); so is certifying the minimum
within `ε < τ` with the union-bound interval.
(b) *The free energy is not:* for `x, y ∉ A`, `K_A(x,y) = Σ_i σ_i² χ_i(x)χ_i(y) + τ²·1[x = y]` with
`σ_i² = (N/τ² + 1/v_i)^{−1}`, hence

    ρ₂  ≤  (e^{β²s²} − 1)  +  e^{β²(s²+τ²)} · e^{−H₂(π̂)} / (1 − π̂(A))²,       H₂(π̂) = −ln Σ_x π̂(x)².

So `N ≥ 2(n+1)β²τ²/(δη²)` evaluations certify `ℓ_β(g)` within `−ln(1−η)` with probability `1−δ`
whenever the Rényi entropy of the *known* Gibbs measure satisfies
`H₂(π̂) ≥ β²τ² + 1 + ln(4/δη²)` — linear in `n` although no tail of the spectrum is small.
(c) *In the frozen regime nothing short of enumeration helps* **[H + N]**: for the pure
random energy model (`a ≡ 0`, `f ≡ 0`) with `β > β_c = (2n ln 2)^{1/2}/τ` the unevaluated
configurations contain the configuration of largest weight with probability `1 − N/2ⁿ`, and
the heuristic extreme-value estimate is `N ≳ 2ⁿ(1 − ε^{β_c/β})` for accuracy `ε`; the measured
posterior spread of `ln Z` is of order `β·τ·`const at every design size tried (§3.4).

*Proof of (b).*  With `XᵀX = N·I` the posterior covariance of `(a_i)` is diagonal with entries
`σ_i²`; the white component at unevaluated points is independent of the data.  For `x ≠ y`
outside `A`, `K_A(x,y) ≤ s²`; on the diagonal `K_A = s² + τ²` off `A` and `0` on `A`; and
`ν(x) ≤ π̂(x)/(1 − π̂(A))` off `A`.  Insert in Theorem 6(iv). ∎

*What this means.*  Under a prior there are **three** kinds of residual component, not two:
*learnable* (few coefficients: must be evaluated), *unlearnable but self-averaging* (many
incoherent coefficients: the prior alone predicts their contribution to `ln Z`, `β²τ²/2`, and
no evaluation is needed), and *unlearnable and frozen* (the Gibbs measure concentrates on
their extremes: exponential cost).  The theory division's worst-case classes have only the
first and the third.  The second is real physics (annealed averages) — and it is also the
part of a Bayesian guarantee that rests most heavily on the prior, because it is certified
*without any data about it*.

### 2.5 Robustness: what each guarantee is worth when its assumption fails

**Proposition 8 [P].**
(a) *A remainder bounded in the supremum norm costs a floor, amplified by the design.*  If
`g = g₀ + h` with `g₀ ∈ 𝔹(K,B)` and `‖h‖_∞ ≤ η`, then for every design, with
`Λ_A(x) = Σ_a |λ_a(x)|` the Lebesgue function of the interpolation weights
(`ĝ_A(x) = Σ_a λ_a(x) y_a`),

    | g(x) − ĝ_A[g](x) |  ≤  B P_A(x) + η (1 + Λ_A(x)),

so the minimum is known within `B max P_A + η(1 + max Λ_A)` and `ln Z` within `β` times that;
and no algorithm can do better than `η` (the class contains the constants `±η`).  For a
random remainder with independent values of variance `η²` the corresponding term is
`η (1 + Σ_a λ_a(x)²)^{1/2}`.
(b) *A first-order remainder costs the first-order price.*  If a class `𝒢` contains the
first-order class of an envelope `d₀` (in particular `𝒢 = 𝔹(K,B) + Lip(d₀)`), every lower bound
of the theory division for `Lip(d₀)` holds for `𝒢`: Theorems 11.22–11.25 (`exists_query_ne`,
`expected_queries_ge_exp_weights_min`, `thermal_expected_queries_ge` **[V]**) use only
membership of the instance and of its dips in the class.
(c) *No free hedging.*  Let `𝒢₀ ⊂ 𝒢₁` and let an algorithm be `(ε/2, δ)`-correct on `𝒢₁`.  Then at
every instance `g ∈ 𝒢₀` its expected number of evaluations is at least the instance-wise lower
bound of `𝒢₁` at `g`.  With `𝒢₁` the first-order class and `g` the zero residual of the cube:
at least `(1−2δ)` times the fractional covering bound for the minimum (Theorem 11.23(b)) and
exponentially many below the accuracy threshold for `ln Z` (Theorem 11.25) — whatever the
algorithm knows or assumes about `𝒢₀`.  Equivalently: a procedure that uses fewer evaluations
at `g` is wrong, with probability more than `δ`, on some member of `𝒢₁` that it cannot
distinguish from `g`; "assume the benign class, and fall back if the data contradict it" is
not available, because the contradiction itself costs exponentially many evaluations to see.

*Proof.*  (a) `ĝ_A[g] = ĝ_A[g₀] + Σ_a λ_a h(a)`; Theorem 1(a) for `g₀`.  (b), (c): the cited
theorems are stated instance by instance for algorithms correct on the class; (c) is their
contrapositive. ∎

*Reading.*  (a) is the precise sense in which "the residual is not an adversary" matters even
for a tiny remainder: against an adversary the regression weights add up in `ℓ¹`
(`max Λ_A ≈ 0.6–0.9·√M` for the designs of §3.5 **[N]**), against noise in `ℓ²`
(`(M/N)^{1/2}`, exactly, for orthogonal arrays).  (b) is the theory division's own finding for
profile classes (workstream P, Corollary 15) in general form: one cannot be "a little bit
first-order".  (c) answers the brief's sentence *"it is not an adversary" is not a theorem*:
inside the evaluation model it **cannot** become one — any formulation in which
non-adversariality is a consequence of data needs exponentially many data.  The formulations
in which it is a theorem are those in which it is a consequence of *structure known in
advance*: `g ∈ 𝔹(K,B)` (then a dip of depth `D` unseen by `A` is impossible as soon as
`D > B_A P_A`, Theorem 1(a)), or `g` drawn from a prior (then it has probability at most
`2e^{−z²/2}` per configuration).

### 2.6 Funnels with interacting known parts (direction 3)

Let `X = ∏_i X_i`, `f(x) = Σ_i θ_i(x_i) + Σ_{(i,j)∈E} θ_ij(x_i,x_j)` pairwise, `d(x,y) = Σ_i c_i[x_i ≠ y_i]`,
and `x*` a candidate.  The theory division proved (`single_evaluation_certificate_iff` **[V]**):
the single evaluation at `x*` is an `ε`-certificate of `min(f+g)` for every `g` admissible for `d`
iff `min_y [f(y) − d(x*,y)] ≥ f(x*) − ε`; for product landscapes this is "every site is sharp",
for chains the droplet criterion (their Theorems 11.7, 11.39).  The function
`f^t := f − t·d(x*,·)` is again pairwise, with the same pair terms and unaries
`θ_i(s) − t c_i [s ≠ x*_i]`.  Define

    τ(x*)    = sup{ t : min f^t = f(x*) }  =  min_{y≠x*} (f(y) − f(x*)) / d(x*,y)        (funnel slope),
    τ_LP(x*) = sup{ t : LP(f^t) = f(x*) }                                               (LP-funnel slope),

`LP` the local-polytope (pairwise) relaxation.

**Theorem 9 (the sharpness certificate) [P; verified numerically on 1 360 instances, §3.7].**
(a) `τ_LP ≤ τ`, and `{t : LP(f^t) = f(x*)} = (−∞, τ_LP]`.
(b) *Dual form.*  `τ_LP` is the value of one linear programme: the largest `t` for which there
are messages `φ` such that, in the reparametrised model `θ̃ = θ^φ`, every pair term is minimal
at `(x*_i, x*_j)` and every unary term satisfies `θ̃_i(s) − θ̃_i(x*_i) ≥ t c_i` for all `s ≠ x*_i`.
(c) *Certificate.*  If `c ≤ τ_LP` (i.e. `τ_LP ≥ 1` for the given constants; with `ε`: 
`LP(f^1) ≥ f(x*) − ε`), the messages `φ` together with the single value `g(x*)` are a proof,
of size `O(|E|·max_i|X_i|)` and checkable by the reparametrisation rule of the tropical
kernel, that `min(f+g) = (f+g)(x*)` for **every** admissible residual `g`; no evaluation at all
is needed for the configuration certificate.
(d) *When `τ_LP = τ`.*  On trees; for binary submodular (ferromagnetic) pair terms on any
graph; more generally for every family of pair terms that is closed under changes of the
unaries and for which the relaxation is tight (balanced signed graphs after a gauge
transformation; multi-label submodular terms).  In these cases the dichotomy "one evaluation
iff `c ≤ τ`" comes with a polynomial-time decision procedure and a polynomial-size proof.
(e) *In general `τ_LP < τ`*, and `τ_LP < 0 < τ` occurs: the triangle with fields
`h = (−½, 0, −½)` and couplings `J₀₁ = J₁₂ = −1`, `J₀₂ = +1` (energy `Σ h_i s_i + Σ J_ij s_i s_j`) has
a unique ground state, `τ = ½` and `τ_LP = −⅔`.

*Proof.*  (a) `LP(f^t) ≤ min f^t ≤ f^t(x*) = f(x*)`; `t ↦ LP(f^t)` is a minimum of affine functions
of `t`, hence concave, and nonincreasing because `d ≥ 0`; the set where a concave function
attains the upper bound `f(x*)` is an interval, unbounded below because for `t → −∞` the
unaries dominate.  (b) Linear-programming duality for the local polytope:
`LP(θ) = max_φ [Σ_i min_s θ̃_i(s) + Σ_ij min θ̃_ij]`, and the dual value equals `θ(x*)` iff `x*`
attains every local minimum (complementary slackness).  Applied to `f^t`, whose reparametrised
unaries are `θ̃_i(s) − t c_i[s ≠ x*_i]`.  (c) By (b), `f^1(y) ≥ f(x*)` for all `y`, which is the
criterion quoted above; weak duality is what the kernel checks.  (d) On trees the relaxation
is tight for every pairwise model; changing unaries preserves submodularity, for which it is
tight (min-cut); (e) by exhaustive search over triangles with half-integer fields (§3.7). ∎

*Reading and relation to stability notions.*  The funnel condition `τ ≥ 1` says: *`x*` stays
optimal under every unary perturbation of size `c_i` at site `i`* — indeed under every
admissible residual (the theory division's Theorem 2.4).  This is stability under additive
perturbations of the **node** costs.  Bilu–Linial stability, and the `(2,1)`-stability under
which Lang–Sontag–Vijayaraghavan prove the pairwise relaxation exact for ferromagnetic Potts
models, is stability under multiplicative perturbations of the **edge** weights; neither
implies the other.  Theorem 9 is the node-stability counterpart with the weakest possible
conclusion one can ask for (tightness of `f^t`, not of all perturbations), and it is
elementary.  The energy-landscape "funnel" of Bryngelson–Wolynes–Onuchic is a *statistical*
statement (the native gap exceeds the roughness for most competing states); `τ ≥ 1` is the
worst-case version (every droplet), and is much stronger.  What the theorem adds to the
programme: for interacting known parts the sharp regime is not only cheap in evaluations
(one) but has a *short proof* under a checkable condition, and where the known part is
frustrated the proof of sharpness may itself need branching (the kernel's other rules) — in
the numerics for about half of the frustrated instances.

### 2.7 Chains: where finite-order weights can live (direction 2, last question)

**Proposition 10 [the rank statement P and trivial; the rest H, a synthesis of the theory
division's §§11.14, 11.17 in the language of §2.1].**  Consider a chain with `n` torsions
(`k` states each) and residuals `g = g_loc + g_pair`,

    g_loc(x) = Σ_i u_i(x_i, …, x_{i+w−1}),         g_pair(x) = Σ_{p<q} φ_{τ(p,q)}(s_pq(x)),

with arbitrary position-dependent window tables `u_i` and radial functions `φ_τ` in the unit
ball of a kernel space `H_κ` on `[0, S_c]`, shared by all bead pairs of the same type `τ`.  With
weights `γ_i`, `γ_τ` this is the ball of

    K(x,y) = Σ_i γ_i 1[x_{W_i} = y_{W_i}]  +  Σ_τ γ_τ Σ_{(p,q),(p′,q′) of type τ} κ(s_pq(x), s_p′q′(y)),

a sum of a finite-order kernel in torsion coordinates (order `w`, weights depending on the
position `i`) and a two-body kernel in bead coordinates (the form of a two-body Gaussian
approximation potential).  Theorem 1 applies verbatim to any set of evaluated conformations.
If the squared distances below the cutoff take `G` values, `rank K ≤ (n−w+1)k^w + |𝒯|·G`, and
that many generic evaluations determine `g`: polynomial in the chain length, for `min` and
`ln Z`, at every accuracy.

*What can and cannot be said about weights* **[H]**.  (i) In *torsion* coordinates a contact
term has interaction order of the order of the loop length (theory division, §11.14: "about
0.6 times the loop length"), and the lever-arm constants grow; so no class with decaying
product weights *in torsion coordinates* contains tertiary contacts, and no relabelling of
the torsion product space changes that, because the order of a function is invariant under
site-wise relabelling.  (ii) The change of variables that works is not a bijection of the
product space but a passage to over-complete **features** (pair distances, local
environments): there the physically motivated expansion is by body order, with functions
shared across pairs of the same type, and the weights are indexed by (body order, type,
spatial range), not by position along the chain.  Sharing across types is what makes the
number of unknowns independent of the chain length; finite body order is what
information-based complexity calls finite-order weights (polynomial tractability with the
order as exponent, Wasilkowski–Woźniakowski 2004).  (iii) There is a physical theorem of this
form for one family of quantum-mechanical models: body-ordered approximations of
tight-binding site energies converge at rates controlled by the gap and the temperature
(Thomas–Chen–Ortner 2022; I read the abstract only).  Whether a given residual of interest
has a useful norm in such a class is the question of the sibling workstream P of this
division; this report only says which *kind* of class makes the evaluation count polynomial.

---

## 3. Numerics

All runs: Python 3.13, numpy/scipy, single-threaded BLAS (`OMP_NUM_THREADS=1`; the machine was
shared and loaded), seeds fixed in the scripts.  Directory `experiments/science/ws_X/`.
Re-run: `OMP_NUM_THREADS=1 python3 <script>`; each writes `<name>.json` and, where noted, a log.

### 3.1 Formulas (falsification tests) — `n1_coset_formula.py`, `n3_ball_lnz.py`

* Lemma 2: 300 random pairs (spectrum, linear design), `n = 3…8`, three kinds of spectra
  (heavy-tailed, sparse/rank-deficient, isotropic).  The coset covariance vanishes on the
  design and `K − K_A` lies in the span of the columns `K(·,a)` — the two properties that
  characterise the Schur complement — to `2.7·10⁻¹⁴`; `max_x P_A² ≤ 4·NL` in all trials, largest
  ratio observed `3.82` (the constant 4 is essentially attained); `avg_x P_A² ≥ T(N)` in all
  trials, smallest ratio `1.05`.
* BCH designs `(n,m) = (7,1), (6,1), (5,1), (15,1), (15,2), (12,2), (10,2), (7,2), (15,3)`:
  minimum distance `≥ 2m+1` verified by brute force; `N = 8, 8, 8, 16, 256, 256, 256, 64, 1024`;
  `NL ≤ τ_m²` and `max P_A² ≤ 4τ_m²` (observed `1.4–2.0·τ_m²`); zero posterior variance for spectra
  supported on orders `≤ m`.
* Theorem 1 and Theorem 5: 60 random instances (kernel of random rank on 8–32 points, random
  design, `f`, `β`, member of the ball).  Band violations: 0.  Exact lower end of the minimum
  attained by the extremal member: `1.8·10⁻¹⁵`.  `U_A` from a search over functions in the ball
  against `sup_π[…]` from a search over the simplex: relative difference at most `1.8·10⁻⁷`;
  `L_A` (a convex problem on both sides): `7·10⁻⁷`; the chain of inequalities of Theorem 5: 0
  violations.  *One wrinkle, kept on purpose:* in a first run one instance disagreed
  (`1.97` against `3.13`) because random starts found only the delocalised local maximum;
  with localised starts both searches agree.

### 3.2 Spectrum ⇒ exponent — `n7_exponent.py`

Two-sided bounds of Theorem 3(d) for the product covariance, relative tolerance `θ = η/σ`:

| `ρ` | `h((1−ρ)/2)` | `n = 200` (θ = ½) | `n = 2000` (θ = ½) | `n = 2000` (θ = 0.1) |
|---|---|---|---|---|
| 0.5 | 0.5623 | [0.570, 0.625] | [0.567, 0.582] | [0.584, 0.594] |
| 0.9 | 0.1985 | [0.214, 0.287] | [0.206, 0.225] | [0.229, 0.243] |
| 0.99 | 0.0315 | [0.037, 0.090] | [0.035, 0.047] | [0.050, 0.060] |

(entries: bounds on `n⁻¹ ln n_p`; convergence to `h` is from above at rate `O(n^{−1/2})`, as the
binomial quantile predicts).  With `ρ = 1 − 2λ/n`: `n_p = n^{[0.9, 2.4]}` for `(λ, θ) = (0.5, 0.5)` and
`n^{[5.0, 6.8]}` for `(2, 0.1)` at `n = 2000`, the brackets being the orders `M(η)` and `M(η/√8)`
require.  Random linear designs (2 000 codes per cell at `n = 10, 12`; 300 at `n = 14`): the mean
non-leader mass is below the bound `Σ_U v_U min(1, rank(U)/N₀)` of the proof in all 12 cells
(e.g. `0.0355 ± 0.0005` against `0.0409` at `n = 12`, `ρ = 0.9`, `N₀ = 256`).  A first attempt with
20 codes per cell exceeded the bound by Monte Carlo noise — the non-leader mass is
heavy-tailed (a rare code aliases a main effect with the constant).
