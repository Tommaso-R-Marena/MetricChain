# Inference limits — addenda (material for version 3)

*Science division, coordinator's thread.  2026-11-25.  These statements were obtained after
the copy of `INFERENCE_LIMITS.md` (version 2) went to our own referee (workstream R3); they
are kept apart so that the referee's copy does not change under review, and will be merged
with the referee's corrections.  **They have been read by nobody but their author.**
Labels and notation as in `INFERENCE_LIMITS.md`.*

---

## A1. The non-adaptive exponent is unchanged by a marginal oracle as well (closes §13, item 1)

**Theorem 4′ [P; uses theory report Theorem 11.45(a), which is machine-checked].**  Cube
class, zero known part, `u = βc`.  Let `C` be a linear code of dual distance `> k`, and let
`D_R = n ln(1 + e^{−u}) − ln Σ_j C(n,j) e^{−u·max(j,R)}` be the drop of `ln Z` when a cone is
flattened at radius `R` (theory report Theorem 11.45(b)).  Consider randomised algorithms
whose set of evaluated points does not depend on the values of `g` but may depend on **all
marginals of `μ_g` on at most `k` sites, given exactly and for free**, and which are
`(ε/2, δ)`-correct for `ln Z` on the class.  If `ε < D_R − ln|C|`, such an algorithm evaluates at
least `(1 − 2δ)·2ⁿ/(|C|·|B(R−1)|)` points in expectation.

*Proof.*  For a centre `s` put `d_C(x) = d_H(x, s + C)`, `cone^C_s = c·d_C`,
`flat^C_s = c·max(d_C, R)`.  Both are in the class (a distance to a set is 1-Lipschitz) and
invariant under translation by `C`, so by Lemma 1 their Gibbs measures have uniform `k`-body
marginals: on this family the oracle always returns the same answer, and the algorithm
restricted to the family is non-adaptive in the sense of Theorem 11.45(a).  The two members
of a pair differ exactly on `{d_C < R}`, a union of `|C|` balls, so every point lies in the
difference sets of at most `|C|·|B(R−1)|` centres.  It remains to bound the separation.  With
`A = Z(cone^C_s)`, `F = Z(flat^C_s)`, and `A₁ = (1 + e^{−u})ⁿ`, `F₁` the same for `C = {0}`:
`t ↦ (e^{−ut} − e^{−uR})₊` is non-increasing and `d_C ≤ d_H(·, s)`, so `A − F ≥ A₁ − F₁`; and
`e^{−u·max(d_C, R)} = max_{a∈C} e^{−u·max(d_H(·, s+a), R)}` gives `F ≤ |C|·F₁`.  Hence
`A/F ≥ 1 + (e^{D_R} − 1)/|C| ≥ e^{D_R}/|C|`, that is, `ln A − ln F ≥ D_R − ln|C| > ε`.  Apply Theorem
11.45(a) with unit weights on the `2ⁿ` centres.  ∎

**Corollary.**  Since `ln|C| ≤ ⌈k/2⌉ ln(2n) = o(n)` and `n⁻¹D_{ρn} → KL(ρ‖p_u)`, the exponent of
non-adaptive algorithms with the oracle is `θ_na(ε₁)` at extensive accuracies and
`KL(p_u‖½)` at every bounded accuracy — the values without the oracle (theory report Theorem
11.45(c)).  Together with Theorem 4: **on the cube class with zero known part, neither the
adaptive nor the non-adaptive exponent is changed by free, exact knowledge of all `k`-body
marginals, for every `k = o(n/ln n)`.**

**With a field the answer may be different [C].**  For a `p`-biased reference there is no
translation symmetry.  A family of dips leaves the `k`-body marginals untouched only if its
*excess mass* has the marginals of the reference, which forces the type of the centres
(`τ(1−δ) + (1−τ)δ = p`, `δ` the typical distance inside a dip) and needs centres drawn from a
`k`-wise independent `τ`-biased law.  An additive counter-term cannot be used to restore the
marginals, because it would differ from the instance at every point.  So with a field a
one-body marginal oracle restricts the adversary to dips of one centre type, and the
exponent with the oracle should be the hinted exponent *restricted to that type* — possibly
strictly smaller than `R^max` of theory report Theorem 11.64.  If so, local data are worthless
on the uniform cube only because of its symmetry.  This is a precise question for the
theory division.

## A2. Extensive stability of maximum-entropy refinement (§6, open item (i))

