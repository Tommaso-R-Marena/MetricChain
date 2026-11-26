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
numbers.  Everything here is the coordinator's.  **Refereed at checkpoint 35 by workstream
R8** (`docs/science/workstreams/R8_REPORT.md`; linked correction of the two messages that
carried it: SCI-MSG-0016): *no numbered statement false*; A16.1, A16.2, A16.3 and Lemma
A16.5 proved (the lemma also checked over general members and its algebraic core
machine-checked, `experiments/science/ws_R8/A16Core.lean`); **Theorem A16.6 (ii)–(iii) said
more than was proved and is proved after the repairs R8.2–R8.5**, entered below and
marked "R8".  Sentences changed by the referee's findings carry the finding's number;
what the text said before is in SCI-MSG-0016 and in the history of this file.  Scripts:
`experiments/science/pi_inference/plateau_twin_check.py` (13 s; the version committed
before checkpoint 35 aborted before the twins — `DEAD_ENDS.md` SD39),
`terrace_twin_explore.py` (1 min), `energy_isoperimetry_check.py` (4 min); the referee's own:
`experiments/science/ws_R8/`.*

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
class, `n ≤ 11`; refereed — R8: 576 further members and an adversarial minimisation of the
entropy over the class.  The lower end is not new here: it is Theorem 2(d) of
`INFERENCE_LIMITS.md`, and in other words the entropy bound of a strong Santha–Vazirani
source (R8, F8; **[K]** at abstract level, see the R8 report §6).  What this addendum adds
is its use with the datum].**  For every `g` of the class, `n·h(σ_u) ≤ S(μ_g) ≤ n ln 2`, that is

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
Then for all large `n` — precisely (R8.1, which writes out the deep end of the proof):
whenever `|U₀| > 1` and the twin's full cone overlaps the visible basin in a weight
fraction below `1/r₂`, a condition that needs no dominance and holds for the stated
centres from `n` of a few hundred to a few thousand depending on `u`:
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
does the same without the datum; `n = 600`, `u = 4`, `ρ₁ = ρ₀ + 0.03`, gap `0.30n`: `r₂ = 190` against `147`.

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

**Lemma A16.5 (isoperimetry with an energy constraint) [P; refereed — R8: proved.  Evidence:
the Harper step on all 65 534 supports of `Q_4` and 8 000 random supports of `Q_5`, `Q_6` with
the clipped-level profile on each (the coordinator's script — it tests that step, not
the lemma: R8, O4); the lemma over *general* members by a convex programme on every
support of `Q_3`, `Q_4` and an exhaustive grid of `2.8·10⁸` Lipschitz functions on `Q_4`
(`ws_R8/r8_03_isoperimetry.py`); algebraic core **[V]** (`ws_R8/A16Core.lean`:
`sum_le_sum_F`, `F_mono`, `F_eq_plateau`, `plateau_optimal`; Harper's step and the existence
of the level are not formal)].**  Units `β = 1`.  Let `U₀ ≤ 0` and `N = |B(n, R)|` (the
hypothesis `R < n/2` of the first version is not used: R8, F6).  Among all members `g` of the
class that vanish outside a set of at most `N` points and have mean energy `U_g ≥ U₀`, the
**plateau on a ball**

    g_pl(x) = −min(c*, u·(R + 1 − |x|)₊),        c* the level with U_{g_pl} = U₀

(the level exists and is unique: with `P` the top of the plateau, `dU/dc = −μ(P)(1 + c + U) < 0`
and `d ln Z/dc = μ(P)`, so `d ln Z^{pl}/dU₀ = −1/(1 + c* + U₀) ∈ [−1, 0)` — R8, F6; the full cone,
`c* = ∞`, if even that has mean energy `≥ U₀`) has the largest partition
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
every `η ≥ 0`.  For the ball, and for the `η` chosen next (for a general `η` with `t*_η < 1` the
maximiser would be a hill, `max(t*_η, e^{−uρ})` — R8, F6), the maximiser inside `F_η` is
`min(t*_η, e^{uρ})`, i.e. the plateau at the level `c = ln t*_η`, which is a member of the class.
(The Lipschitz cone is used only for the pointwise bounds `t(x) ∈ [e^{−uρ(x)}, e^{uρ(x)}]`: the lemma
holds for the larger set `{g : |g(x)| ≤ u·dist(x, supp^c)}` — R8, machine-checked in that form.)  Choose `η = 1/(c* + U₀ + 1)` (positive,
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
last sum is at most its value for a ball of the size of `D` (**R8, F6:** as stated when `|D|`
is known exactly; a sampler knows an upper bound on `|D|` only, and enlarging the ball is
harmless only for `η` with `f_η(t) ≥ 0`, i.e. `η(U + ln t) ≤ 1` — otherwise subtract
`f_η(t)(|B| − |D|)`).  The first sum is an average
of a bounded function of the weights below the level, which sampling estimates.  So the
datum turns plain Monte Carlo into a bracket procedure on the whole class; its
worst-case exponent has not been evaluated (the guess at the end of this addendum is
for it).

**Theorem A16.6 (the complexity at the visible basin, with the datum) [P, given A16.1, A16.3,
A16.5 and — for (ii), (iii) — the referee's repairs R8.2–R8.5, entered below; (i), (iv)
proved as first written; exact sums].**  Let `g₀` be the visible basin of Proposition A16.3 (`ρ₀ < ρ₁`), `V` its
support, `U₀ = U_{g₀}`.
(i) *Every alternative is bounded.*  If `g′` is a member of the class with `U_{g′} = U₀` that
agrees with `g₀` outside a set `D` with `|D| + |V| ≤ |B(n, R)|`, then

    −(S(μ_{g₀}) − n·h(σ_u))  ≤  ln Z_{g′} − ln Z_{g₀}  ≤  G(R) := ln Z^{pl}(R, U₀) − ln Z_{g₀},

the left side by the entropy bracket (it is `o(1)`), the right by Lemma A16.5 (`g′` vanishes
outside `D ∪ V`).
(ii) *An algorithm* (as corrected after the referee's findings F1, F3; the bracket is for
`ln Z + v`, with the gauge `v` — the form printed in SCI-MSG-0013 dropped the gauge and is
wrong at constant instances `g ≡ v ≠ 0`: F4).  Draw one point and read its value `v`; let
`R` be the largest radius at which the bracket
`[max(ln(2ⁿ − |B(n,R)|), n·h(σ_u) − (U − v)), ln Z^{pl}(R, min(U − v, 0))]` for `ln Z + v` has width at most `ε`
(R8.5: so `R` comes from the datum and one sample, not from a hint); draw
`M = ⌈2ⁿ ln(1/δ)/|B(n,R)|⌉` uniform points; if all values equal `v`, return the midpoint; in
every other case evaluate everything.  This algorithm is correct on the whole class
with probability at least `1 − δ·e^{|B(n,R)|/2ⁿ}` (an instance that is not constant outside
`|B(n,R)|` points shows two different values except with that probability; the fallback
is exact), and at `g₀` it stops after the samples **with probability `1 − e^{−Ω(n)}`** whenever
`G(R) + o(1) ≤ ε`.  **Its expected cost at `g₀` is not of that order** (F1): the samples meet
the visible basin with a small probability, and then everything is evaluated.
*A tolerant variant with the cost in expectation* (R8.4 **[P]**, constants not optimised,
not simulated): accept if all but at most `k₀` of `M′ = ⌈6(k₀ + ln(1/δ))·2ⁿ/|B(n,R)|⌉` samples show
one value; it is class-correct, and at `g₀` its expected cost is at most `M′ + 1` for a
constant `k₀ ≈ ln 2/(h(R/n) − h(ρ₁))`.
(iii) *It matches* (rewritten after the referee's findings F1, F2: the first version
rested on eight numerical coincidences "gap `= G(r₂ − 1)`", and compared a lower bound on
the expectation with an upper bound that holds with high probability).  With
`g″ = T_{κ*}` alone on the flat background and `U″` its mean energy,

    G(r₂ − 1) − (U″ − U₀)₊  ≤  ln Z′ − ln Z₀  ≤  G(r₂)

(R8.3 **[P]**, re-derived by the coordinator: `g″` is the plateau on `B(a′, r₂−1)` at its own
energy; `g′ ≤ g″` pointwise; `|d ln Z^{pl}/dU₀| ≤ 1`; the right end is (i).  `U″ − U₀` is
exponentially small at extensive accuracy; equality with `G(r₂ − 1)` holds to `10⁻¹¹` in the
exact cases with extensive gaps and fails by `3·10⁻⁴ … 2·10⁻²` at gaps of 4–8 nats).  And for
every class-correct algorithm and every `m` (R8.2 **[P]**, the quantile form of the packing
bound): `P_{g₀}(#evaluations > m) ≥ (1 − 2δ)(1 − 2/n²) − m·|B(n, r₂ − 1)|/2ⁿ`.  Hence: **with the
datum, at `g₀`, the number of evaluations needed for accuracy `ε` is `2ⁿ/|B(n, R(ε))|` up to a
constant factor and at most two units of the radius, `G(R(ε)) ≈ ε` — in the quantile sense
(more than `½(1−2δ)·2ⁿ/|B(n, R(ε)+2)|` with probability `≥ ½(1−2δ) − o(1)` for every algorithm;
at most `ln(1/δ)·2ⁿ/|B(n, R(ε))|` with probability `1 − e^{−Ω(n)}` for the algorithm of (ii)), and
in expectation for its tolerant variant.**  Per site: `ln 2 − h(ρ₁ − σ_u + σ₂(ε₁))`.  Without
the datum the same packing argument with cone dips (the smallest one that matters at
this instance has radius `(ρ₁ + ε₁/u)n`) gives at least `ln 2 − h(ρ₁ + ε₁/u)`, which is larger:
**at this instance the datum lowers the cost at every extensive accuracy**, and changes
nothing at bounded accuracy.
(iv) *Among flat landscapes with small structures the threshold basin is the hardest
[evaluation of the bracket of (ii) at the exponential scale].*  For an instance that is constant outside a set small against `|B(n,R)|` the width of the
bracket in (ii) depends on the instance through its datum only; with `e = |U − v|/(un)` it is
`n·min(h(R/n − e) − h(σ_u), ue + h(R/n − e) − ln 2)₊ + o(n)`, largest at `e = ρ₀ − σ_u` — the energy of
a basin at threshold dominance.

*Checks* (`energy_isoperimetry_check.py`, four minutes): the Harper step of the lemma; and
`G(r₂ − 2) < ` gap of the twin `≈ G(r₂ − 1) < G(r₂)` in all eight cases (to `10⁻³`; the exact
relation is R8.3).  The referee's: `ws_R8/r8_03_isoperimetry.py` (the lemma over general
members), `r8_04_theorem166.py` (the cost bookkeeping), `r8_08_matching.py` (R8.3; re-run by
the coordinator, output identical).

### (d) What is known, and a conjecture

    bounded accuracy:            θ_U = h                               (A12(c); the datum is worth nothing)
    0 < ε₁ < ε₁ᶜ:                ln 2 − h(ρ₀ − σ_u + σ₂(ε₁))  ≤  θ_U(ε₁)  ≤  ln 2 − h(ρ₀ + ε₁/u)
                                 (the lower value is the cost exponent of the basins `ρ₁ ↓ ρ₀`: A16.6)
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
helps, and have no proof that none exists.  (iv) **The referee's attempts to refute it
(R8 report §3) [N, H]:** five families at the exponential scale (soft basins and global
tilts; a terrace of any depth; products of a flat block and a cone block; exponentially
many visible basins; "egg cartons" `u·dist(x, C)` for a code `C`) — none beats the plateau
twin on the flat background, and each family's optimum degenerates to it; five explicit
pairs with exact sums on non-flat landscapes at `n = 600` (on a global tilt a single
query far uphill finds the twin: a slope is a direction from which a hidden state is
visible); and a "column bound" in the small-slope limit — whatever the visible
landscape, a twin hidden in a fresh direction is bounded by `θ ≤ (u²/8)(√(1 − ε₁/a) − ½)²`,
which is the plateau value in that limit **[H: a Laplace-scale argument in a limit model]**.
**Not excluded:** landscapes with exponentially many prepared sites at several levels;
twins that are not single-level plateaus on a non-flat background; and **the interval
`ε₁ᶜ ≤ ε₁ < a(u)`, where the conjecture says the exponent is zero and there is neither an
algorithm for general instances nor a twin** — the referee has no evidence either way
there, and neither have we.  *What a proof needs:* a
tail lemma with an energy constraint — the largest excess of a modification supported
on a set of given measure **whose excess has a prescribed mean energy** — for an
arbitrary reference instance; equivalently, the largest entropy gain at fixed mean
energy.  The unconstrained lemma is the theory report's Lemma 11.62.

*For non-adaptive algorithms [the lower bound now **P** at sketch level with exact pairs —
R8.6; equality open].*  There the flat mask is not the hardest instance with the datum:
on a cone the unexplored ball around the apex can hold either the truncated cone or
the cone raised by a constant under a plateau ring, with the same mean energy (the
first version said "a displaced inner cone": a displaced one is a member only when
raised by at least `u` times the displacement and gains nothing — R8, F9).  The pair
exists for every radius and was constructed exactly in seven cases; with the averaging
argument of the theory report's Theorem 11.45(a) it gives
**`θ_na^U(ε₁) ≥ θ_na(u·(σ₂(ε₁) − σ_u))`** — the datum acts at best as an amplification of the
accuracy, from `ε₁` to `u(σ₂(ε₁) − σ_u) ≥ ε₁`, with `θ_na^U(0⁺) = a` unchanged and the bound zero
from `ε₁ᶜ` on.  Whether this is the exponent ("`=`") is open: the datum-assisted bracket of
remark (4) meets it within 0.5–2.5 sites on six radial families at `n ≤ 400`, the worst
instances being the two members of the pair; the worst case over the class was not
evaluated.

*Not done.*  The upper bound for the whole class; the plateau twin against the marginal oracle (symmetrise
by a code as in Corollary R6′ — expected to go through, not written); a field; a
tolerance on the datum (as in the referee's remark, any tolerance makes the exact root
unnecessary); a Lean check of the three finite inequalities used (the algebraic core of
A16.5 is now formal, `ws_R8/A16Core.lean`; R8.1 and R8.3 are not); a simulation of the
algorithm of A16.6 (ii) and of its tolerant variant (they were analysed, never run).

*Reading [H].*  A calorimetric mean energy turns a free-energy question into an entropy
question, and the class — a bound on how much one flip can change the energy — bounds
how ordered an ensemble can be.  At bounded accuracy that is no help (a hidden state as
deep and as wide as the visible one changes nothing measurable); at an accuracy of
`a(u)` nats per site it is the whole answer; in between, the hidden state has to be as
deep and exponentially wider, which makes it easier to find than without the datum —
if the conjecture holds, at every accuracy.

---

## A17. Certifying a free energy against a model that can be sampled: which a-priori bound suffices, and what it costs (criticism and extension of the theory division's box-class result, THY-RES-0007 §4; our own request P-T3 of SCI-RES-0002)

*Added at checkpoint 34.  Everything in this addendum is the coordinator's; it has been
read by nobody else.  Labels as elsewhere: **[P]** proved here (with the check named),
**[P-sketch]**, **[K]**, **[N]**, **[H]**.  Script:
`experiments/science/pi_inference/renyi_ball_check.py` (two seconds; log and JSON next to
it).*

***Prior art — revised at checkpoint 39 (marks "A3").***  *Parts (0)–(9) were written
before any literature search, with every reference "from memory".  Workstream A3 has now
done the search (`workstreams/A3_REPORT.md`: 47 sources read in the passages that matter),
and the coordinator has checked five of its citations against the sources.  The outcome
is in the section **"What is in print, and what remains ours"** near the end of this
addendum, and it changes what may be claimed: **the cost table of part (4) is in print —
without a hint and in the sampling model — in a preprint of February 2026 (Block and
Shetty, arXiv:2602.23535), the Rényi rows earlier (Kunsch–Novak–Rudolf 2019; heavy-tailed
mean estimation); the inequality of part (7) is Hoeffding's Theorem 3 of 1963; part (8)
is an inequality of Chazottes, Collet, Külske and Redig (2006).**  No mathematical
statement of the addendum was found wrong; A17.6 is replaced by a sharper form.  The
sentences that said "from memory" are corrected in place and carry the mark "A3"; the
first wording is kept where a published message of ours quoted it.*

**Why.**  We asked the theory division (P-T3) for "a certified typical-norm remainder
for `ln Z`": our force-field pilot had found a solvent term close to a tractable class
in root mean square and far from it in supremum norm.  Its answer, previewed in
THY-RES-0007 §4 (to be its §11.30), is a theorem for **box classes**: if `lo ≤ g − ĝ ≤ hi`
pointwise and the Gibbs measure `π` of the known function `ĝ` can be sampled exactly,
then with a hint `Θ((Z(lo)/Z(g) − 1)/ε)` evaluations certify `ln Z(g)` within `ε` — the
Boltzmann factor of the free-energy distance to the *floor* — independently of the
size of the system; and "what must be certified is the floor, and nothing else can
replace it".  It asked for criticism.  This addendum (0) re-derives the preview,
(1)–(4) shows that the floor is the end point of a family — **any a-priori bound on a
Rényi divergence of order `p > 1` between the true ensemble and the model replaces it,
at a price in the accuracy exponent; a Kullback–Leibler bound does too, at an
exponential price in `1/ε`; no bound on moments of the remainder energy itself does** —
which is the precise answer to what "typical norm" must mean, and (5) says where such
bounds come from for the classes of the programme.

**Setting.**  `X` finite; `ĝ` known, `π ∝ e^{−ĝ}`, `Z₀ = Σ e^{−ĝ}` known; exact samples of `π`
are free.  The true energy is `g = ĝ + r`; `Y := e^{−r} > 0` is the Boltzmann factor of
the remainder; `μ := E_π Y = Z(g)/Z₀`; `π_g = πY/μ` the true ensemble.  Target: `ln μ`.  An
evaluation at `x` returns `r(x)`; cost = number of evaluations.  Units `β = 1`.
`‖Y‖_p := (E_π Y^p)^{1/p}`, `‖Y‖_∞ = e^{−min r}`.  Rényi divergence of order `p`:
`D_p(π_g‖π) = (p − 1)^{−1} ln E_π (dπ_g/dπ)^p = (p/(p−1))·ln(‖Y‖_p/μ)`; `D_1` is the
Kullback–Leibler divergence, `D_∞ = ln max(Y/μ)`.  "With a hint" as in the theory report:
the algorithm is handed a candidate `r̃`, must be correct on the whole class, and its
cost is counted at instances where the hint is right.  Accuracy: an alternative counts
as different if `|ln μ′ − ln μ| > ε`; write `s_ε := 1 − e^{−ε}`, `η_ε := e^ε − 1`.

### (0) The preview re-derived

**[P, independent; three numbers re-computed.]**  (a) `−E_π r ≤ ln μ ≤ −E_π r + L(w)` for a
remainder of oscillation `w`, `L(w) = ln((e^w − 1)/w) − 1 + w/(e^w − 1) ≤ w²/8`: the left side
is Jensen; for the right side `ln E e^Y − E Y` is convex in the law, so its maximum over
laws on an interval is at a two-point law on the end points, and maximising
`ln(1 − t + te^w) − tw` over `t` gives `t = 1/w − 1/(e^w − 1)` and the value `L(w)` (20 000 random
laws: no violation; the optimum attains it).  (b) On a box, unevaluated points are
unconstrained, so after evaluating `Q` the range of `Z` is from "ceiling off `Q`" to "floor
off `Q`"; at the centre of a constant box `[−ρ₋, ρ₊]` the bracket has width `ε` exactly when
`π(Qᶜ) = q* = η_ε/(e^{ρ₋} − e^{ε−ρ₊} + η_ε)` (checked).  (c)–(e) A member that differs from the
hint on `D` raises `Z` by at most the dip weight of `D` and lowers it by at most the bump
weight; sampling in proportion to those weights detects every alternative with
`|Δ ln Z| > η` with probability `p = min{1, ½ min(η_η Z/U, s_η Z/V)}` per sample, `U = Z(lo) − Z`,
`V = Z − Z(hi)`; disjoint sets of dip weight above `η_ε Z` give the lower bound.  Their
numbers: `1088` evaluations at `ρ = 3`, `ε = 0.2`, `δ = 0.05` (ours: `1088`); "about `5·10³`" at a
floor of `3.7` and "about `7·10⁸`" at `15.6` for `ε = 0.1` (ours: `4 610`, `6.96·10⁸`); below
`e^{0.0291n}` from `n ≈ 240` (ours: `240`).  **No error found.**  Two remarks on scope are in
"Reading" below.
*A3:* (a) is in print as stated — the right-hand inequality before the maximisation over
the mean is Hoeffding (1963), Lemma 1 and eqs. (4.12)–(4.13) (with the same letter `L`), and
`L(w) = ln S(e^w)` is the logarithm of Specht's ratio; a sharper form is free when the mean
is known: `ln μ + E_π r ≤ −wp + ln(1 − p + pe^w)`, `p = (max r − E_π r)/w`.  (b) is the stopping
criterion of the provable partition-function algorithms of computational protein design
(Georgiev, Lilien and Donald 2008, Proposition 3) specialised to a constant floor.  And
the count `1088` of (c)–(e) carries a factor two from mixing the two samplers half and
half, **and the hint is not needed for it**: at the centre of a constant box the rule
"stop when the first `N(v) = ⌈ln(1/δ)/q(v)⌉ + 1` values of the remainder are all equal to
`v`", `q(v) = min{η_η/(e^{ρ₋+v} − 1), s_η}`, certifies with **`545` evaluations and no hint**
(A3.3(a); our own check `a3_adoption_check.py`: exact failure probability over
three-level members of the box `0.031 ≤ δ = 0.05`).  What a hint buys in general is the
variance term of the estimation problem, and nothing at instances that are constant
on the bulk.

### (1) Rényi balls: the floor is the case `p = ∞`

For `1 < p ≤ ∞` and `B > 0` let `𝓑_p(B) := {r : ‖e^{−r}‖_{L^p(π)} ≤ B}`.  The box with floor
`−ρ₋` (any ceiling) is inside `𝓑_∞(e^{ρ₋})`.

**Lemma A17.1 (detection) [P; 18 000 extremal alternatives, six orders: smallest ratio
`1.000002`].**  If `r, r′ ∈ 𝓑_p(B)` differ exactly on `D`, then

    π(D)  ≥  ( |μ − μ′| / B )^{p/(p−1)}        (exponent 1 for p = ∞).

*Proof.*  `μ − μ′ = E_π (Y − Y′)1_D`, and since both are non-negative,
`|μ − μ′| ≤ max(E_π Y1_D, E_π Y′1_D) ≤ B·π(D)^{1−1/p}` by Hölder's inequality.  ∎

**Proposition A17.2 (certification with a hint) [P].**  Let the hint `r̃ ∈ 𝓑_p(B)`, `μ̃ = E_π e^{−r̃}`,
`B₀ = ‖e^{−r̃}‖_p`.
(i) *Algorithm.*  Draw `N = ⌈ln(1/δ)/q*⌉` points from `π`, `q* := (s_ε μ̃/B)^{p/(p−1)}`; evaluate; if
`r = r̃` at all of them return `ln μ̃`, otherwise report that the hint is refuted.  For
every `r ∈ 𝓑_p(B)`: if `|ln μ − ln μ̃| > ε` the hint is refuted with probability `≥ 1 − δ`; if
`r = r̃` the output is exact.
(ii) *Lower bound.*  If `B₀ < B` and no state has `π`-mass above
`q_low := (η_ε μ̃/(B − B₀))^{p/(p−1)}`, every randomised algorithm that returns `ln μ` within `ε/2`
with probability `≥ 1 − δ` on `𝓑_p(B)` makes at `r̃` at least `(1 − 2δ)·⌊1/(2q_low)⌋` evaluations
in expectation, with or without the hint.
*Proof.*  (i) `|ln μ − ln μ̃| > ε` implies `|μ − μ̃| > s_ε μ̃` in both directions; Lemma A17.1 gives
`π({r ≠ r̃}) > q*`; each sample lands there with at least that probability.  (ii) For a
set `D` of mass `q > q_low` put `Y′ = Ỹ + a1_D`, `a = (B − B₀)q^{−1/p}`: by Minkowski's inequality
`‖Y′‖_p ≤ B₀ + aq^{1/p} = B`, and `μ′ − μ̃ = (B − B₀)q^{1−1/p} > η_ε μ̃`, i.e. `ln μ′ − ln μ̃ > ε`.  Greedy
grouping of states gives `⌊1/(2q_low)⌋` disjoint sets of mass in `(q_low, 2q_low]`; an
algorithm that is right at `r̃` and at each alternative must touch each set with
probability `≥ 1 − 2δ` when run on `r̃` (the packing argument of the theory report,
machine-checked there as `expected_queries_ge_packing`).  ∎

*In divergence form.*  `B/μ̃ = e^{((p−1)/p)κ}` where `κ` is the bound that the class puts on
`D_p(π_g‖π)` at the hint.  So, for `B − B₀ ≥ B/2` and `ε ≤ 1`,

    certification cost with a hint  =  Θ( e^{κ} / ε^{p/(p−1)} ),      κ = the a-priori bound on D_p(π_g ‖ π),

with constants depending on `δ` only.  **`p = ∞`: `e^{κ}/ε` — the theory division's theorem**
(`κ = ρ₋ + ln(Z₀/Z)`, `e^{κ} = Z(lo)/Z`); `p = 2`: `(1 + χ²)/ε²`, with `χ²` the bound on the
chi-square divergence of the true ensemble from the model.

**Proposition A17.3 (without a hint) [P for the upper bounds; P-sketch for the lower
bound].**  (i) For `p ≥ 2` the plain estimator `μ̂ = N^{−1}Σ Y(x_i)`, `x_i ∼ π`, satisfies
`|μ̂ − μ| ≤ ‖Y‖₂/√(Nδ)` with probability `≥ 1 − δ` (Chebyshev), and
`‖Y‖₂² ≤ μ^{(p−2)/(p−1)}B^{p/(p−1)} ≤ B²` (log-convexity of norms); so
`[μ̂ − B/√(Nδ), μ̂ + B/√(Nδ)]` **is a certificate valid for every member and every `N`**
(simulation on a log-normal instance: miss rate `0.006` at `δ = 0.1`), and relative
accuracy `ε` needs about `e^{κ}/(δ s_ε²)` evaluations (`‖Y‖₂²/μ² ≤ (B/μ)^{p/(p−1)} = e^{κ}`).  (ii) For `1 < p < 2` the median of block means gives accuracy
`ε` with `O(ln(1/δ)·e^{κ}/ε^{p/(p−1)})` evaluations (the median of means under a moment of
order `p ∈ (1, 2]` — *A3:* Bubeck, Cesa-Bianchi and Lugosi, arXiv:1209.1727, Lemma 2, read
by the workstream in full; the matching lower bound is Devroye, Lerasle, Lugosi and
Oliveira, arXiv:1509.05845, Theorem 3.1).  (iii) In the worst case over
the class the variance term is needed without a hint: for instances `Y = 1 + a1_S` with
`S` a random set of mass `q` the mean can only be learned by estimating `q`, which costs
`σ²/(εμ)²`.  Hence

    without a hint:  Θ( e^{κ} / ε^{max(2, p/(p−1))} ) in the worst case;
    the hint saves the factor ε^{−(p−2)/(p−1)} for p > 2 and nothing for p ≤ 2.

For `p = ∞` these are the two terms `σ²/(εμ)²` and `1/(εμ)` of the optimal stopping-rule
theorem for `[0,1]`-valued variables (Dagum, Karp, Luby and Ross, SIAM J. Comput. 29
(2000) 1484–1496) applied to `X = e^{−(r − lo)}` under the floor measure, whose mean is
`Z(g)/Z(lo)`.  *A3:* the original could not be opened (eight routes tried); the theorem
was read in three restatements — `T ≍ max(σ², εμ)·ln(2/δ)/(εμ)²` samples are sufficient
and, for every stopping rule, necessary (Mnih, Szepesvári and Audibert, ICML 2008, §3) —
and one of them reports that the published *proof* of the upper tail has a gap while
the statement holds (Chen, arXiv:0711.2801, Appendix D): cite the theorem, not the proof.
So the reading stands: **the hinted cost of the box-class theorem is the second term of
a known bound; a hint removes the variance term and nothing else.**  And the whole of
this proposition is in print: see "What is in print" below.

### (2) A Kullback–Leibler bound: possible, at an exponential price in the accuracy

**Proposition A17.4 [P at the centre; exact two-level alternatives and 1 108 random
alternatives].**  Let the class be `{r : D_1(π_g‖π) ≤ κ}` and the hint the centre `r̃ = 0`.
(i) Every alternative with `|ln μ′| > ε` differs from the hint on a set of mass at least
`exp(−(κ + ln 2)/s_ε)`.  (ii) There are alternatives with `ln μ′ > ε` on every set of mass
above `≈ η_ε·exp(−(κ + ε)/s_ε)`.  So the cost is `exp(Θ(κ/ε))` for small `ε`: finite, and
exponential in `1/ε`.
*Proof.*  (i) Upward: `π′(D) = 1 − π(Dᶜ)/μ′ ≥ s_ε`, and by the data-processing inequality
`κ ≥ kl(π′(D)‖π(D)) ≥ s_ε ln(1/π(D)) − ln 2`.  Downward: `π′(Dᶜ) = π(Dᶜ)/μ′ ≤ 1` forces
`π(D) ≥ s_ε`.  (ii) `Y′ = 1 + a1_D`, `aπ(D) = η_ε`: `D_1 = −ε + (π(D) + η_ε)e^{−ε} ln(1 + η_ε/π(D))`.  ∎
The Rényi family degenerates consistently: `ε^{−p/(p−1)} → ∞` as `p → 1` at fixed `κ`.

### (3) What does not suffice

**Proposition A17.5 [P; trivial once stated].**  (i) A bound on `‖Y‖₁` (`p = 1`) is a bound on
`μ` itself and nothing more: alternatives exist on every single state, and a certificate
must evaluate all of them.  (ii) **A bound on any polynomial moment of the remainder
energy under the model — its mean, its root mean square, `E_π|r|^k ≤ M` — does not bound
the cost by anything smaller than the number of states**: a dip of depth `d` on a state
of mass `q` costs `q d^k` of the moment budget and changes `μ` by `q(e^d − 1)`, which is
unbounded as `q → 0` at fixed budget (`σ = 0.1 k_BT` in root mean square allows a dip of
`100 k_BT` on a state of mass `10⁻⁶`, a change of `ln μ` by `86`).
So the answer to our own request P-T3 is: **a "typical norm" that certifies must be an
exponential moment of the remainder under the model — a Rényi or Kullback–Leibler
bound on the true ensemble relative to the model — and the root-mean-square remainder
that fits report is not one — *on its own*.**  (Refined after checkpoint 36, part (7)
below: an a-priori bound on the variance of the remainder under the model **together
with a one-sided floor** is an exponential-moment bound, by Bennett's inequality, and
then brackets `ln Z` with no exponential cost at all.)

### (4) The table

Cost of certifying `ln Z` within `ε` (model samples free; `κ` the a-priori bound on the
divergence named; constants depend on `δ`):

