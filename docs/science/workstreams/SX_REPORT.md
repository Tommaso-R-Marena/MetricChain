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
`A` is at most `B·P_A(x)`, a bound that does not depend on the data, and for kernels on the cube
`{0,1}ⁿ` whose Walsh ("ANOVA") spectrum is concentrated on bounded interaction orders it can be
made small with polynomially many evaluations, with a deterministic guarantee.  I prove a
two-sided statement (Theorem 3, Corollary 4): the number of evaluations needed to certify
`min(f+g)` over such an ellipsoid is, up to explicit polynomial factors, the number `M(η)` of
Walsh modes needed to capture all but `η²` of the spectral mass; it is polynomial in `n` **iff**
the interaction-order quantiles of the spectrum are bounded, and otherwise it is exponential
with exponent the binary entropy of the order quantile — for the brief's product covariance
`σ²ρ^{d_H}` with fixed `ρ` the exponent is `h((1−ρ)/2)`, and the polynomial regime is
`ρ = 1 − O(1/n)`.  For `ln Z` the exact interval of values consistent with the data is a
variational formula (Theorem 5), and `ln Z` is strictly cheaper than the minimum: over an
order-2 ellipsoid with a uniform reference the unknown pair part changes `ln Z` by at most
`−½ln(1−βJ) − βJ/2 + o(1)` below the critical temperature `βJ = 1` of its worst member, a
Curie–Weiss ferromagnet (Proposition 5′, proved by Gaussian domination), although it changes
the minimum by `Θ(n)`.  The Bayesian twin (Theorem 6) has the same designs, a band `z_δ·P_A` instead of `B·P_A`, and one genuinely
probabilistic gain: unlearnable high-order components *self-average* in `ln Z`, so the clean
conjecture "polynomial iff the spectrum decays" is **false** for the value of `ln Z` under a
prior (Proposition 7: a white-noise component of fixed variance costs `O(n)` evaluations in
the annealed regime and essentially `2ⁿ` in the frozen one).  **Negative findings, equally
important:** (i) in the *sharp* regime the envelope paradigm is cheaper than any kernel
paradigm (1 evaluation against about `n`; numerics §3.3), and at the sizes that can be
enumerated (`n ≤ 12`) with oracle-tight envelope constants the two paradigms are within a
small factor of each other (the smallest envelope covers are 0.4–2.3 times the kernel counts
up to `n = 11`; best-first search up to 6 times at `n = 12`) — the separation is asymptotic,
or needs a safety factor on the constants, which every certified envelope has; (ii) no
paradigm can be cheap on a benign subclass *and* remain valid on the first-order class: that is exactly what the theory division's instance-wise lower
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
`τ_LP = τ` on trees and for ferromagnetic binary known parts, and fails to equal `τ` in
15–95 % of the frustrated instances tried, depending on the strength of the fields.  For
chains: residuals that are local along the sequence, with arbitrary position-dependent
weights, cost a number of evaluations *linear* in the chain length (Corollary 4′); the lever
arm is a property of the first-order format, not of the residual — an energy that is
quadratic in the positions has per-torsion constants that grow along the chain and
interaction order equal to the chain length, yet only `O(n²)` Walsh modes (interval modes;
with rotations, `9n(n+1)/2` features), and on a toy chain with oracle-tight constants the
envelope format evaluates 42 % of the cube at `n = 12` where the ball needs 41–78 points
(Proposition 4″, §3.9); short-range contacts need type-shared, body-ordered features instead
of coordinates (Proposition 10).  A small
by-product fills a cell of the theory division's summary table: in an *additive* class
randomisation reduces the cost at extensive accuracy from `Θ(n)` to a number independent of
`n` (Proposition 11, Monte Carlo over sites).  **Recommendation: combine** — keep the
envelope/sharpness machinery for the part of the landscape where the known part dominates,
replace the
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
every `θ`; the degree is between `m_θ − 1` and `m_{θ/4}`.  (Here and in (c) the lower bounds
are for `f ≡ 0`; the upper bounds hold for every `f`.)
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