**Theorem 7′ [P; uses Marton's transport inequality, K].**  In the setting of Theorem 7 let
`X = ∏_{i≤n} X_i`, let the refined ensemble `ν` be a product measure (for instance: the features
are single-site), and let the remainder `r` have single-site bounded differences `c`.  Then

    KL(μ‖ν) ≤ n(βc)²/2,        W₁(μ, ν) ≤ nβc/2,
    |E_μψ − E_νψ| ≤ a·nβc/2   for every ψ with single-site bounded differences a,

`W₁` the transport distance for the Hamming metric.  More generally, if `ν` satisfies
`W₁(μ′, ν) ≤ (2κn·KL(μ′‖ν))^{1/2}` for all `μ′` (a transport–entropy inequality with constant `κ`;
`κ = ¼` for product measures), then `KL(μ‖ν) ≤ 2κn(βc)²` and `W₁(μ,ν) ≤ 2κnβc`.

*Proof.*  By Theorem 7(i), `KL(μ‖ν) ≤ KL(μ‖ν) + KL(ν‖μ) = β(E_νr − E_μr) ≤ βc·W₁(μ,ν)`
(Kantorovich–Rubinstein: `r` is `c`-Lipschitz for the Hamming metric), and
`W₁ ≤ (2κn·KL(μ‖ν))^{1/2}`; solve for `KL`.  ∎

So the *per-site* error of the refinement for extensive Lipschitz observables is at most
`2κ·βc`, whatever the size of the system: linear in the strength of the unmeasured part of
the energy.  The transport constant `κ` is a property of the refined model `ν`, which the
analyst knows.  *Numerical check* (`extensive_stability_check.py`; cubes of 6–10 sites, 900
instances, remainders of four kinds): largest `KL/(n(βc)²/2) = 0.12`, largest ratio for
observables `0.24` — the bound holds with room; Theorem 2 gives `≈ n(βc)²/8` from below, so
the constant is within a factor four of best possible **[N]**.

## A3. Ratios of macrostate partition functions: a reduction (§7; §13, item 6)

**Proposition 10 [P].**  Let `A, B ⊂ X` be disjoint and `d` an envelope.  Then

    sup_{g admissible} Z_g(A)/Z_g(B)  =  sup_{v admissible on B}  Z_{f + L[v]}(A) / Z_{f+v}(B),
    L[v](x) = max_{y∈B} ( v(y) − d(y, x) ),

and in the weights `w = e^{−βv}` on `B` the right-hand side is a linear-fractional programme
(maximise the concave piecewise-linear `Σ_{x∈A} μ₀(x)·min_{y∈B} e^{βd(y,x)} w(y)` subject to
`Σ_B μ₀w = 1` and `w(y) ≤ e^{βd(y′,y)} w(y′)`).

*Proof.*  Points outside `A ∪ B` do not enter the ratio, and every admissible function on
`A ∪ B` extends (McShane).  For fixed `v = g|_B`, the admissible `g` on `A` are bounded below by
`L[v]` (from `v(y) − g(x) ≤ d(y,x)`), and `L[v]` together with `v` is admissible on `A ∪ B` by the
triangle inequality; the ratio is decreasing in `g|_A`.  ∎

*Special cases.*  `B = {y}`: `sup = Σ_{x∈A} e^{−β(f(x) − f(y) − d(y,x))}` — the odds form of theory
report Theorem 11.12.  In general `v` is not constant at the optimum: the part of `B` that is
far from `A` is raised (the three-point example of §7 is the mirror image).  The structure
of the extremal `v` on product spaces — and whether the programme decomposes over sites
for macrostates defined by one coordinate or by a counting statistic — is open and is the
content of our request to the theory division.

## A4. Three ways to compute identified sets under a model, an envelope class and data

For `sup{E_μψ : μ = μ_g, g in the class of constant b, E_μΦ ∈ D}` on a product space:

1. **Exact** — the linear-fractional programme in the weights (§11.4): `|X|` variables,
   single-site constraints; done up to 10 beads.
2. **Outer bound, kernel-checkable [P]** — for a *product* reference the class is contained
   in the divergence ball `KL(μ‖μ₀) ≤ ρ_b := Σ_i K_i(b)`, where `K_i(b)` is the largest
   divergence of a single-site tilt in the class (`ln 2 − h(σ(b))` for a uniform binary
   site), and this is exact: by the chain rule every conditional law of `x_i` given
   `x_{<i}` lies in the single-site class, and the product of the single-site maximisers is
   in the class.  Then the Donsker–Varadhan certificate of §8 applies with `ρ = ρ_b`: an
   upper bound from two certified partition functions.  It is an *outer* bound; how loose
   it is has not been measured (for a reference that is not a product measure, such as a
   self-avoiding chain, `ρ_b` must be replaced by `n` times the largest single-site
   divergence over all conditional references).
3. **Exact for additive targets and single-site data on a product reference [P]** — the
   conditional law of each site lies in its single-site class, so
   `sup E_μ Σ_iψ_i = Σ_i sup_{single-site class} Eψ_i`, attained by a product tilt; with data on
   single-site features the Lagrangian relaxation is exact and the identified set is a
   `K`-dimensional convex minimisation of a sum of single-site suprema.  (For the mean
   magnetisation without data this is the half-width `½ tanh(u/2)` of theory report Theorem
   11.35.)

For targets and features that are pairwise in the site variables only 1 and 2 are
available; a tractable exact dual is the open problem of §8 ("flows with gains").

## A5. Theorem 7 sharpened, and attributed (workstream M, follow-up; checked by the coordinator)

**Theorem 7, sharp form [P; workstream M; `stability_sharpened_check.py`: 2 950 random
instances, all three ratios reach 1.0000].**  In the setting of Theorem 7, with `w = β·osc(r)`:

    KL(μ‖ν) ≤ w²/8,        TV(μ, ν) ≤ tanh(w/4),        KL(μ‖ν) + KL(ν‖μ) ≤ w·tanh(w/4).

*Proof.*  (i) `ν` is also the *reverse* I-projection of `μ` on the exponential family
`{ν_θ ∝ μ₀e^{−θ·Φ}}` (moment matching is maximum likelihood), so
`KL(μ‖ν) ≤ KL(μ‖ν_{βλ})`, and `μ ∝ ν_{βλ}e^{−βr}` is a tilt by a function of oscillation `w`:
`KL = ∫₀^β t·Var_t(r) dt ≤ w²/8`.  (ii) For any two laws the symmetrised divergence satisfies
`J ≥ 4·TV·artanh(TV)` (equality for a binary symmetric pair); with `J ≤ w·TV` from Theorem
7(i): `artanh(TV) ≤ w/4`.  ∎

*Attribution.*  The ingredients are textbook (I-projection and its Pythagorean identity,
the Jeffreys identity, Pinsker).  The principle "the error of moment matching is at most a
constant times the square of the part of the log-density outside the span" is Lemma 1 of
Barron–Sheu (1991), read by the workstream only as quoted in a later paper.  **Not found:**
the dimension-free statement for ensemble refinement; reviews of the refinement literature
up to 2025 give no error bound of this kind, only cross-validation (workstream M,
`SM_REPORT.md` §8).  Theorem 7′ is the transport-inequality mechanism of theory report
Theorem 11.14.  We present Theorem 7 as a known mechanism applied to a question for which
no statement was found.

## A6. Theorem 8: the established names, and a remark on sampling

*Names.*  `ρ_min(D)` is the quantity `δ̂` of Christensen–Connault (2023, §3.3) and the *extent
of falsification* / *falsification frontier* of Masten–Poirier (arXiv:1812.11598); its dual
is the exponential-tilting / empirical-likelihood test statistic for moment conditions
(Kitamura–Stutzer; Schennach).  We adopt "extent of falsification".  According to the
workstream's searches the ensemble-refinement literature uses the relative entropy of a
reweighted *sample* as a diagnostic and does not use this test.  **Not found:** a
sampling-independent (certified) lower bound on it for a molecular model, and the
density-ratio analogue `b_min`.

*Remark (workstream M) [P].*  For a sample of size `N` from the model, the plug-in value
`ρ̂_N = sup_λ [−λ·m − ln N⁻¹Σ_s e^{−λ·Φ(x_s)}]` satisfies `E ρ̂_N ≥ ρ_min` (Jensen, twice).  So on
average **finite sampling makes a model look more wrong than it is**: the two sources of
disagreement with experiment are confounded with a definite sign.  A certified lower bound
errs, by construction, only in the other direction.

## A7. Pinned marginals (as first written — see the correction that follows it)

> **Correction (same day; SCI-MSG-0004).**  The "Reading" of this section says that what
> separates pinned marginals from the other rows "is not the order of the observable".
> That is wrong in the exact-oracle model: a conditional marginal is a ratio of marginals
> of higher order of the unperturbed ensemble, and the denominator of the formula below
> is the `n`-body marginal `μ_g(x*)`.  Pinning is a way of *measuring* high-order
> information, not a different kind of information.  The proposition itself is correct;
> the table and its interpretation are replaced by A8.

**Proposition 4″ (self-reducibility) [K; the reduction of counting to conditional marginals,
Jerrum–Valiant–Vazirani 1986 — from memory, not re-read; the identity checked numerically].**
Let an oracle return one-body marginals of the Gibbs measure *conditioned on a partial
assignment* ("pinned").  For any `x*`,

    Z_g = e^{−β(f+g)(x*)} / ∏_{i=1}^{n} μ_g( x*_i | x*_1, …, x*_{i−1} ),

so `n` pinned one-body marginals and **one** evaluation of `g` determine `Z_g` exactly; with
each marginal known to relative accuracy `τ` the error of `ln Z_g` is at most `nτ + O(nτ²)`.  In the
cube class every conditional probability is at least `1/(1+e^{b})`, so absolute accuracy
`τ/(1+e^{b})` suffices.

*Reading.*  Together with Theorems 4, 4′, 5 and Proposition 5b this gives the picture for
the cube class with zero known part:

| second oracle | worst-case cost of `ln Z` to bounded accuracy |
|---|---|
| none | `e^{nh}` evaluations (theory division) |
| all `k`-body marginals of the unperturbed ensemble, exact | unchanged up to `(2n)^{⌈k/2⌉}` |
| mean residual energy of the unperturbed ensemble | unchanged in the exponent (the zero residual becomes easy) |
| one-body marginals of `n` successively *pinned* ensembles | `n` oracle calls and one evaluation |

What separates the last row from the others is not the order of the observable but that
the measurement is made on a **perturbed (constrained) ensemble**.  The physical
counterparts are measurements on systems in which a degree of freedom has been fixed or
biased — restrained, cross-linked, chemically locked — and, in the limit of small
perturbations, response measurements.  This suggests the precise form of the question
"which experiments are worth what": the value of a measurement to certification is
governed by *which family of perturbed ensembles it has access to*, and local measurements
on the unperturbed ensemble are the uninformative end of that scale **[H for the physical
reading]**.

## A8. The order of marginal information against evaluations (replaces the reading of A7)

**Theorem 4‴ [lower bound P (Theorem 4 + Gilbert–Varshamov); upper bound P given theory
report Theorem 11.58; not checked numerically].**  Cube class, zero known part, bounded
accuracy, `h_hint = ln 2 − h(Λ₁/u)`.  With all marginals of `μ_g` of order at most `K` given exactly
and for free, the worst-case exponent `θ` satisfies: `θ = h_hint` for `K = o(n/ln n)`;
`h_hint − h(α) ≤ θ ≤ (1 − α)h_hint` for `K = αn`, `0 < α < ½`; `θ = 0` for `K = n`.

*Proof.*  Lower bound: Theorem 4 with `C = D^⊥`, `D` a linear code of minimum distance `> αn` and
rate at least `1 − h₂(α) − o(1)` (Gilbert–Varshamov), so `|C| ≤ e^{n·h(α)+o(n)}`.  Upper bound: for
`|S| = K`, `Z_g = Z_g(x_S = a)/μ_g(x_S = a)`; the denominator is given and the numerator is the
partition function of a `u`-Lipschitz function on a cube of `n − K` sites.  ∎

For `u = 1`: `h_hint = 0.0291`, and the lower bound stays positive for `α < α₀ ≈ 0.0046`.  The
gap between the bounds is open.

| free information besides evaluations | worst-case exponent |
|---|---|
| none | `h_hint` |
| all marginals of order `o(n/ln n)` | `h_hint` |
| all marginals of order `αn` | in `[h_hint − h(α), (1 − α)h_hint]` |
| the mean residual energy | `h_hint` in the worst case; `0` at the zero residual |
| the full law at one point | `0` |

*Physical reading* **[H]**.  A marginal of order `K` of the unperturbed ensemble is not
measurable for large `K` (the event has exponentially small probability); restraining or
pinning `K − 1` degrees of freedom prepares the conditional ensemble and makes a one-body
measurement carry order-`K` information.  That is the sense in which perturbed ensembles
are the informative experiments.

## A9. Finite precision: what A7 was trying to say, stated correctly

Model: every measured number carries an absolute error of at most `τ > 0`.  Correlation
functions are the expectations of the characters `χ_T(x) = (−1)^{Σ_{i∈T} x_i}`.

**Theorem 2-τ (correlations of every order) [P; exact enumeration,
`finite_precision_check.py`].**  For the mixture `ν_{C,b}` of Theorem 2,

    E_ν χ_T = tanh(b/2)^{|T|}   if T is a word of C^⊥,        E_ν χ_T = 0   otherwise.

Hence, if the dual distance of `C` is at least `k_τ := ⌈ln(1/τ)/ln coth(b/2)⌉`, **every
correlation function of `ν_{C,b}`, of every order up to `n`, is within `τ` of the uniform
ensemble's**, while `S(ν_{C,b}) ≤ n·h(σ(b)) + ln|C|` with `|C| ≤ (2n)^{⌈k_τ/2⌉}`.
*Proof.*  `X = Y ⊕ E` with `Y` uniform on `C` and `E` i.i.d. Bernoulli(`1 − σ(b)`):
`E χ_T(X) = E χ_T(Y)·E χ_T(E) = [T ∈ C^⊥]·(2σ(b) − 1)^{|T|}`.  ∎

For `b = 1` and `τ = 1 %`: `k_τ = 6`, `|C| ≤ (2n)³`.  Thermal noise attenuates a correlation of
order `j` by `tanh(b/2)^j`; beyond the order `k_τ` nothing is left to measure, whatever the
ensemble hides there.

**The same for the query lower bound [exact formula P, enumerated; the asymptotic step a
sketch].**  For the `C`-symmetrised dip of Theorem 4 with disjoint balls, `E_μ χ_T = 0` unless
`T ∈ C^⊥`, and then, with `j = |T|` and `κ_j(d) = K_j(d)/C(n,j)`,

    E_μ χ_T = χ_T(a) · Z⁻¹ · |C|·2^{−n} Σ_{d<r} C(n,d)(e^{u(r−d)} − 1)·κ_j(d).

The excess mass sits on the shell `d ≈ n/(1+e^{u})` and `κ_j(d) → (1 − 2d/n)^j` for fixed `j`, so
`|E_μ χ_T| ≤ (1 + o(1))·tanh(u/2)^{j}`: with correlations of *every* order known to absolute
precision `τ`, the lower bound of Theorem 4 is divided by at most `(2n)^{⌈k_τ/2⌉}` for all large
`n` — **`h_hint` is unchanged by finite-precision correlation data of any order [P sketch;
proved with explicit constants in A10]**.
(Compare A8: with *exact* marginals of order `αn` the exponent does drop.  The drop needs
probabilities of size `2^{−αn}` to be known to relative accuracy.)

**Proposition 4″-τ (pinned ensembles) [P; 200 random instances, largest error 0.36 of the
bound].**  If the one-body marginals of the `n` successively pinned ensembles of A7 are each
known to absolute precision `τ`, then in the class of constant `u`

    | ln Z_g − ( −β(f+g)(x*) − Σ_i ln m̂_i ) |  ≤  n·τ·(1 + e^{u}) + O(n τ²),

because every conditional probability is at least `1/(1+e^{u})`.

**Reading (kept apart from the statements, and not yet sent to the other divisions).**
With finite precision the distinction that A7 mis-stated becomes true: measurements on
the unperturbed ensemble, of any order, are worth a polynomial factor; `n` one-body
measurements on pinned ensembles, each no more precise, determine `ln Z` to `O(nτ)`.  Pinning
converts absolute precision on a conditional ensemble into relative precision on an
exponentially small probability of the unperturbed one.  That, and not the order of the
observable, is what a perturbed ensemble buys.

## A10. Finite precision, proved: the attenuation lemma and Theorem 4-τ (closes `OPEN_PROBLEMS.md` A3)

A9 gave the exact formula for the correlation functions of a symmetrised dip and a sketch
of their size.  Here is the proof, with constants valid for every `n`.

Notation: `z = e^{−u}`, `t = tanh(u/2) = (1−z)/(1+z)`, `p_u = z/(1+z) = 1/(1+e^{u})`;
`κ_j(d) = K_j(d)/C(n,j)` is the normalised Krawtchouk polynomial, i.e. the average of `χ_T(x)`
over the sets `T` of size `j` for any `x` of weight `d` (equivalently over the `x` of weight
`d` for any `T` of size `j`); so `|κ_j(d)| ≤ 1`.  The dip of radius `r` at the origin is the
weight `w_r(x) = 1 + (e^{u(r−|x|)} − 1)_+` (residual `−u(r − |x|)_+`, admissible), and

    S_j(r) := Σ_x (w_r(x) − 1)·χ_T(x) = Σ_{d<r} C(n,d)(e^{u(r−d)} − 1)·κ_j(d)        (|T| = j),

so that `Z(w_r) = 2ⁿ + S_0` and the dip changes `ln Z` by `Δ_r = ln(1 + 2^{−n}S_0(r))`.

**Lemma A10.1 (full cone) [K — the generating function of the Krawtchouk polynomials].**
`Σ_{d=0}^{n} C(n,d) z^d κ_j(d) = (1−z)^j (1+z)^{n−j}`.  *Proof.*  `Σ_x z^{|x|}χ_T(x) = ∏_{i∈T}(1−z)·∏_{i∉T}(1+z)`. ∎
So for the cone weight `e^{−u|x|}` on the whole cube the correlation function of order `j`
is `t^j` **exactly**: thermal noise at strength `u` attenuates a correlation of order `j` by
`tanh(u/2)^j`.

**Lemma A10.2 (dips) [P; exact rational Krawtchouk values, `n ≤ 800`, `dip_attenuation_check.py`].**
Let `A = e^{ur}(1+z)ⁿ`, `V = Σ_{d<r} C(n,d)`, `η = P[Bin(n, p_u) ≥ r]` and `ξ = η + V/A`.  Then for
every `0 ≤ j ≤ n`

    | S_j(r)/A − t^j |  ≤  ξ ,        and, if ξ < 1,        | S_j(r)/S_0(r) − t^j |  ≤  2ξ/(1 − ξ) =: τ₀(r).

*Proof.*  `S_j = e^{ur}Σ_{d<r}C(n,d)z^dκ_j(d) − Σ_{d<r}C(n,d)κ_j(d)`.  By A10.1 the first sum,
extended to all `d`, is `A·t^j`; the extension costs at most `e^{ur}Σ_{d≥r}C(n,d)z^d = A·η`
(because `|κ_j| ≤ 1` and `C(n,d)z^d/(1+z)ⁿ` is the binomial law with parameter `p_u`); the
second sum is at most `V`.  So `S_j/A = t^j + e_j` with `|e_j| ≤ ξ`, and
`S_j/S_0 − t^j = (e_j − t^j e_0)/(1 + e_0)`. ∎

Size of `ξ`.  The sensitive radius is `r ≈ ρ₀n` with `uρ₀ + ln(1+z) = ln 2`, i.e.
`ρ₀ = u⁻¹∫₀^u p_s ds > p_u`: there `A ≈ 2ⁿ`, `η ≤ e^{−n·KL(ρ₀‖p_u)}` and `V/A ≤ e^{−n(ln 2 − h(ρ₀))} = e^{−n·h_hint}`;
for larger radii (extensive accuracy) both terms are smaller.  Computed: `τ₀ = 1.9·10⁻², 1.3·10⁻³,
2.7·10⁻⁶, 1.7·10⁻¹¹` at `n = 100, 200, 400, 800` for `u = 1` (the true deviation
`max_j|S_j/S_0 − t^j|` is five to ten times smaller), and `10⁻⁵ … 10⁻³⁵` for `u = 2`.

**Theorem 4-τ (correlation data of every order, absolute precision `τ`) [P].**
Cube class with constant `u`, zero known part.  Let the algorithm have, besides
evaluations, a **correlation oracle with tolerance `τ`**: for the instance `g` it returns
numbers `m_T`, one for every non-empty `T ⊆ [n]`, subject only to `|m_T − E_{μ_g}χ_T| ≤ τ`.
Let `r` be a radius with `Δ_r > ε` and `τ > τ₀(r)`, put

    k_τ := ⌈ ln(1/(τ − τ₀)) / ln coth(u/2) ⌉ ,

and let `C` be a linear code of dual distance at least `k_τ`.  Then every algorithm that is
`(ε/2, δ)`-correct for `ln Z` on the class makes, on the zero residual (with the legal
oracle answer `m ≡ 0`), at least

    (1 − 2δ) · 2ⁿ / ( |C| · V(n, r−1) )

evaluations in expectation; and `|C| ≤ (2n)^{⌈(k_τ − 1)/2⌉}` is available (duals of BCH
codes).  Consequently **the worst-case exponent is `h_hint`, unchanged, for every tolerance
`τ ≥ exp(−o(n/ln n))`**; for `u = 1`, `τ = 1 %` and `n ≥ 200` the lower bound of theory report
Theorem 11.25(a) is divided by at most `(2n)³`.

*Proof.*  For a centre `a` let `w_a = |C|⁻¹Σ_{c∈C} w_r(· ⊕ a ⊕ c)`: an average of translates
of an admissible weight, hence admissible (the weight cone is convex and
translation-invariant), with `Z(w_a) = 2ⁿ + S_0`.  Its Fourier coefficients are
`Σ_x w_a(x)χ_T(x) = χ_T(a)·[T ∈ C^⊥]·(2ⁿ[T = ∅] + S_{|T|})`, so for `T ≠ ∅`

    | E_{μ_{w_a}} χ_T |  =  [T ∈ C^⊥] · |S_{|T|}| / (2ⁿ + S_0)  ≤  t^{|T|} + τ₀  ≤  t^{k_τ} + τ₀  ≤  τ ,

because the non-zero words of `C^⊥` have weight at least `k_τ` (Lemma A10.2).  The answer
`m ≡ 0` is therefore legal for the zero residual and for every `w_a`.  The residual `−ln w_a`
vanishes at `x` unless `d(x, a ⊕ C) < r`; one evaluation meets at most `V(n, r−1)` of the
`2ⁿ/|C|` cosets `a ⊕ C`; and an algorithm that is correct at `0` and at `w_a` must meet the
coset of `a` with probability at least `1 − 2δ` when run at `0` (the two values of `ln Z`
differ by `Δ_r > ε`).  Summing over cosets gives the bound. ∎

*Remarks.*  (1) The tolerance model is the one of published numbers with error bars: the
oracle may return any value inside the bar.  It is not a model of access to the ensemble:
a **sample** `x ~ μ_{w_a}` lies in a dip with probability at least `S_0/(2ⁿ + S_0) = 1 − e^{−Δ_r}`,
and one evaluation at the sample then reveals the dip — against a sampler this family of
instances is not hard at all **[P for this family; no statement about the class]**.  What
separates the two is exactly the difference between averages known to absolute precision
and configurations drawn from the ensemble.  (2) Together with A8: exact marginals of order
`αn` lower the exponent; marginals of *every* order with tolerance `e^{−o(n/ln n)}` do not.
The crossover — tolerance `e^{−γn}` — is open (`k_τ` becomes proportional to `n` and the
question merges with `θ(α)` of A8).  (3) The statement is about the worst case of the
class.  For Theorem 2-τ (entropy) the corresponding statement is exact (A9).

## A11. Observable free energies: for monotone macrostates the robust interval is attained at two fields (answers SCI-REQ-0001 Q1(a),(b) in one setting; supersedes the pessimism of A3)

A3 reduced the robust ratio of two macrostate partition functions to a linear-fractional
programme and showed by a three-point example that the extremal residual need not be
constant on a macrostate.  Here is a setting — binary sites, a known part without
frustration, macrostates that are monotone in the site variables — in which the programme
has a closed-form solution, the extremal residuals are *additive*, and the answer is
computable by the existing partition-function certificates.

**Setting.**  `X = {0,1}ⁿ` with the coordinatewise order, `x ∨ y`, `x ∧ y` the coordinatewise
maximum and minimum.  Envelope with separate constants for raising and lowering a site,

    d(x, y) = Σ_{i : x_i = 1, y_i = 0} c_i^↑ + Σ_{i : x_i = 0, y_i = 1} c_i^↓ ,        g admissible  ⇔  g(x) − g(y) ≤ d(x, y),

(`c_i^↑ = c_i^↓ = c_i` is the weighted Hamming envelope).  Known part `f` **submodular**:
`f(x ∨ y) + f(x ∧ y) ≤ f(x) + f(y)` — every additive `f`; every pairwise `f` whose couplings
`J_ij x_i x_j` have `J_ij ≤ 0` (no frustration: a ferromagnet in lattice-gas variables, a
helix–coil model with cooperative nearest-neighbour terms).  `μ_e ∝ e^{−βe}`.  Fields
`h^↑(x) = Σ_i c_i^↑ x_i`, `h^↓(x) = Σ_i c_i^↓ x_i`; both `h^↑` and `−h^↓` are admissible.

**Theorem A11 (sandwich in stochastic order) [P; the tool is Holley's inequality [K]; exact
linear programmes on 900 instances, `monotone_ratio_check.py`; **machine-checked at checkpoint
29** — workstream L2, `experiments/science/ws_L2/Sandwich.lean`: `cube_sandwich_mean`,
`cube_mean_isLeast`, `cube_mean_isGreatest`, `cube_mean_range_eq_Icc`; re-compiled by the
coordinator].**  (*What the formalisation fixed:* the statement is for `β ≥ 0` — it fails
at `β = −1`, `cube_sandwich_fails_negative_beta`; "every value in between" for `β > 0`.  It
needs **no** sign condition on `c_i^↑, c_i^↓`: attainment needs exactly `c_i^↑ + c_i^↓ ≥ 0`, which is
equivalent to the class being non-empty.  And it holds on any finite distributive
lattice with an envelope that two functions saturate — `sandwich_mean`.)  For every admissible `g`

    μ_{f + h^↑}  ≼  μ_{f + g}  ≼  μ_{f − h^↓} ,

i.e. `E_{f+h^↑} φ ≤ E_{f+g} φ ≤ E_{f−h^↓} φ` for every increasing `φ : X → ℝ`; both ends are
attained in the class, and every value in between is attained (the class is convex in
the weights).

*Proof.*  Holley's inequality: for strictly positive probability measures on a finite
distributive lattice, `μ₂(x ∨ y)·μ₁(x ∧ y) ≥ μ₁(x)·μ₂(y)` for all `x, y` implies `μ₁ ≼ μ₂`.
*Lower end:* `μ₁ = μ_{f+h^↑}`, `μ₂ = μ_{f+g}`.  The condition reads

    [f(x∨y) + f(x∧y) − f(x) − f(y)] + [g(x∨y) − g(y)]  ≤  h^↑(x) − h^↑(x∧y).

The first bracket is `≤ 0` (submodularity).  `x ∨ y` differs from `y` exactly on
`{i : x_i = 1, y_i = 0}`, where it is raised, so `g(x∨y) − g(y) ≤ d(x∨y, y) = Σ_{x_i=1, y_i=0} c_i^↑`, and
this is `h^↑(x) − h^↑(x∧y)`.  *Upper end:* `μ₁ = μ_{f+g}`, `μ₂ = μ_{f−h^↓}`; the condition reads
`[f(x∨y) + f(x∧y) − f(x) − f(y)] + [g(x∧y) − g(x)] ≤ h^↓(x∨y) − h^↓(y)`, and
`g(x∧y) − g(x) ≤ d(x∧y, x) = Σ_{x_i=1, y_i=0} c_i^↓ = h^↓(x∨y) − h^↓(y)`.  The normalising constants cancel
in Holley's condition. ∎

**Corollary A11.1 (macrostates) [machine-checked: `cube_macrostate_cross_upper`,
`cube_macrostate_cross_lower`, `cube_ratio_range_eq_Icc`; L2 — and stronger than stated here:
it holds for *any* lower set `A` against *any* non-empty upper set `B`, e.g. two
macrostates separated by a transition region, not only for complements].**  Let `B` be an
up-set (`x ∈ B`, `x ≤ x′ ⇒ x′ ∈ B`) and `A = X ∖ B`, both non-empty.  Over the admissible class the ratio `Z_{f+g}(A)/Z_{f+g}(B)` fills
exactly the interval

    [ Z_{f − h^↓}(A)/Z_{f − h^↓}(B) ,   Z_{f + h^↑}(A)/Z_{f + h^↑}(B) ] :

**the two extremal residuals are the uniform fields, the same for every monotone
macrostate.**  (`φ = 1_B` in the theorem; the odds are monotone in the probability.)
The special case `f ≡ 0`, `φ = |x|/n` is the half-width `½ tanh(u/2)` of the theory report's
Theorem 11.35.

**Corollary A11.2 (width; cancellation; locality).**  For `c^↑ = c^↓ = c`, `h = Σ c_i x_i`:

    ln R⁺ − ln R⁻  =  β ∫_{−1}^{1} Σ_i c_i ( ⟨x_i⟩_{B,t} − ⟨x_i⟩_{A,t} ) dt ,

`⟨·⟩_{S,t}` the mean in `μ_{f + t·h}( · | S)`; every summand is nonnegative (FKG).  **A site
contributes its constant times the difference of its mean occupation between the two
macrostates**: uncertainty that is common to both macrostates cancels exactly, and what
remains is carried by the sites that are correlated with the macrostate under the known
part.  *Proof.*  `∂_t ln[Z_{f+th}(A)/Z_{f+th}(B)] = −β(⟨h⟩_{A,t} − ⟨h⟩_{B,t})`. ∎
Example (ferromagnetic chains, macrostate "site 1 occupied", random fields and couplings):
width `0.78, 2.01, 1.48` for `n = 6, 10, 14` where `2βΣ_i c_i = 6.9, 12.7, 12.4`; the site
contributions decay along the chain (`0.27, 0.11, 0.005, 0.003, 0, 0` at `n = 6`).
Compare `ln Z` itself, whose a-priori width over the class is extensive.

**Corollary A11.3 (certificate).**  For pairwise `f` each end is a ratio of partition
functions of a pairwise model with shifted one-body terms.  If the macrostate is a box
(`B = {x_i = 1 for i ∈ I}`; `Z(A) = Z − Z(B)`) these are outputs of a partition-function
certificate as it stands; for a counting threshold `B = {Σ_{i∈I} x_i ≥ r}` the level partition
functions are needed (a kernel over polynomial weights; request K-T2 of SCI-MSG-0005).
No flow with gains is needed in this setting.

**The hypotheses are needed [N, exact linear programmes].**  With a frustrated pairwise `f`
(random signs) and up-sets `B` the field fails to be optimal in 74, 99 and 122 of 150
random instances at `n = 3, 4, 5`, by a factor up to `e^{1.9}` in the ratio.  With a
ferromagnetic `f` and a non-monotone `B` it fails in 134 of 148 and 146 of 150 (`n = 3, 4`).
With both hypotheses it is optimal in 900 of 900 (to `5·10⁻¹⁴` in the logarithm).  *A
numerical trap recorded:* with default solver tolerances and unscaled weights three of the
900 instances showed deviations of `10⁻⁶ … 10⁻⁵`; in scaled variables with tolerances `10⁻¹⁰`
they vanish (`10⁻¹⁵`).

*Remarks.*  (1) *Ordered alphabets.*  The proof works on a product of finite chains
whenever each site's envelope is additive along its order (`d_i(s,t) = Σ_{r=t}^{s−1} c_i^↑(r)` for
`s > t`); then the extremal residuals are the additive functions that saturate it.  For
the discrete envelope `c_i[s ≠ t]` on three or more unordered states no additive function
saturates the envelope and the argument fails.  (2) *Symmetry.*  When a group preserves
`f`, `d`, `A` and `B`, averaging the weights over the group changes neither `Z(A)` nor `Z(B)` and
stays in the class; so extremal residuals can be taken invariant in the weights.  On the
uniform cube with threshold macrostates this alone gives the field.  (3) *What is not
covered.*  Evaluations: with anchors the consistent class is no longer invariant and the
extremes are not fields; the theory division's "no cancellation" (their §11.13) is a
statement about the *cost* of certifying a difference for uncoupled macrostates, not
about its range.  Frustrated known parts; non-monotone macrostates; unordered alphabets
(rotamers) — there the linear-fractional programme of A3 is what remains.  (4) *Prior
art.*  Holley's inequality (1974) and the monotonicity of Gibbs measures in a field are
textbook.  That an *arbitrary* perturbation with bounded single-site differences is
sandwiched between the two fields is a two-line application which one search did not
find stated; we expect it to be folklore in statistical mechanics.  Its use — the exact
robust range of an observable free-energy difference over an uncertainty class, with
cancellation — was not found in the theory branch (which states that it has no closed
form for ratios, THY-RES-0003) nor in that search.

