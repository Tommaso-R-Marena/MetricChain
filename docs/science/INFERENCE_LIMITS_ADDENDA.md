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
