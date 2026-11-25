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
linear programmes on 900 instances, `monotone_ratio_check.py`].**  For every admissible `g`

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

**Corollary A11.1 (macrostates).**  Let `B` be an up-set (`x ∈ B`, `x ≤ x′ ⇒ x′ ∈ B`) and
`A = X ∖ B`, both non-empty.  Over the admissible class the ratio `Z_{f+g}(A)/Z_{f+g}(B)` fills
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