## A12. The oracle-invariance theorem, assembled (the statement our referee called "within reach")

This section proves nothing new.  It puts Theorem 4, addendum A1 and the referee's R5,
R6, R6′ (`workstreams/R3_REPORT.md` §4) into one statement, and records which parts have
been read by whom.

**Theorem A12 (oracle invariance of the complexity diagram of the cube class).**
Cube class `{0,1}ⁿ`, zero known part, `u = βc > 0`; algorithms that return `ln Z` within `ε/2`
with probability `1 − δ` for every member of the class.  Give every algorithm, free and
exact, all marginals of `μ_g` on at most `k` sites, with `k ln n = o(n)`.

(a) *Adaptive algorithms.*  The worst-case number of evaluations is
`exp(n·θ_hint(ε₁) + o(n))` at extensive accuracies `0 < ε₁ < ln cosh(u/2)` and `exp(n·h + o(n))` when
`ln(1/ε) = o(n)`, `ε = o(n)` — the values without the oracle.
(b) *Non-adaptive algorithms* (evaluation points chosen from the oracle's answer and
private randomness).  It is `exp(n·θ_na(ε₁) + o(n))`, respectively `exp(n·a + o(n))` — the values
without the oracle.
(c) *With the mean residual energy `E_{μ_g} g` given exactly as well*, the adaptive exponent
at every fixed accuracy `ε < ln(1 + e^{−u})` is still `h`; yet at the zero residual the cost is
`O(n u²/ε²)`.
(d) *With error bars instead of exact marginals*: (a) holds for correlations of **every**
order known to absolute precision `τ ≥ exp(−o(n/ln n))` (addendum A10).