| what is bounded a priori | with a hint | without a hint (worst case) |
|---|---|---|
| a pointwise floor — `D_∞(π_g‖π) ≤ κ` | `e^{κ}/ε` (theory division) | `e^{κ}/ε²` |
| a Rényi divergence of order `p ≥ 2` | `e^{κ}/ε^{p/(p−1)}` | `e^{κ}/ε²` |
| a Rényi divergence of order `1 < p ≤ 2` | `e^{κ}/ε^{p/(p−1)}` | the same order |
| the Kullback–Leibler divergence `D_1(π_g‖π)` | `e^{Θ(κ/ε)}` | at least that |
| mean, variance or any polynomial moment of `g − ĝ` under the model | the number of states | the number of states |
| **a one-sided floor `b` below the mean *and* the variance `σ²` of `g − ĝ` under the model** (part (7)) | none beyond the mean: `ln Z` is bracketed within `W(b, σ²) ≈ (σ²/b²)(e^b − 1 − b)`; below that width, as in the first row | the mean: `σ²/(δε²)` |

*A3 — whose table this is.*  Rows 1–4, right-hand column, are the main result of Block
and Shetty (arXiv:2602.23535v1, 26 February 2026; statements read by the coordinator; since published in the Proceedings of the 39th Conference on Learning Theory, PMLR 336:760–790, 2026 — search result, the published version not opened):
with samples of the model and the unnormalised density ratio at the samples,
`γ_f(6D_f/ε)·ln(1/δ)/ε ∨ c²/ε²` samples suffice for a `(1 ± ε)` estimate of the partition
function (their Theorem 5) — `e^{κ}ε^{−p/(p−1)}` for Rényi order `1 < p ≤ 2`, `ε^{−2}` beyond,
`exp(c·κ/ε)/ε` for Kullback–Leibler — with lower bounds `γ_f(C/(2ε))/ε` (Theorem 8), `ε^{−2}`
under a bounded density ratio (Proposition 2) and impossibility when `f` is linear
(Proposition 1).  So the fourth row should read `exp(Θ(κ/ε))/ε` in both columns, proved
there beyond the centre.  The exponent `max{2, p/(p−1)}` with lower bounds for all
randomised algorithms that use function values is earlier: Kunsch, Novak and Rudolf
(arXiv:1805.08637; J. Complexity 53 (2019)), Theorems 3.9, 3.10 and Corollary 3.14, for
absolute error and central norms.  The left-hand column is their Theorem 6 re-read: a
one-sided estimator, `(1 − ε)Z ≤ Ẑ ≤ M·Z`, from `ln(1/δ)·M/ε` samples with `M = γ_f(6D_f/ε)` —
"no mass was missed" at the hinted cost, *without* a hint; a hint replaces their loose
upper tail by the claimed value.  The fifth row was not found stated and is elementary;
the sixth is part (7).

**The direction matters [P, trivial; reading H].**  (*A3:* in print — "exclusive"
divergences "exclude parts of the target", Minka, MSR-TR-2005-173 (2005); as an estimate
of sample sizes in free-energy perturbation, Jarzynski, arXiv:cond-mat/0603185, eq. (45);
as a theorem at one pair of ensembles, Chatterjee and Diaconis, arXiv:1511.01437,
Theorem 1.1.)  Every row is a divergence of the
*true ensemble from the model*, `D(π_g‖π)`.  The variational (Gibbs–Bogoliubov) principle
minimises the opposite one, `D_1(π‖π_g) = ln μ + E_π r`, which is the gap of the *cheap* side
of the bracket.  A model chosen variationally is optimal for the side that costs a mean
and can be arbitrarily bad for the side that costs `e^{κ}`: it may ignore a basin of the
true ensemble altogether (`D_p(π_g‖π) = ∞`).  *A planted control* [N, exact sums;
`experiments/science/pi_inference/surrogate_direction_check.py`]: an additive bulk plus a
basin of depth `14–30 k_BT` on a Hamming ball of radius 1 of the 12-cube (true weight of
the basin `0.05–0.74`), product surrogates fitted variationally, by least squares under
the uniform measure, and by likelihood (the true marginals):

| fit | RMS error under its own measure (`k_BT`) | `D_1(π‖π_g)` | `D_2(π_g‖π)` | `D_∞(π_g‖π)` |
|---|---|---|---|---|
| variational | `5·10⁻⁶ – 4·10⁻³` | `0.05 – 1.3` | `11.4 – 28.3` | `13.9 – 29.7` |
| least squares | `0.10 – 0.14` | `0.06 – 1.3` | `10.8 – 26.7` | `13.3 – 28.0` |
| likelihood | `0.46 – 5.9` | `0.15 – 11.7` | `8.3 – 13.3` | `10.8 – 16.3` |

The ranking by either measure of fit quality is the reverse of the ranking by certified
cost (`e^{D_2}/ε²`, `e^{D_∞}/ε`).  In this control no product surrogate is *useful* — every
cost exceeds enumeration of `2¹²` states; the point is the ordering, and that the first
two columns do not see the basin at all.

### (5) Where a divergence bound comes from: first-order classes on product measures

**Proposition A17.6 — sharp form, replacing the first one at checkpoint 39 [P by
workstream A3 (its A3.2), proof read and re-derived by the coordinator; a direct
corollary of two statements in the differential-privacy literature, see below; checked
twice independently: A3's `check_math.py` C5 (1 200 members) and our
`a3_adoption_check.py` (898 members, seven orders, 50 digits): no violation, largest
ratio `0.993`].**  Let `π` be a product measure on a product space and let `r` have
one-site oscillations `c_i` (changing coordinate `i` changes `r` by at most `c_i`);
`K := Σ_i c_i²`; `L` as in part (0).  Then for every `p > 1`

    D_p(π_g ‖ π)  ≤  Σ_i [ (p − 1)c_i²/8 + L(c_i) ]  ≤  pK/8,       and      D_1(π_g ‖ π)  ≤  Σ_i L(c_i)  ≤  K/8;