**Proposition 5′ (the worst member of an order-2 ellipsoid is a ferromagnet) [(a), (b) P; (a)
tested on 2 752 random instances, §3.6; extremality above the transition N].**  On the cube
with `f ≡ 0` and uniform reference, let the main effects be known (and zero) and the remaining
class be `{g = Σ_{i<j} ĝ_ij χ_iχ_j : Σ ĝ_ij²/v₂ ≤ B²}` with extensive scaling `σ₂² = C(n,2)v₂ = n s₂`,
`B = b√n`; put `J = 2b√s₂`, `F = βJ (n/(n−1))^{1/2}` and `φ(F) = −½ ln(1−F) − F/2`.  With
`s_i = χ_i(x)`, every member has `−βg = ½ sᵀ𝐉s` for a symmetric zero-diagonal matrix `𝐉` with
`‖𝐉‖_F ≤ F`, and `U = sup_𝐉 ln E_unif exp(½ sᵀ𝐉s)`.
(a) *Upper bound in the high-temperature phase of the class.*  If `F < 1`, then for every such
`𝐉`:   `ln E_unif exp(½ sᵀ𝐉s) ≤ −½ ln det(I − 𝐉) ≤ φ(‖𝐉‖_F)`;   hence `U ≤ φ(F)`.
(b) *The Curie–Weiss member* `𝐉 = (βJ/(n−1))(𝟙𝟙ᵀ − I)` has norm `F` and

    ln E_unif exp( (βJ/(n−1)) Σ_{i<j} s_i s_j )  =  { φ(βJ) + o(1),                           βJ < 1,
                                                    { n·max_m [βJ m²/2 − I(m)] + O(ln n),     βJ > 1,

`I(m) = ½(1+m)ln(1+m) + ½(1−m)ln(1−m)`.
The lower end is exact (`L = 0`: the pair functions have mean zero under the uniform measure,
so `ln E e^{−βg} ≥ 0` by Jensen).  So for `βJ < 1` the width of the consistent interval is
`U = φ(βJ) + o(1)` — a constant, attained asymptotically by the ferromagnet — whereas the
uncertainty of the *minimum* from the same class is
`B·P = n b√s₂` at every temperature; for `βJ > 1`, `U` is extensive, and numerically
(`n = 8, 10, 12`, seven values of `β`) no member found by ascent from random, localised and
Curie–Weiss starts exceeds the Curie–Weiss value in the fourth decimal.

*Proof.*  (a) `½ sᵀ𝐉s = Σ_{i<j} 𝐉_ij s_i s_j` is linear in each `s_i` separately because the diagonal
vanishes.  Replace the `s_i` by independent standard Gaussians `γ_i` one at a time: conditionally
on the other variables the exponent is `a·s_i + const`, and `E e^{a s_i} = cosh a ≤ e^{a²/2} = E e^{aγ_i}`.
After `n` steps `E exp(½ sᵀ𝐉s) ≤ E exp(½ γᵀ𝐉γ) = det(I − 𝐉)^{−1/2}` (finite because
`λ_max(𝐉) ≤ ‖𝐉‖_F < 1`).  With the eigenvalues `λ_i` of `𝐉` and `Σ λ_i = tr 𝐉 = 0`:
`−½ ln det(I − 𝐉) = Σ_i φ(λ_i)`; and `φ(λ) = λ² ψ(λ)` with `ψ(λ) = ∫₀¹ u/(2(1−λu)) du` increasing, so
`Σ φ(λ_i) ≤ ψ(λ_max) Σ λ_i² ≤ ψ(F) F² = φ(F)`.  (b) `‖𝐉‖_F² = n(n−1)(βJ/(n−1))² = F²`; the value
is the Curie–Weiss free energy (Hubbard–Stratonovich; for `βJ < 1` the limit is
`E exp(βJ(χ²₁ − 1)/2)`). ∎

*With a field the picture changes at first order.*  If `π̂` is not uniform, Theorem 5 has the
term `β B_A (π̂ᵀK_Aπ̂)^{1/2}`: `β` times the worst-case error, over the ball, of *quadrature* of
the residual against the current Gibbs measure.  For the order-2 ball and a product measure
with magnetisations `m_i` it is `≈ (F/2)·Σ_i m_i²`, extensive.  So a design for `ln Z` should be a
quadrature design for `π̂` (Bayesian quadrature in the sense of O'Hagan, with the prior on the
energy rather than on the integrand), not a sup-norm design; I did not pursue this.

So for a uniform reference, below the critical temperature of the *worst member of the class*
the whole unknown pair component — extensive in the supremum norm — changes `ln Z` by a
bounded amount and need not be evaluated at all; above it the `≍ n²` pair coefficients must
be learned — still polynomial.  The theory division's Theorem 11.33 has the same transition
for its second-order class (bounded mixed differences, critical coupling `βc₂n = 4`), with the
opposite conclusion above it (exponential): in their class a droplet can hide, in an
ellipsoid of bounded order it cannot.

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
posterior variance is at least `τ²(1 − N/2ⁿ)` (Theorem 3(a), every eigenvalue being at least
`τ²/2ⁿ`); hence every certificate that goes through the power function (Theorem 1, Theorem
6(i)–(ii)) has a width of order `τ` unless `N` is a positive fraction of `2ⁿ`.
(b) *The free energy is not:* for `x, y ∉ A`, `K_A(x,y) = Σ_i σ_i² χ_i(x)χ_i(y) + τ²·1[x = y]` with
`σ_i² = (N/τ² + 1/v_i)^{−1}`, hence

    ρ₂  ≤  (e^{β²s²} − 1)  +  e^{β²(s²+τ²)} · e^{−H₂(π̂)} / (1 − π̂(A))²,       H₂(π̂) = −ln Σ_x π̂(x)².

So `N ≥ 4(n+1)β²τ²/(δη²)` evaluations certify `ℓ_β(g)` within `−ln(1−η)` with probability `1−δ`
whenever `π̂(A) ≤ ½` and the Rényi entropy of the *known* Gibbs measure satisfies
`H₂(π̂) ≥ β²τ² + ln(32/δη²)` (then `ρ₂ ≤ 0.45·δη²`) — a number of evaluations linear in `n`
although no tail of the spectrum is small.
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

so the minimum is known within `B max P_A + η(1 + max Λ_A)` and `ln Z` within `β` times that.
A floor of order `η` cannot be removed by more evaluations short of evaluating every
configuration within `η` of the minimum (the spikes `−η·1_{{x}}` are in the class).  For a
random remainder with independent values of variance `η²` the corresponding term has
standard deviation `η (1 + Σ_a λ_a(x)²)^{1/2}`.
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
at `g` is wrong with probability more than `δ` on `g` itself or on one of the dips around `g`,
which it does not tell apart from `g`; "assume the benign class, and fall back if the data
contradict it" is not available, because the contradiction itself costs exponentially many
evaluations to see.

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

**Theorem 9 (the sharpness certificate) [P; verified numerically on 1 280 instances, §3.7].**
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
(e) *In general `τ_LP < τ`.*  The triangle with couplings `J₀₁ = J₁₂ = −1`, `J₀₂ = +1` (energy
`Σ h_i s_i + Σ J_ij s_i s_j`, `c_i = 1`) and fields `h = (−1, −½, −1)` has a unique ground state,
`τ = 3/2` and `τ_LP = 1/3`: for envelope constants between `1/3` and `3/2` one evaluation
certifies, but no reparametrisation proves it.  With `h = (−½, 0, −½)`: `τ = ½` and `τ_LP = −⅔`
(the relaxation is not tight even for `f` itself).

*Proof.*  (a) `LP(f^t) ≤ min f^t ≤ f^t(x*) = f(x*)`; `t ↦ LP(f^t)` is a minimum of affine functions
of `t`, hence concave, and nonincreasing because `d ≥ 0`; the set where a concave function
attains the upper bound `f(x*)` is an interval, unbounded below because for `t → −∞` the
unaries dominate.  (b) Linear-programming duality for the local polytope:
`LP(θ) = max_φ [Σ_i min_s θ̃_i(s) + Σ_ij min θ̃_ij]`, and the dual value equals `θ(x*)` iff `x*`
attains every local minimum (complementary slackness).  Applied to `f^t`, whose reparametrised
unaries are `θ̃_i(s) − t c_i[s ≠ x*_i]`.  (c) By (b), `f^1(y) ≥ f(x*)` for all `y`, which is the
criterion quoted above; weak duality is what the kernel checks.  (d) On trees the relaxation
is tight for every pairwise model; changing unaries preserves submodularity, for which it is
tight (min-cut); (e) by exhaustive search over triangles with half-integer fields (§3.7);
`τ = 3/2` of the first example is attained by flipping sites 0 and 1 (gap 3), checked by hand. ∎

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

Theorem 3 makes no assumption of isotropy, so it already contains a statement with
position-dependent weights.  The one that fits a chain in torsion coordinates is locality
along the sequence:

**Corollary 4′ (position-dependent weights: sequence-local spectra) [P].**  Let `v` be an
arbitrary spectrum on `𝔽₂ⁿ` (sites ordered along the chain), `𝒲_w = {S : max S − min S < w}` the
frequencies that fit into a window of `w` consecutive sites (`|𝒲_w| ≤ n2^{w−1} + 1`), and
`τ_w² = Σ_{S∉𝒲_w} v_S` the variance of everything that is not local at range `w`.  For every power
of two `N₀` there is a linear design with at most `N₀` points and

    max_x P_A(x)²  ≤  4 [ τ_w² + σ² (n2^{w−1} + 1) / N₀ ].

Hence, if `τ_w ≤ ε/(12B)`, at most `256 (Bσ/ε)² (n2^{w−1} + 1)` evaluations certify `min(f+g)` within
`ε/2`, and `β⁻¹ ln Z_β` likewise, for every member of `𝔹(K_v, B)` and every known part `f`: **linear in
the chain length**, whatever the dependence of the weights `v_S` on the position of `S`.  If the
spectrum is supported on `𝒲_w`, the `≤ (n−w+1)2^w` evaluations of the anchored design (all
configurations that differ from a reference inside one window) determine `g` exactly.

*Proof.*  The proof of Theorem 3(c) works verbatim with any set `𝓛` of frequencies in place of
the `M` heaviest ones (order the frequencies with `𝓛` first; the non-leader mass is at most the
mass of the frequencies that are not first in their coset for *any* order):
`max_x P_A² ≤ 4[Σ_{U∉𝓛} v_U + σ²|𝓛|/N₀]`.  Take `𝓛 = 𝒲_w`; a nonempty `S ∈ 𝒲_w` is determined by its
least element and a subset of the next `w − 1` sites.  Then Theorem 1(b) and Theorem 5 with
`B·max P_A ≤ ε/2`: `16B²τ_w² ≤ ε²/8` and `16B²σ²|𝓛|/N₀ ≤ ε²/8` for the least power of two
`N₀ ≥ 128(Bσ/ε)²|𝓛|`.  The last sentence is the anchored (cut-HDMR) decomposition. ∎

This covers residuals such as torsion cross-terms between neighbouring residues.

**Proposition 4″ (the invariant is the number of modes, not their order; the lever arm in one
set of coordinates) [P; the comparison measured in §3.9].**
(a) A linear bijection of `𝔽₂ⁿ` permutes the Walsh characters.  Hence `T(N)`, `M(η)` and the
two-sided bound of Theorem 3(d) are invariant under linear changes of coordinates, while the
interaction order is not: the cost of an ellipsoid class is governed by *how many* modes
carry the variance, and "bounded order" in Corollary 4(b) is the form this takes for
isotropic spectra only.
(b) *A lever arm.*  Let `u₀, …, u_n ∈ {±1}` be the bond vectors of a directed chain on the line and
`x_i = 1[u_i ≠ u_{i−1}]`, `i = 1…n`, its torsion-like variables.  Then `u_k u_l = χ_{(k,l]}(x)`, the
character of an interval.  Every energy that is quadratic in the positions `p_j = Σ_{k<j} u_k` —
a squared radius of gyration, an elastic network, harmonic restraints between arbitrary
pairs with arbitrary stiffness — is, in the variables `x`, of the form `Σ_{k<l} w_kl χ_{(k,l]}`:
interaction orders up to `n`, per-flip constants `max_x |g(x) − g(x⊕e_i)|` of order
`Σ_{k<i≤l} |w_kl|` that grow with the distance of `i` from the chain ends (flipping `x_i` reverses
every bond vector beyond `i`), and yet at most `n(n+1)/2` modes.  So the first-order format in
these coordinates has the lever-arm problem of the theory division's D42, and the ball of
the interval spectrum needs at most `n(n+1)/2 + 1` evaluations (rank), or
`O(n²(Bσ/ε)²)` by Theorem 3.
(c) *With rotations.*  For an articulated chain with cumulative frames `F_k` (the product of the
first `k` torsion rotations) and bond vectors `b_k = F_k b̂`: `p_j − p_i = Σ_{k=i}^{j−1} b_k`, so every
squared distance is `Σ_{k,l} ⟨b̂, F_kᵀF_l b̂⟩`, and `F_kᵀF_l` is the product of the rotations of the
torsions in `(k, l]`.  Hence every energy that is quadratic in the Cartesian coordinates is
*linear* in the `9·n(n+1)/2` features "matrix elements of the relative rotation of frames `k` and
`l`", each a function of the torsions of one interval; at most that many evaluations determine
it (theory report Theorem 11.47(c), or Theorem 1 with the corresponding kernel), although its
interaction order in torsion coordinates is the chain length and its per-torsion constants
grow with the lever arm.

*Proof.*  (a) `χ_S(Lx) = χ_{LᵀS}(x)`.  (b) `u_l = u_k ∏_{k<m≤l}(−1)^{x_m}`; a quadratic form in the
positions is a quadratic form in the `u_k`; flipping `x_i` changes the sign of exactly the
characters with `k < i ≤ l`.  (c) The identity is the law of composition of frames; the count is
the dimension of the span. ∎

*What this does and does not answer.*  It answers the brief's question about a change of
variables in the affirmative for one physically meaningful family: in cumulative-frame
(bond-vector) coordinates squared distances are of interaction order two, and in torsion
coordinates the same statement reads "the spectrum sits on interval modes", which an
ellipsoid class handles without any change of variables.  It does **not** make a short-range
contact term low-dimensional: a contact is a collective event of all bond vectors of the
loop (a function of their sum being small), of high order in frames as well; for contact
terms the variables must be features, as discussed next.

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
the *states of each torsion* changes that, because the order of a function is invariant under
site-wise relabelling (changes of variables that mix sites are another matter: Proposition
4″).  (ii) For contact terms the change of variables that works is not a bijection of the
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

*The first-order format with decaying constants* **[P, immediate]**.  For completeness, the
literal analogue of "summable product weights" inside the theory division's own format: if
`d = Σ_i c_i[x_i ≠ y_i]` and `D(ε) = min{D : Σ_{i>D} c_i ≤ ε/2}` (sites ordered by decreasing `c_i`),
then evaluating `g` on the `k^{D(ε)}` configurations of the first `D(ε)` sites (the others at a
reference state) determines `min(f+g)` within `ε/2` for every admissible `g`, because
`|g(x) − g(x_{≤D}, ref)| ≤ Σ_{i>D} c_i`.  The count is independent of `n` iff `Σ_i c_i < ∞` and
polynomial in `1/ε` iff the `c_i` decay geometrically.  The lever arm gives the opposite:
constants that grow along the chain.

### 2.8 Randomisation in a linear class (an answer to theory report §12, item 9(c), for additive features)

The theory division's summary table has, for classes that are linear in features, the entry
"randomised: no lower bound known (a generic evaluation sees every perturbation)".  For
additive features none can exist that grows with the system size at extensive accuracy:

**Proposition 11 (Monte Carlo over sites) [P; checked in §3.8].**  Let `X = ∏_i X_i`,
`f = Σ_i φ_i(x_i)`, and let the class be the additive residuals `g = c₀ + Σ_i γ_i(x_i)` with
`γ_i(x⁰_i) = 0` and `|γ_i| ≤ w` (the box class with the features `1[x_i = s]`).  Then
`min(f+g) = g(x⁰) + Σ_i t_i` and `β⁻¹ ln Z_β(f+g) = −g(x⁰) + Σ_i t′_i` (product reference) with site terms
`t_i = min_s(φ_i + γ_i)(s)`, `t′_i = β⁻¹ ln E_s e^{−β(φ_i+γ_i)(s)}`, each confined to an interval of
length at most `R ≤ 2w`.  The algorithm that draws `k` sites uniformly without replacement,
evaluates `g` at `x⁰` and at the `k(q−1)` single-site modifications of `x⁰` at those sites
(`q` states per site), and returns `g(x⁰) + (n/k)·Σ_{sampled} t_i` (for the free energy:
`−g(x⁰) + (n/k)·Σ_{sampled} t′_i`), is within `ε₁n` of the truth with probability at least `1 − δ`
on the whole class as soon as

    k  ≥  (R² / 2ε₁²) · ln(2/δ),

independently of `n`.  A deterministic algorithm whose error is at most `ε₁n` on the class
needs, for binary sites and `f = e|x|` (`R = w − e`), at least `n(1 − 4ε₁/R)` evaluations at the
zero residual.

*Proof.*  Additivity gives `γ_i(s) = g(x⁰ with site i set to s) − g(x⁰)` exactly; Hoeffding's
inequality for sampling without replacement.  Deterministic bound: at the zero residual the
coefficient vectors consistent with `N` evaluations form the intersection of the box with a
subspace of codimension at most `N`; it has a vertex with at least `n − N` coordinates equal
to `±w`, and that vertex or its negative lowers the minimum by at least `(n−N)(w−e)/2`, which
must not exceed `2ε₁n` because the algorithm returns the same number for it and for zero. ∎

*Scope.*  This is Monte Carlo summation and nothing more; it needs exact additivity (for
pair terms the minimum is not a sum over sites), and at a *fixed absolute* accuracy it gives
`k ≈ n²R²/ε²`, worse than learning all `n` coefficients.  Its point is the accounting: in a
linear class, at the extensive accuracies for which the theory division's exponents are
stated, randomisation turns `Θ(n)` into `O(1)` — the opposite of the first-order class, where
it turns `2^{n(1−o(1))}` into a smaller exponential and has a threshold.

### 2.9 What each guarantee means to a user

| | what is assumed | what is delivered | what can be checked independently | what happens when the assumption fails |
|---|---|---|---|---|
| **W** first-order envelope (theory division) | `g(x) − g(y) ≤ d(x,y)` for *all* pairs; the constants | an interval that contains `min`/`ln Z` for every admissible `g`; the check is a machine-verified kernel | the certificate itself; the envelope can be *refuted* by two evaluations, never confirmed by fewer than all pairs | the bound is off by at most the violation times a distance: graceful |
| **H** ellipsoid (§2.1–2.3) | `‖g‖_K ≤ B`: a spectrum (which interaction orders, how much) and a size | an interval for every member of the ball; `B_A P_A` is a computation | recomputation; the ball can be refuted (`yᵀK_AA⁺y > B²`), not confirmed | a sup-norm remainder `η` costs `η(1 + Λ_A)` (Prop. 8(a)); a dip costs its full depth, undetected |
| **B** Gaussian prior (§2.4) | `g` is a draw from `GP(0,K)`; hyperparameters | an interval of posterior probability `≥ 1 − δ`; for `ln Z` also contributions that were never observed (self-averaging) | recomputation; goodness of fit on the design data and on held-out points sees wrong scales and missing smooth terms (§3.5), not dips | coverage can fall to near zero on the affected instances, silently |
| **C** population calibration (split conformal; §3.5) | the new molecule is exchangeable with a calibration set for which the truth is known | marginal coverage `1 − α` over molecules, for any model and any residual | coverage on further known cases | nothing is promised for an individual instance; fails under distribution shift |

A sentence for each.  **W**: "if the constants are right, the answer is right — and for a long
chain the constants make the computation impossible."  **H**: "if the residual has no
component outside a stated low-order model larger than `B`, the answer is right, at
polynomial cost — and whether it has is a physical question."  **B**: "the answer is right
with probability 95 % *if* residuals of this kind are drawn like this; it is the only
paradigm that can use what it has not measured."  **C**: "of molecules like the ones we
checked, 95 % will be inside their intervals."  No row verifies its own assumption from
polynomially many evaluations, and by Proposition 8(c) no cheaper row could exist that is
safe against the first row's class.

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

### 3.3 The same toy problem under both paradigms — `n5_compare.py`, `n5b_additive.py`

**Toy problem.**  `X = {0,1}ⁿ`, known part `f(x) = e·|x|` (ground state `0`, excitation energy `e`
per site), target `min(f+g)` within the width `ε = 0.25`, `δ = 0.05` where a probability is
involved.  Three procedures, none of which is given the instance as a hint:

* **W (first-order envelope, worst case).**  Class `{g : |g(x)−g(y)| ≤ Σ_i c_i[x_i≠y_i]}` with
  `c_i = κ⁻¹·max_x |g(x) − g(x⊕e_i)|`.  `κ = 1` are the *smallest valid* constants — an oracle
  choice, the best case for W; `κ = ½` is a safety factor 2.  Reported: the fractional covering
  number (a lower bound for every algorithm up to `1−2δ`), a greedy cover (an upper bound on
  the smallest certificate), and the number of evaluations of best-first search.
* **H (ellipsoid, worst case).**  Ball `𝔹(K_v, B)` of the generating spectrum with
  `B = κ⁻¹‖g‖_v` (again oracle-flavoured).  Algorithm: evaluate the minimiser of
  `f + ĝ_A − B_A P_A` until `UB_A − LB_A ≤ ε` (Theorem 1).
* **B (Gaussian prior, `1−δ` credible).**  Same algorithm with the band
  `z_t P_A`, `z_t = (2 ln(|X| t² π²/3δ))^{1/2}` (valid simultaneously for all steps and points).

**Part I: a residual with pair interactions** (isotropic spectrum on orders 1 and 2,
`σ₁² = 0.04n`, `σ₂² = 0.02n`; the realised `c_i` are `1.07–1.37` and grow like `√n`; brute force,
medians over 5 instances; the kernel space has dimension `M = n + C(n,2) = 21, …, 78`).

| κ | e | evaluations | n=6 | n=7 | n=8 | n=9 | n=10 | n=11 | n=12 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | W: fractional cover | 10 | 13 | 17 | 28 | – | – | – |
| 1 | 0 | W: greedy cover | 12 | 16 | 22 | 38 | 77 | 107 | – |
| 1 | 0 | W: best-first search | 19 | 30 | 35 | 65 | 136 | 174 | 336 |
| 1 | 0 | H: kernel best-first | 15 | 18 | 21 | 32 | 40 | 47 | 57 |
| 1 | 0 | B: Bayesian best-first | 20 | 26 | 35 | 39 | 53 | 57 | 70 |
| 1 | 0.5 | W: greedy cover / best-first | 5 / 14 | 11 / 19 | 16 / 30 | 19 / 34 | 34 / 58 | 44 / 71 | – / 156 |
| 1 | 0.5 | H / B | 9 / 12 | 15 / 23 | 21 / 30 | 23 / 31 | 34 / 45 | 35 / 45 | 48 / 57 |
| 1 | 1 | W: greedy cover / best-first | 3 / 4 | 3 / 6 | 6 / 12 | 6 / 13 | 10 / 16 | 15 / 30 | – / 58 |
| 1 | 1 | H / B | 7 / 8 | 8 / 11 | 10 / 11 | 12 / 11 | 16 / 19 | 23 / 18 | 33 / 31 |
| 1 | 2 (sharp) | W: cover = best-first | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 1 | 2 (sharp) | H / B | 1 / 1 | 6 / 8 | 9 / 9 | 10 / 9 | 11 / 11 | 12 / 12 | 13 / 13 |
| ½ | 0 | W: fractional cover | 38 | 51 | 84 | 157 | – | – | – |
| ½ | 0 | W: greedy cover | 40 | 57 | 96 | 183 | 357 | 567 | – |
| ½ | 0 | W: best-first search | 45 | 68 | 118 | 223 | 428 | 763 | 1423 |
| ½ | 0 | H (= M) / B | 21 / 20 | 28 / 26 | 36 / 35 | 45 / 39 | 55 / 53 | 66 / 57 | 79 / 70 |
| ½ | 0.5 | W: greedy cover / best-first | 22 / 30 | 42 / 53 | 79 / 98 | 103 / 144 | 184 / 246 | 281 / 393 | – / 848 |
| ½ | 0.5 | H / B | 21 / 12 | 28 / 23 | 36 / 30 | 45 / 31 | 55 / 45 | 66 / 45 | 79 / 57 |
| ½ | 1 | W: greedy cover / best-first | 13 / 17 | 21 / 33 | 38 / 45 | 45 / 58 | 70 / 87 | 126 / 157 | – / 381 |
| ½ | 1 | H / B | 14 / 8 | 24 / 11 | 29 / 11 | 39 / 11 | 49 / 19 | 61 / 18 | 75 / 31 |
| ½ | 2 | W: greedy cover / best-first | 4 / 5 | 4 / 8 | 8 / 11 | 9 / 13 | 10 / 22 | 14 / 31 | – / 51 |
| ½ | 2 | H / B | 7 / 1 | 8 / 8 | 9 / 9 | 12 / 9 | 13 / 11 | 29 / 12 | 46 / 13 |

In all 280 runs of H and all 280 runs of B the true minimum was inside the reported interval.
What the table shows, and what it does not:

1. **Sharp regime (`e = 2 > c`, `κ = 1`): the envelope paradigm wins** — one evaluation (the
   theory division's Theorem 11.7) against about `n + 1` for H and B.  The ellipsoid with radius
   `‖g‖` lets a single main effect take the whole budget, so it is *larger* in coordinate
   directions than the oracle-tight Lipschitz box, and the sharp-site theorem has no
   counterpart of the same strength.
2. **Non-sharp regime with oracle-tight constants (`κ = 1`, `e ≤ 1`): no dramatic difference up
   to `n = 12`.**  The smallest covers of W are 0.4–2.3 times the counts of H; W's search grows
   by about `×1.6` per site at `e = 0`, H and B like `M ≈ n²/2`.  The envelope's exponent is
   small (`0.19` nats per site at `e/c = ½`), so the exponential is not visible at sizes that can
   be enumerated — exactly the caution the theory division attaches to its own exponents.
3. **With a safety factor 2 on both sides (`κ = ½`) the separation is visible:** W's search
   grows by `×1.8` per site (1 423 evaluations at `n = 12`, a third of the cube); H ends up
   evaluating as many points as the kernel space has dimensions (79 for `M = 78`); B stops at 70.  A certified envelope always has `κ < 1`; the verified
   per-torsion constants of the theory report have `κ` far below `½`.
4. B needs fewer evaluations than H as `n` grows because its band is `z_t ≈ 5–6.5` standard
   deviations where H's is `B_A ≈ κ⁻¹√M` (`8.8` and `17.7` at `n = 12`).

**Part II: the additive toy, any `n`.**  `g(x) = Σ_i γ_i x_i`, `γ_i ~ N(0, 0.16)` (the main-effect part
of the prior above), `c_i = |γ_i|/κ`.  For W the entry is the machine-checked lower bound on the
size of *every* `ε`-certificate — `ln N ≥ max_t [Σ_i max_v r_i(t; v) − tε]`, theory report Theorem
11.8 (`product_exp_weights` **[V]**), which bounds every algorithm up to the factor `1 − 2δ`
(`expected_queries_ge_exp_weights_min` **[V]**) — evaluated by my own code, median of 5 draws.
For H and B the kernel of additive functions has rank `n + 1`, and `n + 1` evaluations on a
unisolvent set determine `g`: the cost is `n + 1` at every accuracy.

| `ln N_W ≥` | n=10 | 20 | 50 | 100 | 200 | 500 | 1000 | rate/site |
|---|---|---|---|---|---|---|---|---|
| `κ = 0.9`, `e = 0` | 0.0 | 0.0 | 0.5 | 1.3 | 3.4 | 9.4 | 19.6 | 0.020 |
| `κ = 0.7`, `e = 0` | 0.3 | 0.8 | 2.9 | 6.1 | 13.1 | 33.6 | 68.3 | 0.068 |
| `κ = 0.5`, `e = 0` | 1.1 | 2.2 | 6.2 | 12.5 | 26.0 | 65.7 | 132.7 | 0.133 |
| `κ = 0.5`, `e = 0.4` | 0.2 | 1.7 | 5.0 | 10.1 | 20.1 | 48.3 | 107.2 | 0.107 |
| `κ = 0.25`, `e = 0` | 2.5 | 4.9 | 12.7 | 24.9 | 50.7 | 127.4 | 255.9 | 0.256 |
| zero residual, `c = 0.4`, `e = 0.2` | 1.0 | 2.8 | 8.3 | 17.7 | 36.4 | 92.4 | 185.8 | 0.186 |
| `ln N_H = ln N_B = ln(n+1)` | 2.4 | 3.0 | 3.9 | 4.6 | 5.3 | 6.2 | 6.9 | — |

So at `n = 100` the envelope paradigm needs at least `e^{12.5} ≈ 2.7·10⁵` evaluations with a
safety factor 2 and `e^{24.9} ≈ 6·10¹⁰` with a factor 4, against 101; the crossover (first `n` of
the grid at which the lower bound exceeds `n+1`) is `n = 500, 100, 50, 10–20` for
`κ = 0.9, 0.7, 0.5, 0.25`.  With `κ = 1` the bound is zero for every `n` — not a defect of the
bound: with oracle-tight constants and an additive residual the envelope is saturated between
`argmax g` and `argmin g`, and two evaluations determine `g` on every geodesic, i.e. everywhere
(the theory report notes that `κ < 1` is needed in Theorem 11.9).  Checks: `n5_compare.py`
part II, an independent non-vectorised implementation with a finer grid of slopes and weights,
gives `12.73` and `26.42` at `n = 100`, `200` (`κ = ½`, `e = 0`) where the table has `12.5` and `26.0` —
every choice of slope and weights is a valid lower bound, the table has the coarser, lower
values; on 12 small additive instances the product bound is below the exact fractional
covering number; the zero-residual row reproduces the theory division's exponent
`R*(½) = 0.1882` up to the `tε` term and the grid (independent replication of that number).

**What the comparison means.**  The cost under W is governed by `κ` (how much slack the
certified envelope has over the truth) and by sharpness; the cost under H by `B/‖g‖` and the
dimension `M` of the kernel space; under B by `M` and by the prior being right.  W is the
cheapest of the three when the known part is sharp and its constants are tight; it is the
only one whose cost is exponential in `n`, at any fixed slack.  *A caution against reading too
much into H:* for a spectrum of exact finite order and a radius that contains the residual
with any margin, H ends up evaluating as many points as there are coefficients — that is the
theory division's own statement for classes that are linear in features ("rank-many
evaluations", Theorem 11.47(c)), with an ellipsoid in place of a box.  What the ellipsoid adds
is not a cheaper finite-dimensional case but a quantitative treatment of what lies outside
the finite model (the tail `T(M)`, Theorem 3, with a lower bound), the exponent when the order
is not bounded, and — in its Bayesian reading — a band that does not grow with `√M`.

### 3.4 Bayesian certificates: coverage and width — `n4_bayes.py`

Prior: orders 1–3 with `σ_m² = n·(0.04, 0.02, 0.004)`; `f = 0.5|x|`; linear designs (dual BCH,
`m = 1`: 8 or 16 points; `m = 2`: 64 or 256 points); 300 prior draws per cell (120 for `n = 15`);
"sampled" = the 95 % posterior interval from 400 posterior samples (150 for `n = 15`).

| n | design | `max P_A` | `ln Z`, β=½: analytic / sampled width | `ln Z`, β=2 | `min`: analytic / sampled width |
|---|---|---|---|---|---|
| 10 | m=1, N=16 | 0.65 | 1.81 / 0.089 | 7.66 / 1.21 | 2.22 / 1.13 |
| 10 | m=2, N=256 | 0.16 | 0.43 / 0.0064 | 1.74 / 0.20 | 0.56 / 0.35 |
| 12 | m=2, N=256 | 0.21 | 0.57 / 0.0076 | 2.33 / 0.25 | 0.81 / 0.51 |
| 15 | m=2, N=256 | 0.30 | 0.81 / 0.0104 | 3.33 / 0.37 | 1.29 / 0.71 |

Coverage: the analytic intervals of Theorem 6(i),(ii) covered in every draw of every cell;
the sampled intervals covered in `0.925–1.0` of the draws for `ln Z` (mean `0.959`) and
`0.917–1.0` for the minimum (mean `0.970`) — nominal `0.95`, with Monte Carlo error from a
posterior sample shared by all draws of a cell.  *Reading:* for the minimum the union-bound
interval is within a factor 2 of the true posterior width; for `ln Z` at high temperature the
true posterior is 20–80 times narrower than the sup-norm interval (the unlearned order-3
tail self-averages; Theorem 6(iii)), and still 6–9 times narrower at `β = 2`.  The widths grow
with `n` at a fixed design order because the tail variance is extensive: a fixed accuracy
eventually needs the next order, in agreement with Corollary 4.

**White tail (Proposition 7)**: prior = main effects + white noise of variance `τ² = 1` at every
configuration, `n = 12`, design `m = 2` (256 points; for this prior it acts as a replicated
main-effects design), 100 draws:

| β | `β²τ²` | `H₂(ν)` | second-moment width (Thm 6(iv)) | true 95 % posterior spread | sup-norm width (Thm 6(i)) |
|---|---|---|---|---|---|
| 0.5 | 0.25 | 8.0 | 0.16 | 0.06 | 2.9 |
| 1 | 1 | 7.3 | 0.60 | 0.24 | 6.1 |
| 2 | 4 | 5.7 | vacuous (`ρ₂ = 0.22 > δ`) | 1.1 | 13.2 |
| 4 | 16 | 3.5 | vacuous | 4.6 | 30.5 |

(coverage of the second-moment interval 100/100 where it is not vacuous; with 16 points
instead of 256 the widths at `β = ½, 1` are `0.36`, `1.79`.)  At `β = ½` 256 evaluations out of 4 096
pin `ln Z` to `±0.08` although every unevaluated energy carries an unlearnable unit-variance
term; no certificate through the power function can be narrower than `2.9`.  At `β = 4` (the
random energy model's critical value is `β_c = 4.08` here) the posterior spread is `4.6` and
nothing short of enumeration reduces it.  The cube is small (`H₂ ≤ 8.3` nats); the certificate
improves exponentially in `n` at fixed `β²τ²` by the bound of Proposition 7(b).

### 3.5 When the assumption fails — `n6_misspec.py`

`n = 10`, `f = 0.5|x|`, target `min(f+g)`; assumed prior: constant + orders 1, 2
(`σ₁² = 0.4`, `σ₂² = 0.2`); design `m = 1` (16 evaluations); certificate = 95 % posterior interval
(mean half-width `0.5`).  600 instances per truth; split conformal with 300 calibration
instances whose true minimum is known (score `|truth − centre|/halfwidth`), tested on the other
300.  "Fit test": `yᵀK_AA⁻¹y` against `χ²₁₆` on the *same* 16 evaluations; "held-out": mean squared
standardised residual at 32 further random points (rejection rates at nominal 5 %; the
held-out test over-rejects, 9 %, because the residuals are correlated).

| truth | coverage of the nominal interval | conformal factor | conformal coverage | fit test rejects | held-out rejects |
|---|---|---|---|---|---|
| as assumed | 0.948 | 1.00 | 0.957 | 0.06 | 0.09 |
| pair variance ×4 | 0.557 | 2.79 | 0.967 | 0.77 | 0.99 |
| an unmodelled order-3 term (`σ₃² = 0.2`) | 0.770 | 2.01 | 0.960 | 0.29 | 0.89 |
| Student-`t₃` coefficients, same variances | 0.930 | 1.00 | 0.940 | 0.11 | 0.14 |
| a dip (depth 2, slope 1: 11 of 1024 configurations) at a low-lying state in 20 % of the instances | 0.795 overall: **0.089 with a dip**, 0.957 without | 2.84 | 0.953 overall: **0.767 with a dip**, 1.00 without | 0.08 (with a dip) | 0.24 (with a dip) |

*Reading.*  A wrong *scale* or a missing *smooth* component is visible in the data and is
repaired by recalibration.  A dip is neither: on the instances that have one the certificate
is wrong 91 % of the time by a mean of `1.1` (twice the half-width), the design data carry
almost no trace of it (8 % rejections against a 6 % baseline), 32 further evaluations see it
in a quarter of the cases at this size (the dip occupies 1 % of the cube; the fraction is
exponentially small in `n`), and conformal recalibration reaches its guarantee — marginal
coverage over the population — by widening every interval 2.8 times while still failing on a
quarter of the dipped instances.  This is Proposition 8(c) in numbers.

*Amplification of a sup-norm remainder (Proposition 8(a)).*  Largest Lebesgue constant
`max_x Σ_a |λ_a(x)|` of the designs: `2.5, 4.3, 2.9, 4.7, 3.3` for
`(n, m) = (7,1), (7,2), (10,1), (10,2), (12,1)` — that is `0.6–0.9·√M` — while the `ℓ²` norm of the
weights is `(M/N)^{1/2} = 1.0, 0.67, 0.83, 0.47, 0.90` exactly.

### 3.6 The ellipsoid's worst member for `ln Z`, and what a dip costs an ellipsoid — `n10_extras.py`

(I) Proposition 5′, `b = 1`, `s₂ = ¼` (so `βJ = β`): numerical supremum of `ln E exp(−βr)` over the
order-2 ball (ascent from 12 random, 4 localised and the Curie–Weiss start) against the
Curie–Weiss member:

| β | n=8: num / CW | n=10 | n=12 | mean-field `n·max_m[…]` (n=12) | sup-norm bound (n=12) |
|---|---|---|---|---|---|
| 0.4 | 0.0588 / 0.0588 | 0.0580 / 0.0580 | 0.0575 / 0.0575 | 0 | 2.4 |
| 0.8 | 0.313 / 0.313 | 0.321 / 0.321 | 0.328 / 0.328 | 0 | 4.8 |
| 1.2 | 0.925 / 0.925 | 1.012 / 1.012 | 1.092 / 1.092 | 0.29 | 7.2 |
| 2.4 | 4.82 / 4.82 | 5.85 / 5.85 | 6.88 / 6.88 | 6.19 | 14.4 |
| 4.0 | 11.15 / 11.15 | 13.77 / 13.77 | 16.38 / 16.38 | 15.69 | 24.0 |

(the high-temperature limit `φ(βJ) = −½ln(1−βJ) − βJ/2` is `0.055` at `βJ = 0.4`).  No start
produced a value above the Curie–Weiss member, and the two values below the transition are
below the proven bound `φ(F)` (`0.062` and `0.485` at `n = 12`).  The inequalities of Proposition
5′(a) were also tested directly (`n12_gauss_comparison.py`): 2 752 zero-diagonal matrices of
seven kinds (Gaussian, sparse, Curie–Weiss, antiferromagnetic, gauged, cliques, rank one),
`n = 3…10`, `‖𝐉‖_F ∈ (0.05, 0.98)`: no violation; the smallest slack, `5·10⁻⁶`, is at a Curie–Weiss
matrix.
(II) Hilbert norm of the dip `−(3 − d_H(x,0))₊` under the product spectrum with `ρ = 1 − 1/n`
(`λ = ½`, unit variance): `3.9·10³, 9.3·10⁴, 2.3·10⁶, 6.1·10⁷, 1.7·10⁹` for `n = 8, 10, 12, 14, 16`;
a typical prior draw has norm `2^{n/2} = 16 … 256`, an additive function of the same depth
`3.3`.  With `λ = 2`: `18, 112, 743, 5.2·10³, 3.9·10⁴`.

### 3.7 Funnels with interacting known parts — `n9_lp_funnel.py`

Binary pairwise known parts `Σ h_i s_i + Σ J_ij s_i s_j` with Gaussian couplings, a fraction `p` of
them antiferromagnetic, Gaussian fields of scale `h`; `τ` by enumeration, `τ_LP` by the linear
programme of Theorem 9(b) (HiGHS).  `τ_LP ≤ τ` in all 1 280 instances.

| family | `p` | field | `τ_LP = τ` | LP tight at `x*` (`τ_LP ≥ 0`) | median `τ` / `τ_LP` |
|---|---|---|---|---|---|
| 4×4 grid | 0 | 0.5 and 2 | 100 % | 100 % | 0.13 / 0.13; 0.24 / 0.24 |
| 4×4 grid | 0.1 | 0.5 | 25 % | 55 % | 0.10 / 0.01 |
| 4×4 grid | 0.3, 0.5 | 0.5 | 7 %, 5 % | 28 %, 38 % | 0.08 / −0.06; 0.15 / −0.05 |
| 4×4 grid | 0.1–0.5 | 2 | 80–85 % | 93–100 % | 0.27–0.38 / 0.25–0.37 |
| chain of 12 with 6 long-range contacts | 0 | 1 | 100 % | 100 % | 0.26 / 0.26 |
| chain of 12 with 6 long-range contacts | 0.3, 0.5 | 1 | 55 % (46–48 % with unequal `c_i`) | 74–84 % | 0.14–0.18 / 0.06–0.11 |
| random trees, 14 sites | 0.5 | 1 | 100 % | 100 % | 0.19 / 0.19 |

So the equality cases of Theorem 9(d) are confirmed, and for frustrated known parts the two
slopes coincide — the short proof exists whenever the funnel does — in 5 % to 85 % of the
instances, depending on how strongly the fields dominate.  Exhaustive search over triangles with
half-integer fields in `[−4, 4]` and couplings `±1` gives the two examples of Theorem 9(e)
(`n9_lp_funnel.py` for the largest relative gap; `n9b_example.py` for the largest one with
`τ_LP > 0`; on the 4-cycle with a chord and integer fields the latter search finds
`τ = 2`, `τ_LP = 2/3`).

### 3.8 Randomisation in an additive class — `n11_site_mc.py`  (Proposition 11, §2.8)

`w = 1`, `e = 0.2`, `β = 1`, `ε₁ = 0.1`, `δ = 0.05`: `k = 119` sampled sites for the minimum, `153` for
`ln Z`, i.e. 120 and 154 evaluations for `n = 10³, 10⁴, 10⁵`, where a deterministic algorithm with
the same error bound needs at least `500, 5 000, 50 000`.  Five adversarial coefficient patterns, 2 000 runs each: failure
frequency at most `0.9 %` (bound `5 %`).

### 3.9 The lever arm in one set of coordinates — `n13_lever_arm.py`  (Proposition 4″)

Directed chain, flip variables `x ∈ {0,1}ⁿ`; residual `g = (1/n) Σ_{k<l} (1 + ½ξ_kl) u_k u_l` (a noisy
squared-radius-of-gyration term, `ξ` standard normal), known part `f = ½·#flips`, `ε = 0.25`,
medians of 3 instances.  W uses the smallest valid constants (`κ = 1`); they are `1.6–2.2` at the
chain ends and `4.5–6.7` in the middle.

| evaluations | n=6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|
| W: fractional cover | 36 | 41 | 103 | 179 | – | – | – |
| W: greedy cover | 36 | 45 | 108 | 190 | 370 | 614 | – |
| W: best-first search | 42 | 65 | 136 | 257 | 508 | 862 | 1719 |
| H, `B = ‖g‖` | 8 | 8 | 19 | 21 | 21 | 23 | 41 |
| H, `B = 2‖g‖` (= `M = n(n+1)/2`) | 21 | 28 | 36 | 45 | 55 | 66 | 78 |
| B (prior with the generating second moments, mis-centred) | 21 | 27 | 36 | 44 | 51 | 58 | 72 |
| `2ⁿ` | 64 | 128 | 256 | 512 | 1024 | 2048 | 4096 |

All H and B intervals contained the true minimum (21/21 each).  Here, unlike in §3.3, the
envelope paradigm is expensive *with oracle-tight constants*: more than half of the cube is
needed in a fractional cover at `n = 6`, a third at `n = 9`, and the search evaluates 42 % of it
at `n = 12`; the spectral class needs 41 points, or all 78 coefficients with a factor 2 on the
radius.  This is the lever arm, and it is the cleanest case I have for the claim that the
kind of class decides: same residual, same coordinates, same oracle knowledge.

---

## 4. Prior art

Reading levels (rule 5): **[full]** full text read; **[abs]** abstract read; **[snip]** search-result
snippet only; **[mem]** from memory — unverified.  I had web search and a page-fetch tool; I
read no paper in full.  "Not found" below means: not found in the searches listed in §4.3; it
is not a claim of novelty.

### 4.1 Mapping the theory division's classes onto tractability theory (direction 2)

Information-based complexity (IBC) asks for the number `n(ε, d)` of information operations
needed in the worst case over a class (or on average over a measure) in dimension `d`, and
calls a problem *polynomially tractable* if `n(ε,d) ≤ C ε^{−p} d^{q}`, *strongly* tractable if
`q = 0`; it suffers the *curse of dimensionality* if `n` is exponential in `d` for some fixed `ε`.
On the cube `{0,1}ⁿ` a variable has two values, so smoothness in one variable is empty and the
only structure is *which interaction orders carry how much* — the weights.

| theory division's result | counterpart in IBC | instance of a known theorem? |
|---|---|---|
| First-order class, deterministic, worst case over instances: `2^{n(1−o(1))}` at the zero residual; certificates are coverings (11.4, 11.23(a)) | radius of information; optimisation is as hard as uniform approximation on convex symmetric classes (Wasilkowski 1984; Novak 1988 **[snip]**); covering numbers of Lipschitz classes (Sukharev 1971 **[mem]**) | the worst-case statement **is** an instance (the curse for Lipschitz classes); the instance-wise covering with gap radii belongs to certified Lipschitz optimisation (their own citations), not to IBC |
| Known part, sharp sites, dichotomy "one or exponential" (11.7–11.9), normal form (11.29) | none: IBC has no instance-dependent known part | **not** an instance |
| Exact exponents as rate–distortion functions (11.9, 11.15) | IBC gives orders in `ε` and `d`, not exponents with constants | **not** an instance (information theory) |
| `ln Z`, randomised: threshold, soft gaps, hinted/non-adaptive/adaptive exponents (11.24–11.28, 11.44–11.58) | integration of `e^{−βg}`: a nonlinear functional; Bakhvalov's averaging; adaption helping on a non-symmetric class (Mathé–Novak 2007) — all cited by them | method known; statements **not** instances |
| Second-order class, dense constants: exponential (11.31–11.32) | curse of dimensionality for classes of fixed smoothness `r ≥ 2`, also when directional derivatives are bounded by `≈ d^{−1/2}` (Hinrichs–Novak–Ullrich–Woźniakowski 2014 **[snip of abstract]**) | the discrete analogue; not literally an instance (other domain, other functional) |
| Second-order class, weak coupling: a star suffices (11.16–11.17) | anchored (cut-HDMR) decomposition truncated at order one with a remainder bound (Kuo–Sloan–Wasilkowski–Woźniakowski 2010 **[mem]**, cited by them) | **is** an instance of the anchored-decomposition calculus |
| Linear in `p` features, box (11.47) | optimal recovery in finite dimension (Micchelli–Rivlin) | **is** an instance (they say so) |
| Pair-additive, Lipschitz radial functions, shared by type (11.48–11.49) | finite-order weights of order 2 in *bead* variables with shared components | tractability **is** an instance in spirit of Wasilkowski–Woźniakowski 2004 **[snip]**; the profile distance is their own packaging |
| Per-torsion constants growing with the lever arm (11.36–11.37) | *increasing* weights; the known necessary conditions for tractability with product weights are `sup_d Σ_j γ_{d,j} < ∞` (strong) and `Σ_j γ_{d,j} = O(ln d)` (polynomial) (Sloan–Woźniakowski 1998 **[snip for the bibliographic data, mem for the conditions]**) | consistent with the known necessity; in their format the summable case is the remark at the end of §2.7 |
| — (absent from their table) | weighted Hilbert spaces with decaying or finite-order weights: (strong) polynomial tractability | this report, §§2.1–2.3, for `min` and `ln Z` on the cube |

The one-line version: their *exponential* rows are the discrete counterparts of the curse for
classes of fixed smoothness in an unweighted supremum norm; their *cheap* rows are
finite-dimensional linear classes; the *middle* that tractability theory is about — infinite
or high-dimensional classes with decaying weights — is missing from their table and is where
a physical residual plausibly lives.

### 4.2 Positioning of the statements of §2

| statement | closest prior art | what I can say |
|---|---|---|
| Thm 1(a) band | hypercircle inequality (Golomb–Weinberger 1959; Micchelli–Rivlin 1977) **[mem]**; "posterior variance = worst-case error in the RKHS unit ball" (Kanagawa–Hennig–Sejdinovic–Sriperumbudur 2018, §3.4 **[snip]**) | known |
| Thm 1(b)–(d) certificate iff power function below gap | regret bounds for GP-UCB over RKHS balls and GP samples through the maximal information gain (Srinivas–Krause–Kakade–Seeger 2010/2012 **[snip]**), expected improvement (Bull 2011 **[snip]**), exponential regret without noise (de Freitas–Smola–Zoghi 2012 **[mem]**); instance-dependent certificates for Lipschitz optimisation (Bachoc–Cesari–Gerchinovitz 2021, via the theory report) | the exact instance-wise "iff" in the form parallel to the theory division's covering theorem: not found; immediate |
| Lemma 2 aliasing posterior | Mitchell–Morris–Ylvisaker, *Two-level fractional factorials and Bayesian prediction*, Statistica Sinica 5 (1995) 559–573 **[abs]**: stationary Gaussian priors on `{−1,1}^k` conditioned on fractional factorials; Kerr 2001, Joseph 2006 **[snip]** | known in substance |
| Thm 3(a) lower bound | `n`-th minimal average-case error with arbitrary linear information = eigenvalue tail (Traub–Wasilkowski–Woźniakowski 1988; Ritter 2000) **[mem]** | known |
| Thm 3(b) BCH/orthogonal-array designs | orthogonal arrays from linear codes (Bose–Ray-Chaudhuri; Hedayat–Sloane–Stufken 1999) **[mem]**; lattice algorithms for approximation, error = mass of the dual lattice minus leaders (Kuo–Sloan–Woźniakowski 2006 **[snip]**) | the `𝔽₂` transposition of known arguments |
| Thm 3(c),(d) random linear designs, two-sided sup-norm bound | "standard information is as powerful as linear information" (Kuo–Wasilkowski–Woźniakowski 2009; Krieg–Ullrich 2021) **[mem]**; low-degree learning on the cube (Linial–Mansour–Nisan 1993; Kushilevitz–Mansour 1993) **[mem]** | not found in this form |
| Cor 4(a) | Wasilkowski 1984; Novak 1988 — quoted in D. Krieg's thesis, arXiv:1905.01166 **[snip]** | an instance |
| Cor 4(b) polynomial iff bounded order | Wasilkowski–Woźniakowski, J. Approx. Theory 130 (2004) 57–77 **[snip]**; Novak–Woźniakowski, *Tractability of Multivariate Problems* I–III **[mem]** | the cube/`min` version is a transposition; additive Gaussian-process models in Bayesian optimisation have regret linear in the dimension (Kandasamy–Schneider–Póczos 2015 **[snip]**), second-order models on binary variables are used in BOCS (Baptista–Poloczek 2018 **[snip]**), product ("diffusion") kernels on the Hamming graph in COMBO (Oh et al. 2019 **[snip]**) — no complexity statement with a lower bound surfaced |
| Cor 4(c) exponent `h((1−ρ)/2)` | — | not found; a two-line computation |
| Thm 5 interval of `ln Z` over a ball | Donsker–Varadhan; Sion; kernel bounds on log-partition functions of a different kind (Bach, arXiv:2202.08545 **[snip]**); worst-case rates for log-partition estimation over smoothness classes (Holzmüller–Bach, arXiv:2303.03237, cited by the theory report) | not found in this form (one search) |
| Prop 5′ | Curie–Weiss model (textbook); domination of a Rademacher chaos of order two by the Gaussian one, variable by variable (a standard comparison argument) **[mem]** | (b) textbook; (a) a short argument I did not look for in print; extremality above the transition is numerical |
| Thm 6(i)–(iii) | Gaussian concentration (Borell 1975; Tsirelson–Ibragimov–Sudakov 1976), Poincaré and first-chaos variance bounds (Houdré–Kagan 1995) **[mem]**; probabilistic numerics, of which a certificate in the sense of §2.4 is an instance (Diaconis 1988; Hennig–Osborne–Girolami 2015; Cockayne et al. 2019) **[mem]**; Bayesian quadrature (O'Hagan 1991; Rasmussen–Ghahramani 2003; Osborne et al. 2012; Gunter et al. 2014, arXiv:1411.0439 **[snip]**) puts the prior on the integrand, not on the energy | standard tools; the dimension-free interval for `ln Z` under a prior on the energy: not searched beyond the Bayesian-quadrature query |
| Thm 6(iv), Prop 7 | second-moment method for high-temperature free energies (Aizenman–Lebowitz–Ruelle 1987; Talagrand) **[mem]**; random energy model (Derrida 1981) **[mem]** | known physics; the reading as a complexity statement and as a counterexample to "polynomial iff decay": not found |
| Prop 8(a) | Lebesgue functions (textbook); misspecified kernelised bandits with a sup-norm error `ε` (Bogunovic–Krause, NeurIPS 2021, arXiv:2111.05008 **[snip]**) | known phenomenon |
| Prop 8(b),(c) | theory report Theorems 11.22–11.25; workstream P, Corollary 15 | corollaries, restated |
| Thm 9 LP-funnel slope | LP relaxation and its dual (Schlesinger 1976; Werner 2007 **[snip]**); tightness for submodular and balanced models (Kolmogorov–Zabih 2004 **[mem]**; Weller–Rowland–Sontag 2016 **[snip]**); stability (Bilu–Linial 2010; Makarychev–Makarychev–Vijayaraghavan 2014 **[mem]**; Lang–Sontag–Vijayaraghavan 2018 **[abs]**, 2019 **[snip]**); side-chain placement solved by LP (Kingsford–Chazelle–Singh 2005; Yanover–Meltzer–Weiss 2006) **[mem]** | the parametric quantity and its use as a certificate of sharpness under envelope uncertainty: not found (two searches); elementary |
| Prop 4″ | Walsh characters under linear maps (textbook); the frame recursion of articulated chains (textbook kinematics); polynomial/elastic-network energies as low-rank features — not searched | elementary; not searched |
| Cor 4′ | finite-order weights (Wasilkowski–Woźniakowski 2004 **[snip]**); anchored decomposition (Kuo–Sloan–Wasilkowski–Woźniakowski 2010 **[mem]**) | an application of Theorem 3; not searched separately |
| Prop 10 | Gaussian approximation potentials (Bartók–Payne–Kondor–Csányi 2010) **[mem]**; body-ordered approximation with rates (Thomas–Chen–Ortner, Arch. Ration. Mech. Anal. 246 (2022) 1–60 **[snip]**) | synthesis |
| Prop 11 | Monte Carlo summation; randomised complexity of sums (Heinrich; Mathé) **[mem]** | textbook; its use to fill the cell of the theory division's table is the only point |
| population calibration | conformal prediction (Vovk–Gammerman–Shafer 2005; Lei et al. 2018) **[mem]** | known; used, not developed |
| average-case optimisation | Wasilkowski, Math. Programming 57 (1992) 313–324 **[abs]**: "optimization is easier on average than in the worst case", upper bounds only, the average complexity "is still unknown" | consistent with §5, item 5 |

### 4.3 Search log

Fourteen web searches and four page fetches, all on 2026-11-25; queries and what each returned
are recorded verbatim in `experiments/science/ws_X/NOTES.md` (entry "literature search log").
Topics: Mitchell–Morris–Ylvisaker; finite-order weights; lattice rules for approximation;
optimisation versus approximation in IBC; Bayesian optimisation on the hypercube
(BOCS/COMBO/Walsh kernels); misspecified Gaussian-process bandits; tightness of LP relaxations
for balanced models; stable instances of MAP inference; body-ordered approximations; Bayesian
quadrature for normalising constants; the curse for smooth functions; Gaussian processes
versus kernel methods; GP-UCB/EGO/additive models; Sloan–Woźniakowski; worst-case
log-partition over a kernel ball; LP certificates and unary margins.  Pages fetched: the
Statistica Sinica abstract page of Mitchell–Morris–Ylvisaker; arXiv:1905.01166 (abstract
page; the relevant passage was seen only in a search snippet); the record of Wasilkowski
1992; arXiv:1711.02195 (abstract).  Not searched at all: superconcentration; coin-weighing and
sketching lower bounds; conformal methods for interatomic potentials; energy-landscape
theory.  Everything about those is from memory.

---

## 5. What I did not settle

1. **Randomised algorithms for ellipsoids beyond the additive case.**  Proposition 11 uses
   that the target is a sum over sites.  For order-2 classes I have neither a randomised
   lower bound of order `M` nor an algorithm below it; the dip argument of the theory division
   has no analogue (a generic evaluation sees every member), and Proposition 11 shows that the
   answer can be dramatically below the deterministic one.
2. **The exact complexity of `ln Z` over an ellipsoid.**  Theorem 5 gives the consistent
   interval for a given design; I have no design theorem for it (the counterpart of Theorem
   3), only the bracket between the Gibbs-averaged and the sup-norm bound.  Proposition 5′
   settles the width of the order-2 ball asymptotically for `βJ < 1` and a uniform reference;
   for `βJ > 1` (is the Curie–Weiss matrix the maximiser of `ln E exp(½ sᵀ𝐉s)` at a given
   Frobenius norm?), for finite `n`, and for a non-uniform reference it is open.
3. **Instance-wise exponents.**  Theorem 3 is a worst case over the ball; Theorem 1(d) is
   instance-wise but I did not compute its smallest designs (a gap-weighted design problem)
   beyond running the greedy algorithm.  There is no analogue here of the theory division's
   rate–distortion formula.
4. **The frozen regime** (Proposition 7(c)) is a heuristic with numerics at `n ≤ 12`.
5. **Average-case complexity of the minimum** under a Gaussian prior on the cube: only upper
   bounds (the algorithms of §3.3) and the lower bounds inherited from recovery; the true
   average-case complexity of global optimisation is open even in the classical settings
   (Wasilkowski 1992 **[abs]**).
6. **Chains.**  Nothing in this report was computed on a chain.  Proposition 10 is a synthesis
   of the theory division's §§11.14, 11.17 in the vocabulary of §2.1; whether a real residual
   has a useful norm or spectrum in such a class is not addressed.
7. **Multi-label known parts** (rotamers) for Theorem 9: only two-state sites were run; for
   three or more labels even ferromagnetic Potts terms do not give `τ_LP = τ`.
8. **The cost of checking.**  Like the theory division I count evaluations of `g`.  Checking a
   kernel certificate means minimising `f + ĝ_A − B_A P_A` over `X`, a hard problem in general;
   the bridge to the pairwise kernel after Theorem 1 covers order `≤ 2` with a uniform bound on
   `P_A` only.
9. **Who certifies `B`, the spectrum, the prior.**  In §3.3 `B` and the envelope constants were
   both oracle choices.  Estimating them from data (empirical Bayes) adds an uncertainty that
   I did not propagate.
10. **Constants.**  The factor `16σ²/η²` in Theorem 3(d) and the constant 4 (essentially
    attained) are what the proofs give; I did not look for optimal designs.
11. **Novelty.**  All reading was at the level of abstracts or snippets; several positioning
    statements in §4.2 rest on memory.

## 6. The three most promising next steps

1. **A sharp–soft decomposition with a verified kernel.**  Use the envelope machinery where
   the known part is sharp (Theorem 9 gives the proof object for interacting known parts)
   and an ellipsoid on the rest: by Theorem 1(d) the design only has to push `B·P_A(x)` below
   `gap_f(x) + ε`, so sites or droplets with a large known gap need no resolution.  The
   concrete deliverable is a soundness theorem of the form
   `min(f+g) ≥ (kernel-certified bound of the pairwise model f + ĝ_A) − B_A·p̄` with a checkable
   certificate for `max P_A ≤ p̄` (for linear designs on the cube: the non-leader mass, a finite
   sum).  This would put a polynomial-cost class next to the three existing kernels.
2. **Measure the three numbers that decide between the paradigms on one real residual:** the
   slack `κ` of the best certifiable first-order constants, the spectrum of the residual in a
   body-ordered feature space (how many modes for a given tolerance: `M(η)`), and the size and
   kind of what is left (supremum norm; any dip-like outliers).  §3.3 says how the costs then
   compare; without these numbers every interface remains hypothetical, as the theory report
   says of its own.
3. **Randomisation for linear-information classes.**  Proposition 11 shows the gain is from
   `Θ(n)` to `O(1)` in the additive case.  Find the right statement for pair terms: at high
   temperature `ln Z` has a convergent cluster expansion whose terms can be sampled; for the
   minimum the natural tool is a sampled lower bound through the LP dual.  Either a
   polylogarithmic algorithm or a lower bound of order `M` would complete the row of the
   theory division's table.

## 7. Requests

**To the theory division.**

* **X-REQ-T1 (formalisation).**  Machine-check Theorem 1(a),(b) for a finite index type and a
  rational positive semidefinite matrix `K`: for `g = K c` with `cᵀKc ≤ B²`, data on `A`, weights
  `λ(x)` with `K_AA λ(x) = K_{A x}`: `|g(x) − λ(x)ᵀ g_A| ≤ (B² − g_Aᵀ K_AA⁺ g_A)^{1/2} · (K_xx − λ(x)ᵀK_{A x})^{1/2}`,
  and the kernel statement of §6 item 1.  The squares avoid square roots; a rational
  certificate `(λ, p̄², B_A²)` suffices.  Expected size: comparable to `LinearClass.lean`.
* **X-REQ-T2 (table).**  In the summary table of §10 of the theory report, consider (i) a row
  "Hilbert ball with a Walsh spectrum of bounded order `m`: `≍ n^m` evaluations, deterministic,
  for `min` and `ln Z`; exponential with exponent `h(α)` for orders up to `αn`" (this report,
  Corollary 4), and (ii) replacing "no lower bound known" in the row of linear classes by
  "for additive features `O(R²ε₁⁻² ln δ⁻¹)` random evaluations suffice at accuracy `ε₁n`"
  (Proposition 11).  Both are short enough to be checked by a referee in an hour.
* **X-REQ-T3 (a question).**  Is `sup { ln E_unif exp(½ sᵀJs) : J symmetric, zero diagonal,
  ‖J‖_F ≤ F }` attained at `J ∝ 𝟙𝟙ᵀ − I` up to a gauge transformation, for every `n` and every `F`?
  Proposition 5′ proves it asymptotically for `F < 1` (Gaussian domination); numerics for
  `n ≤ 12` say yes for `F > 1` as well.  A proof would give the exact width of `ln Z` over the
  order-2 ellipsoid and an exactly solvable relative of Theorem 11.33.
* **X-REQ-T4 (wording).**  D28 and the README present the exponential price as a property of
  "point evaluations under a first-order envelope".  Proposition 8(c) suggests adding the
  converse reading explicitly: *no procedure that is correct on a first-order class can be
  cheap on any subclass* — so a cheaper paradigm necessarily gives up correctness on the
  first-order class, and says which members it gives up.

**To the engineering division.**

* **X-REQ-E1 (computation; estimated minutes to an hour on the existing enumeration data).**
  *Motivation:* compare the cover format with the span/ellipsoid format on real chain
  geometry.  *Inputs:* the enumerated conformation sets of `ENG-RES-0002`/`0007` (diamond
  lattice `n = 5…24` torsions; off-lattice `n = 5…12`), their pair-count profiles.
  *Formulation:* with the feature map `x ↦ Φ(x) = ` (cumulative pair-count profile on the grid of
  attained squared distances, per pair type) and the kernel `K(x,y) = Φ(x)ᵀ W Φ(y)`, `W` the Gram
  matrix of a smooth kernel on distances (take `κ(s,s′) = exp(−(s−s′)²/2ℓ²)`, `ℓ ∈ {1, 2, 4}` in
  lattice units), run the greedy design "add `argmax_x P_A(x)`" and record
  `N(η) = min{|A| : max_x P_A(x) ≤ η·max_x P_∅(x)}` for `η ∈ {½, ¼, 0.1, 0.01}`, and the
  eigenvalue tail `M(η)` of the kernel matrix over profile classes.  *Expected output:* a table
  `N(η)`, `M(η)` against chain length, next to the published cover sizes
  (`[80, 92]`, `[757, 788]`, …).  *Validation:* `N ≥ M(η)` must hold (Theorem 3(a) holds for any
  kernel); `P_A` must vanish on `A`; on the lattice with one feature per type `N` must equal the
  rank reported in the theory report (3).  *Stopping:* largest enumerated size or one hour.
  *What it decides:* whether, on chain geometry, the number of evaluations in a
  linear-information class saturates with the chain length where the cover format grows.
* **X-REQ-E2 (computation).**  On the same data, for the synthetic residuals already used
  (`L = 1` profile class), report the slack `κ = (realised increment)/(certified constant)` of
  the per-torsion and profile envelopes at each size.  §3.3 shows that `κ` decides the cost
  of the envelope paradigm more than anything else; it has not been reported.