*In words:* the exponents are those of the class, not of the oracle.  Local ensemble data
of bounded order change neither; a calorimetric datum changes the hardest instance, not
the exponent.

| part | lower bound | upper bound | read / checked by |
|---|---|---|---|
| (a) | Theorem 4 (symmetrisation of a dip over a code of dual distance `> k`) | theory report Theorems 11.54, 11.58 (paper proofs; **reviewed by our workstream R6 — the cost accounting stands, SCI-REV-0007**) | author; referee R3 ("proved"); **[V]** given the code (L1: `theorem4_adaptive_marginal_oracle`; the code itself for `k = 1` only) |
| (b) | addendum A1 = theory report Proposition 11.104 = referee's R5 (symmetrised cones; R5(2): the drop of `ln Z` is at least `D_R + ln(1−γ)`, `γ = ½(#C − 1)·cosh(u/2)^{−d_min}`) | theory report Theorem 11.44 (plain Monte Carlo ignores the oracle) | three independent derivations; **[V]** given the code (L1: `theorem4'_nonadaptive_marginal_oracle`); the referee's inequality R5(2) **[V]** (L2: `r5_2_abstract`, `r5_2_binary_cube` — for any finite set of centres with pairwise distances `≥ δ`, no linearity needed) |
| (c) | referee's R6: excess identity R6.1, sign lemma R6.2, overlap bound R6.3 | theory report Theorem 11.58; Corollary of Theorem 5 for the zero residual | referee (author of the proof); **second full reading by the coordinator at checkpoint 21: R6.1, R6.2, R6.3 and the assembly re-derived line by line, no gap found** (notes below); numerics by both; **R6.1 and R6.2 machine-checked at checkpoint 29** (L2, `Referee.lean`: `excess_identity`, `r6_2_signs`, `r6_2_root`, `r6_2_binary_cube`, with the sharper gain `r6_2_root_sharp`; hypotheses made explicit: `u > 0`, `r₁ ≥ 1`; the step at `s = −1` uses `ω_{−1} ≤ ω_{+1}`); R6.3 and the assembly are paper proofs |
| (c) with both oracles | referee's Corollary R6′ (cosets of a code in place of the two centres) | as (c) | referee; **written out and re-derived by the coordinator at checkpoint 25** (notes below); step (3), the two signs and the root for the coset profiles, **machine-checked** (L2: `r6_2_cosets`); steps (1), (4), (5) on paper |
| (d) | addendum A10 | as (a) | author only |

*Notes of the second reading of R6 (coordinator).*  R6.1: with `g′ = min(g₀, T)`,
`Z′ = Σ max(e^{−g₀}, e^{−T}) = Z₀ + E` and `U′Z′ = U₀Z₀ + D`, so `U′ − U₀ = (D − U₀E)/(Z₀ + E)`.  R6.2:
the "free" sums (as if the visible basin were absent) are `E^f_{+1} = e^uW⁺ − |B(n,r₁)|`,
`D^f_{+1} = −e^u(A′ + uW⁺)`, `E^f_{−1} = e^{−u}W − V`, `D^f_{−1} = −e^{−u}(A′ − uW)` (checked term by
term, including the boundary shells `d = r₁` and `d = r₁ − 1`); on the overlap each true
summand lies between the free one and zero because `t ↦ te^{−t}` is increasing for `t < 1`;
hence `E^f − ω ≤ E ≤ E^f`, `D^f ≤ D ≤ D^f + u(r₁+1)ω`.  At `s = +1`:
`D + (A′/Z₀)E ≤ −e^uA′(1 − W⁺/Z₀) − ue^uW⁺ + u(r₁+1)ω < 0`, using `W⁺ ≤ Z₀` (`C(n,r₁)` is one term of
`2ⁿ − V`) and hypothesis (ii).  At `s = −1`:
`D + (A′/Z₀)E ≥ u[e^{−u}W − r₁(e^{−u}2ⁿ + V + ω)] > 0`, using `A′ ≤ ur₁W`, `Z₀ ≥ W`, hypothesis (i)
(`r₁e^{−u}2ⁿ ≤ e^{−u}W/8`, `r₁V ≤ e^{−u}W/8`) and (ii) with `ω_{−1} ≤ ω_{+1}` (`r₁ω ≤ e^{−u}W/2`): the
bracket is at least `e^{−u}W/4`.  Continuity in `s` gives the root.  The gain:
`E_{s*}/Z₀ ≥ (e^{−u}W − V − ω)/(2ⁿ + W) ≥ e^{−u}(1 − 3/(4r₁))`, slightly better than stated.  R6.3:
for `x` uniform on a sphere of radius `j ≤ r₁` about `a′`, `d(x, a₀) = D + j − 2i` with `i`
hypergeometric of mean `jD/n`; the event `d(x,a₀) < r₁` needs `i` to exceed its mean by at
least `(n/2 − r₁ − 2Δ)/2`; Hoeffding's inequality for sampling without replacement gives the
bound.  Hypotheses (i), (ii) hold for large `n` when `ρ₀ < ρ₁ < ½` and the two centres are at
distance `n/2 ± √(n ln n)`, which a random centre satisfies with probability `1 − 2/n²`.

*Corollary R6′ written out (coordinator).*  Let `C` be a linear code of dual distance `> k`,
`|C| = e^{o(n)}`; `g₀^C(x) = −u(r₁ − d(x, a₀+C))₊`, twin `T_s^C(x) = −u(r₁ + s − d(x, a′+C))₊`,
`g′_s = min(g₀^C, T_s^C)`.  (1) Both are functions of distances to cosets of `C`, hence
`C`-invariant, so by Lemma 1 all their `k`-body marginals are uniform: the marginal oracle
cannot tell them apart.  (2) The excess identity R6.1 holds for any pair of functions.
(3) With `N_d = #{x : d(x, a₀+C) = d}`, `W^C = Σ_{d<r₁} N_d e^{u(r₁−d)}`, `V^C = Σ_{d<r₁} N_d`,
`A′^C = Σ_{d<r₁} N_d u(r₁−d)e^{u(r₁−d)} ∈ [uW^C, ur₁W^C]`: the twin at `s = 0` is an exact translate of the
visible function (`d(x, a′+C) = d(x ⊕ a₀ ⊕ a′, a₀+C)`), so its free sums at `s = ±1` are those of
R6.2 with `N_d` in place of `C(n,d)`: `E^f_{+1} = e^u(W^C + N_{r₁}) − V^C − N_{r₁}`, `D^f_{+1} = −e^u(A′^C + u(W^C + N_{r₁}))`,
`E^f_{−1} = e^{−u}W^C − V^C`, `D^f_{−1} = −e^{−u}(A′^C − uW^C)`; and `W^C + N_{r₁} ≤ Z₀ = 2ⁿ − V^C + W^C` because the points
at distance exactly `r₁` are outside the visible region.  The two signs follow as before
from (i) `W^C ≥ 8r₁e^u2ⁿ` — true because `W^C ≥ W` — and (ii) `ω^C_{+1} ≤ e^{−u}W^C/(2(r₁+1))`.
(4) Overlap: `e^{−T^C} ≤ Σ_{c′} e^{−T_{c′}}` and the visible region is a union of `|C|` balls, so
`ω^C_{+1} ≤ |C|²·max` over pairs of centres `(a₀+c, a′+c′)` of the single-pair overlap, each bounded
by R6.3 once every word of `a₀ ⊕ a′ ⊕ C` has weight within `Δ` of `n/2`; for a uniform `a′` and
`Δ = √(n(ln n + ln|C|))` this fails with probability at most `2/n²` (union bound over `C`), and
`|C|²·exp(−(n/2 − r₁ − 2Δ)²/(2r₁))` is exponentially small because `|C| = e^{o(n)}`.  (5) The two
instances coincide outside `{d(·, a′+C) ≤ r₁}`, of size at most `|C|·|B(n, r₁)|`; a uniform `a′`
gives `E[#evaluations] ≥ (1 − 2δ)(1 − o(1))·2ⁿ/(|C|·|B(n, r₁)|)` at `g₀^C`.  So with **both** oracles —
exact `k`-body marginals and the exact mean residual energy — the exponent at bounded
accuracy is still `h`.