in particular `D_2 ≤ K/4`.  So plain sampling from `π` certifies `ln Z` within `ε` with at
most `e^{K/4}/(δ s_ε²)` evaluations: `‖Y‖₂ = μ·e^{D_2/2} ≤ μ·e^{K/8}`, so by Chebyshev's
inequality `|μ̂ − μ| ≤ t·μ` with probability at least `1 − δ`, `t := e^{K/8}/√(Nδ)` — a bracket in
relative form, `μ̂/(1 + t) ≤ μ ≤ μ̂/(1 − t)`, that needs nothing but `K` (not even `E_π r`).
*Proof (A3).*  (i) *One site.*  If `P ∝ Q e^{−ρ}` with `osc ρ ≤ c`, then `Λ = ln(dP/dQ)` has
range at most `c`; `D_p(P‖Q) = (p−1)^{−1} ln E_P e^{(p−1)Λ}`; by Hoeffding's lemma under `P`,
`ln E_P e^{(p−1)(Λ − E_PΛ)} ≤ (p−1)²c²/8`, and `E_P Λ = D_1(P‖Q)` is the Jensen gap of `−Λ` under `P`
(because `E_P e^{−Λ} = 1`), hence at most `L(c)`.  (ii) *Conditionals are one-site tilts.*
`π_g(x_i | x_{<i}) ∝ π_i(x_i)·ψ_i(x_{≤i})`, `ψ_i = E_{π_{>i}} e^{−r(x_{≤i}, ·)}`, and `ψ_i` changes by a factor
at most `e^{c_i}` when `x_i` changes, because `r` changes by at most `c_i` pointwise.
(iii) *Chain rule.*  `E_π (dπ_g/dπ)^p = E_π Π_i ρ_i^p` with `ρ_i` the conditional density ratios;
integrate out the last coordinate first and use (i) conditionally.  ∎
*In print (A3; both passages read by the workstream, the first also by the
coordinator).*  Step (i) is "an `α`-bounded-range mechanism" has privacy-loss moment
generating function `≤ e^{λ²α²/8}` and mean privacy loss `≤ α/(e^α − 1) − 1 − ln(α/(e^α − 1))`
(Cesar and Rogers, arXiv:2004.07223, Lemma 3.2 — the second expression is `L(α)`); step
(iii) is the composition property of Rényi divergences (Bun and Steinke,
arXiv:1605.02065, Lemma 2.2).  The dictionary is step (ii): *the conditional law of a
site in the true ensemble, given the earlier sites, is a bounded-range pair with the
model's marginal.*
*The first form, and what changed.*  As first written (checkpoint 34, quoted in
SCI-RES-0007 §3 and in the digest) the proposition read `D_p ≤ p²K/(8(p − 1))`, `D_2 ≤ K/2`,
by McDiarmid's bound `E_π e^{−p(r − E_π r)} ≤ e^{p²K/8}` and `μ ≥ e^{−E_π r}`.  That is true and
weaker by the factor `p/(p − 1)` — two at `p = 2`, unbounded as `p → 1`, where the first form
diverges and the sharp one tends to the classical `K/8`.  The first form discards the
term `−p·ln E_π e^{−(r − E_π r)}`; the composition route keeps it.
*Sharpness.*  At the additive instance `r = u|x|` on the uniform cube
`D_2 = n ln(1 + tanh²(u/2))`, and the sharp bound is `n(u²/8 + L(u))`: ratio `0.997` at `u = 0.1`,
`0.93` at `u = 0.5`, `0.78` at `u = 1` — attained as `u → 0` (exact; `a3_adoption_check.py`).
*What it says and does not say.*  At a fixed slope per site `K = nu²` and the cost is
`e^{nu²/4}` — exponential, with a worse exponent than the optimal non-adaptive sampler
of the theory report (`a(u) ≈ u²/8` at small `u`): **nothing new about the exponents.**  What
it adds is the regime the fixed-slope asymptotics never see: **if the first-order
constants are square-summable, `Σ_i c_i² ≤ K` independently of the size, certification by
plain reweighting is polynomial — `e^{K/4}/ε²` evaluations — with no hint, no adaptivity
and a certificate that is two lines long.**  A remainder made of many weak site terms
(`c_i ≈ 0.1 k_BT` on 200 sites: `K = 2`, a factor `e^{0.5}`) is of this kind; a remainder with
`c_i ≈ 1 k_BT` is not beyond about 60 sites (`e^{15} ≈ 3·10⁶`; "30 sites" with the first form).
*A reference with interactions.*  `π` is then not a product.  Two things are known
(A3, §4.11 and the remark after its A3.2).  (a) The *first* form survives with a
mixing constant: by the coupling inequality of Chazottes, Collet, Külske and Redig
(arXiv:math/0503483, Theorem 1 and its proof, eqs. (9)–(10); read by the coordinator),
`ln E_π e^{λ(r − E_π r)} ≤ λ²‖Dδr‖²/8` with `D` the matrix of coupling probabilities, so
`D_p(π_g‖π) ≤ p²‖D‖²K/(8(p − 1))`; for Gibbs fields under Dobrushin's condition the
statement is attributed there to Külske (Comm. Math. Phys. 239 (2003); not opened).
Part (8) is this inequality for a Markov chain.  (b) The *sharp* form holds for any
reference with `c_i` replaced by `c̃_i := sup_{x_{<i}} osc_{x_i} F_i`, `F_i = −ln E_π[e^{−r} | x_{≤i}]` the
conditional free energy of the remainder — but `c̃_i` is an exponential functional that a
coupling matrix does not bound, so for interacting references the citable bound keeps
the factor `p/(p − 1)`.  How large the `c̃_i` are along a real chain model is not known
(the theory division's open request P2-T3 in another form).

### (6) The prices on real instances [M, exact enumeration; added at checkpoint 36]

`experiments/science/pi_inference/surrogate_divergence_real.py` (two seconds; reads the
enumerated rotamer grids of workstream P2, nothing sampled): 45 instances — homopeptides
of valine, leucine and serine, 2–12 residues, three fixed backbones (strand, PPII,
helix), one rotamer variable per residue, full product domains — with the ff14SB vacuum
energy `f` as known part and the GBn2 polarisation energy as remainder, at 300 K.  Three
surrogates: `m0 = f`; `m1 = f +` the best one-body fit of the solvent term; `m2 = f +` its best
pairwise fit (uniform least squares; `m2` is a pairwise model).  For each, the
divergences of the *true* ensemble from the surrogate — what the table of (4) says
certification costs — next to what a fit reports.  All in `k_BT`; ranges over instances:

| surrogate | side chain | sup-norm width of the remainder | RMS error under the surrogate | `D_2(π_g‖π_m)` | `D_∞(π_g‖π_m)` |
|---|---|---|---|---|---|
| `m0` (known part alone) | Val | up to `11.3` (`0.6–1.0` per residue) | `≤ 0.57` | `≤ 0.18` (`0.002–0.013` per residue) | `≤ 1.7` (`0.005–0.14` per residue) |
| `m0` | Leu | up to `11.9` | `≤ 1.5` | `≤ 0.70` | `≤ 4.6` |
| `m0` | Ser | up to `74` | `1.1–2.3` | `3.1 – 45` (`1.1–7.3` per residue) | `10 – 56` (`4.3–8.9` per residue) |
| `m1` (one-body fit) | Val, Leu | `≤ 1.3` | `≤ 0.10` | `≤ 0.012` | `≤ 0.70` |
| `m1` | Ser | up to `15` | `0.2–0.9` | `0.04 – 1.3` | `0.9 – 8.6` |
| `m2` (pairwise fit) | all 45 instances | `≤ 0.56` | `≤ 0.013` | `≤ 2·10⁻⁴` | `≤ 0.22` |

What the numbers say.
1. **The sup-norm width is the wrong coordinate even for a floor.**  For valine with the
   known part alone the remainder (the whole solvent term) has a width of `7–11 k_BT` at
   twelve residues, and `D_∞ = 0.07–1.7`: the remainder is most negative where the vacuum
   model already has its weight, so the *one-sided* distance that the box-class theorem
   charges for, `ρ₋ + ln(Z₀/Z)`, is a fraction of the width.  With a perfect floor the
   theory division's cost number `Z(lo)/Z(g) − 1 = e^{D_∞} − 1` is `0.07` (Val₁₂, strand) and
   `1.3·10²⁴` (Ser₆, helix).
2. **Fit quality does not predict the price** *(for a model far from the truth — see part (12): between fits of one family to the solvated energy it does, for `D_2`)*.  Serine on the helix, known part alone: the
   root-mean-square error under the surrogate goes *down* from `1.66` to `1.20 k_BT` between
   two and six residues while `D_2` goes from `16` to `45` and `D_∞` from `20` to `56` — thirteen
   orders of magnitude in the certified cost.  The variational gap goes from `1.7` to `4.4`.
3. **Which row of the table is cheaper depends on the instance.**  Serine, six residues,
   helix, one-body fit: `e^{D_2}/ε² = 370` evaluations against `e^{D_∞}/ε = 5·10⁴` at `ε = 0.1` — the
   chi-square row beats the floor row by two orders of magnitude.
4. **Everything is extensive, with very different rates.**  All divergences grow linearly
   with the number of residues: `0.002` (valine, strand) to `7.3` (serine, helix) nats per
   residue in `D_2`.  For valine on a strand a hundred residues would cost `e^{0.2}/ε²`; for
   serine nothing beyond three or four residues is within reach without the pair terms.
5. **With the pairwise fit the price is trivial in all 45 instances** (`D_∞ ≤ 0.22`) — the
   reweighting-side reading of P2's finding that this solvent term is pairwise in the
   rotamers up to small third-order constants.
6. **The first-order bound of A17.6 is the right kind of statement and far from tight.**
   `Σ_i c_i²/2` computed from the one-site oscillations of the remainder exceeded `D_2` in all
   135 rows (it is not a theorem here: the reference is pairwise, not a product) by a
   factor of at least `3.6`, typically 10–100: for Val₁₂ on the strand `2.96` against `0.024`.
   A certificate through first-order constants would price valine at `e^{0.25n}`, the truth
   is `e^{0.002n}`.  (*A3:* with the sharp constant of A17.6, `K/4` in place of `K/2`, every
   factor in this item halves — at least `1.8`, `1.48` against `0.024` for Val₁₂, a price of
   `e^{0.12n}` — and the conclusion is the same.)

**Second batch — charged, aromatic and mixed sequences [M; added after checkpoint 36;
`surrogate_divergence_real2.py`, two minutes].**  The 29 instances of P2 whose domain is
not a product (pairs of rotamers that clash are excluded; all Gibbs measures on the
clash-free domain; fits by sparse least squares on it): poly-lysine (2–4 residues),
poly-phenylalanine (4–8), the mixed sequence LKSELK (3–6).

| surrogate | family | sup-norm width | RMS error under the surrogate | `D_2` | `D_∞` |
|---|---|---|---|---|---|
| known part alone | Lys | `50 – 266` | `1.7–5.4` | `11 – 169` | `30 – 243` |
| known part alone | Phe | `9 – 26` | `0.16–2.8` | `0.2 – 2.5` | `1.6 – 13` |
| known part alone | LKS…LKSELK | `30 – 188` | `1.0–8.8` | `4.7 – 103` | `8 – 130` |
| + one-body fit | Lys / mixed | `25 – 199` / `7 – 136` | `1.3–4.7` / `0.3–4.3` | `1.4 – 40` / `0.2 – 53` | `14 – 108` / `3 – 91` |
| **+ pairwise fit** | **all 29** | up to `14.8` (Lys₄), `6.2` (LKSELK) | `≤ 0.036` | **`≤ 1.3·10⁻³`** | **`≤ 3.7`** (`≤ 1.8` for Lys, `≤ 0.21` for Phe) |

7. **For charged side chains the split "vacuum force field + solvent term" is as bad as
   the first-order constants said** (`D_∞ = 30–243` at two to four lysines; the theory
   division's remark in THY-RES-0008 §5 that no affordable floor exists for it is borne
   out) — **and moving the pair part of the solvent term into the model repairs it
   completely in the sense that matters:** with the pairwise fit `D_2 ≤ 1.3·10⁻³` and
   `D_∞ ≤ 3.7` in all 74 instances of both batches, charged ones included.
8. **The sharpest instance of "sup norm is the wrong coordinate":** for Lys₄ on the PPII
   backbone the remainder beyond the pairwise fit is `14.8 k_BT` wide — P2's third-order
   constants of `2.4–10 kcal/mol` for lysines are real — and the chi-square divergence of
   the true ensemble from the pairwise model is `10⁻⁴`.  The large many-body terms sit on
   states of negligible weight, and mostly where the truth is *less* likely than the
   model says.  A certificate through sup-norm constants would charge `e^{15}`; the
   truth is a factor `1.0`.  So for this energy term the natural row of the table is
   `p = 2`, not the floor — and what would have to be proved is a bound on an
   *exponential moment* of the third-order remainder under the pairwise model.

**What this is not.**  These divergences were computed by enumerating every state: they
are the *prices* that a certificate would have to pay, not certificates.  Whether an
a-priori bound of the right size — on `D_∞`, i.e. a floor, or on `D_2` — can be proved for
this energy term is exactly what is open (workstream P3 for the floor).  Exposed model
peptides on ideal backbones, rotamer grids, at most four lysines and six residues of a
mixed sequence, least-squares fits under the uniform measure only (the variational and
likelihood fits of benchmark B10 were not run on these instances).  In the first batch
the limitation "no charged side chains" stood until the second batch was run; the
message SCI-MSG-0017 was sent before it and says so.

### (7) A floor and a variance: a bracket with no exponential bill [P, K; M for the numbers; added after checkpoint 36]

The measurement of (6) says that for the remainder beyond the pairwise fit the
chi-square divergence is `10⁻³` while the sup-norm width is up to `15 k_BT`.  The
elementary reason has a certificate attached.

**Proposition A17.7 (Bennett bracket) [K for the inequality — *A3:* Hoeffding 1963,
Theorem 3: inequality (2.8), "the best that can be obtained" under a one-sided bound and
a variance, with the extremal two-point distribution (2.10); the weaker exponential
form (2.9) "is due to Bennett" (1962, his inequality (8b)), as Hoeffding writes — page 16
of the original read by the workstream and by the coordinator; at the level of the
moment generating function, with the extremal law: Fan, Grama and Liu, arXiv:1109.4359,
Lemma 3.1.  The sharp form checked on 20 000 random laws: no violation, equality at
the two-point law].**  Let `r = g − m`, expectations under `π_m`.  Write
`ln Z(g) − ln Z(m) = −E r + K`, `K = ln E e^{−(r − E r)} ≥ 0` (the Jensen gap; it is also
`D_1(π_m‖π_g)`).  If `r ≥ E r − b` (a one-sided floor `b > 0` below the mean) and `Var r ≤ σ²`, then

    0  ≤  K  ≤  W(b, σ²) := ln[ (b² e^{−σ²/b} + σ² e^{b}) / (b² + σ²) ]  ≤  (σ²/b²)(e^{b} − 1 − b),

and `W` is attained by the law with a state at the floor of probability `σ²/(b² + σ²)`: *a
rare deep dip is the extremal remainder, and the variance bounds how rare it must be.*
**Corollary (a certificate).**  Given a certified floor `lo ≤ r` and a certified variance
bound `σ²`: draw `N` points from `π_m`, let `r̄` be the mean of `r` on them and
`η = σ/√(Nδ)`.  With probability at least `1 − δ`,

    ln Z(m) − r̄ − η   ≤   ln Z(g)   ≤   ln Z(m) − r̄ + η + W(r̄ + η − lo, σ²).

`N` evaluations, a bracket of width `2η + W`, **no term exponential in anything unless `W`
is**: the bill of the box class, `e^{b}/ε`, is the price of *not* knowing the variance —
of allowing a dip at the floor on a set of probability up to one.  With `Var r ≤ σ²` such
a dip has probability at most `σ²/b²` and contributes at most `(σ²/b²)e^{b}` whether or not
it is ever sampled.  Below the width `W` the first row of the table applies again.
*Against Theorem 11.110(a) of the theory report:* its bound `L(w)` on the same gap uses
the two-sided width only; `W` uses the one-sided floor and the variance, and reduces to
a bound of the same kind when the variance is as large as the range allows.  (*A3:*
the two are the two moment-generating-function lemmas of one paper — range and mean,
Hoeffding's Theorem 2; a one-sided bound and the variance, his Theorem 3.)

**Two additions from the search [K → P; A3 §4.11(c′); both checked by A3 (C9) and by us
(`a3_adoption_check.py`, 29 107 random laws: no violation)].**  (i) Between the two forms
of the upper bound sits a third: `W(b, σ²) ≤ ln(1 + (σ²/b²)(e^{b} − 1 − b)) ≤ (σ²/b²)(e^{b} − 1 − b)`.
(ii) **The cheap side improves to second order as well, if the remainder also has a
ceiling:** if `r ≤ E r + a` everywhere, then

    K  ≥  ln( 1 + Var(r)·(e^{−a} − 1 + a)/a² ),

so with a floor *and* a ceiling the error of first-order perturbation theory is
bracketed from both sides at second order — `K ≈ Var(r)/2` with certified corrections —
where Gibbs–Bogoliubov alone says only `K ≥ 0`.  (This side needs the variance itself,
or a lower bound on it, not an upper bound.)  Both are the theorem of Liao and Berg
("Sharpening Jensen's inequality", arXiv:1707.08644, Theorem 1 with Lemma 1) applied to
the exponential function.

**Its use as a certificate was not found in the free-energy literature [A3: two
extended web searches, four PubMed queries, one Consensus query, eleven arXiv
queries].**  There the rigorous bracket is the two-sided Bogoliubov inequality, which
needs averages under *both* ensembles; the second-order ("mean–variance") truncation
computed from the reference alone is called an approximation that "we cannot expect …
to provide an upper or lower bound" (Delle Site and Hartmann, arXiv:2403.10918, §3.3, as
quoted by the workstream), and its convergence is judged empirically.  **"Not found" is
all that is claimed:** one paper that states rigorous generalisations of the
Gibbs–Bogoliubov inequality to higher order — Decoster, J. Phys. A 37 (2004) 9051–9070 —
could not be opened, and has to be read before this use is called new.

**On the real instances [M; `experiments/science/pi_inference/bennett_bracket_real.py`,
exact sums; 53 instances of both batches, three surrogates, 159 rows; `b` and `σ²` are the
exact values of each instance, so this measures how sharp the bracket is — it is not a
certificate].**

| surrogate | floor `b` (`k_BT`) | `σ` (`k_BT`) | true gap `K` (nats) | Bennett `W(b, σ²)` | `W/K` | range-only `L(w)` |
|---|---|---|---|---|---|---|
| pairwise fit, 42 instances with a non-zero remainder | `≤ 3.7` (`≤ 0.22` neutral, `≤ 1.8` Lys) | `≤ 0.036` | `≤ 6.3·10⁻⁴` | `≤ 3.3·10⁻³` | median `1.04`, at most `5.2` | up to `11` (median `L/K = 735`) |
| one-body fit | up to `124` | up to `4.7` | up to `23` | up to `117` | median `2.9` | up to `192` |
| known part alone | up to `257` | up to `8.8` | up to `26` | up to `247` | median `4.9` | up to `259` |
| known part alone, Val₁₂ on the strand | `0.08` | `0.19` | `0.0159` | `0.0162` | `1.02` | `4.3` |

So **first-order perturbation theory from the pairwise model — `ln Z(g) ≈ ln Z(m) − E_m r` — is
accurate to better than `10⁻³ k_BT` in every instance measured, and a one-sided floor of a
few `k_BT` with a variance bound of `(0.04 k_BT)²` would certify that to within a factor
five.**  Where the floor is tens of `k_BT` (charged or polar side chains without the pair
terms) `W` is as useless as every other bound: Bennett's inequality is exponential in
`b`, and nothing in this addendum removes the need for a moderate floor.

**Where the two inputs would come from.**  (i) *The variance.*  For a remainder that is
an explicit sum of local tables (third-order terms obtained from triples: `O(n³k³)`
evaluations instead of `kⁿ`) and a model with tractable marginals, `E_m r` and `Var_m r` are
exact finite sums — no sampling, no assumption.  For a product reference and one-site
oscillations `c_i`: `Var r ≤ ¼Σc_i²` (the tensorization of the variance, "sometimes called
the Efron–Stein inequality", with the bounded-differences corollary — *A3:* van Handel,
*Probability in High Dimension*, lecture notes of 21 December 2016, Theorem 2.3 and
Corollary 2.4, read by the workstream; Efron and Stein's own paper was not opened); for
a reference with interactions a mixing constant of the model enters (part (8)).  A variance *estimated* from
samples is not such a bound (it misses the rare state that matters; with a two-sided
range `B` its sampling error costs `e^{2b}` samples to make harmless).  (ii) *The floor.*
One-sided, for the remainder beyond pairwise: by analysis of the energy function —
workstream P3 — or, for an explicit local sum, `lo = Σ_T min r_T`.  (iii) What stays
uncertified in every such scheme is the part of the true energy that is in neither the
model nor the explicit remainder (fourth order and beyond): the same question one order
up, with — if the pattern of (6) continues — a smaller floor.

### (8) The same for a chain as reference: contraction coefficients in place of independence [P; added after checkpoint 37]

A17.6 and the variance bound of (7) assumed a product reference.  A known part with
nearest-neighbour couplings along the chain is a Markov chain, and the martingale
method gives the same statements with computable constants.

**Proposition A17.8 (Markov-chain reference) [P — the martingale method.  *A3: in
print.*  The bound on the moment generating function is inequality (10) in the proof
of Theorem 1 of Chazottes, Collet, Külske and Redig, "Concentration inequalities for
random fields via coupling", arXiv:math/0503483 — `exp(λ²‖Dδg‖²/8)` with `D` the matrix of
coupling probabilities; for a Markov chain coupled as in the proof below `(Dδr)_i ≤ C_i`,
which is the statement here (passage read by the coordinator).  In the uniform form,
with `M_n = max_i(1 + θ_i + θ_iθ_{i+1} + ⋯)` and a constant that is not sharp by a factor
four: Kontorovich and Ramanan, Ann. Probab. 36 (2008) 2126–2158, Theorem 1.2 (read by the
coordinator in the arXiv version math/0609835).  Marton's papers of 1995–1998, which
both cite for contracting chains, were not opened.  The variance bound with the
constant `¼` is the same martingale with "range `C_i` ⇒ variance `≤ C_i²/4`"; their Theorem 2
has another constant.  700 random chains and remainders by exact enumeration, `n ≤ 9`,
alphabets of 2–4 letters: no violation, largest ratios `0.98` for the variance and the
moment generating function].**  Let `π` be a Markov chain on `S_1 × … × S_n` with kernels
`P_k` from `x_k` to `x_{k+1}` and Dobrushin coefficients
`θ_k = max_{a,a′} TV(P_k(a,·), P_k(a′,·))`; let `r` have one-site oscillations `c_j`; put

    C_i := Σ_{j ≥ i} c_j · θ_i θ_{i+1} ⋯ θ_{j−1}        (C_i = c_i for a product measure; C_i = Σ_{j≥i} c_j if nothing mixes).

Then `Var_π r ≤ ¼ Σ_i C_i²` and `ln E_π e^{λ(r − E r)} ≤ λ² Σ_i C_i²/8` for every real `λ`; hence, for
`π_g ∝ π e^{−r}`, `D_p(π_g‖π) ≤ p² Σ_i C_i²/(8(p−1))`, in particular `D_2 ≤ Σ_i C_i²/2`.  (*A3:* this
divergence bound keeps the factor `p/(p − 1)` that the sharp form of A17.6 removes for
product references; the sharp route does not pass through a coupling — see the last
paragraph of part (5).)
*Proof.*  Let `M_i = E[r | x_1 … x_i]`.  For two values `a, a′` of `x_i` and the same past, couple
the two futures by the maximal coupling of each transition, staying together once
they meet: `P(x_j ≠ x′_j) ≤ θ_i ⋯ θ_{j−1}`.  Since `r(x) − r(x′) ≤ Σ_j c_j 1[x_j ≠ x′_j]`, the two
conditional expectations differ by at most `C_i`; so the martingale increment
`M_i − M_{i−1}` has conditional range at most `C_i`, conditional variance at most `C_i²/4`, and
Hoeffding's lemma applies to it.  Sum the variances; multiply the conditional moment
generating functions.  The divergence bound is the proof of A17.6.  ∎
*A sharper constant [P, elementary; added at checkpoint 43, prompted by workstream R10
(SCI-REV-0010 §5); `a17_8_sharp_constant_check.py`].*  The step "conditional range `C_i` ⇒
conditional variance `≤ C_i²/4`" gives away what the transition law knows.  The variance
is convex in the function, so over functions with range `C` under a law `q` it is
largest at an indicator:

    Var_π r ≤ Σ_i v_i C_i²,      v_i := max_b v(P_{i−1}(b, ·)),      v(q) := max_A q(A)(1 − q(A)) ≤ ¼

(`v_1` from the initial law).  For two letters `v(q) = q(0)q(1)`, and the increment is a
two-point variable, for which the Kearns–Saul inequality replaces Hoeffding's lemma:

    ln E_π e^{λ(r − E r)} ≤ λ² Σ_i κ_i C_i²,      κ_i := max_b κ(P_{i−1}(b, 1)),      κ(q) := (1 − 2q)/(4 ln((1−q)/q)) ≤ ⅛

(**[K]** Kearns and Saul, UAI 1998, pp. 311–319; proved, and stated to be attained for
every `q` at some `t`, as Theorem 4 / inequality (3) of Berend and Kontorovich, "On the
concentration of the missing mass", arXiv:1210.3248 — statement taken from a fetch of
the arXiv HTML rendering, not read in the typeset version by the coordinator; checked
here on a grid of `2·10⁶` points, largest ratio `1.000000`).  Hence, for two letters,
`D_p(π_g‖π) ≤ p²Σκ_iC_i²/(p−1)`.  Checks by exact enumeration: 700 random chains and
remainders (`n ≤ 9`, 2–4 letters), no violation of the variance bound; 352 binary ones,
no violation of the bound on the moment generating function (largest ratio `0.9965`);
gain over the constant `¼`: median `1.07`, up to `5.2`.  **For the symmetric two-state chain
(neighbours differ with probability `p`) the bound is an equality at every length for
the uniform field** `r = (u/2)Σs_i`: `Var_π r = ¼C_1² + p(1−p)Σ_{i≥2}C_i²`, per site
`(u²/4)(1−p)/p` in the limit — the structure factor at zero wave vector, which
workstream R10 identified as the small-slope factor of the theory division's chain
(Propositions R10.1–R10.2).  There the constant `¼` overshoots by `1/(4p(1−p))`: `1.19` at
`p = 0.3`, `2.78` at `p = 0.1`.  No novelty is claimed: it is the martingale method with
the variance of a two-point law, and no search was made.
*What it gives.*  With `θ_k ≤ θ < 1` and `c_j ≤ c`: `C_i ≤ c/(1 − θ)`, so all bounds of A17.6
and (7) hold for a chain with `c` replaced by `c/(1 − θ)` — a correlation length in units
of sites.  Everything is computed from the transfer matrices of the known part; no
sampling and no enumeration.  For a known part of bounded tree-width, block the sites.
*What it does not give.*  The size of the bound: on the real instances of (6) even the
product-measure form is 4–100 times above the measured `D_2` (2–50 times with the sharp
constant of A17.6), and `1/(1−θ)²` makes it worse.  It is a certificate of the right kind with the wrong constant for apolar side
chains; the sharper inputs remain the one-sided floor and the variance of (7).

### (9) Is a chain enough as the tractable model? [M, exact enumeration; added after checkpoint 37]

A pairwise model is exactly solvable only on a graph of small tree-width (the theory
division's remark on our SCI-MSG-0015).  So the practical question is whether the
*tractable* part can be cut down to a chain.  `experiments/science/pi_inference/chain_model_real.py`
(three seconds): on the 27 product-domain homopeptide instances (valine 6–12, leucine
6–8, serine 4–6 residues; strand, PPII, helix), ANOVA terms of the *total* energy `g`,
models `m_c(w) = g₀ + Σ_i g_i + Σ_{0<j−i≤w} g_ij` (a chain with couplings up to `w` residues apart —
transfer matrices at any length), remainder `r = β(g − m_c)` with everything else in it.

| family | model | floor `b` | `σ` | error of first-order perturbation theory `K` | Bennett `W` | `D_2` |
|---|---|---|---|---|---|---|
| Val, strand / PPII (8) | nearest neighbours, `w = 1` | `≤ 0.47` | `≤ 0.017` | `≤ 1.5·10⁻⁴` | `≤ 1.7·10⁻⁴` | `≤ 2.8·10⁻⁴` |
| | `w = 2` | `≤ 0.11` | `≤ 0.009` | `≤ 3.8·10⁻⁵` | `≤ 3.9·10⁻⁵` | `≤ 7.5·10⁻⁵` |
| Ser, strand / PPII (6) | `w = 1` | `≤ 0.36` | `≤ 0.17` | `≤ 0.013` | `≤ 0.016` | `≤ 0.023` |
| | `w = 2` | `≤ 0.03` | `≤ 0.010` | `≤ 4.9·10⁻⁵` | `≤ 4.9·10⁻⁵` | `≤ 9.7·10⁻⁵` |
| Leu, PPII (2) | `w = 1` | `≤ 0.04` | `≤ 0.035` | `≤ 6.0·10⁻⁴` | `≤ 6.2·10⁻⁴` | `≤ 1.1·10⁻³` |
| Leu, Ser on the helix (5) | `w = 1` or `2` | up to `3.7` | up to `0.36` | up to `0.082` | up to `0.29` | up to `0.24` |
| | all pairs | `≤ 0.22` | `≤ 0.013` | `≤ 7.8·10⁻⁵` | `≤ 8.1·10⁻⁵` | `≤ 1.5·10⁻⁴` |

9. **On a strand or a PPII backbone a next-nearest-neighbour chain is, in the sense
   that matters for a certificate, the whole solvated side-chain ensemble** of these
   homopeptides: first-order perturbation theory from it is accurate to `5·10⁻⁵` nats,
   and a floor of `0.1 k_BT` with a variance of `(0.01 k_BT)²` would certify it.  On the
   helix the pairs `i, i+3` and `i, i+4` are needed (side chains one turn apart touch), as
   one would expect — a window of four, still a chain.
10. **Consequence for size.**  A chain model has an exact partition function and exact
   samples at any length, so the three ingredients of a certified solvated side-chain
   free energy at fifty or five hundred residues are: transfer matrices (exist), a
   sampled mean of the remainder (cheap), and a *proved* one-sided floor and variance
   bound for the remainder of the chosen chain model — the only missing piece, and a
   statement about one energy function, not about algorithms.
(The other six of the 27 instances are degenerate: valine on the helix has one state
per interior residue, and leucine on the strand two states per site with the ensemble
on one of them — `K < 10⁻¹³` for every model.)
*Not shown here:* the tables of `m_c` were obtained from the full enumeration (ANOVA
averages); at a size beyond enumeration they must come from elsewhere (anchored
expansions, a smaller instance), and the remainder statistics at that size are an
extrapolation until measured (workstream P3 was told).  Homopeptides only; no charged
side chains in this part (their domains are not products).

### (10) Beyond enumeration: a chain model, a sampled mean — and what a certificate adds [M; the certificate is workstream P3's; added at checkpoint 40]

Part (9) left two things open: the tables of the chain model came from a full
enumeration, and the remainder statistics at a size beyond enumeration were an
extrapolation.  Both are now measured, and a certificate exists for one family.

**The pipeline, without any enumeration** (`experiments/science/pi_inference/beyond_enumeration_chain.py`;
Ace-X_n-NMe on a fixed ideal backbone, workstream P2's model and evaluator; `E = f + g`,
`f` the ff14SB vacuum energy, `g` the GBn2 term; 300 K).  Chain model
`m(x) = c₀ + g(x⁰) + Σ_i [h_i + a_i](x_i) + Σ_{0<j−i≤W} [J_ij + a_ij](x_i, x_j)`: `h_i`, `J_ij` the exact
tables of `f`; `a_i`, `a_ij` the anchored expansion of `g` at one reference assignment
`x⁰` — `1 + Σ_i k_i + Σ_{pairs in the window} k_i k_j` evaluations of `g`.  `ln Z(m)` and exact
samples of `π_m` by a transfer matrix over blocks of `W` sites (unit-tested against
enumeration for `W = 1 … 4`: `chain_sampler_test.py`).  The remainder `r = β(E − m)` is
evaluated at 4 000 samples.  Exact identity: `ln Z(E) = ln Z(m) − E_m r + K`, `K ≥ 0`.

| instance | assignments | evaluations for the tables | sd of `r` under `π_m` (`k_BT`) | `ln Z(m) − r̄` (± standard error) | gap `K`: exact, or the exponential-average estimate |
|---|---|---|---|---|---|
| Val₁₀, strand, `W = 2` (validation) | `5.9·10⁴` | 184 | `0.0027` | exact `ln Z = 288.9216`; sampled first order − exact `= −1·10⁻⁵` | exact `3.7·10⁻⁶` (exact floor `0.030`) |
| Val₃₀, strand | `10^{14.3}` | 604 | `0.0053` | `743.1665 ± 0.0001` | est. `1.4·10⁻⁵` |
| Val₅₀, strand | `10^{23.9}` | 1 024 | `0.0065` | `1197.4086 ± 0.0001` | est. `2.1·10⁻⁵` |
| Val₁₀, PPII, `W = 2` (validation) | `5.9·10⁴` | 184 | `0.026` | exact `291.3352`; sampled − exact `= −1.1·10⁻³` | exact `3.4·10⁻⁴` (floor `0.036`) |
| **Val₂₀, PPII** | `3.5·10⁹` | 394 | `0.045` | **`518.2618 ± 0.0007`** | est. `1.0·10⁻³` |
| Leu₈, helix, `W = 4` (validation) | 256 | 105 | `0.040` | exact `264.6485`; sampled − exact `= +7.5·10⁻⁴` | exact `8.0·10⁻⁴` (floor `0.25`) |
| Leu₂₀, helix | `10^{6.0}` | 321 | `0.16` | `593.2852 ± 0.0026` | est. `0.014` |
| Leu₃₀, helix | `10^{9.0}` | 501 | `0.19` | `866.8909 ± 0.0030` | est. `0.020` |
| Ser₅, strand, `W = 2` (validation) | `5.9·10⁴` | 613 | `0.46` | exact `118.9779`; sampled − exact `= −0.092` | exact `0.104` (floor `2.3`) |
| Ser₂₀, strand | `10^{19.1}` | 3 178 | `1.75` | `285.985 ± 0.028` | est. `1.3` — **not reliable** |
| Ser₃₀, strand | `10^{28.6}` | 4 888 | `2.0` | `397.798 ± 0.032` | est. `1.7` — **not reliable** |

11. **For valine, a chain model built from a few hundred evaluations is the solvated
    side-chain ensemble at fifty residues** — `10²⁴` assignments, 1 024 evaluations for the
    tables, a remainder of `0.007 k_BT`, first-order perturbation theory accurate to about
    `10⁻⁵` nats *if* the sampled statistics are the true ones.  For leucine on the helix a
    window of four does the same within `0.02` nats.  **For serine the anchored tables
    fail**: the remainder has a standard deviation of `0.5–2 k_BT` and the exponential
    average is the kind of estimate part (4) warns about.

**The model may be chosen freely — fit it** (`beyond_enumeration_fit.py`).  Only the
floor and the variance of the remainder under `π_m` matter, so the tables can be
improved by regression: sample the current model, evaluate `r`, fit it by least squares
with the same chain form, add the fit, repeat (three rounds of 30 000 evaluations;
statistics on 4 000 *fresh* samples of the final model; logs `beyond_enumeration_fit_*.log` —
the helix validation at sixteen residues is `…_L_H_W4_n16.log`, run from a scratch copy of
the same script so that its output name is distinct).

| instance | sd of `r` before each refit | final sd (exact) | `ln Z(m) − r̄` | gap `K`: exact or estimated | floor `b`: sampled / exact |
|---|---|---|---|---|---|
| Ser₅, strand, `W = 2` (validation) | `0.47, 0.0013, 0.0007` | `0.0007` (`0.0007`) | exact `118.9779`; sampled − exact `= −1·10⁻⁵` | exact `2.4·10⁻⁷` | `0.006` / `0.016` |
| Ser₂₀, strand | `1.76, 0.018, 0.004` | `0.0022` | `287.3297 ± 0.00003` | est. `2.4·10⁻⁶` | `0.015` / — |
| Ser₃₀, strand | `2.02, 0.027, 0.006` | `0.0029` | `399.5579 ± 0.00005` | est. `4.1·10⁻⁶` | `0.016` / — |
| Ser₂₀, strand, **`W = 3`** (consistency) | `1.20, 0.007, 0.002` | `0.0012` | `287.3297 ± 0.00002` — the same as with `W = 2` | est. `7·10⁻⁷` | `0.008` / — |
| Val₁₀, strand, `W = 2` (validation) | `0.0028, < 10⁻⁴, < 10⁻⁴` | `0.00009` (`0.00005`) | exact `288.9216`; sampled − exact `< 10⁻⁵` | exact `1.4·10⁻⁹` | `0.002` / `0.018` |
| Val₅₀, strand | `0.0065, 0.0002, 0.0002` | `0.00012` | `1197.4086 ± 0.000002` — the same as with anchored tables | est. `7·10⁻⁹` | `0.002` / — |
| Val₁₀, PPII, `W = 2` (validation) | `0.026, 0.0031, 0.0030` | `0.0033` (`0.0031`) | exact `291.3352`; sampled − exact `= −1·10⁻⁵` | exact `4.8·10⁻⁶` | `0.025` / **`0.162`** |
| **Val₂₀, PPII** | `0.046, 0.0048, 0.0049` | `0.0048` | **`518.2626 ± 0.0001`** | est. `1.1·10⁻⁵` | `0.052` / — |
| Leu₈, helix, `W = 4` (validation) | `0.040, 0.0001, 0.0001` | **`0.00012` (`0.00036`)** | exact `264.6485` | exact `6.5·10⁻⁸` (sampled estimate `7·10⁻⁹`) | `0.004` / **`0.182`** |
| **Leu₁₆, helix, `W = 4` (validation, 65 536 states)** | `0.14, 0.0013, 0.0015` | **`0.00015` (`0.00126`)** | exact `483.8466`; sampled − exact `< 10⁻⁵` | exact `7.6·10⁻⁷` (sampled estimate `1·10⁻⁸`) | `0.004` / **`0.923`** |
| Leu₂₀, helix | `0.17, 0.0005, 0.0011` | `0.0039` (largest sampled `r` `+0.25`) | `593.3030 ± 0.0001` | est. `7·10⁻⁶` | `0.004` / — |
| Leu₃₀, helix | `0.19, 0.0037, 0.0022` | `0.0022` (largest sampled `r` `+0.14`) | `866.9139 ± 0.00003` | est. `2·10⁻⁶` | `0.004` / — |

12. **With fitted tables a next-nearest-neighbour chain reproduces the solvated serine
    ensemble at thirty residues (`10^{28.6}` assignments) to a remainder of `0.003 k_BT`** —
    three orders of magnitude better than the anchored tables — from `10⁵` evaluations.
    The two routes agree where both are usable (Val₂₀/PPII: `518.2618 ± 0.0007` plus an
    estimated gap of `0.0010`, against `518.2626 ± 0.0001`), and the fitted values show
    that the exponential-average estimates of the first table were *low*, as they must
    be when the remainder is wide (Ser₃₀: true gap `399.558 − 397.798 = 1.76`, estimated
    `1.69`; a Gaussian remainder of that width would give `2.0`).
13. **A sampled floor is not a floor, and the fit makes it worse.**  The five
    validation rows have the exact values next to the sampled ones: the exact floor is
    `2.7`, `6.5`, `9`, **`45` and `230` times** the sampled one; for leucine on the helix the
    sampled variance is **nine times too small at eight residues and seventy times at
    sixteen**, and the gap estimated from the samples is too small by the same factors —
    after 90 000 fitting evaluations on domains of 256 and 65 536 states.  The regression
    makes the remainder small exactly on the states it has seen; at sixteen residues
    states of total probability of order `10⁻⁶` (inferred from the exact variance) keep a
    remainder near `−0.9 k_BT` that no sample shows.  Here it is harmless — the exact gap is
    `8·10⁻⁷` nats, and Hoeffding's Theorem 3 with the *exact* floor and variance is within
    a factor `1.5` of it (within `8 %` at eight residues) — but it is the mechanism by which
    an uncertified surrogate fails silently (part (4); Chatterjee–Diaconis, Theorem 2.1),
    seen on a real energy function, and it is worst in the compact geometry.  **Nothing
    in the two tables is a certificate.**

**What a certificate adds [P + M; workstream P3, `workstreams/P3_REPORT.md`, SCI-MSG-0020].**
The two missing numbers of part (7) — a one-sided floor and a variance bound for the
remainder, *proved* — exist for one family.  P3 evaluates the solvent term on the
Hamming ball of radius `m − 1` about an anchor, bounds the tail beyond it term by term
(a Faà di Bruno bound with interval enclosures of the derivatives, summed over all
`m`-subsets in closed form), and obtains banded pairwise models with `m₋ ≤ E ≤ m₊` on the
whole domain; then `ln Z(m₊) ≤ ln Z(E) ≤ ln Z(m₋)`, and for `r = β(E − m₋)`, `u = β(m₊ − m₋)`:
`0 ≤ r ≤ u`, `b ≤ 𝔼u`, `Var r ≤ 𝔼u²`, both exact by transfer matrix.

| Val₂₀ on PPII (`3.49·10⁹` assignments) | evaluations | result |
|---|---|---|
| chain model, anchored tables, first order (this part) | 394 + 4 000 | `518.2618 ± 0.0007` (+ est. gap `0.0010`) — **no guarantee** |
| chain model, fitted tables, first order (this part) | 90 394 + 4 000 | `518.2626 ± 0.0001` — **no guarantee** |
| P3, order `m = 4`: sandwich, no sampling | 9 921 | `[517.4843, 519.2199]` — certified |
| P3, `m = 4`, with 50 000 samples (Hoeffding, `δ = 0.05`) | 59 921 | `[518.2442, 518.2759]` |
| **P3, `m = 5`: sandwich, no sampling** | 87 441 | **`[518.2332, 518.2937]` — certified** |
| P3, `m = 5`, with 50 000 samples | 137 441 | `[518.2598, 518.2648]` |
| P3, `m = 5`, floor-plus-variance bracket of part (7) with certified `b = 0.061`, `s² = 4.8·10⁻³` (`W = 2.4·10⁻³`) | 137 441 | `[518.2608, 518.2659]` |

14. **Two independent pipelines agree to `10⁻⁴` nats at a size where nothing can be
    enumerated.**  The fitted chain model (this part: P2's evaluator, the coordinator's
    construction and code) and P3's sandwich (its own evaluator, validated against
    OpenMM's reference platform to `2·10⁻¹¹` kcal/mol; another construction; other code)
    give `518.2626 ± 0.0001` and `[518.2608, 518.2648]` (the intersection of its twelve
    intervals).  At ten residues both enumerate all 59 049 states: `291.3352` and
    `291.335178`.  The uncertified estimate costs 4 400 evaluations; the certificate
    costs twenty to thirty times more.  Its floor-plus-variance width at `m = 5`,
    `W_cert = 2.4·10⁻³`, is two hundred times the gap estimated for the fitted chain
    (`10⁻⁵`; on enumerated instances P3's `W_cert` is 4–26 times the true gap of its own
    model) — and still a few thousandths of a nat.
    *Added 2026-11-26, after workstream P6 ran the theory division's sandwich sampler on
    this instance (SCI-MSG-0025).*  That sampler gives `518.262414 ± 0.000005` and
    `518.262417 ± 0.000006` from two sandwiches and two seeds (point estimates with one
    standard error, recomputed by the coordinator from the stored points; its certified
    bracket is `[518.262315, 518.262513]`).  The value `518.2626 ± 0.0001` above (seed
    20261127, 4 000 samples: `518.262573 ± 0.000075`) was high by 1.6 of its standard
    errors: two new seeds with 40 000 samples give `518.262443 ± 0.000024` and
    `518.262457 ± 0.000025`, a long run with 600 000 samples `518.262426 ± 0.000006`
    (`beyond_enumeration_recheck_V20.py`, `…_long.py`); pooled, `518.262430 ± 0.000006`.  All
    but the first lie inside the certified bracket.  The pooled value is `1.5·10⁻⁵` nats
    above the sandwich sampler's, 2.1 standard errors of the difference.  Both samplers
    were then tested against exact enumeration at twelve residues with four and six
    million samples (`sampler_precision_check.py`): errors `(+1.5 ± 1.8)·10⁻⁶` and
    `(+0.9 ± 3.4)·10⁻⁶`, site and neighbour-pair frequencies at `rms z = 0.8–1.0`; the two
    energy functions agree to `4·10⁻¹²` on 400 states.  **Not resolved further:** a
    fluctuation of that size has probability about 0.04, and `1.5·10⁻⁵ k_BT` bears on no
    statement made here.  The table row "fitted tables" should read `518.26243 ± 0.00001`
    (pooled, 684 000 samples); the "agreement to `10⁻⁴` nats" of this item stands and is
    now an agreement to `2·10⁻⁵`.
15. **Certifiability, not accuracy, is what the helix breaks.**  For leucine on the
    helix the *price* is as small as anywhere — a fitted window-four chain leaves a
    remainder of `0.002–0.004 k_BT` at twenty and thirty residues — while P3's certified
    constants fall by only 5–8 per order there and nothing is certified at any
    affordable order.  The gap between what is true of this energy function and what
    can be proved about it is widest for compact geometries: the term-by-term bound
    cannot see the cancellation between the many neighbours inside the range of the
    solvent kernel.  That is the open problem this addendum ends on
    (`OPEN_PROBLEMS.md` D6).

*Limits.*  Everything is relative to one force-field model on a three-state rotamer grid
with a rigid ideal backbone and exposed side chains; homopeptides; one anchor and one
seed per run; the "certified" brackets rest on paper proofs and unreviewed code
(SCI-MSG-0020 §4).  The fitted models were not given to P3's sandwich.  *(Corrected at
checkpoint 42: an earlier version of this sentence called that "the obvious next
computation".  It would gain nothing.  For any model `m` the certificate knows the
remainder only through `β(m₋ − m) ≤ r ≤ β(m₊ − m)`, an interval of width `u = β(m₊ − m₋)`
whatever `m` is; the certified variance bound is smallest for the midpoint model
`(m₋ + m₊)/2`, which P3 has run — `W_cert = 6.5·10⁻⁴` at twenty residues — and a fitted
model cannot do better, however small its true remainder: the certificate cannot see
that the remainder is nearly constant.  What tightens a certificate is a narrower
sandwich — a higher order, a tighter tail bound, or the pair form of the penalties —
not a better model.)*

### (11) How often are the error bars wrong?  The baseline of benchmark B10 [M, exact laws; added at checkpoint 41]

The theory says that the usual error bar of a reweighting estimate — two standard
errors — is trustworthy when `e^{D_2}/N` is small and not otherwise, and that a bracket
with a guarantee needs an a-priori input.  On the 45 enumerated product-domain
instances of part (6), with the three surrogates `m0`, `m1`, `m2` (135 rows), the law of
the remainder under each surrogate is known exactly, so the coverage of any bracket can
be measured without evaluating an energy
(`experiments/science/pi_inference/bracket_coverage_real.py`, 80 s; 400 repetitions per
row; `N = 200, 2 000, 20 000` exact samples; `δ = 0.05`; a miss is counted when the exact
`ln μ` lies outside the bracket by more than `10⁻⁶` nats).  Four brackets: **naive** (`μ̂ ± 2`
standard errors); **EB**, the empirical-Bernstein bracket for `e^{−(r − lo)} ∈ [0, 1]` with
the *true* floor `lo` (the bracket of Liu–Fisher–Ihler's Corollary 3.2 and of the theory
division's Theorem 11.110 without a hint); **H3**, first-order perturbation theory with
Hoeffding's Theorem 3 and the *true* floor and variance (the bracket of part (7));
**H3-sampled**, the same formula with the sampled minimum and the sampled variance.

| class of `D_2(π_g‖π_m)` (rows) | naive: smallest coverage at `N = 200 / 2 000 / 20 000` | naive: largest miss (nats) | EB | H3 | H3-sampled: smallest coverage |
|---|---|---|---|---|---|
| `< 10⁻³` (69) | `0.91 / 0.92 / 0.93` | `0.004 / 0.0008 / 0.0003` | `1.000` | `≥ 0.978` | `0.99 / 1 / 1` |
| `10⁻³ … 0.1` (19) | `0.93 / 0.93 / 0.94` | `0.03 / 0.006 / 0.004` | `≥ 0.995` | `1.000` | `≥ 0.998` |
| `0.1 … 1` (23) | `0.92 / 0.93 / 0.94` | `0.16 / 0.05 / 0.02` | `≥ 0.995` | `1.000` | `≥ 0.998` |
| `1 … 5` (5: two of serine with the known part alone, three with the one-body fit) | `0.82 / 0.81 / 0.89` | `0.23 / 0.11 / 0.04` | `1.000` | `1.000` | `1.000` |
| **`≥ 5` (13: serine, known part alone)** | **`0.05 / 0.07 / 0.13`** | **`6.3 / 4.5 / 3.2`** | `1.000` | `1.000` | **`0.22 / 0.67 / 1.00`** (miss up to `4.6`) |

16. **`D_2` is what decides whether the usual error bar can be believed — on a real
    energy function, as the theory says.**  For the 117 rows with `D_2 < 1` the two-sigma
    bar covers the truth in 92–100 % of the repetitions (it is a 95 % bar).  In the 15
    rows with `D_2` between `3.1` and `45` — serine with the vacuum force field as the model —
    it covers in 7–82 % at 2 000 samples, and in the two worst rows (six serines on the
    helix and on PPII) **in 5–17 % of the repetitions at every sample size tried, missing
    by 3–6 nats**: the estimate is reproducible, its error bar is small, and it is wrong.
    Twenty thousand samples do not repair it (`e^{27}` or `e^{45}` would).  The root-mean-square
    error that a fit reports does not order the rows: six serines on the helix and four
    on the strand have remainders of `1.2` and `1.4 k_BT` under the model, and the bar
    covers in 13 % and in 75 % of the repetitions (`D_2 = 45` and `5.3`).
17. **The certified brackets never failed** (smallest coverage `0.995` and `0.978` over all
    rows and sample sizes, for a nominal `0.95`) — and where the divergence is large they
    are honest by being useless: the empirical-Bernstein bracket has no lower end, the
    Hoeffding bracket is 12–53 nats wide.  A certificate does not make a bad model good;
    it says so.
18. **With the floor and the variance known, Hoeffding's Theorem 3 beats the
    empirical-Bernstein bracket by one to two orders of magnitude for a good model** —
    with the pairwise fit (`m2`, floors `≤ 0.22 k_BT`) its width at 2 000 samples is at least
    5 times and in the median 134 times smaller (Val₁₂ on the strand: `4·10⁻⁵` against
    `0.010` nats) — **and loses for a poor one**: with the known part alone (floors of
    several `k_BT`) it is in the median `1.4` times *wider* at 2 000 samples, and it stops
    improving (Leu₈ on the helix, floor `4.7 k_BT`: Hoeffding `0.77` against `1.22` at 2 000
    samples, but `0.70` against `0.13` at 20 000 — its width cannot fall below `W`).  The
    Hoeffding width is `2σ/√(Nδ) + W(b, σ²)` and `W` grows like `e^{b}`; the empirical-Bernstein
    width is range-limited at small `N` and variance-limited at large `N`.  Which of the
    two is better is decided by the floor `b`: below about one `k_BT`, Hoeffding.  (This is
    workstream P3's question P3-T3 with numbers.)
19. **A sampled floor and variance fail exactly where they are needed** (last column):
    in the seven worst rows the "bracket" built from the sample's own minimum and
    variance covers the truth in 22–79 % of the repetitions at 200 samples.

*Limits.*  The floor and the variance given to EB and H3 are the exact ones — this
measures what the brackets deliver *if* those inputs are certified, which is part
(10)'s subject, not this one's.  Exact sampling from enumerated laws; neutral side
chains; least-squares surrogates only.

### (12) Which divergence does a fit control — and which split?  Benchmark B10 completed [M, exact sums; added after checkpoint 43]

Benchmark B10 (`BENCHMARK_DESIGN.md`) predicted that surrogates of one family fitted to
the same energy in different ways — by least squares, by the variational principle
(least `KL(q‖π_g)`), by maximum likelihood (least `KL(π_g‖q)`) — "are close in the
root-mean-square error and the variational gap and can differ by orders of magnitude in
`e^{D_2}` and `e^{D_∞}`", and named its own refutation: a family of instances on which the
root-mean-square error predicts the certified cost within a constant factor across
fits.  `experiments/science/pi_inference/b10_fit_directions.py` (two minutes, one core):
on the 45 enumerated product-domain instances, **two families fitted to the solvated
energy `g = f + g_GB` itself** — a product measure (independent residues) and a
nearest-neighbour chain — each in five ways with exact sums: `LSu` (least squares under
the uniform measure), `LSs` (least squares under the surrogate's own measure, iterated),
`VAR`, `ML`, and `CHI` (least `D_2(π_g‖q)`, the divergence the cost is exponential in).
42 of the 90 (instance, family) pairs are non-trivial (`D_2 ≥ 10⁻³` for the worst fit).

20. **The prediction fails for `D_2` on these instances.**  Across `LSu`, `VAR`, `ML`, `CHI`
    the divergence `D_2` differs by `0.007` nats in the median and `0.34` at most — a factor
    `1.4` in `e^{D_2}`, and that is the uniform-measure least-squares fit against the other
    three; among `VAR`, `ML`, `CHI` the largest difference is `0.008` nats.  The order is the
    same in all 42 pairs — `CHI < ML < VAR < LSu` — so the variational fit is never the
    one that minimises the certified cost, **and it never matters**.  The reason is that
    everything is perturbative: fitted to the solvated energy, even independent residues
    are within `D_2 ≤ 0.34` of the truth on every instance (root-mean-square remainder
    `≤ 0.61 k_BT`), and there all divergences agree to second order
    (`D_2/(2KL)` between `0.81` and `1.77`; `D_2/rms²` between `0.72` and `2.44`, median `0.91`).
    **By the benchmark's own criterion the practical content of hypothesis H11 is refuted
    on this family for the `D_2` cost: the root-mean-square remainder under the surrogate
    predicts it within a factor 2.5.**  What item 2 of part (6) showed — the
    root-mean-square remainder under the model falling with chain length while `D_2`
    rises from 16 to 45 — was for a model that is not fitted and is far from the truth
    (the vacuum force field; item 22), and the planted control has a narrow basin by
    construction.  Neither is a comparison between fits.
21. **It holds for the floor.**  `D_∞` differs across the four fits by `0.51` nats in the
    median and up to `3.2` nats (a factor 26 in `e^{D_∞}`) within one (instance, family)
    pair; `D_∞/rms` ranges from `0.7` to `386`; the variational fit never has the smallest
    floor and has the largest in 17 of 42 pairs (`CHI`: smallest in 26).  So the
    worst-case quantity, the one a certificate needs, is the one that none of these four
    fits controls and the root-mean-square error does not predict — part (10)'s "a
    sampled floor is not a floor" in another guise.  *(Corrected after the first version
    of this item, which said "the one a fit does not control": the floor has a fit of
    its own — item 24.)*
22. **The split matters more than the fit — by orders of magnitude**
    (`b10_split_table.py`).  Part (6) took the vacuum force field `f` as the model and the
    solvent term as the remainder.  For serine with three to six residues:

    | model of the solvated ensemble | `D_2(π_g‖model)` | `D_∞` |
    |---|---|---|
    | `m0`: the vacuum force field alone (exactly pairwise, all pairs) | `4.0 – 45` | `14 – 56` |
    | `m1`: `f` + one-body fit of the solvent term | `0.20 – 1.3` | `2.2 – 8.6` |
    | **independent residues, fitted to the solvated energy** | **`0.0015 – 0.096`** | `0.25 – 3.9` |
    | nearest-neighbour chain, fitted to the solvated energy | `1·10⁻⁵ – 6·10⁻³` | `0.01 – 1.8` |
    | `m2`: `f` + pairwise fit of the solvent term (all pairs) | `≤ 1.5·10⁻⁴` | `≤ 0.22` |

    **A model with no pair interactions at all is 10 to 130 times closer in `D_2` than the
    complete vacuum pair interactions with a one-body solvent correction, and 280 to
    2 600 times closer than the vacuum force field alone.**  The cause is screening,
    visible in the uniform-measure analysis of variance by order: the pair variance of
    the solvated energy is `2.6–3.2 %` of that of the vacuum energy for serine on strand
    and PPII (Ser₆, strand: `1.32 k_BT²` for `f`, `1.03` for `g_GB`, `0.041` for the sum — the
    Coulomb pair term alone `1.33`, with the solvent term `0.049`) and `23–25 %` on the
    helix; for valine it is `83–88 %` (nothing to screen) and for leucine `160–250 %` (the
    two reinforce).  The unscreened Coulomb pair terms of the vacuum energy are, as a
    model of the solvated ensemble, worse than nothing.
    *What of this was already ours, and what is added.*  That the solvent term's pair
    part "nearly cancels the vacuum Coulomb term of the known part", and that "the cost
    of the star depends on how the energy is split; that of the ball does not", is
    workstream P2's finding for the *class constants* (SCI-MSG-0015 §2; its alternative
    split `coul + g_GB`, for which the first-order constants of lysine saturate at 15
    kcal/mol where those of the solvent term alone grow to 56).  The first version of
    this item did not say so.  Added here: the size of the effect in the currency of
    reweighting (`D_2`, `D_∞`), and that a model with *no* pair terms — not only another
    pairwise split — is close.
23. **A self-consistent least-squares fit is the variational fit.**  The normal
    equations of a least-squares fit under the surrogate's own measure are the
    stationarity conditions of `KL(q‖π_g)`; where the iteration converged (45 of the 70
    pairs on which it was run) its end point is the `VAR` fit to `2·10⁻⁸` in `D_2`.  It did
    not converge in 25 (frozen or nearly frozen ensembles); a quasi-Newton minimisation
    of `KL(q‖π_g)` did everywhere.

24. **The floor has its own fit, and it is a convex programme** (`b10_floor_fit.py`; added
    after the first version of this part).  For an exponential family `q_θ ∝ e^{s_θ}` and
    every order `p > 1`,
    `D_p(π_g‖q_θ) = (p−1)^{−1} ln Σ_x exp(p ln π_g(x) − (p−1)s_θ(x)) + ln Z_θ` is convex in `θ`
    (a log-sum-exp of affine functions plus a log-partition function) [P, elementary].
    So the least-`D_p` fits are convex for all `1 < p ≤ ∞`, maximum likelihood is their
    limit `p → 1`, and `p = ∞` minimises the floor; only the variational fit is not
    convex.  (The first version of this part called the least-`D_2` fit non-convex; its
    two starts agreed because it is convex.)  Following `p = 2, 4, …, 256` with warm starts
    on the 40 instances with at most 59 049 states (80 (instance, family) pairs, 55 of
    them non-trivial): **the floor of the least-`D_256` fit is `2.6–47 %` of the floor of
    the least-`D_2` fit, `13.5 %` in the median** — `0.35` nats gained in the median, `1.5` at
    most — **for `7·10⁻⁴` nats of `D_2` in the median (`0.034` at most)**.  The least possible
    floor in the family is bracketed between `min_q D_256` and the floor attained, within
    `0.036` nats in the median (`0.16` at most).  Example, Ser₅ on the helix, independent
    residues: `D_∞ = 3.1` (maximum likelihood), `1.25` (least `D_2`), **`0.42`** (least
    `D_256`; least possible `≥ 0.39`), with `D_2 = 0.092, 0.090, 0.118`.  After the floor fit
    the largest floor over all pairs is `0.42 k_BT` for independent residues and `0.13` for
    the chain.  *What this is not:* a certificate — the fit minimises a maximum over all
    states, which is known here by enumeration; beyond enumeration a floor has to be
    proved (part (10)), and a floor-optimal fit computed from samples would be the
    sampled floor of item 13 again.

25. **Charged and aromatic side chains: the same, more strongly — and one exception
    that shows what a model without the right pairs misses** (`b10_split_charged.py`,
    `b10_split_phe_pairs.py`; added 2026-11-26).  The 29 instances of part (6) that are
    not products: poly-lysine (2–4 residues), poly-phenylalanine (4, 6, 8 residues) and
    the mixed sequence LKSELK cut to 3–6 residues, on three backbones, each on its
    clash-free domain `X_τ` (taken by mask; 225 to 898 619 states).  Families: independent
    residues and nearest-neighbour chains *restricted to* `X_τ`, fitted to the solvated
    energy by maximum likelihood (all 29) and by the floor fit of item 24 (the 23 with
    at most 60 000 states).  `D_2` of the solvated ensemble from each model, and the floor
    of the independent-residue model:

    | instances | `m0` (vacuum) | `m1` (`f` + one-body solvent) | **independent residues on `X_τ`** | chain on `X_τ` | `m2` (`f` + pairwise solvent) | `D_∞`, ML fit | `D_∞`, floor fit |
    |---|---|---|---|---|---|---|---|
    | poly-Lys (9) | `11 – 169` | `1.4 – 40` | **`2·10⁻⁵ – 0.023`** | `2·10⁻⁶ – 0.023` | `≤ 1.3·10⁻³` | `0.8 – 8.2` | `0.031 – 0.085` (Lys₂, Lys₃) |
    | LKSELK (12) | `4.7 – 103` | `0.19 – 53` | **`1·10⁻⁴ – 0.082`** | `5·10⁻⁷ – 0.081` | `≤ 1.2·10⁻³` | `0.8 – 4.5` | `0.028 – 0.21` (3–5 residues) |
    | poly-Phe, strand and helix (6) | `0.20 – 1.9` | `0.002 – 0.047` | `4·10⁻⁶ – 0.0097` | `≤ 1.5·10⁻⁷` | `≤ 3.5·10⁻⁴` | `0.23 – 2.0` | `0.05 – 0.22` |
    | **poly-Phe, PPII (2)** | `1.7, 2.5` | `0.16, 0.17` | **`0.086, 0.33`** | `0.079, 0.33` | `4·10⁻⁵, 1·10⁻⁴` | `1.1, 3.9` | `0.20, 0.44` |

    **For poly-lysine the vacuum force field is `11–169` nats away (`D_∞` up to `243`: the
    unscreened repulsion of the charged groups), and the solvated ensemble is within
    `0.023` nats of independent residues on the clash-free domain** — closer by factors
    of `6 400` to `490 000` than the vacuum model, and of `1 100` to `60 000` than the vacuum
    model with a one-body solvent correction.  After the floor fit even the worst state
    is within `0.03–0.09 k_BT` for two and three lysines.  The mixed sequence behaves the
    same (`120` to `12 000` times closer than `m1`).
    **The exception is phenylalanine on PPII:** independent residues are at `0.086`
    (Phe₄) and `0.33` (Phe₆), a nearest-neighbour chain is no better (`0.079`, `0.33`), and
    here `m1`, which keeps all pair terms of the vacuum energy, is *better* (`0.17` at Phe₆)
    — the only one of the 29 where it is.  Pair tables at one sequence separation at a
    time (`b10_split_phe_pairs.py`) say which pairs: **separation 3 alone gives `0.0066`
    and `0.0073`; separations 1 and 2 alone change nothing** (`0.079`, `0.086`; `0.328`, `0.333`);
    1 and 3 together `3.8·10⁻⁴`, `6.1·10⁻⁴`; 1, 2 and 3 `2·10⁻⁶`, `1·10⁻⁵`.  On PPII, with three
    residues per turn, the side chains of residues `i` and `i + 3` are neighbours in space.
    On the helix of these short peptides separation 1 does everything (`0.007–0.010 →
    6–8·10⁻⁸`); on the strand nothing is needed (`≤ 2·10⁻⁵` without pairs).  (Which energy
    term carries the `i, i + 3` contact was not decomposed.)
    *Reading.*  The tractable model has to be chosen by the geometry of the backbone:
    its band must reach the sequence separations that are contacts in space (three on
    PPII for large side chains), and in 13 of the 29 instances the nearest-neighbour
    chain gains less than a factor two over independent residues — what is left there is
    beyond nearest neighbours (at `D_2 ≤ 0.082` except for Phe on PPII).  *What this is
    not.*  (i) A recipe: on a masked domain these families can be sampled exactly by a
    transfer matrix only if the mask is itself banded, which was not examined.  (ii) A
    statement about class constants: workstream P2 found that even with the split
    `coul + g_GB` the star certificate fails for lysine — a worst case over a class; `D_2`
    and `D_∞` here belong to one energy function on enumerated domains.  (iii) Beyond four
    lysines, six residues of the mixed sequence, eight phenylalanines; above 60 000
    states the floor is that of the maximum-likelihood fit only (which does not control
    it, item 21).

*Consequences.*  (i) For the design of the tractable model of parts (9)–(10): fit the
*solvated* energy, as those parts did; never use the vacuum force field as the model
and the solvent term as the remainder for polar side chains.  (ii) For the theory
division's "known part plus residual": the physically given split (force field + solvent
correction) is not the one with the small residual; the class constants measured for
`g_GB` in workstream P2 are those of the bad split, and the constants of `g − (fitted
low-order model)` are the ones a certificate pays for (P3 bounded exactly these, order
by order).  (iii) For hypothesis H11: demote it — fit direction is a second-order
matter wherever a fitted model is perturbatively close; what remains true is that the
*floor* is not controlled by the usual fits (it has its own, item 24), and that an
unfitted model can be exponentially
expensive while looking adequate in root mean square (part (6); the planted control).
*Limits.*  Homopeptides of valine, leucine, serine on product domains, at most
531 441 states; two families; `VAR` is non-convex (`CHI` is convex, item 24) and both
were minimised from two starts (one start for the ten instances above 20 000 states) —
the two starts agreed to `10⁻⁸` in the objective wherever both were run; exact sums, nothing
sampled.  Charged and aromatic side chains: item 25 (maximum-likelihood and floor fits
only, on masked domains).

### (13) What a certified sandwich gives beyond `ln Z`: certified populations [P, elementary; M for the numbers; the sandwiches are workstream P3's and P6's; added 2026-11-26]

*Script:* `experiments/science/pi_inference/certified_populations.py` (+ log, JSON; three
minutes).  Model-relative as everywhere in this addendum: populations of the rotamer
model (fixed backbone, ff14SB known part, GBn2 solvent term, P2's grid), not of a
molecule.

**Statement.**  Let `m₋ ≤ E ≤ m₊` at every state, and for an event `A` write
`Z_∓(A) := Σ_{x∈A} e^{−m_∓(x)}`.  Then `Z₊(A) ≤ Z_E(A) ≤ Z₋(A)`, and since the odds
`Z_E(A)/Z_E(Aᶜ)` increase in the first and decrease in the second,

    P_E(A)  ∈  [ Z₊(A) / (Z₊(A) + Z₋(Aᶜ)),   Z₋(A) / (Z₋(A) + Z₊(Aᶜ)) ],

an interval of width `D_A + D_{Aᶜ}` in log-odds, `D_S := ln Z₋(S) − ln Z₊(S)`.  It cannot be
improved from the sandwich alone: `A` and `Aᶜ` are disjoint, so the energy function equal
to `m₋` on `A` and `m₊` on `Aᶜ` lies in the sandwich.  For `A = {x_i = a}` the restricted
sums are transfer-matrix sums of the same banded models with the other states of site
`i` removed: **no sampling and no further evaluation of the solvent term** — everything
is read off the certificate.  (For ratios of two macrostates the theory division's
Corollary 11.114 gives the *cost* of certifying in a box class; this is the range the
box allows, which is what a sandwich already in hand delivers.)

**With the sandwich sampler** (the theory division's Proposition 11.113): with
`q ∝ e^{−m₋} − e^{−m₊}` and `W` as there,
`P_E(A) = [Z₊(A) + (Z₋ − Z₊)·E_q(1_A W)] / [Z₊ + (Z₋ − Z₊)·E_q W]`; both means are of
`[0, 1]`-valued variables, so Hoeffding's inequality with a union bound gives all
populations simultaneously from the points already evaluated for `ln Z`.

26. **Validation** [M].  On ten enumerated instances (Val₈, Val₁₀, Val₁₂ on strand and
    PPII; Leu₈ on strand and helix; Ser₆ and Phe₆ on the strand), orders 3–6, site form,
    banded pair form and (three cases) triple form: **1 542 exact single-site populations
    against their intervals, no violation**; the sandwich itself re-checked at every
    state of every case, and the exact `ln Z` inside every bracket.
27. **Twenty residues on PPII (`3.5·10⁹` assignments)** [M; certified in the sense of the
    sandwich used].  Every one of the 60 single-site rotamer populations, the
    probability of the anchor assignment and the mean number of side chains off the
    anchor:

    | sandwich (band 8) | evaluations | width of `ln Z` | log-odds width of a population, largest | relative half-width of the minor populations, largest | `P`(anchor assignment) | mean number of sites off the anchor |
    |---|---|---|---|---|---|---|
    | order 4, site form (P3) | 9 921 | 1.74 | 3.95 | 0.96 | `[0.0069, 0.0389]` | `[0.64, 11.6]` |
    | order 4, pair form (P6) | 9 921 | 0.306 | 0.79 | 0.37 | `[0.0151, 0.0205]` | `[2.64, 4.73]` |
    | **order 4, triple form (P6)** | 9 921 | 0.0546 | 0.160 | 0.079 | `[0.01734, 0.01831]` | `[3.35, 3.75]` |
    | order 5, site form (P3) | 87 441 | 0.0605 | 0.141 | 0.069 | `[0.01732, 0.01840]` | `[3.35, 3.74]` |
    | order 5, pair form (P6) | 87 441 | 0.0162 | 0.042 | 0.021 | `[0.01771, 0.01800]` | `[3.49, 3.60]` |
    | **order 5, triple form (P6)** | 87 441 | 0.0090 | 0.024 | **0.012** | `[0.01778, 0.01794]` | `[3.51, 3.57]` |
    | order 5, pair form + its 50 000 sampled points (prob. ≥ 0.95, all 60 simultaneously) | 137 441 | `2·10⁻⁴` | — | **0.011** (the major populations to `3·10⁻⁴`) | — | — |

    From the narrowest deterministic sandwich an interior residue has populations
    `[0.1693, 0.1723]`, `[0.8144, 0.8176]`, `[0.01305, 0.01336]` for its three rotamers; with
    the sampled points (of the pair-form sandwich) `[0.17053, 0.17086]`, `[0.81582, 0.81634]`,
    `[0.01308, 0.01337]` — the first two inside the former, the third overlapping it (its
    upper end is `6·10⁻⁶` above; both intervals are valid, so is their intersection).
    **Without the pair or triple form the minor populations are not
    certified at order 4 at all** (relative half-width 0.96): the site form charges every
    assignment that leaves the anchor at one site the full site penalty, and the minor
    population of a site *is* such assignments; the pair form charges them nothing.
28. **Thirty residues on the strand (`2·10¹⁴` assignments), order 4, pair form, 34 281
    evaluations** [M]: every population within `0.8 %` of itself — anchor rotamer
    `[0.99070, 0.99085]`, the others `[0.00876, 0.00890]` and `[0.000396, 0.000402]` for an
    interior residue; `P`(anchor assignment) `∈ [0.7487, 0.7500]`.
29. *Two things the numbers show without being asked* [M; H for the reading].  The
    interior residues are equivalent to five digits (a check of the whole pipeline that
    was not built in), and the chain ends are not: on PPII the last residue has
    `[0.0568, 0.0579]` where the interior has `0.17`, the first `[0.1521, 0.1546]`.  A
    certified end effect, of the model.
30. *Checks of the sampled points used* (they are workstream P6's, stored): the stored
    model energies equal those of the models rebuilt here; `W` and the bracket
    `[518.262315, 518.262513]` recomputed; the frequencies of the 60 site states in the
    sample against the *exact* marginals of `q` (restricted transfer-matrix sums): largest
    `|z| = 2.5`, root mean square 1.15; the energy re-evaluated at 300 of the points
    (the same evaluator: identical).

*What this is not.*  A statement about a molecule; a certificate beyond the sandwich
it rests on (P3's constants and proofs, not machine-checked; P6's share lemmas, paper
proofs checked here on random data); populations of events other than single-site
states (pairs and blocks of neighbouring sites work the same way and were not run).
*Why it matters for the programme:* a free energy is rarely the observable; a
population is, and the same certificate bounds it — sharply, in the sense above — at no
further cost.


### (14) The leucine helix with pair shares: two workstreams combined [P for validity: workstream P6's Proposition P6.1 on workstream P3's constants; M for the numbers; added 2026-11-26]

*Script:* `experiments/science/pi_inference/helix_pair_form.py` (+ three logs, JSON).
Workstream P5 (SCI-MSG-0024) certified Ace-Leu_n-NMe on the helix with P3's unchanged
pipeline at order 6 and *site* penalties; workstream P6 (SCI-MSG-0025) proved the banded
*pair* form of the same penalties and found it decisive on the enumerated
sixteen-residue helix (0.523 → 0.015 nats at order 6).  Neither ran the pair form
beyond sixteen residues.  Here it is applied to the balls P5 had evaluated and
cached — **no new evaluation of the solvent term for the deterministic brackets** (the
ball of radius 4 is a prefix of the ball of radius 5).  What is whose: the certified
constants, band models, transfer matrix and evaluator are P3's; the closed-form sums
with excluded sites and the pair allocation are P6's; the evaluations are P5's; the
driver, the comparison and the sampled checks are the coordinator's.

31. **Twenty and thirty residues** [M; certified in the sense of the sandwich].

    | Ace-Leu_n-NMe, helix | assignments | order; band; evaluations | site form (P3/P5) | **pair form (P6), no sampling** | sandwich sampler, 1 200 accepted (prob. ≥ 0.95) | uncertified chain estimate, part (10) |
    |---|---|---|---|---|---|---|
    | `n = 20` | `1.05·10⁶` | 6; 19; 21 700 | `[593.065327, 593.699191]`; 0.634 | **`[593.297430, 593.313404]`; 0.0160** | `[593.302430, 593.303686]`; point estimate `593.303058` | `593.3030 ± 0.0001` |
    | **`n = 30`** | **`1.07·10⁹`** | 6; 20; 174 437 | `[866.650699, 867.380406]`; 0.730 | **`[866.899704, 866.932637]`; 0.0329** | `[866.912609, 866.915197]`; point estimate `866.913904` | `866.9139 ± 0.00003` |
    | `n = 30` | `1.07·10⁹` | 5; 20; 31 931 (a prefix of the cached ball) | `[866.377251, 908.218712]`; 41.8 — useless: the site-form floor has a minimum 21.8 kcal/mol below the anchor | **`[866.879220, 866.980721]`; 0.1015** | `[866.910159, 866.918248]`; point estimate `866.914212` | `866.9139 ± 0.00003` |

    The site-form brackets are those of workstream P5's run of P3's pipeline **in every
    digit** — two drivers of the same core.  60 of the cached ball values re-evaluated
    in each run: identical.  1 000 exact samples of the pair-form floor in each run (8
    distinct assignments; 0.47–0.48 sites off the anchor on average): `m₋ ≤ E ≤ m₊` at all.
    The sandwich sampler (the theory division's Proposition 11.113) evaluates five and
    eight distinct assignments for its 1 200 accepted points; `W` never outside `[0, 1]`.
    *Order 5 (row added when its run had finished):* with the pair form thirty
    residues are certified within **0.10 nats from 31 931 evaluations** — a fifth of the
    ball of order 6 — where the site form certifies nothing at that order: the same
    constants, charged to sites, pull the floor's own minimum 21.8 kcal/mol below the
    anchor.  With 1 200 sampled points (eleven distinct assignments) the bracket is
    0.008 nats.
32. **Reading.**  For this ensemble — leucine, two rotamers per site, 95 % of the weight
    on assignments with at most one side chain off the anchor — the compact case is now
    at the precision of the extended backbones: **0.033 nats at thirty residues without
    a random number**, 0.003 with a few evaluations more, and the point estimate of the
    sampler agrees with the uncertified fitted-chain value of part (10) to `4·10⁻⁶` (to
    `6·10⁻⁵` at twenty residues, where that estimate carries `± 10⁻⁴`).  The certified
    tail constant is unchanged — `Γ₆ = 32.7` kcal/mol at thirty residues, hundreds of
    times the true remainder: the gain is entirely in which assignments are charged.
    Workstream P5's request P5-E2 (order 7, to bring thirty residues below 0.1 nats) is
    thereby met at order 6 and withdrawn.
33. *What this is not.*  A statement about helices in general: for serine, lysine and
    the patterned sequence on the helix the pair and triple forms gain less than a
    factor two or leave several hundredths of a nat at orders where the ball is
    already most of the domain (workstream P6, §6).  A state-by-state check: none is
    possible at these sizes (P6 validated the pair form on the enumerated
    sixteen-residue helix at orders 4–6: 2.4 million checks, no violation).  A
    certificate beyond P3's constants and two floating-point allowances.


### (15) Where the certificate stops: a compact ensemble that is not frozen [M, exact enumeration; added 2026-11-26]

*Scripts:* `experiments/science/pi_inference/serine_helix_shares.py` (+ log, JSON; ten
seconds on workstream P6's caches) and `serine_helix_shares_law.py` (+ log).  Parts
(13)–(14) and workstreams P5, P6 certify ensembles that stay near their anchor.
Workstream P6 had already said that this is the mechanism — the pair form gains the
reciprocal of the fraction `p` of sites off the anchor, mean penalty about `Γ_m p²`
against `Γ_m p` — had measured `p = 0.55` for Ser₅ on the helix and concluded that the
polar helix ensembles "are helped by a factor below two or left useless"
(`workstreams/P6_REPORT.md` §3(i), §6(ii)–(iii)).  What was left open is whether a
*better allocation of shares* could do what pairs and triples do not.  This part closes
that: serine on the helix (2.2, 2.7, 3.3 of 4, 5, 6 side chains off the anchor under the
true ensemble; nine or six rotamer states per site), every enumerated instance and
order for which P6 left pair sums on disk.  Computed: (1) the widths of the banded
sandwiches a certificate can use (site, pair, triple form; all pairs and triples in
band); (2) with the evaluated terms kept *exact* — possible only by enumeration — the
brackets for the three share forms **and for the envelope `Σ_{T ⊆ S(x)} ĉ_T` itself, the
pointwise smallest penalty the certified constants allow and therefore a lower limit
for every share allocation**.

34. **Serine on the helix: no allocation rescues it, and it gets worse with length.**
    Widths in nats (the exact `ln Z` lies in every bracket; the sandwich holds at every
    state).

    | instance | order; ball (share of the domain) | `Γ_m` (`k_BT`) | true remainder, sup (kcal/mol) | banded models: site, pair, triple | exact evaluated terms: site, pair, triple | **envelope** |
    |---|---|---|---|---|---|---|
    | Ser₄, helix | 4; 1 316 (45 %) | 0.066 | `1.3·10⁻⁴` | 0.079, 0.047, 0.030 | 0.073, 0.041, 0.023 | **0.013** |
    | Ser₅, helix | 4; 2 696 (15 %) | 0.356 | `1.1·10⁻³` | 0.39, 0.22, 0.12 | 0.38, 0.21, 0.11 | **0.063** |
    | **Ser₆, helix** | 4; 4 751 (4.5 %) | 1.42 | `1.6·10⁻³` | 1.54, 0.85, 0.48 | 1.52, 0.83, 0.47 | **0.27** |
    | Ser₅, helix | 5; 9 496 (54 %) | 0.004 | `3.0·10⁻⁵` | 0.0150, 0.0130, 0.0119 | 0.0044, 0.0024, 0.0013 | 0.0004 |
    | Ser₆, strand (for comparison: 1.5 of 6 off the anchor) | 4; 11 249 (2.1 %) | 0.070 | `1.8·10⁻⁴` | 0.035, 0.0087, 0.0023 | 0.034, 0.0084, 0.0021 | 0.0005 |

    At order 3 on the helix every form is useless (5–16 nats).  At order 4 the best
    possible bracket is 0.013, 0.063, **0.27** nats at four, five, six residues —
    fourfold per residue, with `Γ₄` (0.07 → 0.36 → 1.42 `k_BT`: `0.07–0.1 k_BT` for each of
    the `C(n, 4)` subsets, none of them far apart yet) — while the true remainder is
    `0.003 k_BT`; the forms a certificate can actually solve give 0.48 (triples), 0.85
    (pairs), 1.54 (sites) at six residues.  Order 5 is narrow and needs more than half
    of the domain; there the banded models (0.012–0.015) are limited not by the
    allocation but by P3's reduction of the evaluated three-site terms to pair tables
    (exact terms: 0.0004–0.0044).  **For a compact ensemble with real side-chain
    entropy the certificate, with these constants, does not reach beyond enumeration
    at order 4, and at order 5 it needs the reduction replaced before the shares
    matter.**
35. **The law behind it: the bracket of the `k`-share form is `2 p^k Γ_m`** [M; the
    identity is elementary, the law is an observation].  The `k`-share penalty at a
    state is `Σ_T ĉ_T·C(|T ∩ S(x)|, k)/C(m, k)` (`k = m`: the envelope).  If sites left
    the anchor independently with probability `p`, `|T ∩ S|` would be binomial and its
    `k`-th factorial moment gives a mean penalty of exactly `p^k Γ_m`; a narrow bracket is
    twice the mean penalty.  Measured on the 13 enumerated rows (52 brackets, exact
    evaluated terms): **where the site bracket is below 0.5 nats the ratio
    `width/(2 p^k Γ_m)` lies within 0.97–1.09 for `k = 1, 2, 3` and for the envelope**
    (Ser₆ on the helix at order 4, with a site bracket of 1.5 nats: 0.99–1.08); at order
    3, where brackets are 0.6–16 nats, the first-order law fails by up to a factor 2.6.
    P6's statement is the cases `k = 1, 2`.  Consequences: each level of shares gains
    `1/p` and the envelope gains `p^{−(m−1)}` over sites — 20–40 for the frozen leucine
    helix with pairs alone (part (14)), a factor **6 in total** for serine on the helix
    at order 4 (`p = 0.54`), 60 on the strand (`p = 0.25`).  **A design rule that needs no
    run: a `k`-share certificate of order `m` reaches precision `ε` when `2 p^k Γ_m ≲ ε`,**
    with `p` from any cheap uncertified sample.
36. **What would move it** [M for the numbers; H for the reading].  Not the allocation
    (item 34).  The certified constants: here `Γ₄` is 520 times the largest true
    remainder (0.85 kcal/mol against `1.6·10⁻³` at six residues).  For serine — unlike
    leucine — workstream P5 found that the proven price of ignoring signs is small (a
    bound that does not look at signs must be 3.4–19 times the truth; for leucine
    16–153 at orders 3–5) and that slack of the inequalities is the larger part: on
    its serine instances P3's bound is 58–297 times the truth, 15–136 times that
    sign-blind floor, and 3–16 times the best bound that treats atom pairs one at a
    time.  A sharper sign-blind bound could therefore gain an order of magnitude and,
    by item 35, bring the envelope bracket at six residues to a few hundredths of a
    nat; nobody has written it.  And the decay with distance: at six residues every
    subset is local; on a longer helix the far subsets carry less, but the many-body
    terms decay like `r⁻⁴` (P5), slowly.  Whether order 5 certifies serine on a helix
    too long to enumerate has not been run: at twelve residues its ball would be
    about `4.8·10⁵` evaluations for a domain of `4.9·10⁹` (if interior sites keep six
    states, as at six residues) — the size of the runs of part (14).
37. *For the record of parts (13)–(14):* "the helix is certified" there means leucine,
    two rotamers per site, 95 % of the weight within one flip of the anchor.  This part
    is the counter-example to any wider reading.

### (16) The certificate reaches a compact ensemble that is not frozen: a first-order law, exact window terms, serine on the helix at twelve residues — and the frontier moves to charged side chains [V for the lemma; P for the validity of the window models; M; added 2026-11-26; not refereed]

*Scripts (coordinator's), all in `experiments/science/pi_inference/`:* `window_model.py`
(the model class), `window_model_check.py` (+ log: against exhaustive enumeration),
`serine_helix_reach.py` (+ one log and one JSON per run: `serine_helix_reach_<peptide>_m<order>_w<band>.log`),
`certificate_reach_table.py` (+ log, JSON), `reach_side_checks.py` (+ log: the true
remainder against the certified constants by residue type; the leucine far field).
Part (15) ended with "at order 5 it needs
the reduction replaced before the shares matter" and "whether order 5 certifies serine
on a helix too long to enumerate has not been run".  Both are done here.

**A. The cost of a sandwich is its mean band.**

38. **Lemma A17.16** [**V**: `experiments/science/pi_inference/lean/SandwichCost.lean`,
    `ScienceA17.sandwich_cost` — 228 lines, Mathlib only, the three standard axioms;
    elementary; two of its four one-sided inequalities are the Gibbs–Bogoliubov
    inequality, here with the mean under the *true* ensemble, which is the one that
    can be sampled before any model exists; no reference opened].
    Let `m₋ ≤ E ≤ m₊` on a finite set, `a = β(E − m₋)`, `b = β(m₊ − E)`, `⟨·⟩` the mean
    under the Gibbs measure of `E`, `A = sup a`.  Then
    `ln Z(m₋) − ln Z(m₊) = ln⟨e^a⟩ − ln⟨e^{−b}⟩`, and

    `⟨a⟩ ≤ ln Z(m₋) − ln Z(E) ≤ ⟨a⟩ + ½ e^A ⟨a²⟩,   ⟨b⟩ − ½⟨b²⟩ ≤ ln Z(E) − ln Z(m₊) ≤ ⟨b⟩.`

    *Proof.*  `Z(m₋) = Σ e^{−βE} e^{a} = Z(E)⟨e^a⟩` and `Z(m₊) = Z(E)⟨e^{−b}⟩`.  First
    pair: `e^t ≥ 1 + t` at `t = a − ⟨a⟩` gives `⟨e^a⟩ ≥ e^{⟨a⟩}`; `e^a ≤ 1 + a + ½a²e^A` on
    `[0, A]` and `ln u ≤ u − 1` give `ln⟨e^a⟩ ≤ ⟨a⟩ + ½e^A⟨a²⟩`.  Second pair:
    `⟨e^{−b}⟩ ≥ e^{−⟨b⟩}` likewise; `e^{−b} ≤ 1 − b + ½b²` for `b ≥ 0` and `−ln u ≥ 1 − u`
    give `−ln⟨e^{−b}⟩ ≥ ⟨b⟩ − ½⟨b²⟩`.  ∎
    *Machine-checked* as stated, with `Z(m)/Z(E) = ⟨e^{β(E − m)}⟩` (`Z_ratio`), the floor's
    side (`floor_side`) and the ceiling's side (`ceiling_side`) as separate theorems; the
    two Taylor bounds are `exp_le_quadratic_mul_exp` (by monotonicity of
    `e^a s²/2 − (e^s − 1 − s)` on `[0, a]`) and `exp_neg_le_quadratic` (from
    `1 + b + b²/2 ≤ e^b`).  What the machine check does not cover: that the sandwiches of
    this part satisfy its hypotheses (that is items 40–41), and the rule of item 39.
    So the bracket is `β⟨m₊ − m₋⟩` to first order.  **The two sides are not alike:**
    the ceiling's defect is first-order whatever the model does far from the
    ensemble (no exponential on that side); the floor's carries `e^A`.
    *Checked exactly* on 378 enumerated sandwiches (`window_model_check.py`): no
    violation; the first-order term is within 6 % of the bracket at orders `m ≥ 4`
    wherever the bracket is below 0.5 nats, within 21 % at order 3 (few states with
    penalties of several `k_BT`).
39. **The two rules** [M].  With exact evaluated terms `m₊ − m₋` is twice the penalty,
    so the bracket of a form is `2β⟨penalty⟩` to first order — computable from the
    closed-form sums of the constants and an uncertified sample of the true ensemble,
    *before the ball is paid for* ("refined rule"; the scripts print it before any
    bracket is computed).  For sites that leave the anchor independently with
    probability `p` it is `2 p^k Γ_m` (part (15), "crude rule").  The crude rule needs
    homogeneous sites: for Leu₁₂ on the helix, where only the three N-terminal side
    chains move (off-anchor frequencies 0.08, 0.11, 0.27, then zero), it is wrong by
    a factor 3 for pairs and 15 for triples at order 5 (0.138 against a bracket of
    0.047; 0.0054 against 0.00036).  *Correction of part (15),
    item 35:* its sentence "20–40 for the frozen leucine helix with pairs alone"
    quoted measured gains next to a rule that does not hold there; the measured
    gains stand, the rule is the refined one.

**B. Exact window terms (open problem D9(b), done).**

40. **The observation is not new in our record; its use here is** [P, immediate].
    Workstream P3's models are pairwise, so every evaluated term `d_U` of order
    3 … `m − 1` is replaced by a minorant in the floor and a majorant in the ceiling
    that depend on two in-band sites (`pwmodel.build_band_models`).  But its transfer
    matrix eliminates site `i` from an *array over the sites `i … i + w`*, and any
    function of sites that fit into one such window can be added to that array at no
    extra cost.  Workstream P6 used this for its triple penalty; workstream P5 wrote
    it down for evaluated terms (`P5_REPORT.md` §3.3: "the model `Σ_{U ∈ 𝒟_w} d_U` is an
    exact banded function") as part of a route it abandoned — bounding every subset
    *outside* the window by its certified constant, which fails for leucine because
    those constants are too large.  Here nothing outside the window is bounded by a
    constant: the order of the certificate and its ball are unchanged, every
    evaluated term with `max U − min U ≤ w` is kept exact, identically in floor and
    ceiling, and only the others are reduced as P3 does (`window_model.py`).  The
    penalties and therefore the validity argument are unchanged:
    `m_∓ = f + [exact or minorised/majorised I_{m−1}g] ∓ penalty`, `|g − I_{m−1}g| ≤ penalty`.
41. **Checked against exhaustive enumeration** [M, `window_model_check.py`]: 189
    sandwiches (serine, helix and strand, orders 3–5, three windows each, three
    penalty forms, three rules for the terms that do not fit a window): the model energies equal a direct evaluation that does not use
    the model class to `1.9·10⁻¹³` kcal/mol at every state; `m₋ ≤ E ≤ m₊` at every
    state; the transfer matrix equals the sum over states to `6·10⁻¹⁴`; with the full
    window the brackets equal the "exact evaluated terms" columns of part (15) up
    to the floating-point allowances those columns do not carry (`4·10⁻⁵` nats).  A
    variant of P6's triple form with a narrower window for the triples than for
    the model (`triple_form_two_windows`; P6's Lemma A′ holds for any set of triples
    declared in-window) holds at every state of 11 further enumerated sandwiches
    and equals P6's tables when the two windows coincide.  *An error of the check
    itself, found by the check:* its first version double-counted a constant in the
    direct evaluation and reported a difference of 17–21 kcal/mol while the three
    other checks passed; the constant was `c₀` (`−18.3` kcal/mol for Ser₆), corrected.
    *A better reduction of the terms that do not fit a window was tried and gains
    nothing worth having* [M, `window_model_rules.py`]: replacing such a term by its
    minimum / maximum over as few sites as possible — a maximal sub-tuple that fits a
    window instead of P3's pair — narrows the serine brackets at twelve residues by
    less than 2 % (order 5, band 6: 0.1373 → 0.1365; order 6: 0.0565 → 0.0557): the slack
    of such a term is its dependence on the far site, which every rule gives up.  Two
    rules are implemented and checked at every enumerated state; P3's stays the
    default.  *A wrong sentence of the first version, found by the check:* "the new
    rule is pointwise tighter than P3's" — false for the rule of least sup-norm slack
    (22 725 enumerated states to the contrary), true by construction for the rule
    that extends P3's chosen pair (no state to the contrary).

**C. Serine on the helix at twelve residues** (Ace-Ser₁₂-NMe, `4.9·10⁹` assignments; 6.3 of
12 side chains off the anchor under the true ensemble — heat-bath Gibbs sampling,
3 200 states, uncertified).

42. **Order 5 certifies it** [P for validity: Proposition P6.1 and item 40; M].
    Ball of radius 4: 481 506 evaluations of the solvent term, 0.0098 % of the domain,
    four minutes on one core.  Widths in nats; "rule" is the refined rule of item 39.

    | band `w` | site, pair, triple form with P3's reductions | **with exact window terms** | refined rule | terms of order ≥ 3: exact / reduced | sandwich sampler on the triple form (2 000 points; prob. ≥ 0.95) |
    |---|---|---|---|---|---|
    | 6 | 0.364, 0.259, 0.211 | 0.290, 0.185, 0.137 | 0.242, 0.138, 0.089 | 245 / 470 | [227.36446, 227.37283] |
    | 7 | 0.336, 0.227, 0.174 | 0.257, 0.148, **0.094** | 0.242, 0.133, 0.080 | 350 / 365 | [227.36590, 227.37162] |
    | 8 | 0.328, 0.216, 0.159 | 0.246, 0.134, **0.077** | 0.242, 0.131, 0.073 | 462 / 253 | [227.36642, 227.37111] |

    **Certified without sampling: `ln Z ∈ [227.329971, 227.407160]`, 0.077 nats** (triple shares,
    band 8).  The sandwich holds at all 3 200 Gibbs states of the true ensemble and at
    4 000 exact samples of the floor (3 989 distinct, 6.3 sites off the anchor on
    average); an uncertified estimate by reweighting the floor's samples
    (`227.36887 ± 0.00050`) and the sampler's point estimates lie inside every bracket; the
    fraction of sites off the anchor re-estimated from the reweighted floor samples
    is 0.523 (Gibbs: 0.527).  The bracket equals `β⟨m₊ − m₋⟩` over the Gibbs states
    within 2.5 % in all nine cases.  What is left above the rule is the reduction of
    the terms that do not fit a window.
43. **Orders 4 and 6** [M].  At order 4 (38 256 evaluations, band 6) the brackets are
    5.80, 3.41, 2.27 nats with exact window terms (rule: 5.80, 3.24, 2.01): useless,
    as predicted; the theory division's sampler on that sandwich still gives
    `[227.259, 227.497]` from 2 000 points.  At order 6
    (4 329 006 evaluations, 0.088 % of the domain, 22 minutes on one core) the rule
    says 0.014, 0.008, 0.006, and:

    | band `w` | site, pair, triple form with P3's reductions | **with exact window terms** | terms of order ≥ 3: exact / reduced | sandwich sampler on the triple form (2 000 points; prob. ≥ 0.95) |
    |---|---|---|---|---|
    | 6 | 0.137, 0.132, 0.130 | 0.064, 0.058, 0.057 | 341 / 1 166 | [227.36699, 227.37043] |
    | 7 | 0.109, 0.103, 0.102 | 0.030, 0.024, 0.022 | 546 / 961 | [227.36801, 227.36937] |
    | 8 | 0.102, 0.095, 0.093 | 0.020, 0.013, **0.012** | 798 / 709 | [227.36836, 227.36907] |

    **`ln Z ∈ [227.362266, 227.373868]`, 0.0116 nats without sampling** (triple shares,
    band 8); the reweighting estimate is `227.368707 ± 0.000037`; no violation of the
    sandwich at the 9 200 sampled states of any run.  At this order the penalties are
    spent — the three share forms differ by a third — and what is left is the
    evaluated terms that do not fit a window: with P3's reductions the bracket is
    0.09–0.14 nats whatever the form and whatever the band.
44. **Where the rules fail, and what survives: leucine at order 4** [M, exact
    enumeration; P for the survival, by item 38].  Ace-Leu₁₂-NMe on the helix (4 096
    assignments, exact `ln Z = 374.345343`; only the three N-terminal side chains
    move): at order 4 (`Γ₄ = 316 k_BT`; 299 evaluations) the refined rule gives 18.7,
    0.34, 0.0006 nats for sites, pairs, triples — and the certified brackets are
    187 nats in all three forms.  The floor has *delocalised*: its 4 000 exact
    samples are one state, all twelve side chains flipped, which costs `129 k_BT` in
    truth and is charged the full `Γ₄` by every share form.  The lemma allows it
    (`e^A` with `A = 316`).  (The uncertified reweighting estimate from those samples
    is meaningless there — 244.9 — and the script's line says "inside the certified
    bracket: False"; it is the estimate that fails, not the bracket.)  **So the rule is a lower estimate of the bracket; it is
    accurate when the penalty is small at every state after reweighting (`βΓ_m ≲ 1`
    suffices: serine at order 5), and it says nothing when `βΓ_m` exceeds the cost
    of leaving the anchor.**  *What survives:* **the lower end of the bracket never
    delocalises** — at order 4 it is `374.344556`, within 0.0008 nats of the exact
    value, from 299 evaluations.  A certified *upper* bound on the free energy is
    cheap; the price of the certificate is its other side.  (Why no cheap floor
    exists far from the anchor: over all 4 096 states the true solvent term varies
    by `[−2.7, +1.2]` kcal/mol while the known part rises by 3–78 kcal/mol with the
    number of flips; the certified constants of orders 1 and 2 are 5 251 and 3 924
    kcal/mol.  The ensemble is frozen by the known part; the bound does not know
    that the unknown part is small.)
    *The same peptide at orders 5 and 6* (794 and 1 586 evaluations; all pairs and
    triples in band):

    | order | form | with P3's reductions | with exact window terms | refined rule |
    |---|---|---|---|---|
    | 5 | site | 3.81 | 3.71 | 2.72 |
    | 5 | pair | 0.0570 (workstream P6's number) | 0.0472 | 0.0474 |
    | 5 | triple | 0.0071 | **0.00036** `[374.345178, 374.345533]` | 0.00009 |
    | 6 | site | 0.3186 (workstream P5's certificate, every digit) | 0.3085 | 0.310 |
    | 6 | pair | 0.0125 | 0.0049 | 0.0052 |
    | 6 | triple | 0.0074 | **0.000046** `[374.345321, 374.345366]` | 0.000019 |

    With triple shares the limit had been P3's reductions (factors 20 and 160); the
    exact value lies in every bracket.  Not run: the leucine helix at twenty and
    thirty residues with triple shares (part (14) used pairs; a narrow triple
    window loses most of the gain — 0.021 nats with triples within four residues at
    order 5 — so the triple sums of all in-band triples are needed: hours of closed
    forms at thirty residues).

**D. The reach of the certificate on the helix, predicted before paying for it**
(`certificate_reach_table.py`: constants by closed form, the true ensemble by Gibbs
sampling; twelve residues; nothing in this table is a certificate).

45. | peptide | assignments | off the anchor | `Γ₄`, `Γ₅`, `Γ₆` (`k_BT`) | refined rule, triple form, orders 4, 5, 6 (nats) | ball at orders 4, 5, 6 | verdict |
    |---|---|---|---|---|---|---|
    | Ser₁₂ | `4.9·10⁹` | 6.3 of 12 | 5.4, 0.23, 0.0073 | 1.8, 0.080, 0.0064 | `3.8·10⁴`, `4.8·10⁵`, `4.3·10⁶` | **certified at order 5 (item 42)** |
    | Leu₁₂ | 4 096 | 0.47 (three sites) | 316, 45, 5.0 | (delocalises), `9·10⁻⁵`, `2·10⁻⁵` | 299, 794, 1 586 | certified at order 5 (item 44) |
    | Phe₁₂ | `7.7·10⁴` | 0.73 (two sites) | 8.2, 0.26, 0.0056 | `2·10⁻⁶`, `8·10⁻⁶`, `3·10⁻⁵` | 1 260, 4 910, 13 700 | in reach at order 4–5 (not run) |
    | **Lys₁₂** | `9.5·10¹⁰` | 1.2 | 689, 145, 23 | 31, 7.3, 1.3 | `9.6·10⁴`, `1.6·10⁶`, `1.9·10⁷` | **out of reach** |
    | **(LKSE)₃** | `7.1·10¹⁰` | 2.8 | 1 874, 568, 147 | 100, 34, 10 | `1.8·10⁵`, `3.5·10⁶`, `4.5·10⁷` | **out of reach** |

    (Valine has no rotamer left on the ideal helix at the workstreams' threshold.)
    *Serine at sixteen and twenty residues* (`6.4·10¹²` and `8.2·10¹⁵` assignments; half
    of the side chains off the anchor): the refined rule for triples gives 0.14 and
    0.21 nats at order 5 (balls `1.6·10⁶` and `4.0·10⁶`) and 0.026 and 0.080 at order 6
    (balls `2.1·10⁷` and `6.8·10⁷`) — at order 6 the estimate is no longer the penalty but
    the floating-point allowance, which grows with the number of evaluated terms.
    Not run.
46. **The frontier of the certificate is no longer "compact" but "charged"** [M for
    the numbers; H for the reading].  Serine's and phenylalanine's constants fall
    24–46-fold per order and order 5 is enough; leucine's fall only 7–9-fold from
    `316 k_BT`, and it is certified because its ensemble is frozen (item 44).  Lysine
    and the patterned sequence have both handicaps — constants of hundreds of `k_BT`
    that fall 3–6-fold per order, and 1.2 and 2.8 of 12 side chains off the anchor —
    and no affordable order brings even the first-order estimate below a nat.  On small enumerated
    helices the ratio of the certified constant to the largest true remainder is of
    the same size for all of them (Lys₄: 178, 290 at orders 3, 4; LKSE:5: 603, 578, 347
    at orders 3–5; Ser₅: 183, 187, 80; Leu₆: 2 320, 428, 350) — what differs is the size:
    per subset the true many-body term of lysine is about twenty times that of
    serine (order 4: `2.9·10⁻³` against `1.3·10⁻⁴` kcal/mol for the one four-subset of
    four residues; `reach_side_checks.log`).  A charged group has no dipolar cancellation to lose (workstream
    P5's Theorem 9 is about neutral clusters).  Workstream P8 is on the question of
    which lever moves this (the measurement of P5 for the charged side chains; the
    decay of P3's cross bound for far pairs; what an ideal certificate would need).
47. **What this part changes** [summary].  (i) Open problem D6, "a compact ensemble
    that is not frozen": certified for serine at twelve residues (0.077 nats at order
    5, 0.012 at order 6); open for charged side chains.  (ii) D9(b), exact in-window terms: done, a factor 2–3 on the
    serine brackets and 20–160 on leucine with triple shares.  (iii) A certificate
    can be costed before it is paid for (item 39), with the proviso of item 44.
    (iv) The ceiling alone is a cheap one-sided certificate (items 38, 44).
    *Limits:* model-relative throughout; the certified constants are workstream
    P3's paper proofs; two floating-point allowances are allowances, computed by
    P3/P6 for their models and taken over unchanged for the window models (whether
    they still cover the larger number of exact terms has not been examined by
    anyone but the author — a referee workstream, R14, was stopped at launch by a
    platform safeguard and has not been replaced); at twelve residues nothing can be enumerated — the
    support beyond the proof is the enumeration checks at up to six residues, the
    sandwich at 9 200 sampled states per run (three kinds of samples), and two
    estimates inside the brackets.


### (17) Two statements of the theory division run on real instances — a sampler that pays for the envelope, and which shares — and what each needed [P for validity: their Propositions 11.113a and 11.18f, read in their report at `f7df44f`, and the elementary statements of items 52–54 (one of them **V**); M for the numbers; added 2026-11-26]

*What is whose.*  The nested sampler and its error bound, the allocation problem, its
convexity and the first-order rule are the theory division's (THY-RES-0012 §2.3, §3.2;
their Propositions 11.113a, 11.18f, unrefereed by their own account; our review of them
is workstream R15).  They asked us to run the first and said of the second "we have not
tried this on your instances".  The certified constants and band models are workstream
P3's, the closed-form sums and share forms workstream P6's.  Ours here: the inner
sandwich as built (item 48), the variant with one known mean (item 51), the reading of
site shares as the core of a convex game with its consequences (items 52–54), the runs.
*Nothing in this part has been refereed inside our division.*

**A. The nested sampler.**

48. **The inner sandwich, as built** [P, immediate].  Proposition 11.113a needs
    `m₋ ≤ e₋ ≤ E ≤ e₊ ≤ m₊` with `e_∓` computable at a state without an evaluation.  We take
    the envelope of the anchored expansion, the pointwise smallest penalty the
    certified constants allow (part (15)):
    `e_∓(x) = f(x) + Ĩ_{m−1}g(x) ∓ [env(x) + a(t) + ε_g]`, clipped into `[m₋(x), m₊(x)]`, with
    `env(x) = Σ_{T ⊆ S(x)} ĉ_T` (workstream P6's closed form with the complement of the
    changed set excluded — no subset is enumerated; or, when `C(n, m) ≤ 6000`, a table of
    all `ĉ_T` and subset sums; the two agree to `3·10⁻¹⁶` kcal/mol), `ε_g = 10⁻⁷` kcal/mol
    workstream P3's allowance for one evaluated value, and
    `a(t) = ε_g·Σ_{v=0}^{m−1} C(t, v)·C(t−v−1, m−1−v)` for a state with `t ≥ m` changed sites —
    the sum of the absolute coefficients with which evaluated ball values enter the
    interpolant there (the coefficient of `g(x_V)` in `I_{m−1}g(x)` is
    `Σ_{j ≤ m−1−|V|} (−1)^j C(t−|V|, j) = (−1)^{m−1−|V|} C(t−|V|−1, m−1−|V|)`; checked against brute
    force for `t ≤ 13`, `m ≤ 7`).  **At a state inside the ball `e₋ = e₊` = the cached value:
    `ρ = 0`, never evaluated again.**  Clipping makes the nesting hold whatever the
    bookkeeping of allowances in the outer models; it was never active.  The estimator
    targets `Z(Ê)`, `Ê` the evaluated energy clipped into `[m₋, m₊]`; `|Ê − E| ≤ ε_g`, so
    `β ε_g` is added to both ends once (the theory division's sharper form of our rounding
    remark, THY-RES-0012 §2.2).

49. **Validation by enumeration** [M; `nested_sampler.py --enum`].  Serine on the helix
    at order 4, triple shares, exact window terms: five residues (17 496 states) and six
    (104 976).  Both sandwiches hold at every state; `Z(e₊) = Z(m₊) + A·E_q β`,
    `Z(e₋) − Z(e₊) = A·E_q ρ` and `Z(Ê) = Z(m₊) + A·E_q W` hold to `3·10⁻¹⁴`; `ρ = 0` at every ball
    state; `W_in ∈ [0.41, 0.50]` and `[0.19, 0.50]`.  In 100 repetitions each of three
    proposal budgets, with 1 200 evaluations, the truth is inside every one of the eight
    kinds of bracket of items 50–51 (plain and nested; Hoeffding and empirical
    Bernstein; as stated, two ends, one known mean) in 100 of 100.

50. **What it gives at 1 200 evaluations** [M].  Widths in nats, `δ = 0.05`.  "Plain" is
    the sandwich sampler of Proposition 11.113 on the outer sandwich with the same
    number of evaluations.  "H": Hoeffding half-widths, as both propositions are stated.
    "EB": the empirical Bernstein bound of Maurer and Pontil (2009, Theorem 4:
    `E Z − Z̄ ≤ √(2V_n ln(2/δ)/n) + 7 ln(2/δ)/(3(n−1))` for i.i.d. variables in `[0, 1]`, `V_n` the
    sample variance — read in the ar5iv rendering of arXiv:0907.3740 by a fetch
    subagent, and in the same form by the theory division; applied two-sided).
    "two ends": the sharper bound found by our review workstream R15 (item 51 (iii));
    "one mean": item 51 (iii).

    | instance (order; outer form) | outer `D` | envelope bracket | `E_q ρ` | proposals | plain H | plain EB | **nested, as stated (H)** | nested, two ends (H) | nested, two ends (EB) | **nested, one mean (EB)** |
    |---|---|---|---|---|---|---|---|---|---|---|
    | Ser₅, helix (4; triples, window) — enumerated | 0.1139 | 0.0628 (exact) | 0.551 | 253 200 | 0.00897 | 0.00254 | 0.00704 | 0.00633 | 0.00205 | 0.00182 |
    | Ser₆, helix (4; triples, window) — enumerated | 0.4666 | 0.2678 (exact) | 0.566 | 239 776 | 0.0390 | 0.0166 | 0.0314 | 0.0283 | 0.0127 | 0.0122 |
    | **Val₂₀, PPII** (4; triples, workstream P6's models; `3.5·10⁹` assignments) | 0.0546 | ≈ 0.0075 | 0.137 | 400 000 | 0.00429 | 0.00147 | **0.00121** | 0.00094 | 0.00030 | **0.00027** |
    | **Ser₁₂, helix** (5; triples, window, band 7; `4.9·10⁹` assignments) | 0.0942 | ≈ 0.0185 | 0.196 | 400 000 | 0.00739 | 0.00216 | **0.00257** | 0.00211 | 0.00055 | **0.00047** |

    (Enumerated rows: means over 100 repetitions.)  **The theory division's stopping
    condition — at twenty residues and order 4, narrower than `4.3·10⁻³` from the same
    1 200 evaluations — is met: `[518.261814, 518.263022]`, `1.2·10⁻³` nats, as stated
    (`[518.261948, 518.262888]` with two ends);
    `[518.262283, 518.262553]`, `2.7·10⁻⁴`, with one mean and empirical Bernstein** — from
    11 121 evaluations in all, where 137 441 (order 5 and 50 000 sampled) gave `2.0·10⁻⁴`
    on the pair sandwich and `7.4·10⁻⁴` on the site sandwich (SCI-MSG-0025 §3).  For the serine helix: `[227.367412, 227.369984]` as stated,
    `[227.368462, 227.368935]` with one mean and empirical Bernstein — 25 times narrower
    than the order-6 certificate of part (16) (`0.0116` nats from 4.3 million
    evaluations), from 482 706 evaluations, with probability 0.95 instead of
    certainty.  The point estimate `227.368699` agrees with the uncertified estimate of
    part (16) (`227.368707 ± 0.000037`) to `8·10⁻⁶`.  No evaluated energy lay outside the
    inner sandwich (2 400 evaluations); the true remainder is on average `0.0024` and
    `0.0003` of the envelope at the evaluated states.  The envelope bracket of the serine
    helix estimated from the proposals alone, `0.01847`, is the rule `2p^mΓ_m` of part (16)
    (`0.0184`).

51. **What decides the gain** [P, arithmetic; M].
    (i) *With Hoeffding half-widths the nested bound is `2t_f + ρ̄·t₆` against the plain
    sampler's `t₂`* (`t_j = √(ln(j/δ)/(2N))`): the gain at equal evaluations is at most
    `√(ln(2/δ)/ln(6/δ))/E_q ρ = 0.878/E_q ρ` (at `δ = 0.05`), reached only as the proposals
    grow; at the "balanced" number `4N/(E_q ρ)²` of the proposition the nested bracket
    is *wider* than the plain one unless `E_q ρ < 0.44` (rows 1, 2: `0.0113` and `0.0502`
    against `0.0090` and `0.0390` at that number).  Workstream R15 gives the exact
    criterion: narrower iff `2√(N/N_f) + ρ̄ < 0.878`.  (ii) *`E_q ρ ≈ p^{m−k}`* for an outer form
    of level `k` in an ensemble with a fraction `p` of changed sites — the ratio of the
    two rules of part (16): `0.55`, `0.57` (order 4, triples, `p = 0.54`), `0.20` (order 5,
    triples: `p² = 0.28`), `0.14` (valine, `p = 0.18`).  So the nested sampler helps most
    where the outer form is far below the order — and for frozen ensembles.
    (iii) *The proposal term can be halved, in two ways* [P].  **Two ends** (workstream
    R15, SCI-REV-0015; found in review, added to the script afterwards): the error of
    the free part, `(E_qβ − β̄) + (E_qρ − ρ̄)μ`, is affine in `μ = E W_in ∈ [0, 1]`, so it is at
    most the larger of the errors of the means of `β` and of `β + ρ` — the two ends
    `Z(e₊)`, `Z(e₋)`: `|E_q W − (β̄ + ρ̄W̄_in)| ≤ max(h_β, h_{β+ρ}) + ρ̄·h_w`, i.e. `t_f + ρ̄t` in place of
    `2t_f + ρ̄t`, at the same `ln(6/δ)`.  **One known mean** (ours, written before the
    review): `c = β + ρ/2` is computable without an evaluation and
    `E_q W = E_q c + E_q ρ·(E_in W_in − ½)`, so
    `|E_q W − (c̄ + ρ̄(W̄_in − ½))| ≤ h_c + h_ρ(|W̄_in − ½| + h_w) + ρ̄·h_w`.  With Hoeffding
    half-widths the two-end form is never wider than this (R15); with a
    variance-sensitive bound the order reverses on every row of item 50, because the
    centre of the inner sandwich hardly moves relative to the outer one and `c`
    varies far less than either end (standard deviations under `q` on Ser₅: `β` 0.18,
    `β + ρ` 0.19, `ρ` 0.37, `c` 0.012).  (iv) *The variance-sensitive bound
    matters more than the nesting* on these instances: it narrows the plain sampler
    by 2.3–3.5, because `W` and `W_in` vary little (the energy sits in the middle of
    the envelope: `W_in ≈ 1/(1 + e^{β·env})`), and what remains is mostly its term
    `7 ln(·)/(3(N−1))`, two to five times the variance term at 1 200 evaluations — **the
    certified width still falls nearly as `1/N`, not `1/√N`**, until the two terms cross
    (at about `49 ln(12/δ)/(18·Var W_in)` evaluations: 7 000 for the valine instance,
    120 000 for the serine helix).  With it the nested sampler *as stated* is no
    better than the plain one on the two enumerated rows even with 16 times the
    balanced number of proposals (`0.0026` against `0.0025`; `0.0149` against `0.0166`) —
    the two proposal means `β̄`, `ρ̄` have large variances — while with two ends or with
    one known mean it is better in every row.

**B. Which shares.**

52. **Site shares are the core of a convex game** [P; classical facts, see the
    reading levels below; one consequence **V**].  Let `Γ(R) = Σ_{T ⊆ R} ĉ_T`.  Site
    penalties `γ ≥ 0` cover iff `Σ_{i∈R} γ_i ≥ Γ(R)` for every `R`.  `Γ` is supermodular
    (`Γ(R ∪ {i, j}) − Γ(R ∪ {i}) − Γ(R ∪ {j}) + Γ(R) = Σ_{T ∋ i, j, T ⊆ R ∪ {i,j}} ĉ_T ≥ 0`; checked on all
    4 096 sets of item 55), i.e. a convex game, a non-negative combination of
    unanimity games.  Hence (a) the minimal covering vectors are its *core* (cover,
    with equality on the full set); (b) the allocations of Proposition 11.18f at level
    one parametrise exactly the core (the core of a sum of convex games is the sum of
    their cores; the core of a unanimity game is the simplex on its set); (c) its
    vertices are the *marginal vectors* of the orderings of the sites,
    `γ_i = Γ(R_i) − Γ(R_i ∖ {i})`, `R_i` = `i` and the sites after it — `n + 1` closed-form sums
    on nested sets, no subset enumerated (equal to the direct assignment of every `ĉ_T`
    to the first site of `T` to `3·10⁻¹³` kcal/mol); (d) equal shares, workstream P3's
    site form, are the Shapley value, the barycentre of the `n!` marginal vectors;
    (e) **for a first-order cost `Σ p_i γ_i` the marginal vector of the ordering by
    increasing `p` — most frozen first — is optimal among all covering vectors**
    (Abel summation: `Σ p_iγ_i = Σ_j (p_(j) − p_(j−1))·γ(R_(j)) ≥ Σ_j (p_(j) − p_(j−1))·Γ(R_(j))`, with
    equality for the marginal vector) — **[V]** `ScienceA17.greedy_optimal` in
    `experiments/science/pi_inference/lean/CoreGreedy.lean` (Mathlib only; exit 0;
    standard axioms).  This is the formula of Proposition 11.18f(c).  *Reading levels:*
    Shapley, "Cores of convex games", Int. J. Game Theory 1 (1971) 11–26 — statement
    and bibliographic data confirmed by a web search (publisher's page and secondary
    sources), the paper not opened; the converse (Ichiishi 1981) and the greedy rule
    on base polyhedra (Edmonds 1970) from memory, attribution confirmed by secondary
    sources only.  Nothing here is claimed new as mathematics.

53. **The two ends are two different problems** [P].  With `m_∓ = B ∓ Σ_i γ_i[x_i ≠ x⁰_i]`
    (`B` the evaluated model or its solvable minorant / majorant): `ln Z(m₋)` is convex in
    `γ` (a log-sum-exp of affine functions) with gradient `β ×` the off-anchor marginals
    of the floor model itself — exact by transfer matrix.  So **the best floor over
    the core is a convex programme whose linear oracle is item 52(e) applied to the
    tilted marginals**: Frank–Wolfe, with a duality gap that certifies how far the
    iterate is from the best floor any site allocation can give.  `ln Z(m₊)` is convex
    too, and is to be *maximised*: its maximum over the core is at a vertex — an
    ordering; "most frozen first" by item 52(e) to first order, improved by adjacent
    swaps.  Floor and ceiling use different penalties (each covers).  The theory
    division states the convexity and "the two ends want different allocations"
    (Proposition 11.18f(b)); what the core adds is that the vertices are orderings,
    that the oracle is a sort, and that everything is computable beyond enumeration.

54. **A floor no site allocation can beat** [P, elementary].  For 0/1 indicators
    `e^{βγ·s} = Π_i (1 + s_i(e^{βγ_i} − 1)) ≥ 1 + Σ_i s_i(e^{βγ_i} − 1)`, so for the floor
    `m₋(γ) = B − Σ_i γ_i s_i` over a base model `B`,
    `ln Z(m₋(γ)) − ln Z(B) ≥ ln(1 + Σ_i p_i(e^{βγ_i} − 1))`, `p_i` the off-anchor marginal of
    site `i` under `B` (exact by transfer matrix); and every covering `γ` has
    `Σ_i βγ_i ≥ βΓ_m`.  The minimum of the right-hand side under that constraint is
    water-filling: `βγ_i = ln(λ/p_i)⁺` with `Σ_i ln(λ/p_i)⁺ = βΓ_m`, value
    `ln(1 + Σ_{active}(λ − p_i))` — **each site is charged what its rarity can pay**, and the
    site level cannot work **when `βΓ_m` does not fit under the depths `−ln p_i`**.  The
    bound is exact to first order in the boosts.  **On Leu₁₂ (item 55) the closed-form
    water-filling vector is itself a valid allocation — it covers all 4 096 sets — and
    attains the bound:** order 5: bound `0.00742`, the vector `0.00744`, Frank–Wolfe after
    2 000 steps `0.00752`; order 6: `2.64594·10⁻⁵`, `2.64597·10⁻⁵`, `2.64613·10⁻⁵`.  So where it
    covers, *the optimal site shares are known in closed form*; that it covers is not
    a theorem (a subset made of uncharged sites only would defeat it) and beyond
    enumeration it is Frank–Wolfe that guarantees the covering.  At order 4 the bound
    is 19.3 and the truth 186.7: the all-changed state is not a first-order effect.
    (A weaker form, with the probability of the cheapest single-change state of each
    site in place of its marginal, needs only `Γ_m` and the ball of radius one: `0.0045`
    and `1.6·10⁻⁵` at orders 5 and 6.  The water-filling routine was checked against a
    numerical optimiser on random instances.)

54a. **The floating-point allowance is a convex game too** [P, immediate].  Workstream
    P3 bounds the rounding of the evaluated terms at a state with changed set `S` by
    `Φ(S) = ε_g Σ_{s=1}^{m−1} C(|S|, s)·2^s` — a sum over the subsets of `S` of non-negative
    weights, the same structure as `Γ`.  Its site allocation in P3's models
    (`ε_g Σ_s C(n−1, s−1)2^s/s` per site) is the Shapley value of that game and charges a
    mobile site as if every other site had changed: `0.0049 k_BT` per site at twenty
    residues and order 6, which on three mobile sites costs `0.0023` nats — ten times
    the optimal remainder penalty there.  Allocated by the same rule (the marginal
    vector of `Γ + Φ`: the head of a suffix of `r` sites gets `ε_g Σ_s C(r−1, s−1)2^s`), the
    mobile sites pay next to nothing.  `site_allocation_fw.py` does this from here on.

55. **Leucine on the helix, twelve residues, enumerated** [M, exact;
    `allocation_core_test.py`].  Off-anchor frequencies `0.074, 0.106, 0.280` at three
    sites and below `10⁻³` at nine; the cheapest single change costs `0.9–2.5 k_BT` at the
    three and `11.4–14.1 k_BT` at the nine.  Exact evaluated terms, no allowances;
    `U` = `ln Z(m₋) − ln Z(E)` (upper end), `L` = `ln Z(E) − ln Z(m₊)` (lower end), nats.

    | order (`βΓ_m`; ball) | equal shares: `U`, `L` | most frozen first (Proposition 11.18f(c)): `U`, `L` | **Frank–Wolfe floor, best-ordering ceiling**: `U`, `L` | equal pair shares: `U + L` | equal triple shares: `U + L` |
    |---|---|---|---|---|---|
    | 3 (1 734; 79) | 1 606, 0.53 | 1 621, 0.076 | 1 606, 0.076 | 1 606 | 1 606 |
    | 4 (316; 299) | 186.9, 0.53 | 243.3, `4.8·10⁻⁵` | 186.7, `3.8·10⁻⁵` | 186.8 | 186.7 |
    | **5 (45.1; 794)** | 3.21, 0.50 | **8.59**, `2.3·10⁻⁵` | **0.0075**, `2.1·10⁻⁵` | 0.047 | 0.00035 |
    | 6 (5.0; 1 586) | 0.173, 0.135 | `3.1·10⁻⁵`, `7·10⁻⁶` | `2.6·10⁻⁵`, `7·10⁻⁶` | 0.0049 | `3.6·10⁻⁵` |

    Three things.  **(i) The first-order rule makes the ceiling exact and can break
    the floor.**  At every order from 4 on, "most frozen first" brings the lower end
    from 0.5 nats to a few `10⁻⁵` — the mobile sites carry no penalty at all, because
    every subset of four or more sites contains a frozen one.  But at order 5 it puts
    `20.2 k_BT` on a site whose cheapest change costs `14.1`, and the floor moves there:
    `U = 8.6` nats, worse than equal shares.  The rule is first-order, the floor is
    not (Lemma A17.16: the floor's side carries `e^A`); the theory division's own
    homogeneous example shows the same direction.  **(ii) The convex optimum repairs
    it:** Frank–Wolfe over the core gives `U = 0.0075` at order 5 — 430 times below equal
    shares and 4 times below equal *pair* shares — with penalties of `4.3–7.0 k_BT` on the
    frozen sites, all under their costs, and none on the mobile ones.  **(iii) Where
    the constants are small the rule alone suffices:** at order 6 it turns the site
    form's 0.31 nats into `3.9·10⁻⁵`, what equal triple shares give.  At order 4 nothing
    helps the floor, as part (16) said: the envelope's own floor is 186.7 nats.
    **(iv) The lower end alone is a one-sided certificate at order 4:** `ln Z ≥ 374.345305`
    (exact `374.345343`) from the 299 evaluations of the order-4 ball — but for a frozen
    ensemble a lower bound of `Z` is cheap anyway (the eight states of the three mobile
    sites alone give it to `10⁻⁵`); the upper end is what an order is paid for.

56. **Beyond enumeration** [M; `site_allocation_fw.py`: transfer matrices, closed-form
    sums on nested sets, the floating-point game allocated as in item 54a;
    `site_level_bound.py` for the bound of item 54].  The instance of item 55 through
    that code path, with exact window terms: equal shares `[373.850181, 377.559803]`
    (the site form of part (16), digit for digit); most frozen first at both ends
    `[374.345320, 382.933716]`; Frank–Wolfe floor (200 steps, duality gap `1.8·10⁻³`) and
    best-ordering ceiling **`[374.345322, 374.353599]`, 0.0083 nats** (exact `374.345343`).
    Longer helices, with workstream P3's reduced (pairwise, banded) models; widths in
    nats:

    | instance | `βΓ_m` | bound of item 54: floor above the penalty-free minorant | equal site shares (P3) | most frozen first, both ends | **Frank–Wolfe floor, best-ordering ceiling** | equal pair shares (part (14)) |
    |---|---|---|---|---|---|---|
    | **Leu₂₀, order 6** (band 19; ball 21 700) | 24.3 | `2.4·10⁻⁴` | 0.634 | 0.0170 | **0.0087**, `[593.300656, 593.309394]` (31 steps, duality gap `10⁻⁶`) | 0.0160 |
    | Leu₂₀, order 5 (band 19; ball 6 196) | 166.6 | 0.89 | 10.5 | 73.6 | 2.02 after 40 steps (duality gap 1.95) | not run |
    | Leu₃₀, order 5 (band 20; ball 31 931) | 340.6 | 3.46 | 41.8 | 130 | 24.5 after the two steps allowed (the bound already says no) | 0.1015 |
    | **Leu₃₀, order 6** (band 20; ball 174 437; *added after the first version of this item, when its run had finished*) | 54.8 | `4.6·10⁻⁴` | 0.730 | 0.0837 | **0.0105**, `[866.910485, 866.921008]` (6 steps, duality gap `8.8·10⁻⁴`) | not run |

    Three things.  **(i) Where `βΓ_m` fits under the depths** — order 6 at twenty
    residues — the Frank–Wolfe floor reaches the bound of item 54 to six decimals
    (`593.309394`) in 31 steps and 414 closed-form sums, and the site form — one-body
    penalties on P3's pairwise models, the simplest class of the certificate — is
    narrower than equal pair shares and 73 times narrower than equal site shares.
    What is left of the bracket there, `0.0085` of `0.0087` nats, is P3's reduction of
    the evaluated terms to pair tables (the penalty-free minorant and majorant,
    `593.309150` and `593.300678`, are that far apart; `0.0067` to `0.0086` on all four
    instances of this item), not the penalties: with optimal shares **the remainder is no
    longer the bottleneck of a frozen helix at order 6**; open problem D9(b), (c) is.
    **(ii) Where it does not fit** — order 5 at twenty and thirty residues — the bound
    says so before anything is built (0.89 and 3.46 nats), and there the level of the
    shares is the lever, as the theory division says.  **(iii) Even there the site
    level gives the best ceiling:** at thirty residues and order 5 the vertex "most
    frozen first" gives `ln Z ≥ 866.911009` where the pair form has `866.879220`; every
    certified bracket is valid, so their intersection is: `[866.911009, 866.980721]`,
    0.070 nats where the pair form alone had 0.10.  Sandwiches checked at 400 Gibbs
    states of the true ensemble and 2 000 exact samples of each floor: no violation.
    *Thirty residues at order 6* (the run finished after the first version of this
    item, 45 minutes on one core; row added above): `βΓ₆ = 54.8` does fit under the
    depths — the bound of item 54 is `4.6·10⁻⁴` nats and the Frank–Wolfe floor
    `866.921008` is within `8.4·10⁻⁴` of the penalty-free minorant `866.920168` after six
    steps — and the certified bracket is **0.0105 nats for `1.07·10⁹` states**, where
    order 5 had 0.070 by intersecting two forms; at most 0.0097 of it is P3's
    reduction of the evaluated terms.  *Not done:* exact window terms at twenty and
    thirty residues (each transfer-matrix pass adds thousands of tables in the
    present code — too slow for an optimiser); the split of part (18), item 59, on
    these models (leucine is apolar; valine gained nothing from it).

57. **What this part changes** [summary].  (i) The theory division's nested sampler
    works on real sandwiches as stated, and their stopping condition is met; its gain
    is `0.88/E_q ρ` at best with Hoeffding half-widths, `E_q ρ ≈ p^{m−k}`, and two small
    changes — one known mean, a variance-sensitive bound — are worth more than the
    nesting itself on these instances.  (ii) With sampling the order-5 ball certifies
    the serine helix within `5·10⁻⁴` nats at probability 0.95: the statement of part
    (16) with 25 times less width and 9 times fewer evaluations than order 6.
    (iii) Open problem D9(a), "optimal shares", which part (15) closed for mobile
    ensembles ("no allocation helps"), is **solved at the site level for frozen ones**:
    the valid site penalties are the core of a convex game, the best floor is a convex
    programme with a sort as oracle, the best ceiling an ordering — and the simplest
    model class of the certificate (one-body penalties) then matches or beats equal
    pair shares.  (iv) The first-order rule of Proposition 11.18f(c) needs a caveat for
    the floor: it is optimal for the lower end, and for the upper end only while each
    site's penalty stays below the cost of changing it.  (v) Not done: optimal shares
    at the pair level (the oracle is no longer a sort); the nested sampler with an
    optimally allocated outer sandwich; a referee.

### (18) The charged case: workstream P8's constants checked; what "limited by the band" was; the sampler inside the result [P, elementary, for items 59–60; M for the numbers; the constants are workstream P8's; added 2026-11-26]

*Scripts: `experiments/science/p8_verification/` (the checks of item 58);
`experiments/science/pi_inference/window_model_occ.py`, `occ_reduction_test.py`,
`nested_sampler_ext.py` (items 59–63).  Nothing in this part has been refereed.*

58. **What workstream P8 found, and what was checked before it was adopted**
    [K: `workstreams/P8_REPORT.md`, read in full; the checks are the coordinator's].
    Parts (15)–(16) left the charged sequences outside the certificate: workstream
    P3's constants gave `βΓ_m = 689, 145, 23.4` for Ace-Lys₁₂-NMe on the helix at
    orders 4, 5, 6.  P8 was asked whether the factor `e^{−r²/4B_aB_b}` was missing
    for far pairs.  It is not; the loss is elsewhere: P3's closed form takes the
    maximum over the rotamers of a term's *host* side chains ingredient by
    ingredient, and for a long charged side chain the merged maxima never occur
    together.  With the maximum taken **state-wise** — P3's own theorem, evaluated
    subset by subset ('Sb') — and a new statement, **Theorem AH**: expanding every
    term in an order of the sites that puts its own hosts last, a host outside `T` sits at
    the anchor in every evaluation ('SAb') — the constants become, in `k_BT`:

    | peptide | P3, orders 4, 5, 6 | 'Sb' | **'SAb'** |
    |---|---|---|---|
    | Lys₁₂ | 689, 145, 23.4 | 36.3, 2.54, 0.142 | **34.0, 2.40, 0.136** |
    | (LKSE)₃ | 1 874, 568, 147 | 312, 44.5, 5.00 | **296, 42.8, 4.87** |
    | Ser₁₂ | 5.44, 0.226, 0.0073 | 3.49, 0.139, 0.0042 | 3.47, 0.138, 0.0042 |
    | Leu₁₂ | 316, 45.1, 5.01 | 292, 41.4, 4.58 | 286, 40.8, 4.53 |

    (P8's table; the 'P3' and 'SAb' columns at orders 4 and 5 for Lys₁₂ re-read by my
    own summation.)  **Checked by the coordinator** (the note at the end of the
    report has the details): the proof of Theorem AH re-derived — sound, and its
    hypothesis can be weakened from "at most `m − 1` hosts" to "at most `m`", which
    is sharp; an exact test on a family of functions built to break it (no
    violation in `1.2·10⁶` checks, the inequality attained with ratio 1, three
    deliberately wrong versions all violated — while on Gaussian tables eleven wrong
    versions pass, a warning about that kind of test); the inequality the
    certificate needs, `|g − I_{m−1}g| ≤ Σ_{T⊆S(x)} ĉ_T`, at **every** state of Lys₄,
    Lys₅ and LKSE:5 with my own remainder code (no violation; the bound is at least
    12 times the remainder at every state and `10⁴`–`4·10⁵` times it in Boltzmann
    mean); the
    same at 4 250 uniformly random states of Lys₁₂ (no violation; at order 5 the
    true remainder never exceeds `8.3·10⁻⁴` kcal/mol, even with all twelve side
    chains off the anchor); P8's nine certified brackets for Lys₁₂ reproduced by
    another driver to every printed digit; P8's validation chain for Lys₄ re-run.
    **Not recomputed by anyone but P8: the constants themselves** — the checks are
    a review of the theorem, necessary conditions, and re-runs.  *What rests on
    what:* most of the gain is P3's theorem ('Sb'); Theorem AH takes another 4–7 % off
    the constants, which is 2–4 % of the bracket at order 5 and a factor two at order 4
    (3.25 against 1.56 nats), where the floor is in its exponential regime.

    With these constants and the pipeline of part (16) (exact window terms, band 7,
    order 5, ball 1 621 056) Lys₁₂ is certified within **0.598 / 0.220 / 0.192 nats**
    (site / banded pair / banded triple form), and P8 observed that 0.141 of the
    0.192 remain when all penalties are set to zero: "limited by the band, not by
    the constants any more".

59. **What the band's part was: the split of the pairs beyond the band**
    [P, elementary].  A pair table `P = J_ij + d_ij` with `|i − j| > w` cannot be kept
    by the transfer matrix and is replaced by one-site functions.  Workstream P3
    uses `b(x_j)` = column mean, `a^∓(x_i)` = row minimum / maximum of `P − b`.

    *Split around the anchor.*  Put `A(x_i) = P(x_i, x⁰_j)`,
    `B(x_j) = P(x⁰_i, x_j) − P(x⁰_i, x⁰_j)`, `D = P − A − B`.  Then `D` vanishes on the
    anchor row and the anchor column, and with `λ(x_i) = min_{x_j} D(x_i, x_j) ≤ 0 ≤
    μ(x_i) = max_{x_j} D(x_i, x_j)`:

    ```
    A(x_i) + B(x_j) + λ(x_i)   ≤   P(x_i, x_j)   ≤   A(x_i) + B(x_j) + μ(x_i),          λ(x⁰_i) = μ(x⁰_i) = 0.
    ```

    (Proof: `λ(x_i) ≤ D(x_i, x_j) ≤ μ(x_i)` by definition; `D(x⁰_i, ·) = 0`.)  The same
    with the roles of `i` and `j` exchanged.  **Both bounds are exact whenever the
    kept site is at its anchor**, whatever the other site does; by the first-order
    law of part (16) (Lemma A17.16) the pair then costs the bracket about
    `β E[(μ − λ)(x_i)] ≤ β·P(x_i ≠ x⁰_i)·max(μ − λ)` — proportional to how often the
    *kept* site leaves the anchor, so the kept site should be the rarer one.  P3's
    split is exact nowhere in general: at the anchor row its slack is the range over
    `x_j` of the column means of `D` — it charges the non-additive part of a far pair
    **even in the anchor state itself**, i.e. always.  For two side chains that each
    leave the anchor a few per cent of the time the two splits differ by that
    factor.  Any choice is valid (each replaces the pair by a pointwise minorant /
    majorant), so the choice may be guided by an uncertified sample: for each far
    pair I take, of the three candidates (around the anchor keeping `i`, keeping `j`,
    P3's), the one with the least sample mean of `max − min`.

60. **The terms of order ≥ 3 that do not fit a window** [P for validity; M].  The
    same idea: an anchored term `d_U` reduced to a sub-tuple `K ⊂ U` that fits a
    window, `min_{x_{U∖K}} d_U`, is non-zero only when all sites of `K` are off the
    anchor; rule "occ" keeps the maximal sub-tuple with the least sample mean of
    `max − min` (the rules of part (16) choose by sup-norm).  **It changes nothing
    measurable on these instances** — those terms cost `3·10⁻⁶` to `2.5·10⁻³` nats
    to first order — and is reported because it was tried, not because it helps.

61. **Numbers** [M; `occ_reduction_test.py`; every bracket certified, the sandwich
    checked at 960 Gibbs states of a second sample and 2 000 exact samples of the
    floor; for Lys₅ at every state, with the exact `ln Z` inside].  "Reductions" is
    the width of the same models with all penalties zero (not a sandwich: what the
    band costs by itself).  Widths in nats, banded triple form; constants 'SAb' for
    the lysine peptides and (LKSE)₃, workstream P3's closed form otherwise.

    | instance | order, band; far pairs | reductions: P3's split | reductions: split around the anchor | certified bracket: P3's split | **certified bracket: split around the anchor** |
    |---|---|---|---|---|---|
    | Lys₅ (115 248 states, enumerated; exact `ln Z = 251.348445`) | 4, band 2; 3 | 3.54 | 0.046 | 4.00 | **0.374** `[251.198528, 251.572785]` |
    | Lys₅ (enumerated) | 4, band 3; 1 | 0.950 | 0.019 | 1.15 | **0.164** `[251.279396, 251.442920]` |
    | **Lys₁₂** (`9.5·10¹⁰` states) | 5, band 7; 10 | 0.1414 | 0.0071 | 0.1916 | **0.0567** `[517.101364, 517.158058]` |
    | Lys₁₂ | 5, band 6; 15 | 0.3542 | 0.0211 | 0.4461 | **0.1115** `[517.073860, 517.185350]` |
    | (LKSE)₃ (`7.1·10¹⁰` states) | 5, band 7; 10 | 0.1721 | 0.0167 | 4.487 | **4.301** `[654.981476, 659.282763]` |
    | Ser₁₂ (`4.9·10⁹` states; mobile, `p ≈ 0.5`) | 5, band 7; 10 | 0.0160 | 0.0091 | 0.0942 | **0.0872** `[227.325848, 227.413092]` |
    | **Ser₂₀** (`8.2·10¹⁵` states; mobile; ball 3 963 696 evaluations, 78 minutes on one core) | 5, band 7; 78 | 0.0768 | 0.0431 | 0.2870 | **0.2534** `[347.033552, 347.286942]` |
    | Val₂₀ / PPII (`3.5·10⁹` states; apolar) | 4, band 8; 66 | `4.3·10⁻⁵` | `1.4·10⁻⁵` | 0.04994 | 0.04991 |

    Site and banded pair forms of Lys₁₂ at band 7: 0.598 → **0.459**, 0.220 →
    **0.085**.  In every row the far pairs chose the split around the anchor (none
    chose P3's), and rule "occ" alone (item 60) moved the bracket by less than
    0.7 %.  **Reading.**  The band's part of the lysine bracket was not the band:
    it was the way ten pairs of charged side chains more than seven residues apart
    were split — P3's split paid their non-additive part at every state, the split
    around the anchor pays it when the kept side chain moves (2–7 % of the time
    for nine of the twelve).  Where every side chain moves half of the time
    (serine) the gain is the factor 1.8 on a part that was small; where far pairs
    carry nothing (valine: apolar) there is nothing to gain.  *Serine at twenty
    residues* is new in this part (the run of part (16) at a length that cannot be
    enumerated by eight orders of magnitude): certified within 0.287 nats at order
    5, 0.253 with the split; the refined rule of part (16) had said 0.210 before the
    ball was paid for, and the difference is the reductions to the third decimal
    (`0.210 + 0.077 = 0.287`, `0.210 + 0.043 = 0.253`) — the bracket is the mean
    penalty plus the mean reduction, as Lemma A17.16 says.  **Lys₁₂ on the helix
    is now certified within 0.057 nats, deterministically, at order 5** — the same
    order of magnitude as the neutral helices of parts (10), (16) — and what is left
    is the constants again (0.050 of the 0.057; the far pairs 0.007).

62. **The nested sampler on Lys₁₂** [M; `nested_sampler_ext.py`; the theory division's
    Proposition 11.113a as run in part (17), with the outer sandwich of item 61
    and the envelope from P8's constants; prediction written into the research log
    before the run].  The inner sandwich pays only the envelope
    `Σ_{T⊆S(x)} ĉ_T`, whose bracket is `9·10⁻⁶` nats (predicted `2·10⁻⁵` from P8's
    first-order estimate), so nearly nothing is left for evaluations: of 400 000
    proposals **19** are accepted for evaluation (60 on the narrower outer
    sandwich).  With probability at least 0.95, given the sandwich:

    | outer sandwich | `D` | as stated (Hoeffding) | two-end (Hoeffding) | **two-end, empirical Bernstein** | new evaluations of `g` |
    |---|---|---|---|---|---|
    | P3's split | 0.1916 | `1.88·10⁻³` (predicted `2·10⁻³`) | `9.5·10⁻⁴` (predicted `1·10⁻³`) | `2.2·10⁻⁴`, `[517.128424, 517.128646]` (predicted `4·10⁻⁴`) | 19 |
    | split around the anchor | 0.0567 | `5.6·10⁻⁴` | `2.8·10⁻⁴` | **`3.3·10⁻⁵`, `[517.128526, 517.128559]`** | 60 |
    | **order 4** (ball 96 366), split around the anchor; `4·10⁶` proposals (*added after the first version of this item*) | 1.4125 | 0.032 | 0.028 | **`6.0·10⁻³`, `[517.125561, 517.131531]`** | 12 000 |

    The two runs agree (the second interval lies inside the first); P8's and my
    uncertified reweighting estimates, `517.1285 ± 0.0009` and `517.1284 ± 0.0010`,
    contain both.  **One order less** (third row, run after the first version of
    this item; prediction in the research log, cycle 58: bracket 1.4 nats, width
    0.007): from the order-4 ball — 96 366 evaluations, two minutes — the certified
    bracket is 1.41 nats, the envelope's own bracket 0.62 (predicted 0.3–0.5),
    `E_q ρ = 0.34` (predicted 0.15), and 12 000 evaluations give **0.006 nats**: the
    same `ln Z` to a hundredth of a nat from `1.1·10⁵` evaluations in all, fifteen
    times fewer than the order-5 ball, and its interval contains the two of order 5
    — two balls, two sets of constants, one answer.  The plain sampler with the same
    12 000 evaluations: 0.025 (empirical Bernstein), 0.063 (Hoeffding).  **The free energy of a charged dodecamer with `9.5·10¹⁰` states is
    known to `3·10⁻⁵` nats at probability 0.95** from the ball of order 5
    (1 621 056 evaluations, 24–31 minutes on one core by P8's measurement) plus 60
    evaluations; the width is the proposal term and falls as `1/√N_f` at a cost of
    seconds.  *Not predicted:* that so few evaluations would be used — my recorded
    figures for a plain sampler "with the same 1 200 evaluations" were therefore not
    tested.  *A practical finding:* workstream P3's band sampler recomputes the
    transfer-matrix messages at every call; the sampler of part (17) calls it once
    per batch, and for Lys₁₂ at band 7 the proposals would have taken about an hour
    (the first run was stopped after sixteen minutes); with the messages computed
    once (`nested_sampler_ext.py`; identical output on Lys₅) they take 14 seconds.

62a. **The neutral mobile helix at twenty residues, with the sampler** [M;
    `nested_sampler_p3table.py`; added after the first version of this part; the
    prediction is in the research log, cycle 56, written at 07:46 UTC before the
    ball of this instance existed].  Ace-Ser₂₀-NMe on the helix, `8.2·10¹⁵` states,
    order 5 (ball 3 963 696), outer sandwich of item 61 (`D = 0.2534`), workstream
    P3's constants from a table of all 15 504 subsets (24 minutes; the proposals
    have 296 795 distinct changed sets, which is why one closed-form sum per set —
    the route of part (17) for frozen ensembles — was stopped):

    | | predicted | measured |
    |---|---|---|
    | envelope bracket (nats) | 0.040 (the rule `2p^mΓ_m`) | 0.0401 |
    | `E_q ρ` | 0.19 (for the outer bracket 0.209 of the refined rule) | 0.157 (the outer bracket is 0.253) |
    | width as the theory division states the bound (Hoeffding) | about `6·10⁻³` | `6.08·10⁻³` |
    | width with one known mean and empirical Bernstein | about `1·10⁻³` | **`1.03·10⁻³`**, `[347.155238, 347.156272]` |

    with 1 200 evaluations (`E_q ρ = 0.157`; no evaluated energy outside either
    sandwich); the plain sampler with the same evaluations: `2.0·10⁻²` (Hoeffding),
    `5.1·10⁻³` (empirical Bernstein).  The uncertified reweighting estimate of the
    certificate run, `347.1553 ± 0.0010`, contains the interval.  **A neutral,
    mobile twenty-residue helix is known to `10⁻³` nats at probability 0.95, and
    the three numbers that describe the run were written down before its ball was
    computed** — the first-order law of part (16) and the sampler's arithmetic of
    part (17) are predictive at a size eight orders of magnitude beyond enumeration.

63. **The patterned sequence** [M].  For (LKSE)₃ P8's constants leave `βΓ₅ = 42.8`
    and a certified bracket of **4.49 nats** (triple form, band 7) — the floor
    delocalises (nine side chains off the anchor in its samples, three in the
    ensemble), and no deterministic combination at an affordable order brings it
    below one nat.  The sampler does not need the deterministic bracket to be
    small, only the proposals to be cheap:

    | run | outer `D` | envelope bracket (estimated from the proposals) | `E_q ρ` | proposals; evaluations | two-end, empirical Bernstein, probability 0.95 | plain sampler, same evaluations (empirical Bernstein) |
    |---|---|---|---|---|---|---|
    | P3's split | 4.487 | 1.23 | 0.058 | 400 000; 1 200 | **0.169**, `[655.522897, 655.691668]` | 1.18 |
    | split around the anchor | 4.301 | 1.23 | 0.062 | 4 000 000; 12 000 | **0.041**, `[655.592089, 655.632643]` | 0.182 |

    *The first run against its prediction:* I had guessed an envelope bracket of
    0.1 nats and a width of 0.03–0.04; the envelope bracket is 1.23 nats — the
    envelope, the smallest valid penalty, delocalises too — and the width 0.17.
    The second run was predicted at 0.05 nats before it started and gave 0.041; its
    interval lies inside the first.  With the same 12 000 evaluations the plain
    sampler has 0.18 (empirical Bernstein) and 1.0 (Hoeffding).  P8's uncertified
    reweighting estimate of this `ln Z`, `655.79 ± 0.09`, lies above both intervals,
    1.9 of its standard errors above their point estimates: reweighting 2 000
    samples of a delocalised floor has a heavier tail than its standard error says.  **A sequence of mixed
    charge with `7·10¹⁰` states, 4.5 nats wide deterministically, is within
    0.041 nats at probability 0.95.**

64. **What this part changes** [summary].  (i) The charged case is inside the
    certificate: with workstream P8's constants and the split of item 59, Lys₁₂ on
    the helix is certified within 0.057 nats and sampled within `3·10⁻⁵`; the
    constants' validity rests on P3's theorem, on P8's Theorem AH (re-derived and
    tested here, not refereed), and on code nobody has re-implemented.  (ii) Every
    certificate of parts (10)–(17) whose band is shorter than the chain used P3's
    split of the far pairs; for apolar and mobile side chains that cost little
    (valine: nothing; serine: 7 % of the bracket), for charged, mostly frozen ones
    it was three quarters of the bracket.  (iii) The mixed-charge sequence is
    reachable by sampling and not deterministically: its constants (`βΓ₅ = 43`,
    still 119 times the exact four-body terms by P8's measurement) are the open
    problem; what is left of them sits on neutral pairs, where workstream P5's
    sign-reversal theorem says a sign-blind bound cannot be sharp.
    (iv) *Not done:* penalties resolved by rotamer state (P8's request P8-E4: the
    proof of Theorem AH gives them); the state-wise constants beyond twelve
    residues (no closed form over the subsets; P8's hybrid, request P8-E2); the
    first-order-optimal split of a far pair, which is a transport problem (the best
    additive minorant of `P` against given site marginals is a Kantorovich dual) —
    the split around the anchor is one feasible point of it; optimal site shares
    (part (17)) on top of these models; twenty residues with a charged sequence; a
    referee.

### (19) Penalties resolved by rotamer state (workstream P9, checked) — and the band's own slack taken back out of the bracket [P for validity: workstream P9's Theorem R and Proposition P, re-derived by the coordinator, and Proposition A17.19 below (elementary); X on Lys₅ and LKSE:5; M for the numbers; added 2026-11-26; not refereed]

*What is whose.*  Items 65–68: workstream P9 (`workstreams/P9_REPORT.md`, with the
coordinator's note at its end); the checks named there as mine are mine.  Items 69–75:
the coordinator (`pi_inference/slack_recovery.py`, `first_order_recovery.py`).  Nothing in
this part has been read by a referee; the part continues (18), whose items are numbered
58–64.

65. **Workstream P9: the penalty of a subset as a function of the rotamers of its
    sites** [P9; P].  Workstream P8's constants `ĉ_T` are maxima over the rotamers of
    the sites of `T` — of the hosts, which P8's code had in hand, and of the non-host
    sites, whose increments `δ̄ = max_y |C(y) − C(x⁰)|` P3's computable forms take as
    maxima.  P3's theorem is *stated* with the increments that occur; P9 evaluated it so.
    **Theorem R**: `|g − I_{m−1}g|(x) ≤ Σ_{T⊆S(x), |T|=m} Θ_T(x_T)`, block by block, with the
    hosts in `T` *and* the non-host sites of `T` at their actual states, hosts outside
    `T` at the anchor (P8's Theorem AH before its maximum).  **Proposition P**: for any
    weights `w_{T,U}` on the sub-tuples of `T`, the tables
    `γ_U(b_U) = Σ_{T⊇U} w_{T,U} max{Θ_T(y_T) : y_U = b_U}` (zero when a site of `U` is at
    the anchor) are a valid penalty — the actual `x_T` is among the points of the
    maximum; and a table that does not fit the band may be reduced by maxima over the
    sites given up.  With `Θ_T` constant these are P3's site form, P6's Lemmas A, A′ and
    the theory division's allocations (Proposition 11.18f).  *What the resolution is
    worth* (P9's numbers): the dependence on the *host's* rotamer alone is weak (site
    penalty 0.72–1.00 of the constant one at the visited rotamers); with the non-host
    sites resolved the typical subset bound is 42–590 times below P8's constant, and
    even its maximum over the states is 41–61 % of it — new state-independent constants
    `βΓ_m = 18.2, 0.99` (Lys₁₂, orders 4, 5) and `26.1` ((LKSE)₃, order 5) where P8 has
    `34.0, 2.40, 42.8`.  The bound is still far from the truth: at its tightest state
    8–15 times the exact term, in Boltzmann mean 255–880 times the remainder on the
    enumerated instances (P8's constants: `9·10³`–`4·10⁵`).

66. **Checked by the coordinator before publication** [M; `experiments/science/p9_verification/`].
    §1 of the report re-derived, no gap found.  The raw tables against exact
    remainders with my code: at every state of Lys₄, Lys₅, LKSE:5 and every order
    (`R ≤ B₂ ≤ B₁ ≤ B_SAb`, no violation); at twelve residues **every** state with exactly
    `m` side chains off the anchor against the exact anchored term — 92 525 and 1 524 690
    states of Lys₁₂ (orders 3, 4), 175 185 and 3 290 515 of (LKSE)₃ — no violation,
    smallest ratio 8.25–15.05, and two deliberately wrong tables fail (minimum in place
    of the value: 14 334 – 1 853 296 violations; table reversed: 438 – 170 176); at order
    5, where no ball of radius 5 exists, 2 000 random states per peptide (a necessary
    condition only).  From the raw tables to the brackets with a driver of mine
    (`resolved_brackets.py`): the tables re-built equal P9's stored ones exactly;
    "envelope ≤ tables" at 32 000 – 40 000 random states per case, with equality where
    the envelope is one entry, and failing for two wrong allocations; **all twelve
    brackets of the next item reproduced digit for digit**; the sandwich at 6 980 states
    of mine per case and form, no violation.  *How much the last check can see:* with
    the tables left out it fails at 829–929 states (Lys₁₂, order 3), 18 (order 4), 92
    ((LKSE)₃, order 4) and at **none** at order 5 or for serine; with tables ten times
    smaller it never fails.  The checks with teeth are the per-entry ones.  *Not
    checked by me:* the stage-1 tables, the forms S and B, the rows with constants,
    P3's enclosures.

67. **The brackets** [M; validity P; band 7, helix; the models of part (18): exact
    window terms, occupancy-aware reductions, far pairs split around the anchor].
    "T": equal shares on triples (the form of part (18)); "W": every subset charged in
    full to one sub-tuple of its sites that fits a window.

    | peptide | order (ball) | P8's constants, T (part (18)) | resolved, T | **resolved, W** | reductions alone |
    |---|---|---|---|---|---|
    | Lys₁₂ | 3 (3 841) | none | 0.832 | **0.0769** `[517.108870, 517.185731]` | 0.00710 |
    | Lys₁₂ | 4 (96 366) | 1.41 | 0.1115 | **0.00735** `[517.125649, 517.132996]` | 0.00713 |
    | Lys₁₂ | 5 (1 621 056) | 0.0567 | 0.0160 | **0.00723** `[517.125705, 517.132938]` | 0.00713 |
    | (LKSE)₃ | 4 (181 268) | none | 1.147 | **0.0191** `[655.603013, 655.622116]` | 0.0167 |
    | (LKSE)₃ | 5 (3 471 783) | 4.30 | 0.1946 | **0.0170** `[655.604050, 655.621038]` | 0.0167 |
    | Ser₁₂ | 5 (481 506) | 0.0547 (P3's closed form: 0.0872) | 0.0226 | **0.0117** `[227.363089, 227.374782]` | 0.0091 |

    (LKSE)₃ at order 3 is not certified (659 nats: the floor delocalises completely,
    although the first-order number on a sample of the true ensemble is 0.4; P9 could
    not predict on which side of that threshold a set of tables lies, and was wrong
    about it five times of nine — its request P9-T2).  **The sequence that part (18)
    called "reachable by sampling and not deterministically" is certified
    deterministically within 0.017 nats, and from its order-4 ball within 0.019;
    Lys₁₂ is certified from 96 366 evaluations more tightly than it was from
    1 621 056.**  In the window form the bracket is the width of the models *without any
    penalty* plus one to three per cent (14 % for (LKSE)₃ at order 4): what the band
    gives up — ten pairs of side chains more than seven residues apart, and the
    evaluated terms that fit no window.  P9 did not touch that; items 69–74 do.

68. **The sampler with the resolved envelope** [M; the algorithm is the theory
    division's Proposition 11.113a; probability 0.95, given the sandwiches].  P9 ran
    the coordinator's `nested_sampler.main()` with the window-form sandwich outside and
    the fully resolved `Σ_{T⊆S(x)} Θ_T(x_T)` as envelope.  (LKSE)₃ from the order-5 ball:
    the envelope's own bracket falls from 1.23 nats (P8's constants) to `3.5·10⁻⁶`;
    as the theory division states the bound `[655.612610, 655.612778]` (`1.7·10⁻⁴`),
    two-end form with empirical Bernstein `[655.612673, 655.612715]` (`4.3·10⁻⁵`), from
    400 000 proposals and **90** new evaluations (part (18): 0.188 and 0.041 from
    4 000 000 proposals and 12 000 evaluations).  From the order-4 ball:
    `[655.612562, 655.612814]` and `[655.612657, 655.612719]` with 1 200 evaluations —
    **repeated by the coordinator with another driver and another seed**
    (`p9_verification/nested_resolved.py`): `[655.612563, 655.612815]` and
    `[655.612658, 655.612720]`.  *A run P9 could not make (memory), made by the
    coordinator:* Lys₁₂ from the **order-3** ball — 3 841 evaluations — with 12 000 more:
    as stated `[517.127247, 517.129738]` (0.0025), two-end with empirical Bernstein
    `[517.128107, 517.128879]` (`7.7·10⁻⁴`; predicted `5·10⁻⁴`, range `3·10⁻⁴`–`10⁻³`); it
    contains the interval of part (18).  There the envelope no longer helps: 78 % of the
    proposals are accepted for evaluation and the plain sampler with the same 12 000
    evaluations is as narrow (`7.8·10⁻⁴`) — at order 3 the resolved bound is the size of
    the outer sandwich itself.

69. **The slack of the band is a table, and a table can be averaged** [P, elementary:
    Proposition A17.19].  For a pair beyond the band the ceiling model holds
    `A(x_i) + B(x_j) + max_{x_i} D(x_i, x_j)` where the energy has `P(x_i, x_j)`; the
    difference `s⁺_{ij}(x_i, x_j) ≥ 0` is a function of two sites that no band model can
    hold but that is known exactly.  The same for an evaluated term replaced by its
    maximum over the sites given up, and for a subset `T` charged to a sub-tuple `K`
    (`[max over the given-up sites of Θ_T](x_K) − Θ_T(x_T)[T ⊆ S(x)] ≥ 0`, because the
    remainder is bounded by the envelope, not only by the allocated tables).
    *Let `m₋ ≤ E ≤ m₊`, and let `s₊ = Σ_g S⁺_g`, `s₋ = Σ_g S⁻_g` be sums of non-negative
    functions with `m₊ − E ≥ s₊` and `E − m₋ ≥ s₋` pointwise; `⟨·⟩` is the mean under the
    ceiling model `e^{−βm₊}/Z(m₊)`.  Then*

        (LJ)  ln Z(E) ≥ ln Z(m₊) + β Σ_g ⟨S⁺_g⟩,
        (LP)  ln Z(E) ≥ ln Z(m₊) + ln( 1 + Σ_g ⟨e^{βS⁺_g} − 1⟩ ),
        (UE)  ln Z(E) ≤ u*,  u_{t+1} = ln Z(m₋) − β C e^{ln Z(m₊) − u_t},      C  = Σ_g ⟨S⁻_g e^{βS⁺_g}⟩,
        (UP)  ln Z(E) ≤ v*,  v_{t+1} = ln Z(m₋) − ln(1 + C′ e^{ln Z(m₊) − v_t}),  C′ = Σ_g ⟨(e^{βS⁻_g} − 1) e^{βS⁺_g}⟩,

    *with `u_0 = v_0 = ln Z(m₋)`; every iterate is an upper bound.*
    *Proof.*  `Z(E)/Z(m₊) = ⟨e^{β(m₊−E)}⟩ ≥ ⟨e^{βs₊}⟩`; Jensen gives (LJ);
    `∏_g(1 + y_g) ≥ 1 + Σ_g y_g` for `y_g = e^{βS⁺_g} − 1 ≥ 0` gives (LP).  Above:
    `Z(m₋)/Z(E) = ⟨e^{β(E−m₋)}⟩_E ≥ ⟨e^{βs₋}⟩_E`, a mean under the **true** ensemble; by
    Jensen it is at least `e^{β Σ_g⟨S⁻_g⟩_E}`, by the product inequality at least
    `1 + Σ_g ⟨e^{βS⁻_g} − 1⟩_E`.  For any `X ≥ 0`, since `e^{−βE} ≥ e^{−βm₊} e^{βs₊} ≥ e^{−βm₊} e^{βS⁺_g}`,

        ⟨X⟩_E = Σ_x X e^{−βE} / Z(E)  ≥  Z(m₊) ⟨X e^{βS⁺_g}⟩ / Z(E)  ≥  ⟨X e^{βS⁺_g}⟩ e^{ln Z(m₊) − u}

    for every upper bound `u` of `ln Z(E)`; with `X = S⁻_g` this is (UE), with
    `X = e^{βS⁻_g} − 1` it is (UP).  ∎
    (LJ) and the Jensen step of (UE) are the Gibbs–Bogoliubov inequality in its two
    directions.  The two-sided form is in print with a mean under each ensemble
    (Reible, Hartmann and Delle Site, Lett. Math. Phys. 112, 97 (2022),
    arXiv:2111.10282 — seen in search summaries only, not read); what makes it
    computable here is the change of measure in the last display, which trades the
    mean under the true ensemble for a mean under the ceiling model at the price of
    the factor `e^{ln Z(m₊) − u} ≥ e^{−D}`.  *Searched:* our own addenda (the two-sided
    bracket is used in part (7) as a datum; far pairs appear in (18) only as a choice of
    split), and three web queries (two-sided Bogoliubov bounds; one-ensemble variants;
    mini-bucket bounds with corrections for dropped terms): nothing of this form was
    found.  A reduction by minimum or maximum is the sum-max limit of a mini-bucket
    relaxation, and that literature tightens such bounds by Hölder weights and by
    shifting cost between the parts (Liu and Ihler, ICML 2011, and the anytime search
    bounds of Lou, Dechter and Ihler — both in workstream L2's prior-art report,
    `docs/prior_art/L2_relaxations_partition.md`, C8(a), verified there), not, as far as
    that report and the summaries show, by a perturbative correction with exact
    marginals of the relaxed model.  **"Not found in our reports and in three queries"
    is all that is claimed.**

70. **Computing the means exactly** [P, elementary; mine].  What is needed is the law
    of a table on sites that do not fit a window, under a band model.  If all sites of
    an item but one lie in the last `w` sites of the chain, run the transfer matrix
    with that one site **held** at each of its states in turn and read the joint law of
    the last `w` sites from the final array ("fwd"); the mirrored chain serves the
    items whose sites but the last lie in the first `w` ("rev").  All items that share
    the held site form a group `g`; `S_g` is a function of the held site and of one
    window, so every `⟨φ(S_g)⟩` is exact.  For a chain of at most `2w` sites every far
    pair and every triple has a route; an item without one is left out, which keeps
    the bound valid.  Cost for Lys₁₂ at band 7: 47 + 28 held-site passes of about half
    a transfer-matrix run each (three minutes once the arrays of the terms are
    cached).  *Which site to hold matters for tightness:* the slack of a far pair occurs
    when the site its reduction **keeps** is off the anchor, so all pairs that keep the
    same site have their slack at the same states; held at that site they are one
    group and are treated exactly together, held at the other end they fall into
    different groups and the product inequality loses their cross terms (on Lys₅ at
    band 2: 0.0083 against 0.0029 nats).

71. **Every state of Lys₅ and LKSE:5** [X; `first_order_recovery_*_enum.log`].  The
    hypotheses `m₊ − E ≥ s₊` and `E − m₋ ≥ s₋` hold at every state, with a smallest margin
    of exactly the constant allowance `10⁻⁷` kcal/mol (inside the ball the accounting is
    an identity); every item doubled violates them at 22 687 – 229 329 states, and the
    far items of floor and ceiling exchanged at 12 011 – 112 163; the group means from
    the held-site passes agree with enumeration to `10⁻¹²`; the exact `ln Z` is inside
    every corrected bracket.

    | instance, order, band | sandwich `D` | corrected bracket | width | `D` / width | the same items put back exactly (enumeration) |
    |---|---|---|---|---|---|
    | Lys₅, 4, band 2 | 0.0477 | `[251.3475751, 251.3504878]` | 0.00291 | 16 | 0.00167 |
    | Lys₅, 4, band 3 | 0.0189 | `[251.3484184, 251.3484828]` | `6.4·10⁻⁵` | 294 | `5.0·10⁻⁵` |
    | Lys₅, 5, band 3 | 0.0187 | `[251.3484424, 251.3484495]` | `7.1·10⁻⁶` | 2 633 | `1.6·10⁻⁶` |
    | LKSE:5, 4, band 2 | 0.205 | `[276.4668782, 276.4684894]` | 0.0016 | 128 | `8.8·10⁻⁴` |

    (exact `ln Z`: 251.3484449 and 276.4672934.)  At band 2 the "far" pairs are helix
    neighbours and their slack is of order `kT`; the inequalities then lose a factor
    two against an exact treatment of the same items.

72. **What was left after the recovery: a rounding allowance — and where to put it**
    [M; P for validity, elementary].  With the grouping of item 70 the corrected bracket
    of (LKSE)₃ at order 5 was still `3.9·10⁻⁴` nats, and neither its envelope
    (`3·10⁻⁶`) nor its allocation slack (`10⁻⁵`) accounts for that.  It is workstream
    P6's allocation of the **floating-point allowance** of the evaluated terms.  Every
    `d_U` is an alternating sum of `2^{|U|}` values of `g`, each allowed an error
    `ε_g = 10⁻⁷` kcal/mol (workstream P3: an a-priori worst case of `3·10⁻⁸` for the
    evaluator's sums, "not proved for the summation order of the evaluator used";
    measured errors `2·10⁻¹²`), and P6 charges the allowance of every term through a pair
    to that pair — `1.5·10⁻⁵` kcal/mol per in-band pair at order 5 — whenever the pair is
    off the anchor, although nearly all of those terms are not.  First-order cost
    `2β⟨allowance⟩` on the Gibbs samples:

    | | order 3 | order 4 | order 5 |
    |---|---|---|---|
    | Lys₁₂ (1.2 side chains off the anchor on average) | `3.9·10⁻⁶` | `2.2·10⁻⁵` | `1.06·10⁻⁴` |
    | (LKSE)₃ (2.8) | `9.4·10⁻⁶` | `5.8·10⁻⁵` | `2.7·10⁻⁴` |
    | Ser₁₂ (6.3) | `3.2·10⁻⁵` | `2.2·10⁻⁴` | `1.04·10⁻³` |

    It grows five- to sevenfold per order while the truncation error falls: once the band's slack
    is recovered, a higher order is no longer free.  The allowance is not slack — the
    rounding error is unknown — but **its allocation is a choice**: attached to each
    term's own table, `d_U ∓ 2^{|U|}ε_g` where all sites of `U` are off the anchor (elsewhere
    `d_U` vanishes exactly), it is charged only when the term is.  The lowered table is a
    minorant of the true term and the raised one a majorant, and so is every minimum or
    maximum of them over sites given up.  The sandwiches of items 73–74 are built so
    (`first_order_recovery.py`; each log prints P9's bracket, with P6's allocation, beside
    it).  Effect on the sandwich: Lys₁₂ 0.007347 → 0.007329 (order 4) and 0.007233 →
    0.007138 (order 5); (LKSE)₃ 0.016987 → 0.016757; Ser₁₂ 0.011693 → 0.011076.  Effect
    on the corrected bracket (the code version before this change — its logs are not
    kept — against the final one): Lys₁₂ order 4 `1.02·10⁻⁴` → `8.3·10⁻⁵`; (LKSE)₃ order 5
    `3.9·10⁻⁴` → `1.43·10⁻⁴`.
    What `ε_g` itself should be is a question for whoever evaluates `g` (request A19-E2).

73. **Twelve residues** [M; validity P; `first_order_recovery_*.log`; band 7; predictions
    in the research log, cycle 59].  "Sandwich": P9's window form with the allowance
    attached term by term.  The three columns add the far pairs, then the evaluated
    terms that fit no window, then the allocation slack of the penalty.

    | peptide, order (ball) | sandwich `D` | far pairs | + terms | **+ allocation: corrected bracket** | `D` / width | items: with a route / all |
    |---|---|---|---|---|---|---|
    | Lys₁₂, 3 (3 841) | 0.07686 | 0.0703 | 0.0703 | **0.0611** `[517.1160739, 517.1771913]` | 1.3 | 100 / 100 |
    | Lys₁₂, 4 (96 366) | 0.007329 | `2.5·10⁻⁴` | `2.2·10⁻⁴` | **`8.3·10⁻⁵`** `[517.1285101, 517.1285931]` | 88 | 380 / 465 |
    | Lys₁₂, 5 (1 621 056) | 0.007138 | `5.2·10⁻⁵` | `2.2·10⁻⁵` | **`2.2·10⁻⁵`** `[517.1285395, 517.1285614]` | 327 | 818 / 1 346 |
    | (LKSE)₃, 4 (181 268) | 0.019067 | 0.00296 | 0.00250 | **0.00154** `[655.6119691, 655.6135057]` | 12 | 380 / 465 |
    | (LKSE)₃, 5 (3 471 783) | 0.016757 | `6.2·10⁻⁴` | `1.5·10⁻⁴` | **`1.43·10⁻⁴`** `[655.6126377, 655.6127810]` | 117 | 818 / 1 346 |
    | Ser₁₂, 5 (481 506) | 0.011076 | 0.00437 | 0.00198 | **0.00179** `[227.3678308, 227.3696220]` | 6.2 | 818 / 1 346 |

    *Checks, every row:* the two hypotheses at 5 380 states of mine with new evaluations
    of the energy (Gibbs states, exact samples of floor and ceiling, random states,
    states with `m` and `m + 1` side chains off, states inside the ball) — no violation,
    and at the Gibbs states and the samples the margin is exactly the constant allowance
    `10⁻⁷` (inside the ball the accounting is an identity); every item doubled violates
    them at 4 341 – 10 011 of those states, the far items of floor and ceiling exchanged
    at 1 316 – 4 138; the exact means against 20 000 exact samples of the ceiling: within
    1.6 standard errors in all twelve comparisons (the six for Lys₁₂ share a seed and
    nearly the same ceiling and all lie 0.8–1.6 standard errors low; those for (LKSE)₃
    and Ser₁₂ are within 0.3 — the test of the means is item 71, not this).  *Against the sampler:* every
    corrected bracket contains the sampled interval of the same `ln Z` — Lys₁₂:
    `[517.128526, 517.128559]` of part (18), except that at order 5 the deterministic
    bracket is now the narrower of the two and the intervals overlap
    (`[517.1285395, 517.1285614]` against `[517.128526, 517.128559]`); (LKSE)₃:
    `[655.612658, 655.612720]` (item 68); Ser₁₂: `[227.368425, 227.368972]` of part (17).
    *Against the predictions:* Lys₁₂ order 4 `8·10⁻⁵` predicted; (LKSE)₃ order 5
    `1.2·10⁻⁴`; order 4 `10⁻³` (range `5·10⁻⁴`–`2·10⁻³`); Ser₁₂ `1.5·10⁻³`; Lys₁₂ order 5
    `3·10⁻⁵`–`6·10⁻⁵` (found below the range); Lys₁₂ order 3 0.035, range 0.015–0.06 (found
    just above it).  **Lys₁₂ — `9.5·10¹⁰` states — is certified within `8.3·10⁻⁵` nats
    from 96 366 evaluations and within `2.2·10⁻⁵` from the order-5 ball; (LKSE)₃ within
    `1.4·10⁻⁴`.**  *What is left in each row:* the envelope where it is not small —
    `2β⟨Σ_{T⊆S(x)} Θ_T⟩` on the two Gibbs samples is 0.053–0.064 for Lys₁₂ at order 3,
    `8·10⁻⁴` for (LKSE)₃ at order 4, `1.3·10⁻³` for Ser₁₂ (and `10⁻⁵`–`10⁻⁴`, `10⁻⁹`,
    `10⁻⁶` for the three other rows) — and otherwise what the inequalities lose between
    groups (the factor `e^{ln Z(m₊) − u}` of (UE), (UP) costs about `D/2` times the amount
    recovered above: `1.3·10⁻⁵` for Lys₁₂, `7·10⁻⁵` for (LKSE)₃) and the items without
    a route.  **[Corrected in part (21), item 83 (a): the two numbers are `D²/4` evaluated,
    not measurements; the loss between groups, measured, is 0.06 to 2.2 times `D²/4`.]**

74. **A narrower band** [M; Lys₁₂, order 4; `first_order_recovery_K12_m4_w{4,5,6}.log`;
    sub-tuples chosen by the rule of item 67 with my own code, since P9 stored choices
    for band 7 only].  If the band's slack can be taken back, the band need not be as
    wide as memory allows.

    | band | pairs beyond it | sandwich `D` | **corrected** | items with a route / all | run time, peak memory |
    |---|---|---|---|---|---|
    | 7 | 10 | 0.00733 | **`8.3·10⁻⁵`** | 380 / 465 | 515 s, 2.7 GB |
    | 6 | 15 | 0.0214 | **`2.8·10⁻⁴`** `[517.1284536, 517.1287322]` | 420 / 610 | 214 s, 1.4 GB |
    | 5 | 21 | 0.0253 | **`4.2·10⁻⁴`** `[517.1284057, 517.1288274]` | 352 / 742 | 199 s, 1.1 GB |
    | 4 | 28 | 0.0288 | **`6.9·10⁻⁴`** `[517.1283040, 517.1289915]` | 262 / 854 | 192 s, 1.1 GB |

    (The times of the narrow bands are the Gibbs samples and the checks; the transfer
    matrices take seconds.)  **Band 4 with the recovery is ten times tighter than band 7
    without it**, with arrays 343 to 2 352 times smaller; every bracket contains the sampled
    interval.  Predicted before the runs: sandwich 0.05, 0.04, 0.1 (found 0.021, 0.025,
    0.029 — the last below my range); corrected `10⁻³`, `7·10⁻⁴`, `3·10⁻³` (found
    `2.8·10⁻⁴`, `4.2·10⁻⁴`, `6.9·10⁻⁴` — the first and the last below my ranges).  At bands
    5 and 4 the chain is longer than `2w` and half to two thirds of the items have no
    route; a held-site pass with a backward message would serve them (not built).

75. **What this part changes** [summary].  (i) The slack of the charged case was, twice,
    a maximum taken too early: over the hosts' rotamers (P8), then over the rotamers
    of the other sites of a subset (P9) — the theorem never asked for either.  (ii) With
    the resolved tables in the window form the certificate holds one order earlier
    (Lys₁₂ from 3 841 or 96 366 evaluations, (LKSE)₃ from 181 268) and what it then
    measures is the band.  (iii) The band's slack is known and comes back out by a
    classical inequality with exact marginals: **deterministic brackets of `10⁻⁴`–`10⁻⁵`
    nats for the charged twelve-residue peptides**, narrower than the sampled interval
    of part (18) in one case, and a band of 4 or 5 does where 7 was needed.  (iv) What
    is left is, in this order: the envelope — the resolved bound itself, still 255–880
    times the remainder in Boltzmann mean, which only sampling (item 68: 90
    evaluations) or a tighter theorem removes; the losses between groups; the items
    without a route; and the evaluation tolerance `ε_g`, now a line of its own.
    (v) *Not done:* held-site passes for chains longer than `2w` (a backward message);
    two held sites for the items with two sites at each end; the recovery on the older
    certificates of parts (10)–(17) (serine at twenty, leucine at thirty residues: their
    reductions are 17 % and more of the bracket); a criterion for when a floor
    delocalises (P9's request P9-T2; (LKSE)₃ at order 3 has none); resolved tables beyond
    twelve residues (no closed form over the subsets); an independent implementation
    of the stage-2 tables; **a referee** — parts (13)–(19) have had none except for Lemma
    A17.16, the greedy lemma and one section of SCI-RES-0017.

### (20) After part (19): why the sign-blind bound is slack on lysine (the theory division's question, measured); held-site passes for a window anywhere on the chain; all thirteen recovery runs repeated; a charged chain of twenty residues [M for item 76; P, elementary, for item 77; X on four enumerated instances; M for the rest; added 2026-11-26; not refereed]

76. **Between two ammonium groups the mixed-difference kernel is not nearly constant**
    [M; `experiments/science/p8_verification/kernel_spread.py`, `kernel_spread_K5.log`;
    the kernel is workstream P5's, the stored `g` workstream P8's; SCI-RES-0021 §1].
    *The question.*  Workstream P8's sign-blind class bounds a mixed difference
    `Δ_T g = ½·pre·qᵀ(Δ_T M)q` by the same form with the charges replaced by their
    absolute values and the worst signs, and on lysine that loses a factor 3–7 (part
    (18)).  We had asked the theory division (P8-T2) whether a statement
    `SB ≤ C·R²·Φ(g)` holds for charges dominated by one sign.  Its answer (THY-RES-0015
    §4) is a lemma: for a bilinear form `t = q_aᵀMq_b` between two groups, a reference
    value `m̄ ≠ 0`, `ρ = max|M_pq − m̄|/|m̄|` and `R = Σ|q|/|Σq|`,

        SB  ≤  (1 + ρ)/(1 − ρR_aR_b) · R_aR_b · |t|        whenever  ρR_aR_b < 1,

    with equality `SB = R_aR_b|t|` for a constant kernel — and the question back whether
    lysine head-to-head pairs are in that regime.
    *The measurement.*  Ace-Lys₅-NMe on the helix, order 4, each of the five 4-subsets
    at the context and states where `|Δ_T g|` is largest; `Δ_T M` from sixteen kernel
    evaluations (`Δ_T g` recomputed from it agrees with the mixed difference of the
    stored `g` to `10⁻⁸` kcal/mol in all five); for every pair of lysines the block
    between their ammonium groups (NZ, HZ1–3) and between the groups extended by CE,
    HE2, HE3; `ρ` for the best constant reference (the midrange); the block's exact
    sign-blind value by enumeration of all sign patterns.

    | | ammonium (4 atoms) | with CE, HE2, HE3 (7 atoms) |
    |---|---|---|
    | charges | NZ `−0.3854`, HZ `+0.34` each; net `+0.6346` | CE `−0.0143`, HE `+0.1135` each; net `+0.8473` |
    | `R`; `R²`; the regime needs `ρ` below | 2.2146; 4.905; 0.204 | 1.9435; 3.777; 0.265 |
    | `ρ` in the fifty blocks: smallest, median, largest | 0.953, 1.00, 2.11 | 0.999, 1.01, 4.23 |
    | blocks with `ρR_aR_b < 1` | **0 of 50** | **0 of 50** |
    | exact sign-blind value over the absolute value of the block's `t`: median; in the four blocks that carry the mixed difference | 3.88; 2.62–4.28 | 2.82; 2.18–3.71 |

    In the four blocks whose `t` is at least a tenth of the largest, the sixteen
    entries are **of one sign and span a factor of forty to a factor of `10⁵`** (for the
    largest: mean `−4.4·10⁻⁴`, from `−2.0·10⁻³` to `−1.7·10⁻⁶` per nm): the fourth mixed
    difference of the kernel is carried by the nearest atom pairs of the two groups,
    and `ρ ≈ 1` says "from nearly zero to the maximum".  **The lemma's regime is not
    where this instance is.**  The loss in those blocks is nevertheless below `R²`
    (2.6–4.3 against 4.9): a one-signed block concentrated on few atom pairs has
    `SB = w_aᵀ|M|w_b` and a `t` in which the charges of the dominant atoms hardly cancel.
    That is a property of these blocks, not a bound: for a one-signed block with weight
    on one N–H pair and one H–H pair in the ratio of the charges `t` vanishes and the
    ratio is unbounded.
    *What it means.*  The slack of the sign-blind class on lysine is not explained by a
    group acting as a point charge with internal cancellation; a statement that covers
    it has to see which atom pairs carry the mixed difference.  We have none.  (Since
    part (19) the question matters less for the certificate — the resolved penalties
    and the recovery do not go through the sign-blind class beyond the stage-2 tables —
    but the stage-2 tables are sign-blind bounds, and the envelope they give is still
    255–880 times the remainder in Boltzmann mean: item 75 (iv).)
    *A hint that was wrong.*  SCI-RES-0020 §4, sent forty minutes before this
    computation, said that P8's measured loss `0.127/0.0250 = 5.1` against `R² ≈ 4.9` was
    "consistent with a small `ρ` for the pairs that carry the remainder".  It is a
    coincidence of two numbers.  Withdrawn by a linked correction in SCI-RES-0021 §1;
    `DEAD_ENDS.md` SD65.
    *Limits.*  One peptide, one order, five points (the maxima), two definitions of the
    head group; the sign-blind values are exact for the blocks, not for the whole
    remainder.

77. **Held-site passes for a window anywhere on the chain** [P, elementary; X;
    `experiments/science/pi_inference/held_site_laws.py`].  Item 70 computes, under a band
    model, the exact joint law of one held site and the *last* `w` sites (or, on the
    mirrored chain, the first `w`), which serves every item of a chain of at most `2w`
    sites and leaves the others without a route.  For a window `s … s+w−1` anywhere to
    the right of the held site `i`:

        law(x_i = b, x_s … x_{s+w−1})  ∝  exp(F_b + B + I),

    `F_b` the message of the forward elimination of the sites `0 … s−1` with `x_i` held at
    `b`, `B` the message of the backward elimination of the sites `n−1 … s+w` — the forward
    message of the mirrored chain, computed once per model — and `I` the terms that lie
    inside the window.  Every term of a band model (largest site minus smallest at most
    `w`) is in exactly one of the three: a term whose first site is at most `s − 1` cannot
    reach `s + w`, so it is in `F_b`; one whose last site is at least `s + w` starts at `s`
    or later and is in `B`; the rest are inside.  *Routing.*  An item on sites `U` gets the
    route of item 70 where it has one — so that chains of at most `2w` sites are treated
    as before; else its first site is held if its other sites span at most `w − 1`, or its
    last site if the others do (the kept end where both would do, as in item 70); items
    with the same direction, held site and window form a group; windows are shared
    greedily among the items of a held site.  Items in which neither end can be held —
    two sites at each end, or sites spread over more than `w` either way — still have no
    route and are left out, which keeps every bound valid.  *Cost.*  One forward and one
    backward sweep per model, and per held site and state a propagation from the held
    site to its furthest window (Lys₂₀ at band 7: 156 groups, 464 s, 5.5 GB).
    *Test at every state* (Lys₅ and LKSE:5 at band 2, where the chain is longer than
    `2w`): four items go through a window inside the chain (18 of 25 routed, 14 before);
    every clamped total mass is one to `5·10⁻¹⁴`; **the five group statistics agree with
    enumeration to `9·10⁻¹³`**; the hypotheses hold at every state and the two controls
    fail (229 329 and 112 163 violations on Lys₅); the exact `ln Z` is inside every
    corrected bracket.

78. **The thirteen runs of items 71, 73, 74 repeated with the general module — and an
    expectation of mine that was wrong** [X for four rows; M; `first_order_recovery_*.log`,
    which are now the logs of the changed driver; the numbers of part (19) are those of
    commit `90abf0e`].  Before the runs I wrote that the band-7 cases "must reproduce the
    committed brackets digit for digit".  They do in every row that uses only the old
    routes — far pairs; far pairs and terms; all three stages where no item goes through
    an inner window (Lys₅ at band 3, twice; Lys₁₂ at order 3) **[item 83 (b): the
    far-pairs-and-terms row is unchanged in six of the thirteen runs only]** — and not in the last row
    of the others, **because four-site subsets that had no route now have one**.  The
    statement that holds, in all thirteen: *same items, same digits; more items, a
    bracket inside the old one at both ends.*

    | instance, order, band | items with a route: before → now (through an inner window) / all | corrected width: before → now | bracket now |
    |---|---|---|---|
    | Lys₅, 4, band 2 (every state) | 14 → 18 (4) / 25 | 0.002913 → 0.002885 | `[251.3475876, 251.3504722]` |
    | Lys₅, 4, band 3 (every state) | 10 → 10 (0) / 11 | `6.437·10⁻⁵`, unchanged | `[251.3484184, 251.3484828]` |
    | Lys₅, 5, band 3 (every state) | 12 → 12 (0) / 15 | `7.104·10⁻⁶`, unchanged | `[251.3484424, 251.3484495]` |
    | LKSE:5, 4, band 2 (every state) | 14 → 18 (4) / 25 | 0.001611 → 0.001558 | `[276.4669085, 276.4684663]` |
    | Lys₁₂, 3, band 7 | 100 → 100 (0) / 100 | 0.06112, unchanged | `[517.1160739, 517.1771913]` |
    | Lys₁₂, 4, band 7 | 380 → 415 (35) / 465 | `8.297·10⁻⁵` → `8.161·10⁻⁵` | `[517.1285108, 517.1285924]` |
    | Lys₁₂, 5, band 7 | 818 → 996 (178) / 1 346 | `2.184·10⁻⁵` → `2.178·10⁻⁵` | `[517.1285396, 517.1285614]` |
    | Lys₁₂, 4, band 6 | 420 → 505 (85) / 610 | `2.786·10⁻⁴` → `2.738·10⁻⁴` | `[517.1284560, 517.1287298]` |
    | Lys₁₂, 4, band 5 | 352 → 543 (191) / 742 | `4.217·10⁻⁴` → `3.890·10⁻⁴` | `[517.1284232, 517.1288122]` |
    | Lys₁₂, 4, band 4 | 262 → 513 (251) / 854 | `6.875·10⁻⁴` → `6.449·10⁻⁴` | `[517.1283300, 517.1289748]` |
    | (LKSE)₃, 4, band 7 | 380 → 415 (35) / 465 | 0.001537 → 0.001414 | `[655.6120305, 655.6134443]` |
    | (LKSE)₃, 5, band 7 | 818 → 996 (178) / 1 346 | `1.433·10⁻⁴` → `1.407·10⁻⁴` | `[655.6126392, 655.6127798]` |
    | Ser₁₂, 5, band 7 | 818 → 996 (178) / 1 346 | 0.001791 → 0.001666 | `[227.3678932, 227.3695587]` |

    Checks in every row as in item 73 (the hypotheses at 5 380 states or at every state,
    no violation; both controls fail; the means against exact samples within 1.6 standard
    errors), and one more in the nine sampled rows: **P9's raw tables entry by entry at
    5 000 random states with exactly `m` side chains off the anchor** — where the
    remainder is the exact anchored term of the changed set — no violation, with the
    control (every table replaced by its minimum) failing at 343 to 2 733 states.
    *What the narrow bands show.*  Item 74 had said that at bands 5 and 4 "half to two
    thirds of the items have no route; a held-site pass with a backward message would
    serve them".  It serves 191 and 251 of them, and the brackets tighten by 8 and 6 per
    cent: **the items without a route were not where the loss was.**  At band 4 the
    subsets that still have none carry `1.1·10⁻⁴` nats of first-order slack per side;
    the rest of the `6.4·10⁻⁴` is the loss between groups (`D²/4 = 2·10⁻⁴` for
    `D = 0.029`) and the envelope.  **[Corrected in part (21), item 83 (a): measured,
    the loss between groups at band 4 is `4.31·10⁻⁴` — twice `D²/4`, two thirds of the
    bracket; the subsets without a route, the envelope and the allowances are the other
    `2.13·10⁻⁴` together.  So the sentence "the items without a route were not where
    the loss was" stands, and the split given here was wrong in its main term.]**

79. **A charged chain longer than twice the band: Lys₂₀** [M; validity P;
    `first_order_recovery_K20_m4_w7.log`; prediction written at 14:26 UTC before the run,
    research log, cycle 60].  Ace-Lys₂₀-NMe on the helix: `5.5·10¹⁷` states (three sites
    with 14, 14, 12 states, seventeen with 7); the ball of radius 3, 385 566 evaluations
    (`pi_inference/ball_cache.py`, 19 minutes); workstream P9's 4 845 raw tables of order
    4 through `p9_verification/dump_theta2.py` (26 minutes on two cores), whose call
    reproduces P9's own stored tables bit for bit on 18 subsets of Lys₁₂ and on the four
    small instances (`dump_theta2_check_K12_m4.log`); band 7; sub-tuples by the rule of
    item 67.

    | | predicted | found |
    |---|---|---|
    | sum of the table maxima, `βΓ₄` | about 35 | **45.2** (a miss: 2.5 times Lys₁₂'s for 1.67 times the length) |
    | the floor stays at the anchor | three chances in four | yes |
    | sandwich (allowance attached term by term) | 0.02 (0.012–0.04) | **0.01814** `[800.505214, 800.523352]` |
    | corrected bracket | `3·10⁻⁴` (`10⁻⁴`–`10⁻³`) | **`4.05·10⁻⁴`** `[800.5150660, 800.5154710]` |

    Stages: far pairs `7.6·10⁻⁴`, with the out-of-window terms `7.0·10⁻⁴`, with the
    allocation `4.05·10⁻⁴` (`D`/width 45).  6 175 items — 156 far, 1 664 terms, 4 355
    subsets — of which 3 823 have a route, 2 029 through a window inside the chain; of
    the 2 352 without, 2 240 are four-site subsets (`1.2·10⁻⁵` nats of first-order slack
    per side).  Checks: the hypotheses at 5 380 states, no violation (controls: 8 029
    and 3 501); the means against 20 000 exact samples of the ceiling within 1.4
    standard errors; P9's tables entry by entry at 20 000 states with exactly four side
    chains off, no violation — smallest ratio of entry to remainder 10.9, median 240 —
    with the control failing at 5 556.  The tables are heterogeneous over five orders
    of magnitude: the largest entry of a subset's table is between `2·10⁻⁶` and `0.8`
    `kT`, median `4·10⁻⁴`.  1 390 s, 5.5 GB.  **So the method of part (19) carries to
    a chain of `5.5·10¹⁷` states with nothing new but the general windows: a
    deterministic bracket of `4·10⁻⁴` nats from 385 566 evaluations.**  Not measured for
    this instance: the envelope on a Gibbs sample; a sampled interval to compare with.

80. **What a checker of a recovered bracket would have to hold** [a description for the
    engineering division, promised in SCI-RES-0022 §5; not yet a specification].
    (i) *The sandwich*, as in SCI-MSG-0025 §8: two band models as sums of tables.
    (ii) *Each model as a sum of labelled pieces*, each either exact (a pair in the band,
    an evaluated term in a window) or a **reduction of a named source table** (the
    maximum or minimum over the sites given up; the split of a far pair around the
    anchor; a subset's resolved table charged to a sub-tuple) — so that every item is
    "reduction minus source" and its non-negativity and the hypotheses
    `Σ items ≤ m₊ − E`, `Σ items ≤ E − m₋` follow from identities a checker can recompute
    table by table, not from a statement over all states.  (iii) *The routes* — for
    every item the direction, the held site and the first site of its window — and
    *the five statistics of every group*; a checker recomputes them with its own
    held-site passes (we know no cheaper verification).  (iv) *The four bounds* from
    the two `ln Z` and the statistics (item 69).  What it cannot check from these
    objects: the resolved tables themselves (workstream P9's Theorem R; request P9-E2)
    and the evaluation tolerance (request A19-E2).

81. **What part (20) changes** [summary].  (i) The recovery is no longer limited to
    chains of at most twice the band; the limit that remains is items that need two
    held sites.  (ii) All certified numbers of parts (19)–(20) now come from one driver
    and one module, with every log re-produced; the brackets of part (19) are confirmed
    as brackets — the new ones lie inside them **[item 83 (c): nesting shows consistency
    of two versions of one code, not validity]**.  (iii) Routing more items helps little
    once the far pairs are routed: what is left is the loss between groups, which the
    theory division's answer to our question A19-T2 (THY-RES-0016 §4) says cannot be
    removed from the group laws alone when the groups' events overlap, and can be
    reduced by the joint law of pairs of groups — not built.  (iv) *Not done:* pair
    terms; two held sites; the envelope and a sampled interval for Lys₂₀; a referee.
    (v) Under the research owner's directive of 2026-11-26 no further instance of this
    kind is run in this phase; what the line needs now is in
    `docs/science/ASSUMPTION_AUDIT.md` (obligations `G-1 … G-8`).

### (21) Parts (19)–(20) refereed (workstream R19): what holds, what was wrong in our texts, what a certified number here means — and two things measured since: the transition of a floor, and where the evaluations of a shell go [review and replication by R19, checked by the coordinator; M for items 84–85; added 2026-11-26]

*The referee:* workstream R19, an adversarial review of items 69–75 and 77–81 and of Part A of
`ASSUMPTION_AUDIT.md`, asked for by the coordinator of his own results
(`workstreams/R19_REPORT.md`, 639 lines; code and logs `experiments/science/ws_R19/`; an
internal review by an AI session, not external peer review).  *What the coordinator
checked:* the report read in full; the measurement behind its first major finding repeated
with another seed (below); its audit tests re-run, output identical; its numbers for the
enumerated instances compared with our own logs.  All of its findings are accepted.

82. **What holds** [review + replication, R19 §§2.1, 3, 4].  (i) The accounting behind the
    recovery is right term by term, and it is more than an inequality:
    `m₊ − E − s₊ = (env − r) + allowances` holds as an **identity to `10⁻⁹` kcal/mol at
    every state** of the four enumerated instances and at the driver's 5 380 states of
    Lys₁₂ at bands 4 and 7.  No slack is counted twice: the allocation item is valid on
    both sides because the ceiling needs `r ≤ env` and the floor `−r ≤ env`.  Controls
    the coordinator had not run: every single item doubled is seen by the driver's
    check (25 of 25, 11 of 11, 15 of 15, 25 of 25 on the enumerated instances; all far
    and term items and 458 of 462, 277 of 285 allocation items at twelve residues); the
    allocation slack moved to one side fails at 1 931 to 86 594 states; the whole penalty
    claimed fails everywhere.  (ii) **The held-site passes compute exact means:** 3 000
    random band models, 65 670 group statistics against the referee's enumeration,
    largest relative deviation `6.4·10⁻¹³`; all 56 groups of Lys₁₂ at band 4 and five at
    band 7 by a variable elimination that knows nothing of windows, `5.8·10⁻¹²` — **the
    published bracket of Lys₁₂ at band 4 is reproduced by an independent computation of
    everything between the tables and the number**; no illegal route in 238 267 fuzzed
    items; input that violates the precondition of the routing stops at an assertion.
    (iii) The regression claim of item 78 is true in all thirteen runs; 104 of 104
    numbers of its table agree with the logs; six logs re-run, identical.  (iv) **No
    published bracket is put in doubt.**  Critical findings: none; major: four (one
    here, three in the audit); minor: fifteen.

83. **What was wrong in our texts — linked corrections** [SCI-MSG-0030].
    (a) **"The loss between groups is about `D²/4`" was a formula that we called a
    measurement** (items 73, 78, 81 (iii); SCI-MSG-0028 §6 (b); SCI-RES-0024 §2 and its
    limitations; the audit, A6 and H4).  The numbers `1.3·10⁻⁵` and `8·10⁻⁵` are
    `D²/4` evaluated; no log beyond five residues contained a measurement.  Measured
    (loss := corrected width − width with the same routed items put back exactly):

    | instance | `D` | corrected width | same items put back exactly | loss | loss / (`D²/4`) | loss / corrected width | source |
    |---|---|---|---|---|---|---|---|
    | Lys₅, order 4, band 2 | 0.04765 | 0.002885 | 0.001614 | 0.001271 | 2.24 | 0.44 | our own log (enumeration) |
    | Lys₅, order 4, band 3 | 0.01891 | `6.437·10⁻⁵` | `4.996·10⁻⁵` | `1.44·10⁻⁵` | 0.16 | 0.22 | the same |
    | Lys₅, order 5, band 3 | 0.01870 | `7.104·10⁻⁶` | `1.573·10⁻⁶` | `5.5·10⁻⁶` | 0.06 | 0.78 | the same |
    | LKSE:5, order 4, band 2 | 0.2054 | 0.001558 | `8.185·10⁻⁴` | `7.4·10⁻⁴` | 0.07 | 0.47 | the same |
    | **Lys₁₂, order 4, band 4** | 0.02877 | `6.449·10⁻⁴` | `2.135·10⁻⁴ ± 6·10⁻⁷` | **`4.314·10⁻⁴ ± 6·10⁻⁷`** | **2.085 ± 0.003** | **0.67** | R19 §3.4: first order exact, second order from `10⁶` exact samples of the floor; **repeated by the coordinator with another seed: `4.312·10⁻⁴ ± 5.6·10⁻⁷`, 2.084** |
    | **Lys₁₂, order 4, band 7** | 0.007329 | `8.161·10⁻⁵` | `6.099·10⁻⁵ ± 1.9·10⁻⁷` | **`2.061·10⁻⁵ ± 1.9·10⁻⁷`** | **1.535 ± 0.014** | **0.25** | R19 §3.4 (`4·10⁵` samples) |
    | 810 random sandwiches with `D < 0.3` | | | | | quartiles 0.002, 0.25, 0.57; largest 13.3 | | R19 §3.2 (enumeration) |

    So `D²/4` is neither a bound nor a typical value; the first four rows were in our own
    logs when we wrote "about `D²/4`".  *What changes:* at band 4 two thirds of the
    bracket is loss between groups, and what an exact treatment of the routed items
    would leave is `2.1·10⁻⁴` for the items without a route, the envelope and the
    allowances together; at band 7 the loss is a quarter of the bracket and the envelope
    about `5.4·10⁻⁵` (R19's first-order accounting).  The sentence of SCI-RES-0024 §2,
    "pair terms could remove up to about half of what is left [Lys₁₂ at order 5] and a
    fifth [Lys₂₀]; the rest is the envelope", is **withdrawn**: for order 5 the logs leave
    no room for an envelope (`10⁻⁹`), so most of that bracket would be loss between
    groups [H, R19's inference, not a measurement]; for Lys₂₀ nothing is measured.
    *What does not change:* every bracket; and the direction of the advice — what is
    left to gain at these widths is between groups (pair terms, the joint law of two
    groups), more than we said.
    (b) Item 78: the far-pairs-and-terms row is unchanged in six of the thirteen runs,
    not in all; in seven, term items are newly routed and that row moves.  "Same items,
    same digits" is unaffected.
    (c) Items 81 (ii) and SCI-RES-0024 ("the published brackets stand"): that the new
    brackets lie inside the old ones shows that two versions of one code are consistent;
    that either is a bracket rests on items 71 and 73 and now on item 82.
    (d) What our checks can and cannot see: the hypothesis check tests the accounting of
    the reductions item by item, and **sees nothing when every resolved table is halved
    or divided by ten** (the envelope is at least 10.75 times the remainder at every
    state tested), so it does not test the size of workstream P9's tables; the
    comparison of the means with exact samples "within 1.6 standard errors" has no
    power (rare states dominate; with 400 000 samples 15 of 280 statistics are more
    than three standard errors off while the exact replication agrees to `6·10⁻¹²`).
    (e) Code, recorded and **not changed in this commit** (the logs must be those of the
    code; to be changed together with the next re-run of the fourteen logs):
    `slack_recovery.bounds` returns the 60th iterate of (UE), (UP), not the limit — valid,
    and converged to machine precision for `D ≤ 0.2`, but short by `2.3·10⁻³` at
    `D = 2.4`; it tests neither finiteness nor lower ≤ upper; a comment in
    `window_model_occ.py` (l. 52) says "common to floor and ceiling" of choices that are
    made once per side.
    (f) **What a certified number of parts (16)–(20) is** (R19 §2.4, adopted as our own
    statement): an interval for `ln Z` of one *model* energy — a vacuum force field plus
    an implicit-solvent term, side chains from a finite rotamer library on a fixed
    backbone, one temperature — **given** that workstream P9's tables satisfy its Theorem
    R at every state (a paper proof by one workstream, machine-checked in its abstract
    skeleton only, tested where the tables exceed the remainder at least 8.9-fold, so
    that a table too small by less than that would pass every test); **given** the
    evaluation tolerance `ε_g = 10⁻⁷` kcal/mol (assumed); with one implementation of the
    evaluator and of the tables; in double precision with margins of `10⁻⁹` and no
    interval control.  It is not a statement about a peptide in water, not a
    machine-checked certificate, and its width does not measure what the evaluations
    know.  For Lys₂₀ the number has been compared with nothing (no sampled interval;
    38 % of its items without a route; above the referee's limits).

84. **A floor leaves its reference by a sharp transition in the size of its penalty
    tables: four cases, and a two-state test** [M, exact transfer-matrix values; the
    occupancy from 1 000 exact samples per `λ`; `pi_inference/floor_transition.py`,
    `floor_transition_*.log`, `floor_two_state.py`, `floor_two_state.log`; prediction
    written at 16:05 UTC before the script existed].  The theory division reads a floor
    that delocalises as a first-order transition (THY-RES-0016 §5 (i)) and asked for
    numbers.  With every penalty table multiplied by `λ` (the certificate is `λ = 1`):

    | case | sum of the table maxima (`kT`) | `λ_c` | predicted | displaced sites go from below 2 to above 8 within a factor | slope `β⟨pen⟩` in the reference state, in the displaced state | `ln Z` of the floor at `λ = 1` minus at `λ = 0`; first order |
    |---|---|---|---|---|---|---|
    | Lys₁₂, order 4, band 4 | 16.6 | **15.32** | 1.5 – 4 (**missed**) | 1.14 | `8.6·10⁻⁴`, 5.9 | `5.349·10⁻⁴`; `5.270·10⁻⁴` |
    | Lys₁₂, order 4, band 7 | 17.9 | **18.80** | 2 – 6 (**missed**) | 1.06 | `1.6·10⁻⁴`, 5.8 | `9.814·10⁻⁵`; `9.748·10⁻⁵` |
    | Lys₁₂, order 3, band 7 | 271.6 | **1.318** | 1.05 – 1.5 (met) | 1.22 | 0.27, 71 | 0.0528; 0.0249 |
    | (LKSE)₃, order 3, band 7 | 1 233.9 | **0.198** | 0.1 – 0.4 (met) | — (2.8 sites off already at `λ = 0`) | 0.18, 723 | 658.8; 0.18 |

    `ln Z(λ)` is convex on every grid (it must be; the control, the same test on `−ln Z`,
    fails); at `λ = 1` the script reproduces the upper end of the committed sandwich of
    each case.  **The certificate of Lys₁₂ at order 4 stands a factor 15 to 19 below its
    own transition, the one at order 3 a factor 1.32, and (LKSE)₃ at order 3 is beyond
    it** — which is the bracket of 658.9 nats that workstream P9 reported as lost.
    *Two states* (`floor_two_state.py`): if the floor's ensemble near the transition is
    a mixture of the reference state and one displaced state, every mean is linear in
    the weight; the exact slope predicted from the sampled occupancy by the line through
    the two states, at the points where the weight is between 0.1 and 0.9, is within
    0.99–1.18, 1.00–1.17, 1.11–1.22, 1.11–1.33 of the exact slope in the four cases
    (medians 1.04, 1.08, 1.20, 1.23), and the lever rule gives 0.82, 0.60, 0.64, 0.41
    for the excess of `ln Z` at `λ_c` against 0.76, 0.61, 0.77, 0.40 observed.  The
    systematic excess above one has a reason: the displaced state is not one state —
    its slope still grows with `λ`.  The control (the same points with `λ` as the
    abscissa, a smooth response between the same two grid points) is off by factors
    1.2–5, 0.59–2.3 and 1.5–4.6 in three cases and only by 0.87–1.6 for Lys₁₂ at order
    3: **there the test discriminates weakly**.
    *Why the two predictions at order 4 failed:* a displaced lysine was priced at the
    cost of a typical state off the anchor (`2.2 kT`); the state the penalty selects is
    where the tables are large, which is where charged groups come close, and it costs
    about 90 to 110 `kT` in the model without penalty (the displaced slope times `λ_c`)
    — eight to nine `kT` per residue.  A prediction of `λ_c` needs the least ratio (cost without
    penalty)/(penalty) over states, not a typical cost.  *What follows for a
    certificate:* `λ_c` is a safety factor that can be reported with every bracket, at
    the cost of a few more transfer-matrix runs (`OPEN_PROBLEMS.md` D12).

85. **Where the evaluations of a shell go** [M on a model of the occupation, with its
    control; no certificate; `pi_inference/subset_concentration.py`,
    `subset_concentration_K12_m{3,4}.log`].  With the occupation taken from the product
    of the one-site marginals of a Gibbs sample of Lys₁₂: nine tenths of the first-order
    envelope of order 3 lie in 3.2 % of the triples, which cost 7.9 % of the evaluations
    of the shell of radius 3 (99 %: 20 % of the triples, 34 % of the evaluations); at
    order 4, nine tenths in 2.0 % of the subsets (6.2 % of the shell).  **The control —
    the same tables shuffled among the subsets — gives almost the same shares:** the
    concentration is that of the occupation, and the rule "rank a subset by the product
    of its sites' probabilities of being off the anchor" is available before any
    evaluation.  The estimate on the 960 sampled states themselves is inconclusive (its
    control shows the concentration of the sample).  Not done: the remainder bound of a
    down-closed family that is not a ball, and a run (`OPEN_PROBLEMS.md` D14).

### What is in print, and what remains ours (workstream A3; added at checkpoint 39)

`workstreams/A3_REPORT.md` has the statements side by side, the reading level of every
source, the search log, and what could not be accessed.  The coordinator checked
against the sources: Block–Shetty (Theorems 5, 6, 8, Propositions 1, 2), Hoeffding 1963
(pages 16, 20–22 of the scanned original: Theorem 3 with (2.8)–(2.10) and the sentence on
Bennett; Lemma 1; (4.12)–(4.16)), Georgiev–Lilien–Donald 2008 (Proposition 3 in the PubMed
Central text; record according to PubMed: J Comput Chem 29(10):1527–42,
[doi:10.1002/jcc.20909](https://doi.org/10.1002/jcc.20909)), Cesar–Rogers (Lemma 3.2),
Chazottes–Collet–Külske–Redig (Theorem 1 and (9)–(10)), Kontorovich–Ramanan (Theorem 1.2),
and fourteen shorter passages (the list of all twenty is in SCI-RES-0009 §4).  Every
quotation agreed.  A3's own three statements (its A3.1–A3.3)
were re-derived and re-checked (`a3_adoption_check.py`), and its script was re-run from
a clean state to its last line with identical output.

| statement of this addendum | status after the search | the source to cite |
|---|---|---|
| (0)(a) Jensen bracket with `L(w)`, two-point law extremal | **in print as stated** | Hoeffding 1963, Lemma 1, (4.12)–(4.15); `L(w) = ln` of Specht's ratio (Specht 1960, as quoted by Fujii–Lee–Seo 2002); the "maxkl" of bounded-range mechanisms (Dong–Durfee–Rogers, arXiv:1909.13830) |
| (0)(b) deterministic certificate on a box; `q*` | known special case; the necessity half elementary | Georgiev–Lilien–Donald 2008, Proposition 3 |
| (0)(c)–(e) hinted cost `Θ((Z(lo)/Z − 1)/ε)` (the theory division's theorem) | the cost quantity and both mechanisms are corollaries of known statements; **not found as a theorem on hinted query complexity of a box class** | Liu–Fisher–Ihler (NeurIPS 2015), Proposition 3.1, Corollary 3.2; Aaronson, arXiv:quant-ph/0210020, Definition 3, Lemma 5 (randomised certificate complexity — the framework of "with a hint"); Dagum–Karp–Luby–Ross 2000 through restatements; Block–Shetty, Theorem 6 |
| A17.1 (detection lemma) | Hölder; analogues in print | Block–Polyanskiy, arXiv:2302.04658, Lemma 27 |
| A17.2 (hinted cost `e^{κ}/ε^{p/(p−1)}`) | **direct corollary**: the count is Block–Shetty's Theorem 6, the lower-bound instance their Theorem 8 | Block–Shetty |
| A17.3 (unhinted, `ε^{−max(2, p/(p−1))}`), A17.4 (Kullback–Leibler, `exp(Θ(κ/ε))`) | **in print** (sampling model; A17.4 there beyond the centre and with one more factor `1/ε`) | Block–Shetty, Theorems 5, 8, Propositions 1, 2; Kunsch–Novak–Rudolf 2019; Bubeck et al.; Devroye et al. |
| A17.5(i) | in print in spirit (linear `f`) | Block–Shetty, Proposition 1 |
| A17.5(ii) (no polynomial moment of the remainder energy suffices) | elementary; not found stated; in the sampling model an instance of Bahadur–Savage 1956 (not opened; via Wang–Ramdas) | — |
| "the direction matters" | in print | Minka 2005; Jarzynski 2006, eq. (45); Chatterjee–Diaconis, Theorem 1.1 |
| A17.6 (product reference) | **direct corollary**, in the sharp form now stated | Cesar–Rogers, Lemma 3.2; Bun–Steinke, Lemma 2.2 |
| A17.7 (Bennett bracket): the inequality, its extremal law, the variance input | **in print as stated** | Hoeffding 1963, Theorem 3, (2.8)–(2.10); Fan–Grama–Liu, Lemma 3.1; van Handel's notes, Theorem 2.3, Corollary 2.4 |
| A17.7 used as a certified second-order bound for free-energy perturbation | **not found** (Decoster 2004 unread) | set against Delle Site–Hartmann 2024 |
| A17.8 (Markov-chain reference) | **in print** | Chazottes–Collet–Külske–Redig, proof of Theorem 1, (9)–(10); Kontorovich–Ramanan, Theorem 1.2 |
| parts (6), (7), (9), (10): the measured prices on force-field instances | ours (measurements; no prior-art question) | — |

**What remains ours, stated without inflation.**  (1) The *reading* of the table as a
verification cost: with a hint the one-sided cost is the whole cost, so verification is
cheaper than estimation exactly for `p > 2`; and its converse, which is A3's: at an
instance that is constant on the bulk the hint is worth nothing (`545` evaluations
against the `1088` quoted with a hint).  (2) The negative statement A17.5(ii) and its
consequence for what a fit may claim.  (3) A17.6 in the sharp form — a two-line corollary
of the differential-privacy literature that we did not find applied to remainders of a
force field.  (4) The use of Hoeffding's Theorem 3 as a certificate for first-order
perturbation theory — "not found", pending Decoster.  (5) **The measurements**: which row
of the table real remainders are in (parts (6), (7), (9), (10)).  That last item is the
part of this addendum that no search could have replaced.

**Three sentences of ours and of the theory division that say more than the literature
allows (A3 §4.8).**  (i) "What must be certified is the floor, and nothing else can
replace it" (THY-RES-0007 §4) — contradicted as a literal statement by the heavy-tail
literature and by Block–Shetty; what is true, and is Bahadur–Savage, is that *some*
a-priori control of the upper tail of the Boltzmann factor is indispensable.  This
addendum said so; the literature said it first.  (ii) "With a hint" overstates what the
hint does (above).  (iii) The headline `Θ((Z(lo)/Z(g) − 1)/ε)` drops the bump term
`(1 − Z(hi)/Z(g))/(1 − e^{−ε})`, which is the whole cost near the floor, where the headline
reads zero.  And one of ours: "(the lower bound) costs a mean" is the cost of the
Gibbs–Bogoliubov bound, which is not `ε`-tight; an `ε`-tight lower bound on `Z` costs the
variance term — in `ε`, the "expensive" side of the certificate is the cheap one
(Block–Shetty, Theorems 5–6, Proposition 2).

**Not accessed (so nothing here rests on them):** the original of Dagum–Karp–Luby–Ross;
Bennett 1962; pages 23–30 of Hoeffding 1963 (the proof of Theorem 3); Specht 1960;
Bahadur–Savage 1956; Külske 2003; Marton's papers; Efron–Stein 1981; Decoster 2004;
Block–Shetty's appendices (their Theorems 6 and 8 are taken as stated in a preprint
nine months old).

### Reading (kept apart from the statements)

1. **"Independent of the size of the system" is true of a constant box and moves the
   size into the floor [M for the numbers, from our pilot].**  For the one real remainder
   we have measured against a pair-additive class in backbone torsions (workstream P,
   `SP_REPORT.md` Statement 5(c)), the largest absolute remainder — an upper bound on the
   needed floor — is `0.5, 1.0, 2.3, 4.8 kcal/mol` at 2–5 residues and `9.3` at 8 residues on
   a coarser grid: `0.8, 1.7, 3.9, 8.1, 15.6 k_BT`.  It roughly doubles per residue at these
   sizes.  The two illustrations in THY-RES-0007 (`5·10³` evaluations "whatever the chain
   length" at `3.7 k_BT`; `7·10⁸` at `15.6`) are the same remainder at four and at eight
   residues.  With an extensive floor `ρ₋ = nρ₁` the cost is `e^{nρ₁}/ε`: the exponential has
   been renamed, not removed.  What the theorem does give is the right *coordinate*: the
   cost is exponential in the free-energy gap to the floor, in `k_BT`, not in the number
   of variables.
2. **The floor should be a function, and then it is a lower model [H].**  Nothing in
   the theorem needs `lo` constant: with a computable lower model `m ≤ g` whose Gibbs
   measure can be sampled, the cost is `(Z(m)/Z(g) − 1)/ε = (e^{F(g) − F(m)} − 1)/ε`.  The
   pairwise lower model of third order (our P2, Statement 5(d); the theory division's
   accepted item P2-T1) is such an `m` — provided its constants are *certified*, which
   so far they are only by enumeration (workstream P3 is trying analysis), and provided
   `π_m` can be sampled exactly, which for a pairwise model on a general graph it cannot
   (it can on a chain or a graph of small tree-width).
3. **In rotamer variables the picture is better than in torsions [M, from P2].**  There
   the remainder beyond pairwise has third-order constants of `0.003–0.2 kcal/mol` for
   neutral side chains; for apolar ones a floor of a few `k_BT` at tens of residues is
   conceivable.  Whether analysis can certify it is P3's question.
4. **Which row of the table a real remainder is in is an empirical and analytical
   question nobody has asked.**  Floors (row 1) need worst-case analysis of the energy
   function; row 2 at `p = 2` needs a bound on a chi-square divergence, which A17.6 reduces
   to one-site oscillations when the reference is a product measure.  For orders of
   magnitude only: the measured first-order constants of the solvent term in rotamer
   variables (P2: largest `c_i` `0.44–0.84 kcal/mol` for valine, `5–10` for serine, i.e.
   `0.7–1.4` and `8–17 k_BT` at 300 K) would give `K ≈ n·(0.7…1.4)²` for valine — tens of
   residues within reach of plain certified reweighting — and `K ≈ n·(8…17)²` for serine,
   which is hopeless.  **These are not certificates, for two reasons:** the constants were
   measured by enumeration, and the known part of that measurement is pairwise, not a
   product measure, so A17.6 does not apply to it as it stands (with a product reference
   the pair terms of the known part enter the oscillations as well).

### What is not done

No second reader of the proofs of A17.1–A17.5 (workstream A3 compared statements with
the literature and did not referee them; it re-derived A17.6 in a sharper form).  The
prior-art search is A3's, with its limits listed above ("Not accessed").  The lower
bound of A17.3(iii) is a sketch — in print as a theorem in the sampling model
(Block–Shetty; Kunsch–Novak–Rudolf), not proved here in the query model on a finite
space with atoms.  A17.4 is proved here at the centre only (in print beyond it).  The
instance-optimal sampler for `p < ∞` (the analogue of the dip-weighted sampler of the
box) was not looked for.  For non-product references the sharp form of A17.6 needs the
ranges of the conditional free energy of the remainder, which nobody has measured on a
real chain model.  Parts (6), (7), (9) compare with exact enumerations of a force-field
model on rotamer grids, not with a laboratory measurement; their floors, variances and
divergences are computed by enumeration and are prices, not certificates.