**What the theorem does not cover** — unchanged: any known part without the translation
symmetry of the uniform cube (**the field case for one-body data is settled, checkpoint
30:** workstream F, `workstreams/SF_REPORT.md`, Theorems A and B — with a field a free exact
one-body oracle changes neither class exponent, for every `n`, by a compensation lemma;
at an additive instance it does help, and the instance-wise exponent is bracketed;
two-body data with a field: an exact construction at `n = 13` and a sketch; SCI-RES-0006);
the thermodynamic
oracle at extensive accuracy (**addendum A16, added at checkpoint 26: there the
invariance fails** — beyond `a(u)` nats per site the datum alone gives the answer, and
below it the exponent is bracketed by a new "plateau twin"); exact marginals of order
proportional to `n` (addendum A8: there the exponent does drop); samples from the
ensemble (addendum A10, remark 1).

## A13. The sandwich of A11 on ordered alphabets (written out; replaces remark (1) of A11)

**Setting.**  `X = ∏_i {0, …, q_i − 1}` with the product order (a finite distributive lattice);
`d(x, y) = Σ_i d_i(x_i, y_i)` with each `d_i` a quasi-metric on the site alphabet (zero diagonal,
triangle inequality); `g` admissible iff `g(x) − g(y) ≤ d(x, y)`; `f` submodular on the lattice
(for example site terms plus convex functions of the differences of neighbouring sites).
Step fields

    Γ^↑(x) = Σ_i Σ_{r < x_i} d_i(r+1, r) ,          Γ^↓(x) = Σ_i Σ_{r < x_i} d_i(r, r+1) .

**Theorem A13 [P; Holley's inequality [K]; exact linear programmes on 360 instances,
`ordered_alphabet_ratio_check.py`; **machine-checked at checkpoint 29** (L2, `Sandwich.lean`:
`stepField_sandwich_mean`, `stepField_macrostate_ratio`; for a path envelope the
attainment: `chain_mean_range_eq_Icc`, `chain_ratio_range_eq_Icc`; again for any lower set
against any non-empty upper set).  Not machine-checked: "not attained in general
otherwise", which is numerical].**  For every admissible `g`:
`μ_{f + Γ^↑} ≼ μ_{f + g} ≼ μ_{f − Γ^↓}`.  Hence for every up-set `B`, `A = X ∖ B`:

    Z_{f − Γ^↓}(A)/Z_{f − Γ^↓}(B)  ≤  Z_{f+g}(A)/Z_{f+g}(B)  ≤  Z_{f + Γ^↑}(A)/Z_{f + Γ^↑}(B) .

If every `d_i` is additive along the order (a "path envelope": `d_i(s, t)` is the sum of the
unit steps between `t` and `s`), the two step fields are admissible and **both bounds are
attained**.  Otherwise the bounds are sound and not attained in general.

*Proof.*  Holley's condition for the lower end is
`[f(x∨y) + f(x∧y) − f(x) − f(y)] + [g(x∨y) − g(y)] ≤ Γ^↑(x) − Γ^↑(x∧y)`.  The first bracket is `≤ 0`.
`x∨y` differs from `y` on the sites with `x_i > y_i`, so
`g(x∨y) − g(y) ≤ Σ_{x_i > y_i} d_i(x_i, y_i) ≤ Σ_{x_i > y_i} Σ_{r = y_i}^{x_i − 1} d_i(r+1, r)` (triangle inequality along
the order), which is `Γ^↑(x) − Γ^↑(x∧y)`.  The upper end is symmetric.  For a path envelope
`Γ^↑(x) − Γ^↑(y) ≤ d(x, y)` with equality when `x ≥ y`, so the fields are members of the class. ∎

*Numerics.*  Three and four ordered states, three and four sites, random site terms and
convex nearest-neighbour couplings, random up-sets: with path envelopes the bounds equal
the exact linear-programming extremes in 180 of 180 instances (to `3·10⁻¹⁵` in the
logarithm); with the discrete envelope `c_i[s ≠ t]` they are valid in 180 of 180 and
attained in none (slack up to a factor `e^{2.7}` in the ratio).

*What it covers and what it does not.*  Sites with a natural order along which both the
known part is submodular and the uncertainty accumulates additively — occupation
numbers, heights, ordered levels of a degree of freedom.  **Not rotamers:** an unordered
alphabet with the discrete envelope gets a valid but loose bound, and a Potts-type known
part is not submodular for any order of three states.  For those the linear-fractional
programme of A3 remains.

## A14. An illustration of A11 on a classical model: the helix–coil chain (numbers; reading labelled)

*Model (synthetic, classical).*  Zimm–Bragg chain of `n` residues, `x_i ∈ {coil, helix}`,
statistical weight `∏ s^{x_i}·σ^{#helix starts}` with nucleation parameter `σ = 10⁻³`: in
lattice-gas variables a ferromagnetic nearest-neighbour energy, hence submodular.
*Class.*  Every residual whose change under the flip of **one** residue is at most `c`
(in `k_BT`) — whatever its form: an error of the cooperativity, capping, `i/i+4` terms,
sequence effects.  *Theorem A11 says:* for every increasing observable and every monotone
macrostate the extremes over the whole class are those of the two uniform fields, i.e. of
the same chain with `s·e^{−c}` and `s·e^{+c}`.  Exact transfer matrices
(`helix_coil_robust_range.py`); the linear programme over the whole class agrees with the
fields to `10⁻⁶` at `n = 10` (three cases).

| chain | mean helix fraction at `s` | robust interval, `c = 0.05` | `c = 0.1` | `c = 0.3` |
|---|---|---|---|---|
| `n = 20`, `s = 1.2` | 0.336 | [0.224, 0.465] | [0.142, 0.586] | [0.024, 0.830] |
| `n = 50`, `s = 1.0` | 0.218 | [0.104, 0.415] | [0.053, 0.614] | [0.009, 0.879] |
| `n = 50`, `s = 1.2` | 0.788 | [0.703, 0.838] | [0.551, 0.870] | [0.043, 0.932] |
| `n = 100`, `s = 1.0` | 0.347 | [0.145, 0.617] | [0.065, 0.776] | [0.010, 0.934] |
| `n = 100`, `s = 1.5` | 0.955 | [0.947, 0.961] | [0.936, 0.966] | [0.787, 0.979] |

**One residue helical against coil** (the middle one; `c = 0.1`): width of the robust
interval of the log odds `2.0–2.5` at `n = 20`, `1.1–4.0` at `n = 50`, `1.0–4.9` at `n = 100`
(`s = 1.5 … 1.0`), against `2c = 0.2` without cooperativity and `2cn = 4, 10, 20` without
cancellation.  By Corollary A11.2 the width is `2c` times an effective number of residues —
5 to 25 here — and 90 % of it comes from the 12 to 54 residues around the chosen one.

**Reading [H].**  (i) Near the transition a per-residue uncertainty of `0.1 k_BT`
(`0.06 kcal/mol` at 300 K) leaves the helix content of a 50-residue cooperative chain
undetermined over more than half of its range — the textbook sensitivity of a cooperative
transition to its propagation parameter, here as an exact statement about *all* model
errors with bounded single-residue effect, not only about errors of `s`.  (ii) The robust
uncertainty of a *local* conformational free energy is the per-site constant times the
cooperative length (`≈ σ^{−1/2}`), neither `2c` nor `2cn`: cooperativity amplifies local model
error, and cancellation between the two macrostates removes everything beyond the
correlated region.  (iii) Far from the transition (`s = 1.5`, `n = 100`) the same class
determines the helix content to within one or two per cent for `c ≤ 0.1`.  A model, not a
molecule: no parameter here is fitted to anything.

## A15. What a scattering curve of finite range and finite precision determines, model-free (`OPEN_PROBLEMS.md` C4)

*Setting.*  Diamond-lattice chain of `N` identical point scatterers; Debye intensity
`I_x(q) = N + 2Σ_{i<j} sin(qr_ij)/(qr_ij)`, a linear functional of the pair-distance histogram
(workstream A2, Proposition A2.1).  Data: the ensemble-averaged intensity at the first `K`
Shannon channels `q_k = kπ/D_max` (`D_max` the largest possible distance), each within a relative
tolerance `τ`.  Question: the exact range of an unmeasured ensemble average over **all**
ensembles of conformations consistent with the data.  Exact linear programmes
(`experiments/science/pi_chain/scattering_identified.py`); truth = the athermal ensemble.

*Why precision, not range, is the variable.*  `I(q)` is an entire function of `q`: exact
knowledge on any interval determines the whole averaged histogram.  What a curve
determines is therefore a question about its error bars — the same lesson as addenda
A9, A10.

**Unidentified fraction of the a-priori range, 13-bead chain (49 833 conformations) [N,
exact linear programmes]:**

| data | `R_g²` | end-to-end `R²` | gauche fraction | population of the most compact decile |
|---|---|---|---|---|
| `K = 1` (`q_max R_g = 0.6`), exact | 0.06 | 0.42 | 0.75 | `[0, 0.76]` |
| `K = 3` (`q_max R_g = 1.9`), exact | 0.00 | 0.38 | 0.74 | `[0, 0.57]` |
| `K = 12` (`q_max R_g = 7.6`), exact | 0.00 | 0.34 | 0.52 | `[0, 0.53]` |
| full distance histogram, exact (`K → ∞`) | 0 | 0.22 | 0.31 | `[0, 0.50]` |
| `K = 3`, 1 % | 0.09 (`R_g²` within −6 %, +12 %) | 0.45 | 0.77 | `[0, 0.60]` |
| `K = 12`, 1 % | 0.08 (−5 %, +11 %) | 0.43 | 0.59 | `[0, 0.56]` |
| `K = 3`, 5 % | 0.32 | 0.60 | 0.81 | `[0, 0.68]` |
| `K = 12`, 5 % | 0.30 (−16 %, +43 %) | 0.58 | 0.71 | `[0, 0.65]` |

**Three chain lengths under the same instrument [N, exact linear programmes;
`scattering_fixed_instrument.py`, two and a half minutes].**  The same absolute grid of
eleven points up to `q_max = 1.745` per lattice unit (`q_max·b = 3.0` for the bond length `b`; the
Shannon grid of the longest chain, slightly oversampled for the shorter ones) and the
same tolerance; unidentified fractions at exact data / 1 % / 5 %:

| chain (conformations; Shannon channels in range) | `R_g²` | end-to-end `R²` | gauche fraction | compact decile, upper bound |
|---|---|---|---|---|
| 11 beads (5 849; 7.9) | 0.00 / 0.08 / 0.29 | 0.32 / 0.43 / 0.57 | 0.47 / 0.58 / 0.70 | 0.48 / 0.52 / 0.61 |
| 13 beads (49 833; 9.4) | 0.00 / 0.08 / 0.27 | 0.34 / 0.43 / 0.57 | 0.57 / 0.64 / 0.74 | 0.53 / 0.56 / 0.65 |
| 15 beads (422 825; 11.0) | 0.00 / 0.08 / 0.27 | 0.34 / 0.42 / 0.54 | 0.62 / 0.67 / 0.75 | 0.55 / 0.58 / 0.66 |

With the Shannon grids of each chain the picture is the same (`K = 12`, exact: gauche
fraction 0.36 / 0.52 / 0.61 at 11 / 13 / 15 beads; end-to-end 0.31 / 0.34 / 0.34; all rows in
`scattering_identified_n8_10.json`, `scattering_identified_n12.json`).  Consistency: the exact-data
columns lie between the earlier results for `R_g²` alone and for the full histogram
(`INFERENCE_LIMITS.md` §11.1).

**What the numbers say.**
1. A curve fixes `R_g²` and little else: with exact data three channels identify `R_g²` to
   better than 1 % of its range, while the end-to-end distance stays undetermined over a
   third of its range and the population of a compact state anywhere between zero and
   one half — *whatever the range of `q`*.
2. **Precision matters more than range.**  At 1 % precision twelve channels are hardly
   better than three (0.43 against 0.45 for the end-to-end distance); and even `R_g²` is
   then known only to about ±8 %, because the first channels sit where the curve is
   insensitive.  At 5 % the curve leaves `R_g²` itself uncertain by −16 %, +43 %.
3. The population of a compact state is bounded above and never below — the scattering
   analogue of Theorem 3: averaged data exclude dominance and identify no population.
4. **Under one instrument, the local content is determined less and less as the chain
   grows** (three sizes — a trend, not a law): the unidentified part of the gauche
   fraction rises from 0.47 to 0.57 to 0.62 with exact data (0.58, 0.64, 0.67 at 1 %),
   the bound on the compact population drifts upward (0.48, 0.53, 0.55), while the global
   quantities do not change (`R_g²`: ±8 % at 1 % at every size; end-to-end distance: a third
   of its range).  The number of Shannon channels in range grows with the chain (7.9, 9.4,
   11.0) in step with the number of torsions (8, 10, 12), and the unidentified fraction
   grows all the same.  Whether it tends to one for a local observable is the question
   the class tables requested of the engineering division (S-E1) would answer.

*Limits.*  Chains of 11–15 beads on a lattice; identical point scatterers; no solvent
contrast, no hydration shell, no instrument resolution; the tolerance is a hard band at
`K` points (an adversarial error model, as in A10), not a noise model.  The model-free set
is the widest one can honestly report; with a model and its envelope class the intervals
narrow several-fold (`INFERENCE_LIMITS.md` §11.4).  That a scattering curve carries about
`q_max D_max/π` independent numbers is classical (the Shannon-channel count used in the
small-angle literature; cited through workstream M's search log, not read by us); the
exact identified sets as functions of `K` and `τ` are computations, not theorems.


## A16. A thermodynamic datum at extensive accuracy: the entropy bracket and the plateau twin (our own question R3-T3 of SCI-MSG-0008; `INFERENCE_LIMITS.md` §5, "Open (i)")

*Added at checkpoint 26; part (c) (Lemma A16.5, Theorem A16.6) added at checkpoint 28 —
numbering: Propositions A16.1, A16.3, Corollary A16.2, Conjecture A16.4 keep their
numbers.  Everything here is the coordinator's; nothing has been read by a second
party.  Scripts: `experiments/science/pi_inference/plateau_twin_check.py` (30 s),
`terrace_twin_explore.py` (1 min), `energy_isoperimetry_check.py` (4 min).*

*Setting and conventions.*  Cube `Q_n`, zero known part, class `|g(x) − g(y)| ≤ c·d_H(x,y)`,
`u = βc`; units `β = 1` in proofs.  `σ = σ_u = 1/(1+e^u)`, `h` the binary entropy,
`a(u) = ln 2 − h(σ_u) = KL(σ_u‖½)` (the non-adaptive exponent at bounded accuracy),
`ρ₀ = ln(2/(1+e^{−u}))/u`.  The datum is `U = E_{μ_g} g`, exact.  An algorithm is *`ε`-accurate*
if it returns `ln Z_g` within `ε/2` with probability at least `1 − δ` on the whole class (the
convention of the theory report's Theorem 11.25 and of the referee's Theorem R6);
`θ(ε₁)` denotes an exponent at `ε = ε₁n`.  Without the datum the adaptive exponent is
`θ_hint(ε₁) = KL(ρ₀ + ε₁/u ‖ ½) = ln 2 − h(ρ₀ + ε₁/u)` for `0 < ε₁ < ln cosh(u/2)` (theory report
Theorems 11.25(a) and 11.54; `ρ₀ = Λ₁/u` in its notation) and `h = θ_hint(0)` at bounded
accuracy (its Theorem 11.58); beyond the threshold `n ln cosh(u/2)` of its §11.10 the
exponent is zero.  With the datum, the exponent at bounded accuracy is still `h`
(addendum A12(c)).  What the datum is worth at extensive accuracy was open.

**The identity behind everything [K].**  `ln Z_g = S(μ_g) − βU_g`, `S` the Gibbs entropy.  Given
the datum, computing `ln Z` *is* computing the entropy of the ensemble; and two members
of the class with the same datum differ in `ln Z` by exactly the difference of their
entropies.

### (a) The datum alone

**Proposition A16.1 (entropy bracket) [P; checked by enumeration on 400 random members of the
class, `n ≤ 11`].**  For every `g` of the class, `n·h(σ_u) ≤ S(μ_g) ≤ n ln 2`, that is

    n·h(σ_u) − βU  ≤  ln Z_g  ≤  n ln 2 − βU,          width  n·a(u).

Both ends are attained (the cone `c·d_H(·, b)`; the zero residual).  So **with the datum
and no evaluation at all, the midpoint is within `n·a(u)/2` of `ln Z_g`, with certainty.**
For a product reference `Bern(p)ⁿ` the same argument gives
`−βU − n·max{KL(a₀‖p), KL(a₁‖p)} ≤ ln(Z_g/Z_0) ≤ −βU`, `a₀, a₁` the letter laws of the two
extreme cones.
*Proof.*  The upper end is `S ≤ n ln 2` (and is the upper end of Theorem 5).  Lower end: by
the chain rule `S(μ_g) = Σ_i E[h(p_i)]`, `p_i` the conditional probability of `x_i = 1` given
the earlier coordinates; the ratio of the two partial sums that define `p_i` lies in
`[e^{−u}, e^{u}]`, so `p_i ∈ [σ_u, 1 − σ_u]` and `h(p_i) ≥ h(σ_u)`.  (This is steps 1–2 of
Proposition A1.1 with `r = ½`: `KL(μ_g‖uniform) ≤ n·a`.)  ∎

**Corollary A16.2 (where the datum removes an exponential cost) [P, given theory report
Theorem 11.25].**  The two "free" accuracies are the two relative entropies between a
fair coin and the coin `σ_u`:

    without the datum:  ln cosh(u/2) = KL(½‖σ_u)        with the datum:  a(u) = KL(σ_u‖½),

    KL(½‖σ_u) − KL(σ_u‖½)  =  Σ_{k≥2} tanh(u/2)^{2k}·(k−1)/(k(2k−1))  >  0      (u > 0).

For `a(u) ≤ ε₁ < ln cosh(u/2)`: with the datum an `ε₁n`-accurate answer costs **no
evaluation**; without it every `ε₁n`-accurate algorithm needs
`(1 − 2δ)·2ⁿ/|B(n, r−1)| = exp(n[ln 2 − h(ρ₀ + ε₁/u)] − o(n))` evaluations at the zero residual.
*Proof.*  A16.1 and Theorem 11.25(a) (the dip of radius `r` raises `ln Z` by more than `ε₁n` as
soon as `r/n > ρ₀ + ε₁/u`, and this radius is below `n/2` exactly when `ε₁ < u/2 − uρ₀ =
ln cosh(u/2)`).  The identity `ln cosh(u/2) = KL(½‖σ_u)`: `σ(1−σ) = 1/(4cosh²(u/2))`.  The series:
with `σ = (1−t)/2`, `t = tanh(u/2)`: `KL(½‖σ) = Σ_k t^{2k}/(2k)` and
`KL(σ‖½) = Σ_k t^{2k}/(2k(2k−1))`.  ∎

| `u` | `a(u)` (free with the datum) | `ln cosh(u/2)` (free without) | exponent without the datum at `ε₁ = a(u)` |
|---|---|---|---|
| 0.5 | 0.03030 | 0.03093 | `3·10⁻⁶` |
| 1 | 0.11094 | 0.12011 | 0.00017 |
| 2 | 0.32781 | 0.43378 | 0.0056 |
| 4 | 0.60305 | 1.32500 | 0.0667 |

For weak residuals the window is of relative width `O(u²)` and the exponent in it is
tiny: the datum buys almost nothing.  For strong residuals (`u ≥ 2`) it is wide: at `u = 4`
an accuracy of `±0.3n` nats is free with the datum and costs `e^{0.067n}` evaluations
without.  **So the oracle invariance of addendum A12 is a statement about bounded
accuracy; for the thermodynamic datum it fails at coarse extensive accuracy, and the
failure is exactly an entropy bound.**

### (b) Below `a(u)`: the plateau twin

At extensive accuracy the equal-depth twin of Proposition 5b gives only
`θ ≥ h − ε₁` (it takes `e^{ε₁n}` equal twins to raise `ln Z` by `ε₁n`).  By the identity, a
twin must have the mean energy of the visible state and an entropy larger by `ε₁n`: it
must be *as deep and wider*.

**Proposition A16.3 (plateau twin) [P — an adaptation of the referee's Lemmas R6.1–R6.3, which
the coordinator has re-derived (A12); exact sums with overlapping supports at
`n = 600 … 2000`, ten cases].**  Let `ρ₀ < ρ₁ < ρ̄ < ½`, `r₁ = ⌈ρ₁n⌉`, `g₀ = −u(r₁ − d_H(x,a₀))₊` (a
visible basin that dominates), `S₀ = S(μ_{g₀})`, `U₀ = U_{g₀}`.  For an integer `r₁ < r₂ ≤ ρ̄n`, a
centre `a′` with `|d_H(a₀,a′) − n/2| ≤ √(n ln n)` and a real `κ ∈ (0, r₂]` let

    T_κ(x) = −u·min(κ, (r₂ − d_H(x,a′))₊),        g′_κ = min(g₀, T_κ)

(a truncated cone: a plateau of depth `uκ` and radius `r₂ − κ`, with walls of slope `u`).
Then for all large `n`:
(a) there is `κ* ∈ ((|U₀| − 1)/u, r₂)` with `U_{g′_{κ*}} = U₀` **exactly**;
(b) `ln Z_{g′_{κ*}} − ln Z_{g₀} ≥ ln|B(n, ⌊r₂ − (|U₀| − 1)/u⌋)| − S₀ − 1 − o(1)`;
(c) `g′_{κ*} = g₀` outside `B(a′, r₂ − 1)`.
Hence an algorithm with evaluations and the exact datum that is `ε`-accurate for an `ε`
below the right-hand side of (b) needs at `g₀`

    E[#evaluations]  ≥  (1 − 2δ)(1 − 2/n²)·2ⁿ/|B(n, r₂ − 1)|.

Here `S₀ = n·h(σ_u) + o(1)` and `|U₀| = u(r₁ − σ_u n) + o(1)`, so with
`σ₂(ε₁) := h⁻¹(h(σ_u) + ε₁)` and `ρ₁ ↓ ρ₀`:

    θ_U(ε₁)  ≥  ln 2 − h( ρ₀ − σ_u + σ₂(ε₁) ),        for  ε₁ < ε₁ᶜ := h(½ − ρ₀ + σ_u) − h(σ_u).

*Proof.*  (1) *Excess identity* (R6.1, valid for any two functions): with
`E = Σ(e^{−g′} − e^{−g₀})₊` and `m` the mean over the excess mass of the *effective energy*
`ĝ = g′ − t/(e^t − 1)`, `t = g₀ − g′ > 0`: `Z′ = Z₀ + E` and `U′ − U₀ = (E/(Z₀+E))(m − U₀)`.
(2) *The shallow end.*  `0 < t/(e^t−1) < 1` and `g′ = T_κ ≥ −uκ` on the excess, so
`m(κ) ≥ −uκ − 1` for every `κ`, with no assumption on the overlap; hence `m(κ) > U₀` for
`κ < (|U₀| − 1)/u`.  (3) *The deep end.*  At `κ = r₂` the twin is a full cone of radius
`r₂ ≥ r₁ + 1`; the algebra of R6.2 at `s = +1` (every weight of the basin multiplied by
`e^{u(r₂−r₁)}` and every depth increased by `u(r₂−r₁)`), with the cone's mass beyond `r₁`
exponentially small and the overlap bounded as in R6.3 with `r₂` in the denominator, gives
`m(r₂) < U₀`.  `κ ↦ m(κ)` is continuous: (a).  (4) `E` is non-decreasing in `κ`; at
`κ_lo = (|U₀| − 1)/u` the plateau alone contributes `|B(n, ⌊r₂ − κ_lo⌋)|(e^{|U₀|−1} − 1)` minus the
overlap, and `Z₀ = e^{S₀ + |U₀|}`: (b).  (c) is the definition.  The counting is that of
Theorem R6.  ∎

*Exact checks* (`plateau_twin_check.py`; the root is computed through the excess
identity — the difference `U′ − U₀` itself cancels to nothing in floating point, which
cost one false "no root"): in all ten cases the root exists and lies above `κ_lo`; the gap
is above the bound of (b) by one to three and a half nats; the plateau edge `(r₂ − κ*)/n`
agrees with `σ₂(gap/n)` and `r₂/n` with `ρ₁ − σ_u + σ₂` to a few sites; centres at distance
`0.45n`, `0.5n`, `0.55n` give identical numbers.  Examples: `n = 2000`, `u = 1`, `ρ₁ = ρ₀ + 0.01`,
gap `0.050n`: `r₂ = 899`, `κ* = 244.57`, against the radius `860` of the smallest dip that
does the same without the datum; `n = 600`, `u = 4`, gap `0.30n`: `r₂ = 190` against `147`.

**Exponents per site** (`h − ε₁`: equal twins; plateau: A16.3; last column: no datum):

| `u` | `ε₁` | equal twins | **plateau twin (lower bound with the datum)** | `θ_hint(ε₁)` (upper bound with it; exact without) |
|---|---|---|---|---|
| 1 | `0.1a = 0.0111` | 0.0180 | **0.0238** | 0.0240 |
| 1 | `0.5a = 0.0555` | void | **0.0059** | 0.0084 |
| 2 | `0.25a = 0.0820` | 0.0153 | **0.0600** | 0.0632 |
| 2 | `0.5a = 0.164` | void | **0.0263** | 0.0369 |
| 4 | `0.25a = 0.151` | 0.0885 | **0.1715** | 0.1840 |
| 4 | `0.5a = 0.302` | void | **0.0969** | 0.1374 |
| 4 | `0.75a = 0.452` | void | **0.0275** | 0.0985 |

The gap between the two last columns is of second order in `ε₁` (it is the curvature of
`h` at `σ_u`: `σ₂ − σ_u ≥ ε₁/u`, with equality to first order) and grows to a factor of
several near `a(u)`.  For `ε₁ᶜ ≤ ε₁ < a(u)` the plateau would have to cover more than half the
cube and the bound is void (`ε₁ᶜ = 0.086, 0.273, 0.557` against `a = 0.111, 0.328, 0.603` at
`u = 1, 2, 4`).

### (c) An isoperimetric inequality with an energy constraint; the plateau twin is optimal at the visible basin (added at checkpoint 28)

The step that was missing at checkpoint 26 — "a tail lemma with an energy constraint" — has
a short proof for the flat reference, and that is enough to make the bound of A16.3 exact
at the instance where it was proved.

**Lemma A16.5 (isoperimetry with an energy constraint) [P; brute force: all 65 534 supports
in `Q_4`, 8 000 random supports in `Q_5`, `Q_6`, 1 398 random members with dips and hills,
`n ≤ 10`].**  Units `β = 1`.  Let `U₀ ≤ 0` and `N = |B(n, R)|`, `R < n/2`.  Among all members `g` of the
class that vanish outside a set of at most `N` points and have mean energy `U_g ≥ U₀`, the
**plateau on a ball**

    g_pl(x) = −min(c*, u·(R + 1 − |x|)₊),        c* the level with U_{g_pl} = U₀

(the full cone, `c* = ∞`, if even that has mean energy `≥ U₀`) has the largest partition
function: `Z_g ≤ Z_{g_pl} =: Z^{pl}(R, U₀)`.  For sizes that are not ball sizes, replace the
ball by the complement of an initial segment of the simplicial order.
*Proof.*  Write `t = e^{−g}`.  The constraint `U_g ≥ U₀` is `φ(t) := Σ t ln t + U₀ Σ t ≤ 0`, a
*convex* constraint in the weights, so for every `η ≥ 0`
`Z_g = Σ t ≤ Σ_x f_η(t(x))`, `f_η(t) := (1 − ηU₀)t − η t ln t` — concave, with its maximum at
`ln t*_η = 1/η − 1 − U₀`.  If `ρ(x)` is the distance from `x` to the complement of the support,
`t(x) ∈ [e^{−uρ(x)}, e^{uρ(x)}]`, so `f_η(t(x)) ≤ F_η(ρ(x))` with
`F_η(ρ) := max{f_η(t) : e^{−uρ} ≤ t ≤ e^{uρ}}` — **nondecreasing in `ρ`** (a maximum over a
growing interval).  By Harper's theorem the numbers `#{x : ρ(x) ≥ k}` are, for all `k`
simultaneously, largest when the support is the ball; hence `Z_g ≤ Σ_x F_η(R + 1 − |x|)` for
every `η ≥ 0`.  For the ball the maximiser inside `F_η` is `min(t*_η, e^{uρ})`, i.e. the plateau
at the level `c = ln t*_η`, which is a member of the class.  Choose `η = 1/(c* + U₀ + 1)` (positive,
because a plateau at level `c` has mean energy `≥ −c`, so `c* ≥ |U₀|`): then
`Σ_x F_η = Z_{g_pl} − ηφ(t_pl) = Z_{g_pl}`.  If the full cone is feasible take `η = 0`.  ∎
*Remarks.*  (1) For a given support the optimal profile is "the deepest dip, flooded up
to a level"; for a general reference instance the same Lagrangian gives the level
clipped between the two McShane envelopes — but then Harper's theorem is not
available.  (2) Hills are allowed in the statement and never help.  (3) The unconstrained
case `η = 0` is the tail lemma of the theory report (its Lemma 11.43(b)).  (4) *Above any
level of any member.*  As in that lemma, the argument does not need a flat background:
for a member with weights `w`, datum `U`, a level `t` and `D = {w > t}`, for every `η ≥ 0`

    Z  =  Σ_x f_η(w(x))  ≤  Σ_{x∉D} f_η(w(x))  +  Σ_{x∈D} max{ f_η(s) : t ≤ s ≤ t·e^{u·dist(x,Dᶜ)} },

(`f_η` with `U₀ = U`; the first equality because the constraint holds with equality), and the
last sum is at most its value for a ball of the size of `D`.  The first sum is an average
of a bounded function of the weights below the level, which sampling estimates.  So the
datum turns plain Monte Carlo into a bracket procedure on the whole class; its
worst-case exponent has not been evaluated (the guess at the end of this addendum is
for it).

**Theorem A16.6 (the complexity at the visible basin, with the datum) [P, given A16.1, A16.3,
A16.5; exact sums].**  Let `g₀` be the visible basin of Proposition A16.3 (`ρ₀ < ρ₁`), `V` its
support, `U₀ = U_{g₀}`.
(i) *Every alternative is bounded.*  If `g′` is a member of the class with `U_{g′} = U₀` that
agrees with `g₀` outside a set `D` with `|D| + |V| ≤ |B(n, R)|`, then

    −(S(μ_{g₀}) − n·h(σ_u))  ≤  ln Z_{g′} − ln Z_{g₀}  ≤  G(R) := ln Z^{pl}(R, U₀) − ln Z_{g₀},

the left side by the entropy bracket (it is `o(1)`), the right by Lemma A16.5 (`g′` vanishes
outside `D ∪ V`).
(ii) *An algorithm.*  Draw `M = ⌈2ⁿ ln(1/δ)/|B(n,R)|⌉` uniform points.  If all values equal one
number `v`, compute from the datum the bracket
`[max(ln(2ⁿ − |B(n,R)|), n·h(σ_u) − (U − v)), ln Z^{pl}(R, min(U − v, 0))]` for `ln Z + v` and return its
midpoint if its width is at most `ε`; in every other case run any class-correct
procedure.  This algorithm uses no hint, is correct on the whole class with probability
`1 − δ(1+o(1))` (an instance that is not constant outside `|B(n,R)|` points shows two
different values, except with probability `δ`), and at `g₀` it stops after the `M` samples
with probability `1 − e^{−Ω(n)}` whenever `G(R) + o(1) ≤ ε`.
(iii) *It matches.*  The plateau twin of radius `r₂` has `ln Z′ − ln Z₀ = G(r₂ − 1)` up to
`10⁻³` in all eight exact cases (e.g. `100.036` against `100.036` at `n = 2000`), so with
Proposition A16.3: **with the datum, the number of evaluations needed at `g₀` for accuracy
`ε` is `Θ(2ⁿ/|B(n, R(ε))|)`, `G(R(ε)) ≈ ε`** — lower and upper bound differ by the factor
`ln(1/δ)/(1−2δ)` and one unit of the radius.  Per site: `ln 2 − h(ρ₁ − σ_u + σ₂(ε₁))`.  Without
the datum the same packing argument with cone dips (the smallest one that matters at
this instance has radius `(ρ₁ + ε₁/u)n`) gives at least `ln 2 − h(ρ₁ + ε₁/u)`, which is larger:
**at this instance the datum lowers the cost at every extensive accuracy**, and changes
nothing at bounded accuracy.
(iv) *Among flat landscapes with small structures the threshold basin is the hardest
[evaluation of the bracket of (ii) at the exponential scale].*  For an instance that is constant outside a set small against `|B(n,R)|` the width of the
bracket in (ii) depends on the instance through its datum only; with `e = |U − v|/(un)` it is
`n·min(h(R/n − e) − h(σ_u), ue + h(R/n − e) − ln 2)₊ + o(n)`, largest at `e = ρ₀ − σ_u` — the energy of
a basin at threshold dominance.

*Checks* (`energy_isoperimetry_check.py`, four minutes): the lemma as stated above; and
`G(r₂ − 2) < ` gap of the twin `= G(r₂ − 1) < G(r₂)` in all eight cases.

### (d) What is known, and a conjecture

    bounded accuracy:            θ_U = h                               (A12(c); the datum is worth nothing)
    0 < ε₁ < ε₁ᶜ:                ln 2 − h(ρ₀ − σ_u + σ₂(ε₁))  ≤  θ_U(ε₁)  ≤  ln 2 − h(ρ₀ + ε₁/u)
                                 (the lower value is the exact cost at the threshold basin: A16.6)
    ε₁ᶜ ≤ ε₁ < a(u):             0  ≤  θ_U(ε₁)  ≤  ln 2 − h(ρ₀ + ε₁/u)
    a(u) ≤ ε₁ < ln cosh(u/2):    θ_U = 0  <  θ_hint(ε₁)                (A16.2; the datum is worth everything)

**Conjecture A16.4 [C].**  `θ_U(ε₁) = ln 2 − h(min{½, ρ₀ − σ_u + σ₂(ε₁)})` for every `ε₁ ≥ 0`: the
plateau twin is the best hiding place, and the datum lowers the exponent at *every*
extensive accuracy.
*Evidence.*  (i) **Now a theorem (A16.6):** for instances that are constant outside a small
set, no alternative of any shape or support does better than the plateau twin, an
algorithm without a hint attains the bound, and the threshold basin is the hardest such
instance.  What the conjecture still needs is the same for instances that are *not*
flat outside a small set — sloped landscapes, on which an adaptive algorithm walks
downhill — i.e. the lemma for a general reference, combined with the theory division's
nested algorithm.  (ii) Hiding the twin on a visible, just
sub-dominant terrace instead of the flat background (less digging, fewer places) is
never better: maximum at the flat background in twelve cases
(`terrace_twin_explore.py`; exponential-scale formulas, a valid lower bound within the
family).  (iii) On the wall of the visible basin, which is maximally steep, a dip must
contain with each of its points everything farther out, and its depth at a point is at
most `2u` times the number of that point's own flips that must be undone to leave the
dip; the simple dips there have depth `O(1)`.  We found no construction on a slope that
helps, and have no proof that none exists.  *What a proof needs:* a
tail lemma with an energy constraint — the largest excess of a modification supported
on a set of given measure **whose excess has a prescribed mean energy** — for an
arbitrary reference instance; equivalently, the largest entropy gain at fixed mean
energy.  The unconstrained lemma is the theory report's Lemma 11.62.

*For non-adaptive algorithms [H, exponential-scale reasoning, not worked out].*  There the
flat mask is not the hardest instance with the datum: on a cone the unexplored ball
around the apex can hold either the truncated cone or a displaced inner cone with the
same mean energy, and the same counting gives `θ_na^U(ε₁) = θ_na(u·(σ₂(ε₁) − σ_u))` — the datum
acts as an amplification of the accuracy, from `ε₁` to `u(σ₂(ε₁) − σ_u) ≥ ε₁`, with `θ_na^U(0⁺) = a`
unchanged and `θ_na^U = 0` from `ε₁ᶜ` on.  A guess to be tested, not a claim.

*Not done.*  The upper bound for the whole class; the plateau twin against the marginal oracle (symmetrise
by a code as in Corollary R6′ — expected to go through, not written); a field; a
tolerance on the datum (as in the referee's remark, any tolerance makes the exact root
unnecessary); a Lean check of the three finite inequalities used.

*Reading [H].*  A calorimetric mean energy turns a free-energy question into an entropy
question, and the class — a bound on how much one flip can change the energy — bounds
how ordered an ensemble can be.  At bounded accuracy that is no help (a hidden state as
deep and as wide as the visible one changes nothing measurable); at an accuracy of
`a(u)` nats per site it is the whole answer; in between, the hidden state has to be as
deep and exponentially wider, which makes it easier to find than without the datum —
if the conjecture holds, at every accuracy.
