# Phase-2 digest for S3: what the consolidated archive already contains

*Read-only digest of `MetricChain-archive/consolidated/` (pinned final version, built 2026-11-27).  All paths
are relative to `consolidated/`.  Quotations are verbatim (Markdown back-ticks kept as in the source; long
statements cut with "…" where marked).  "Not found" means not found by grep in the files read.  Nothing in the
archive was run; the only computation was reading JSON files with a standard parser.  Every document quoted
was written by AI sessions and none has been externally reviewed (see `00_MASTER_INDEX.md`, "Read this
before anything else").*

**S3 dictionary.**  S3's weight box `l ≤ w ≤ u` is the archive's "box class" / "sandwich" / "density-ratio
class": with energies, `l = e^{−m₊}`, `u = e^{−m₋}` for `m₋ ≤ E ≤ m₊` (theory §11.30 writes `lo ≤ r ≤ hi` for a
remainder `r` around a sampleable known part `f̂`, so `l = π e^{−hi}·Z₀`, `u = π e^{−lo}·Z₀`).  S3's sampler
`q ∝ u − l` is **exactly** the sampler of Proposition 11.113 (`q(x) ∝ e^{−m₋(x)} − e^{−m₊(x)}`).  S3's
identified interval for exact data is item 89(d) of the science addenda (threshold rule with a multiplier
`λ`), and the ensemble division's F3/E2(a)/E17.2/E23 give the dual form with tolerances and ratios.

---

# Part 1 — existing mathematics

## (a) Interval / box / density-ratio classes; sup/inf of ratios; threshold ("bang-bang") extremals

### (a1) The threshold rule (exact range of `E_w ψ` over the box) — ensemble division, adopted by science

`04_ensemble_identifiability/docs/collaboration/responses/ensemble/ENSEMBLE-RES-0002.md` §4 ("Science's
second question: is the population bracket of a sandwich the identified set"):

> **Yes** — as your A17 (13) already argues, and with one addition.  [P, elementary; K for the
> rule.]  Over the box `m₋ ≤ E ≤ m₊` the weights `e^{−E(x)}` range independently over
> `[e^{−m₊(x)}, e^{−m₋(x)}]`, the population `P_E(A)` is monotone in each, so your interval is
> exactly its range and every value in it is attained: it is the identified set and cannot
> be sharpened without further information.  **What can be sharpened for free is any
> observable that is not an indicator.**  For a general `ψ` the exact range of `E_E ψ` over
> the box is given by the threshold rule of the density-ratio class (DeRobertis–Hartigan
> 1981): the upper end is the unique `t` with
>
>     Σ_x e^{−m₋(x)} (ψ(x) − t)₊  =  Σ_x e^{−m₊(x)} (ψ(x) − t)₋ ,
>
> (take `m₋` where `ψ > t` and `m₊` where `ψ < t`), and symmetrically for the lower end.  Sums
> of single-site intervals are *not* sharp for a multi-site observable … the identified set of a vector of populations of a
> partition is the image of a box under a linear-fractional map, smaller than the product of
> the intervals.

* **Status:** "[P, elementary; K for the rule.]" (same place).
* **Prior art:** `03_scientific_translation/docs/science/workstreams/R24_REPORT.md` §5, row "(1) threshold rule":
  "**in print** | Angers and Delampady, "Fuzzy sets in nonparametric Bayes regression", IMS Collections 3 (2008)
  89–104, arXiv:0805.3209, **Theorem 5.1 [passage]**: over `Γ_DR = {π : L ≤ απ ≤ U}`, `sup ∫q₁π/∫q₂π` is the unique
  solution `λ` of `∫(q₁ − λq₂)⁺U + ∫(q₁ − λq₂)⁻L = 0` (their `q⁻ ≤ 0`), "see [6]" = DeRobertis and Hartigan,
  Ann. Statist. 9 (1981) 235–244, and "[8], Theorem 3.9" = Ghosh, Delampady, Samanta (2006).  **The 1981 paper
  itself was not opened** … A sample version: Wasserman and Kadane 1992, per Cozman's page **[tool summary]**;
  Geweke and Petrella, J. Bus. Econ. Statist. 16 (1998) 469–478 **[tool summary]**."
  Same table: "(2) the sandwich as a class of pairwise ratio constraints | **in print as the definition** | G. Walter,
  "Density Ratio Class Models and Imprecision", slides, 2 June 2014 **[full, 9 slides]**, slide 2: "If `l(ϑ) > 0 ∀ϑ`,
  then `M_{l,u} = {p : p(ϑ)/p(ϑ′) ≤ u(ϑ)/l(ϑ′) ∀ϑ, ϑ′}`, hence the name""; "population bracket of a sandwich …
  Walter, slide 3 **[full]**: `P̲(A) = [1 + ∫_{A^c}u/∫_A l]^{−1}`"; "(4) sandwich + averaged data | **not found**
  (queries 4, 6) | Generalised moment problems and their duality are classical **[memory, unverified]**; no source
  read that combines them with a density-ratio class."
* `04_ensemble_identifiability/docs/ensemble/PRIOR_ART.md` (row Angers–Delampady): "read by the science
  division's referee (SCI-MSG-0033 §3, SCI-RES-0037 §2); not opened here.  The 1981 paper itself has been opened
  by nobody".
* **Numerical check:** `03_scientific_translation/docs/science/INFERENCE_LIMITS_ADDENDA.md` item 88: "[K per them;
  checked here against brute force over the vertices of 168 boxes, `7·10⁻¹⁶`; M for the numbers]".  Implementation
  (not run here): `03_scientific_translation/experiments/science/ensemble_checks/sandwich_class.py`, functions
  `upper_end(psi, u, l)`, `lower_end`, `brute` (vertex enumeration), `hub_polytope`.

### (a2) Sandwich + averaged data: the identified set — science item 89, with R24's corrections  **(closest overlap with S3)**

`03_scientific_translation/docs/science/INFERENCE_LIMITS_ADDENDA.md` §(22), item 89 (label "[P, elementary; exact
checks in `sandwich_class.py synthetic`]"):

> 89. **A sandwich is a first-order class of the Ensemble division's kind, for a "hub"
>     metric — so their Theorem E13 says which ensembles averaged data can pin inside it**
>     [P, elementary; exact checks in `sandwich_class.py synthetic`].  Weights `l ≤ w ≤ u`
>     (`l = e^{−m₊}`, `u = e^{−m₋}`).  (a) With `π = √(lu)` and `d(x, y) = (D(x) + D(y))/2`,
>     `D = m₊ − m₋`, the class `{μ : μ(y)π(x) ≤ e^{d(x,y)}μ(x)π(y)}` is the sandwich.  (b) … (c) *Stability:* with `t*`
>     the upper end for `f`, `μ_f` the threshold member and `γ = min_x |f(x) − t*|`:
>     `TV(μ, μ_f) ≤ (t* − E_μ f)/γ` for every member; for a population
>     `TV(μ, μ_A) ≤ [μ_A(A) − μ(A)]/min(P, 1 − P)`, and the constant is approached (0.97).
>     *Proof:* `Σ w(t* − f) = Σ (w − v)(t* − f) ≥ γ Σ|w − v|` for the threshold weights `v`, and
>     `TV ≤ Σ|w − v|/Σw`.  ∎  (d) *Sandwich plus data:* for members with `E_μΦ = m`, `E_μψ ≤ t`
>     whenever some `λ` has `Σ u(ψ − t − λ·(Φ − m))₊ ≤ Σ l(ψ − t − λ·(Φ − m))₋`, with equality at the
>     best `λ` (linear-programming duality; 30 cases against the programme).  On a band model
>     this needs the law of `ψ − λ·Φ`, a counter per additive statistic — W[1]-hard in their
>     number by the Complexity division's COMPLEXITY-RES-0001.  This is a fourth version of
>     `INFERENCE_LIMITS.md` §8 ("model within a sandwich").  No prior-art search; the class is
>     the density-ratio class of robust Bayesian analysis and (c), (d) are likely in print.

Corrections (same file, item 95, after referee R24; the archive marks item 89(b) "false as printed"):

> *Item 89 (b)* is false as printed: the Ensemble division's E13 (b) ends "and on which the data map is
> injective", which the item dropped.  Counterexample (four states, `l = (0.5, 0.5, 2, 1)`, `u = (1, 1, 3, 2)`,
> `w = (1, 1, 2, 1.5)`, `f = (2, 2, 0, 1)` and the population of the fourth state: two means identify a member
> strictly inside at one state; `ensemble_checks/r24_m2_check.py`).  Replacement: a member is identified iff
> for some `f` its energy is at the floor above the upper end `t*`, at the ceiling below it, **and the data
> determine the weights on the level set `{f = t*}`**; a member strictly inside at every state is not
> identified by fewer than `|X| − 1` independent means.
> *Item 89 (d)*: "W[1]-hard in their number by COMPLEXITY-RES-0001" is withdrawn — that reduction uses a
> threshold function of the vector of statistics; the certificate needs the law of the **one** statistic
> `ψ − λ·Φ`, and rounded up to a grid `ε` one counter gives a sound end within `nε` for any number of data.
> The cost of the exact end is open.  *Item 89 (a), (c)*: the pairwise form is the definition of the
> density-ratio class; the best stability constant is `C*(f) = max_y (1 − μ_f(y))/|f(y) − t*| ≤ 1/γ`.

R24's assumption table (`R24_REPORT.md` §1): "89 (d), equality | the data are attained by a member | essential for
equality, not for soundness | duality"; "89 (d), cost | exactness | replaceable by a quantitative condition: rounding
`ε` costs `nε` in the end and one counter | H4"; "89 (a) | `l > 0` | essential (the pairwise form divides by `l`)".
Item 88's implicit assumption per R24: "in double precision without interval control".

**Note for S3.**  89(d) is stated for exact means `E_μΦ = m` of the normalised member; S3's "observation region"
version is the same LP with the region's support function (cf. (e) E17.2 below).  No statement with a sampled
(compressed) box or a Hausdorff/concentration allowance was found anywhere in the archive.  Infeasibility as a
certificate of inconsistency exists in the model-free setting (ensemble F3 "INFEASIBLE with a Farkas certificate";
E28) but **not found** for the box class with data.

### (a3) The box class around a sampleable known part — theory §11.30, Theorem 11.110 (definitions)

`01_theory/docs/THEORY_REPORT.md` §11.30, *Setting*:

> `X` finite; energy `E = f̂ + r` in units of `k_BT`.  The function `f̂` is *known and
> tractable*: its partition function `Z₀` is known and independent samples from its Gibbs
> measure `π ∝ e^{−f̂}` can be drawn exactly … The
> remainder `r` is evaluated on demand and is known a priori only through pointwise bounds,
>
>     lo(x) ≤ r(x) ≤ hi(x)      (the box class 𝓑;   lo ≡ −ρ₋, hi ≡ ρ₊:  one-sided sup norms).
>
> `Z(r) = Σ_x e^{−f̂(x) − r(x)}`, so `Z(r)/Z₀ = E_π e^{−r}`.  At an instance `r` the *dip weight* of
> a point is `dip(x) = π(x)(e^{−lo(x)} − e^{−r(x)})` and its *bump weight*
> `bump(x) = π(x)(e^{−r(x)} − e^{−hi(x)})`: what the partition sum can gain or lose there.  Their
> totals are `U = (Z(lo) − Z(r))/Z₀` and `V = (Z(r) − Z(hi))/Z₀`.

Theorem 11.110 (status line "[(a) K; (f) K and V (`BennettTwoPoint.lean`, `BoxBennett.lean`); (b), (e) P; (c), (d) V
(`BoxClass.lean`, `BoxAdditions.lean`)]"; quoted in (b), (c) below).  The section's own label: "**Not refereed.**"

### (a4) Ranges of ratios and populations in a box before any evaluation — Corollary 11.114, "The range before any evaluation"

`01_theory/docs/THEORY_REPORT.md`, after Corollary 11.114:

> *The range before any evaluation* (the Scientific Discovery Division, SCI-MSG-0025 §7, its
> addendum A17(13); elementary).  In a box class the ratio itself lies between
> `W_A(hi)/W_B(lo)` and `W_A(lo)/W_B(hi)`, and a population between
> `Z_hi(A)/(Z_hi(A) + Z_lo(Aᶜ))` and `Z_lo(A)/(Z_lo(A) + Z_hi(Aᶜ))` — sharply, by the member that is
> at the floor on one set and at the ceiling on the other; this is the box counterpart of
> the transport range of §11.28, and what the cost of this corollary is the cost of
> narrowing.

### (a5) Envelope classes with the triangle inequality (generalising the density-ratio class) — Theorem 11.105, §11.28

`01_theory/docs/THEORY_REPORT.md` §11.28.  Positioning paragraph: "*For a separable
envelope the theorem is classical:* if `e^{d(x,y)} = U(y)/L(x)` for `x ≠ y` with two positive
functions `L ≤ U` (densities relative to `w`), the class is the **density-ratio class** of
robust Bayesian analysis — all measures between a lower and an upper one, up to a
constant (DeRobertis–Hartigan 1981) — and the programme of Theorem 11.105(a) has the
closed form `R⁺(A,B) = Σ_A wU/Σ_B wL` (`t = U` on `A`, `t = L` on `B`), the textbook range of a
posterior odds … **Theorem 11.105 is the extension from separable envelopes to envelopes with the
triangle inequality**".  Setting: "`R⁺(A, B) := sup{ Z_g(A)/Z_g(B) : g admissible }`" with admissible
"`g(x) − g(y) ≤ d(x,y)`".  Theorem 11.105 "[(c) weak duality, (d) upper bound, (e), and the admissibility in (b): [V]
… the rest P]":

> (a) *Only the constraints from `B` to `A` matter.*
>
>     R⁺(A, B) = max{ Σ_{y∈A} w(y)t(y) / Σ_{z∈B} w(z)t(z) :  t > 0 on A ∪ B,  t(y) ≤ e^{d(z,y)} t(z) for all z ∈ B, y ∈ A }
> …
> (c) *Transport with gains.*
>
>     R⁺(A, B) = min{ λ :  ∃ ψ ≥ 0 on B × A,   Σ_{y∈A} e^{d(z,y)} ψ(z,y) ≤ λ·w(z)  (z ∈ B),   Σ_{z∈B} ψ(z,y) ≥ w(y)  (y ∈ A) }.
>
> … **Every feasible pair `(ψ, λ)` is a certificate: `Z_g(A) ≤ λ·Z_g(B)` for every admissible `g`** (three lines; **[V]**).

Prior art listed in `01_theory/docs/prior_art/L9_review_additions.md` (row DeRobertis–Hartigan; Wasserman 1992;
Geweke–Petrella 1995): "the density-ratio class is the cone of §11.28 for a **separable** envelope … **known special
case** (separable envelopes); the general duality not found in six searches at summary level"; Jewell 1962 (flows
with gains) "**known** as an object"; Chatzikokolakis et al. 2013 "same class, another question".
Limitation (same §): "*Closed is necessary for optimality, not sufficient*" with "not optimal in a large fraction of
random frustrated instances (**[N]**; the division's count: 49, 66 and 81 % at `n = 3, 4, 5`; ours: 17 of 25)".

Also `01_theory/docs/THEORY_REPORT.md` §11.6, Theorem 11.12 [V]: "In the weights `w = e^{−βg}` the class is the
polyhedral cone `w(y) ≤ e^{βd(x,y)} w(x)` (`admissible_iff_weights`), so robust Boltzmann
averages of any observable are linear-fractional programs with optima at polytrope vertices;
the closed form is special to single states (`prior_art/L5`, P5–P6)."

### (a6) Prior-art files (what they say about the box class)

* `01_theory/docs/prior_art/L10_box_classes.md` — prior art for §11.30 (reading level: "three web searches,
  results read as search summaries and abstract-level snippets; no full text was opened").  Rows: Zwanzig 1954,
  Jarzynski 2006, Chatterjee–Diaconis 2018, Dagum–Karp–Luby–Ross 2000 (with the caveat "arXiv:0711.2801 …
  states that the proof of the stopping-rule theorem of Dagum et al. has a significant gap | recorded as a
  caveat; **we do not use that theorem**"), Maurer–Pontil 2009 Thm 4, Hoeffding 1963.  "**What we did not find
  and did not look for properly:** a statement of the *certification* cost for a class of remainders given by
  pointwise bounds — matching upper and lower bounds `Θ((Z(lo)/Z(r) − 1)/ε)` …".  Second addendum (science A3,
  47 sources): adds Georgiev–Lilien–Donald 2008 Prop. 3, Liu–Fisher–Ihler NeurIPS 2015 ("weights bounded by an
  upper-bounding model"; Corollary 3.2 = empirical Bernstein without a hint), Aaronson (randomised certificate
  complexity), Mathé–Novak, Block–Shetty arXiv:2602.23535, Kunsch–Novak–Rudolf 2019, Fan–Grama–Liu, Liao–Berg;
  "Not searched by anyone: the statement for ratios (Corollary 11.114) and the sandwich sampler (Proposition
  11.113) — the latter is importance sampling in proportion to an envelope and is certainly classical in the
  theory of randomised integration; we cite no source for it."
* `01_theory/docs/prior_art/L5_polytropes_interval_uncertainty.md` P5 (Gibbs probability of one state under a
  Lipschitz class): verdict "KNOWN-IN-SPIRIT … the formula itself is a known specialised result in neural-network
  verification (Wei et al. 2023, eq. (5))"; DeRobertis–Hartigan "`[V-abs]` Classes `L <= Q <= U` of unnormalised
  measures; "upper and lower expectations and variances induced by such intervals of measures are obtained"".
  "Wasserman 1992 and DeRobertis-Hartigan 1981 (Project Euclid): abstracts only."
* `01_theory/docs/prior_art/L6_transport_entropy_and_information_limits.md` (T5): "The explicit formula `sup
  Q(A)/Q(X) = U(A)/(U(A) + L(A^c))` is my recollection of that paper `[U]`"; Bailie–Gong 2024 `[V]`: "the odds
  `P(A)/P(B)`, for any `P` in `I(L,U)`, are bounded between `L(A)/U(B)` and `U(A)/L(B)`".  Limits: "the primary
  texts of … DeRobertis-Hartigan 1981 were not reachable".
* `01_theory/docs/prior_art/L9_review_additions.md` — row quoted under (a5).
* Grep for "density ratio"/"DeRobertis" in `03_scientific_translation/docs/science/`: hits in
  `PRIOR_ART_MATRIX.md` (row Theorem 11.105: "for a *separable* envelope the cone is the density-ratio class and the
  value is the classical range of a posterior …"), `INFERENCE_LIMITS_ADDENDA.md` §(22), (24), `R24_REPORT.md`,
  `SM_REPORT.md`, `M_brief.md`, `R15_REPORT.md`, `R3_REPORT.md`, `A3_REPORT.md`.  "box class" in
  `THEORY_REPORT.md`: §11.30 and register rows G35, G36.

---

## (b) Certified reweighting from samples of a reference, with concentration inequalities

### (b1) Theory: Theorem 11.110 (a), (c)–(f) — `01_theory/docs/THEORY_REPORT.md` §11.30

(a) "*What must be certified.*  `ln Z(r) − ln Z₀ = ln E_π e^{−r}`, and

    −E_π r  ≤  ln E_π e^{−r}  ≤  −E_π r + L(w),      L(w) = ln((e^w − 1)/w) − 1 + w/(e^w − 1)  ≤  w²/8,

`w = sup hi − inf lo` the width of the box; `L(w)` is the largest Jensen gap of a random
variable of range `w`, attained by a two-point law (lower end: `jensen_bracket` **[V]**)." … "Hoeffding's bound itself is
sharper when the mean is known … with a floor `b` below and a ceiling `a` above the mean, `w = a + b` and `p = a/w`,
`K ≤ −wp + ln(1 − p + p·e^{w}) ≤ L(w)`".  Attribution: "the right one is Hoeffding's bound on the moment generating
function of a bounded variable (1963, his (4.12)–(4.13)) maximised over the mean, and `e^{L(w)}` is Specht's ratio".

(c) "*A sampling certificate* (`Zw_sub_le_dip`, `Zw_sub_le_bump`, `detect_ge`, `box_spotCheck_correct`) … every member with
`|ln Z′ − ln Z| > η` differs from `r` on a set of probability at least

    p(η) = min{ 1,  ½ · min( (e^η − 1)·Z/(Z(lo) − Z),  (1 − e^{−η})·Z/(Z − Z(hi)) ) }

under the sampler `q = ½·dip/U + ½·bump/V` … The spot check of the hint `r` with `N = ⌈ln(1/δ)/p(ε/2)⌉` independent samples
of `q` is `(ε/2, δ)`-correct for `ln Z` **on every class contained in the box**, with at most `N` evaluations at the hint:

    N  =  ⌈ ln(1/δ) · max( 1,  2(Z(lo)/Z(r) − 1)/(e^{ε/2} − 1),  2(1 − Z(hi)/Z(r))/(1 − e^{−ε/2}) ) ⌉ ."

(d) lower bound for every algorithm: "every randomised algorithm that is `(ε/2, δ)`-correct on the box makes at least
`(1 − 2δ)k` evaluations on `r` in expectation … `k ≥ max( ⌊(Z(lo)/Z(r) − 1)/(2(e^ε − 1))⌋ , ⌊(1 − Z(hi)/Z(r))/(2(1 − e^{−ε}))⌋ )`."

(e) "**the cost of certifying a free energy in a box class, with the instance as a hint, is, up
to a factor that depends on `ε` and `δ` only and an additive constant,

    (Z(lo)/Z(r) − 1)/ε   +   (1 − Z(hi)/Z(r))/ε :**" … explicit constants for `ε ≤ 1`:
"`(1 − 2δ)·((a + b)/(6.9ε) − 1) ≤ cost ≤ ln(1/δ)·(2.7(a + b)/ε + 1) + 1`".

(f) "If under `π` the remainder satisfies `r ≥ E_π r − b` (a one-sided floor `b > 0` below its mean) and `Var_π r ≤ σ²`, then

    0  ≤  K  ≤  W(b, σ²) := ln[ (b² e^{−σ²/b} + σ² e^{b}) / (b² + σ²) ]  ≤  ln(1 + (σ²/b²)(e^{b} − 1 − b))  ≤  (σ²/b²)(e^{b} − 1 − b),

… given a **certified** floor `lo ≤ r` and a **certified** variance bound `σ²`: draw `N` independent samples of `π`, let `r̄` be
the sample mean of the remainder and `η = σ/√(Nδ)`.  With probability at least `1 − δ` (Chebyshev)

    ln Z₀ − r̄ − η   ≤   ln Z   ≤   ln Z₀ − r̄ + η + W(r̄ + η − lo, σ²) :"

sharpened: "`ln Z ≤ ln Z₀ − r̄ + η + W(r̄ − η − lo, σ²)`" when `lo < r̄ − η`.  "A variance *estimated* from the
samples is not such a bound: it misses exactly the rare state that matters."  (f) status: [K] attribution
"confirmed in the scanned original by the science division … machine-checked since the eighteenth checkpoint — by
the science division … `proofs/Frontiers/BennettTwoPoint.lean`".

Hoeffding side ("*Three readings*" (2)): "by Hoeffding's inequality **[K]**, `⌈w² ln(1/δ)/(2ε²)⌉` samples of `r` under `π`
certify `ln Z ≥ ln Z₀ − r̄ − ε` with probability `1 − δ`".  Without a hint (after Proposition 11.112): "the sample mean
of `e^{−r(x_i)}` … with `m = ⌈3 e^{w} ln(2/δ)/(1 − e^{−ε/2})²⌉` samples is `(ε/2, δ)`-correct on the whole box
(multiplicative Chernoff bound …) **[K]** … an empirical Bernstein inequality (Maurer–Pontil 2009, Theorem 4 — **[K]** …)
turns the same samples into a bracket for `E_π e^{−r}` of half-width

    √(2 V̂ ln(4/δ)/m)  +  7 (e^{ρ₋} − e^{−ρ₊}) ln(4/δ) / (3(m − 1)),"

Recorded failures (theory): `01_theory/docs/DEAD_ENDS.md` item "3. **The naive interval is not a certificate**
(harness DEAD.28).  "The sample mean of the Boltzmann factors of the remainder plus two standard errors is an upper
confidence bound for `E_π e^{−r}`": false for every sample size at members of a box class with a rare deep dip — with
a dip of probability `1/m` the sample contains no dip point with probability about `e^{−1} ≈ 0.37`, the sample
variance is then zero and the interval a point below the truth (frequency `0.3705` in the test)."  Theorem
11.110(e) corrected after science SCI-RES-0009 (bump term was missing; `DEAD_ENDS.md` D58 item 1).

### (b2) Science: Proposition A17.7 (Bennett bracket) and its corollary

`03_scientific_translation/docs/science/INFERENCE_LIMITS_ADDENDA.md` A17 (7), "**Proposition A17.7 (Bennett bracket)
[K for the inequality — *A3:* Hoeffding 1963, Theorem 3: inequality (2.8) …; the weaker exponential form (2.9) "is
due to Bennett" (1962, his inequality (8b)) … The sharp form checked on 20 000 random laws: no violation, equality at
the two-point law]**":

> Let `r = g − m`, expectations under `π_m`.  Write
> `ln Z(g) − ln Z(m) = −E r + K`, `K = ln E e^{−(r − E r)} ≥ 0` (the Jensen gap; it is also
> `D_1(π_m‖π_g)`).  If `r ≥ E r − b` (a one-sided floor `b > 0` below the mean) and `Var r ≤ σ²`, then
>
>     0  ≤  K  ≤  W(b, σ²) := ln[ (b² e^{−σ²/b} + σ² e^{b}) / (b² + σ²) ]  ≤  (σ²/b²)(e^{b} − 1 − b),
> …
> **Corollary (a certificate).**  Given a certified floor `lo ≤ r` and a certified variance
> bound `σ²`: draw `N` points from `π_m`, let `r̄` be the mean of `r` on them and
> `η = σ/√(Nδ)`.  With probability at least `1 − δ`,
>
>     ln Z(m) − r̄ − η   ≤   ln Z(g)   ≤   ln Z(m) − r̄ + η + W(r̄ + η − lo, σ²).

Addition (ii): "if `r ≤ E r + a` everywhere, then `K ≥ ln( 1 + Var(r)·(e^{−a} − 1 + a)/a² )`" (Liao–Berg
arXiv:1707.08644 Thm 1).  Novelty: "**Its use as a certificate was not found in the free-energy literature** … "Not
found" is all that is claimed".  Where certified inputs come from: `03_scientific_translation/docs/science/workstreams/P3_REPORT.md` §2.9 "Proposition 6 [P; checked by enumeration] — certified inputs of the floor-plus-variance (Bennett) bracket" (heading only read).

### (b3) Science: "certified reweighting on 74 enumerated instances" — A17 (6)

`INFERENCE_LIMITS_ADDENDA.md` A17 (6) "[M, exact enumeration; added at checkpoint 36]": 45 instances (first batch:
"homopeptides of valine, leucine and serine, 2–12 residues, three fixed backbones … ff14SB vacuum energy `f` as known
part and the GBn2 polarisation energy as remainder, at 300 K"), plus a charged batch; item 7: "with the pairwise fit
`D_2 ≤ 1.3·10⁻³` and `D_∞ ≤ 3.7` in all 74 instances of both batches, charged ones included."  Item 8: "for Lys₄ on
the PPII backbone the remainder beyond the pairwise fit is `14.8 k_BT` wide … and the chi-square divergence of the true
ensemble from the pairwise model is `10⁻⁴` … A certificate through sup-norm constants would charge `e^{15}`; the truth is a
factor `1.0`."  Stated limit: "These divergences were computed by enumerating every state: they are the *prices* that
a certificate would have to pay, not certificates."

### (b4) Coverage of error bars — A17 (11) (benchmark B10 baseline)

`INFERENCE_LIMITS_ADDENDA.md` A17 (11) "[M, exact laws; added at checkpoint 41]": 45 product-domain instances × 3
surrogates = 135 rows; "400 repetitions per row; `N = 200, 2 000, 20 000` exact samples; `δ = 0.05`"; brackets **naive**
(`μ̂ ± 2` s.e.), **EB** ("the empirical-Bernstein bracket for `e^{−(r − lo)} ∈ [0, 1]` with the *true* floor `lo`"),
**H3** ("Hoeffding's Theorem 3 and the *true* floor and variance"), **H3-sampled** ("the sampled minimum and the
sampled variance").  Results:

> 16. … For the 117 rows with `D_2 < 1` the two-sigma
>     bar covers the truth in 92–100 % of the repetitions (it is a 95 % bar).  In the 15
>     rows with `D_2` between `3.1` and `45` — serine with the vacuum force field as the model —
>     it covers in 7–82 % at 2 000 samples, and in the two worst rows … **in 5–17 % of the repetitions at every sample size tried, missing
>     by 3–6 nats** …
> 17. **The certified brackets never failed** (smallest coverage `0.995` and `0.978` over all
>     rows and sample sizes, for a nominal `0.95`) — and where the divergence is large they
>     are honest by being useless: the empirical-Bernstein bracket has no lower end, the
>     Hoeffding bracket is 12–53 nats wide.
> …
> 19. **A sampled floor and variance fail exactly where they are needed** (last column):
>     in the seven worst rows the "bracket" built from the sample's own minimum and
>     variance covers the truth in 22–79 % of the repetitions at 200 samples.

Stated limit: "The floor and the variance given to EB and H3 are the exact ones — this measures what the brackets
deliver *if* those inputs are certified … Exact sampling from enumerated laws; neutral side chains; least-squares
surrogates only."

### (b5) The consolidation row "A guaranteed bracket for a reweighting / free-energy-perturbation estimate"

`03_scientific_translation/docs/collaboration/consolidation/science.md` §D, row 1, verbatim: "**1. A guaranteed
bracket for a reweighting / free-energy-perturbation estimate** (one-sided floor + variance; Hoeffding's Theorem 3,
Bennett) as a replacement for a standard error where a floor is known | yes (known inequalities) | scripts
(`pi_inference/`, `ws_P3`) | yes: 45–74 enumerated rotamer instances, coverage never below 0.978 against 5–82 % for
standard errors when the model is poor | **no** — no molecular-dynamics data, no explicit solvent | none".  Text after
the table: "it needs no new mathematics … the missing piece is a floor for a realistic model".  §C: "**Rediscoveries**
… The cost table of certified reweighting (Block and Shetty 2026) and its bracket (Hoeffding 1963) — sent to the
theory division as "our extension" before the search returned"; negative result: "A pointwise floor costs
`e^{floor}/ε`; no polynomial moment of the remainder suffices."

### (b6) Other recorded failures for (b)
* Proposition 11.113(c′): "For Bernoulli variables the one-sided bound is checked exactly, and it fails without its last term (harness XXIV.11)."
* `L10_box_classes.md`: Dagum–Karp–Luby–Ross stopping-rule proof gap (not used).
* `P3_REPORT.md` §2.7: samples "produced by inverse-CDF backward sampling from double-precision conditional tables with numpy's PCG64 generator: "exact samples" means exact up to that arithmetic (total-variation error of order `n·2⁻⁵²` per sample [H])".

---

## (c) Theory: share certificates, sandwiches, envelope sampler (`01_theory/docs/THEORY_REPORT.md`)

Note: §11.6 holds Theorems 11.12–11.15 (finite temperature); Theorems 11.16–11.18f are in §11.7; 11.110–11.114 in §11.30; 11.115 in §11.31.

**Theorem 11.18 (order `m`) [V] (`HigherOrderEnvelope.lean`; harness XI.10).**  "If all mixed differences of order `m`
over a set `T` of sites are bounded by `c_T` (`HigherDiffBound`), then the anchored interpolant `I_{m−1} g` of order
`m−1` (… which uses `g` on the Hamming ball of radius `m−1` and is exact there …) satisfies `|g(x) − I_{m−1}g(x)| ≤
Σ_{T ⊆ changed sites, |T| = m} c_T` (`higherOrder_remainder`), and for nonnegative constants the bound is attained at
every configuration by a member of the class with the same ball data.  (Machine-checked for zero ball data … for
`m ≥ 3` with arbitrary data it is **[P]** …)".  Prior art: "Kuo–Sloan–Wasilkowski–Woźniakowski 2010; Griebel–Holtz
2010; its use as a certified residual class with an exact reduction to a kernel was not found (`prior_art/L5`, P9)".
*Certified:* a pointwise sandwich of the energy from ball evaluations.  *Cost:* evaluations on the Hamming ball of
radius `m−1`.  *Residual class:* bounded order-`m` mixed differences `c_T`.

**Theorem 11.18a (third-order classes reduce to pairwise lower models) [V; (d) P]** — "(a) `I₂g` is a pairwise function …
(b) Let site penalties `γ_i` and pair penalties `γ_ij` *cover the triples*: `Σ_{T ⊆ S, |T| = 3} c_T ≤ Σ_{i∈S} γ_i +
Σ_{i<j∈S} γ_ij` for every set `S` of sites.  Then for every configuration `x`
`E₀(x) + g(x) ≥ E₀(x) + I₂g(x) − Σ_{i changed} γ_i − Σ_{i<j both changed} γ_ij` (`thirdOrder_pairwise_lower`) … a certificate of it
accepted by the tropical kernel bounds the true energy (`verify_sound_thirdOrder`).  (c) Two coverings.  The **site
form** `γ_i = ⅓Σ_{T∋i}c_T` … and the **pair form** `γ_ij = ⅓Σ_{T⊇{i,j}}c_T` … The pair form is the tighter one … (d) **[P]**
Neither is the exact envelope."  Cost: `1 + Σ_i(k_i − 1) + Σ_{i<j}(k_i − 1)(k_j − 1)` evaluations.  Limitation: "What is
missing for a guarantee is unchanged: an a-priori bound on `c_T`, obtained without enumerating the domain."  Measured
constants are "**not certified constants**".

**Proposition 11.18b (share certificates: the row-sum condition completed) [(a) V; (b) P from K; (c) V for the covering,
P for the rest; (d) V; (e) V for soundness, P for the duality; N for the frequencies; M for the division's instances]**.
"(a) *Soundness* **[V]**.  Let the known part be additive.  If every pair constant can be split between its two sites,
`c_ij ≤ s_ij + s_ji` with shares `s ≥ 0`, so that every site carries at most its excitation energy, `Σ_{j≠i} s_ij ≤ Δ_i`,
then `x₀` minimises `E₀ + g′` for every residual `g′` of the class … (b) *Completeness* **[P from K]** … no set `S` of sites
is *over-dense*, `Σ_{i<j∈S} c_ij ≤ Σ_{i∈S} Δ_i` … **iff shares as in (a) exist** … **the exact second-order sharp-minimum
condition is decided by one maximum flow and has a certificate of `n(n−1)` numbers that is checked by additions** …
(d) *A pairwise known part* **[V]** … With the *deficits* `w_ij := max_{a ≠ x₀_i, b ≠ x₀_j}[c_ij − T_ij(a, b)]₊`, shares of the
`w_ij` with loads at most `Δ_i` are sufficient … Computing the deficits costs `O(n²k²)` operations and no evaluation of
the residual beyond the star.  (e) *Shares that depend on the state* … `s_ij(a) + s_ji(b) ≥ c_ij − T_ij(a, b)`, `Σ_{j≠i}
s_ij(a) ≤ A_i(a)` … **Such shares exist iff `x₀` is an optimal solution of the pairwise linear relaxation** … they fail
exactly where the relaxation has an integrality gap at `x₀`."  Prior art: max-flow min-cut, Hakimi, Goldberg/Picard
("cited from memory"); Schlesinger's dual ("**known** … cited from memory by both divisions, no source opened").
*Certified:* that the anchor `x₀` is a minimiser for every residual in the second-order class (zero temperature).
Limitation: fails on domains with exclusions (Proposition 11.18c(a)); "an accepted certificate is the output of a
compiled checker with `verify_sound` as its specification, not a kernel theorem (§12, item 7)".

**Proposition 11.18c (domains with pairwise exclusions) [P; N, harness XI.18]**: "(a) *On a reset-closed domain the
bounds and the sufficient conditions survive; the completeness of shares does not.* … (The Lean statements are for
full products; this extension is on paper.)  **The completeness part (b) of Proposition 11.18b fails on `D`** — *found
by the Scientific Discovery Division, SCI-REV-0012 §3*".

**Theorem 11.18d (the remainder of the anchored expansion as an identity; anchored constants; shares of every level)
[V]**: "(a) *Identity* (`anchored_remainder_identity`).  For every function `g`, reference, `y` and order `m ≥ 0`:
`g(y) − I_{m−1}g(y) = Σ_{T ⊆ S, |T| = m} Δ_T g(z_T(y); y_T)` … (a′) *Any down-closed family of evaluated subsets* … (a″) *Every
term in its own order* … **`m` hosts cannot be replaced by `m + 1`**".  Attribution: science workstreams P3, P5, P6.

**Proposition 11.18e (the Hamming ball is necessary for a deterministic certificate) [P; the core of (b) V; (b′)(ii) C]**:
"(a) Every deterministic algorithm, adaptive or not, that returns a finite lower bound for `min(E₀ + g)` or a bracket of
finite width for `ln Z`, valid for every `g ∈ 𝒢`, evaluates `g` at no fewer than `N_ball` configurations — on every input
… (b) *Randomised algorithms without a hint: what is asked decides* (**corrected** …) The first version claimed the count
of (a) for randomised algorithms as well … **For the task of (a) that is false.** … finite, valid with probability `1 − δ`
on every member, from at most `⌈k^{m−1} ln(1/δ)⌉` evaluations **whatever the number of sites**."

**Proposition 11.18f (which shares: the allocation for a law) [P; harness XI.23]**: "the two ends of the bracket of
`ln Z` are `ln Z(A) + U(λ)` and `ln Z(A) − L(λ)`, `U(λ) = ln E_P e^{pen_λ(S)}`, `L(λ) = −ln E_P e^{−pen_λ(S)}`.  (a) *The cost
depends on the changed set only.*  The cost number of Theorem 11.110(e) at the model is `E_P e^{pen(S)} − 1` … in a nearly
frozen ensemble … the cost is of order `p^k` … (b) *The upper end is convex and the lower end concave* in `λ` … **the
minimum of `L` is attained at a vertex — at an ordering vertex**".  "elementary convexity, nothing claimed new".

**Theorem 11.110** — quoted in (b1).  *Certified:* `ln Z` within `ε/2` w.p. `1 − δ` on every member of the box (c);
deterministic bracket from evaluations (b); cost lower bound for every algorithm (d), (e).  *Cost:* `(Z(lo)/Z(r) −
1)/ε + (1 − Z(hi)/Z(r))/ε` with a hint.  *Class:* pointwise box `lo ≤ r ≤ hi` around an exactly sampleable known part.

**Corollary 11.111 (a sup-norm bound caps the cost of every class) [P from V]**: "At a hint `r ∈ 𝒞_ρ` the spot check
with the mixture of the sampler of Theorem 11.110(c) and any sampler that is valid for `𝒞` … is correct on `𝒞_ρ` with at
most twice the smaller of the two sample sizes."

**Proposition 11.113 (a sandwich of two sampleable models: sample where the bracket is wide) [P; harness XXIV.10]**
("elementary — importance sampling in proportion to an envelope, which is the classical optimal design for
integrating a function known only through pointwise bounds; no novelty claimed"):

> Let `m₋ ≤ E ≤ m₊` pointwise, with both `Z(m₋)` and `Z(m₊)`
> known and the Gibbs measure of `m₋` sampleable.  Put
>
>     q(x) ∝ e^{−m₋(x)} − e^{−m₊(x)},        W(x) = (e^{−E(x)} − e^{−m₊(x)}) / (e^{−m₋(x)} − e^{−m₊(x)}) ∈ [0, 1].
>
> (a) `Z(E) = Z(m₊) + (Z(m₋) − Z(m₊))·E_q W` exactly.
> (b) `q` is the law of an accepted draw when `x ∼ π_{m₋}` is accepted with probability
> `1 − e^{−(m₊(x) − m₋(x))}`; the acceptance rate is `1 − Z(m₊)/Z(m₋)`.  Only accepted draws are
> evaluated.
> (c) Hence `N` evaluations at independent samples of `q`, with sample mean `Ŵ`, give with
> probability at least `1 − δ` (Hoeffding, for a variable in `[0, 1]`)
>
>     | Z(E) − Z(m₊) − (Z(m₋) − Z(m₊))·Ŵ |   ≤   (Z(m₋) − Z(m₊))·√(ln(2/δ)/(2N)) :
> …
> (c′) *Variance-sensitive form* **[K]** (Maurer and Pontil 2009 … Theorem 4 …):
>
>     | E_q W − Ŵ |   ≤   √(2 V_N ln(4/δ)/N)  +  7 ln(4/δ)/(3(N − 1))          with probability at least 1 − δ.
> …
> (d) … `N_KL ≈ ln(2/δ)·(e^{Δ} − 1)²/(2 e^{Δ} ε²) = 2 ln(2/δ)·sinh²(Δ/2)/ε²` evaluations … and this order, `sinh²(Δ/2)/ε²`, is
> necessary in the worst case over the box `{m₋ ≤ E ≤ m₊}` **[P]** (a two-point argument …) … "Fine-grained" is … `Σ_x q(x)² ≪ ε²/sinh²(Δ/2)`

Remark in (c): "an error of at most `e` in every evaluated energy is harmless … with evaluated energies `Ẽ` the estimator
is unbiased for `Z(Ẽ)`, and `|ln Z(Ẽ) − ln Z(E)| ≤ e`."  Science's run (not re-run by theory): "on enumerated instances
the truth was inside the bracket in 1 460 of 1 460 repetitions."  *For S3:* this is S3's sampler, for the scalar
`Σ w` only (not for the moment vector, not for a ratio with data).

**Proposition 11.113a (nested sandwiches: the inner bracket at the price of free rejections) [P; harness XXIV.12]**:
"Let `m₋ ≤ e₋ ≤ E ≤ e₊ ≤ m₊` pointwise, where `Z(m₋)`, `Z(m₊)` are known and the Gibbs measure of `m₋` can be sampled … while
`e₋`, `e₊` can be computed at any given state without an evaluation of `E` but have no computable partition functions …
`β = (e^{−e₊} − e^{−m₊})/(e^{−m₋} − e^{−m₊})`, `ρ = (e^{−e₋} − e^{−e₊})/(e^{−m₋} − e^{−m₊})`, `W_in = (e^{−E} − e^{−e₊})/(e^{−e₋} − e^{−e₊})`.
(a) … `W = β + ρ·W_in` … (c) … with probability at least `1 − δ`,
`| Z(E) − Z(m₊) − A·(β̄ + ρ̄·W̄_in) | ≤ A·( t_f + ρ̄·t )`, `t_f = √(ln(6/δ)/(2N_f))`, `t = √(ln(6/δ)/(2N))` … The bound is not
proved if proposals are drawn *until* `N` have been accepted … nor for a stopping rule that looks at the running bracket.
(d) **In evaluations the price is that of the inner sandwich.**"  "elementary, nothing claimed new".

**Proposition 11.113b (one side at a time) [(a) V — science's `SandwichCost.lean`; (b), (c) P]**: "(b) *A floor and its sampler
certify both sides, at the price of the floor's own excess.* … `ln Z(m₋) + ln(W̄ − t) ≤ ln Z(E) ≤ ln Z(m₋) + ln(W̄ + t)`,
`t = √( ln(2/δ) / (2N) )` … (c) *A ceiling and its sampler certify the lower side only.* … **no algorithm certifies a finite
upper bound of `ln Z` on the class `{E′ ≤ m₊}` with fewer than `(1 − δ)·|X|` evaluations in expectation**".

**Corollary 11.114 (a ratio of two macrostate weights in a box class) [(a)–(c) V; (d) P] (`BoxRatio.lean`, `BoxAdditions.lean`)**:
"(a) … A member of the box whose `ln(W_A/W_B)` differs from that of `r` by more than `η > 0` differs from `r` on a set of
probability at least `½·min(p_A(η), p_B(η))` under the mixture of the two macrostates' samplers … (d) … **the cost of
certifying a free-energy difference between two macrostates in a box class is, up to a factor depending on `δ` only and
an additive constant, `max_{M∈{A,B}} [ (W_M(lo)/W_M(r) − 1)/ε + (1 − W_M(hi)/W_M(r))/ε ]`** … (1) The cost does not depend on
the weights of the macrostates … provided `π` can be sampled *conditionally* on it … (2) Nothing cancels … (3) If `A` and
`B` partition the domain, the ratio costs at least as much as `ln Z` … and can cost arbitrarily more".  *For S3:* the
only theorem in the archive on a ratio `Σ_A w / Σ_B w` in a box class with sampling; `E_w[f]` for general `f` is not
covered.

**Proposition 11.112 (the floor is the end `p = ∞` of a family) [P]** — Rényi/KL balls; attributed to Block–Shetty (2026)
and Kunsch–Novak–Rudolf (2019) (heading and attribution only read).

**Theorem 11.115 (barrier and trap certificates) [V] (`KineticsCertificates.lean` — the division's;
`BarrierCertificate.lean` — ours)**: "(a) *Cuts* … If every move that leaves a set `S ∋ a`, `S ∌ b` lands on energy at
least `L`, every walk from `a` to `b` visits energy at least `L` … (c) *Tree cuts* … with residual leaves, of true energy
at least `L` for every residual of the class … (f) *Traps* … For every stochastic kernel that is stationary for weights `w`
— no reversibility — the probability of not having left a basin `A` after `T` steps, started from `w` restricted to `A`,
is at least `1 − T·U/Lo` whenever `U` bounds the weight of the wall from above and `Lo` the weight of the basin from
below".  "**Not refereed.**"  Not relevant to S3 beyond kinetics.

Proposition numbers 11.113/11.113a: exist as quoted.  No "envelope sampler" under that exact name: the "sampler that
pays for the envelope" is Proposition 11.113a (science A17 (17) title).

---

## (d) Science: "certified many-body thermodynamic brackets" = consolidation §B1

`03_scientific_translation/docs/collaboration/consolidation/science.md` §B1 "Certified two-sided free-energy brackets
for a force field with a many-body solvent term, and a checkable certificate":

> * **Contribution.**  For `E = f + g` on a product of rotamer states — `f` the pairwise vacuum part of Amber
>   ff14SB, `g` the GBn2 polarisation energy, which is not pairwise — evaluate `g` on a Hamming ball about an
>   anchor state, bound the remainder of the anchored expansion term by term *for every order* with interval
>   enclosures of the derivatives of the Born-radius rescaling and kernel, sum those bounds over all `m`-subsets in
>   closed form, and assemble a floor `m₋ ≤ E` and a ceiling `m₊ ≥ E` that are banded pairwise models, so that
>   `ln Z(m₊) ≤ ln Z(E) ≤ ln Z(m₋)` by transfer matrix, with no sampling. … Results: Ace-(Val)₂₀-NMe, `3.5·10⁹` states, `[518.2552, 518.2715]`; Ace-(Leu)₃₀-NMe,
>   `[866.910485, 866.921008]` (0.0105 nats); Ace-(Lys)₂₀-NMe on a helix, `5.5·10¹⁷` states,
>   `[800.5150660, 800.5154710]`; Ace-(Lys)₁₂-NMe `[517.1284375, 517.1286523]`.

Status: "Paper proofs with stated floating-point allowances … **Unrefereed: parts (13)–(18) … and parts (23)–(24)** …
Nothing else is machine-checked."  Assumptions: "an evaluation tolerance of `10⁻⁷` kcal/mol per energy value (measured
`1.8·10⁻¹²`, not proved); `mpmath` interval arithmetic; and, for a Stage 1 file, three data assumptions (G1)–(G3) that
are **not checked**".  Prior art: K\*/BBK\*/MARK\*, LUTE, Rahman 2014 ("All at abstract level").  "Evidence against.
Every ingredient is standard … the remainder inequality with class constants is the theory division's Theorem 11.18".

Main statement — `03_scientific_translation/docs/science/workstreams/P3_REPORT.md` §2.5, "**Theorem 5 [P; checked by
enumeration at every state of every enumerated instance] — a certified floor and ceiling that are banded pairwise
functions**": recipe (tables; anchor; constant `Γ_m` or site penalties `γ_i`; "*Evaluations*: `g` on the Hamming ball of
radius `m − 1` about `x⁰`, `N_ball = Σ_{j<m} C(n,j)(k−1)^j`"; models `m_∓`), then "*Claim: `m₋(x) ≤ E(x) ≤ m₊(x)` for every
`x ∈ X`; both are pairwise with pairs of separation at most `w`.*" … "6. *Exact partition functions and sampling.*
Eliminating the sites in order with a message over the next `w` sites gives `ln Z(m_∓)` in `O(n k^{w+1})` operations, the
maximum of `m₊ − m₋` (max-plus), and exact independent samples of `π_{m₋}` by backward sampling.  **Consequences.**  (a)
*Deterministic bracket:* `ln Z(m₊) ≤ ln Z(E) ≤ ln Z(m₋)` … (c) *Sampling:* `ln Z(E) = ln Z(m₋) + ln 𝔼_{π_{m₋}} W`, `W :=
e^{−β(E − m₋)} ∈ [e^{−βρ_cert}, 1]`".  Checks: "160 enumerated runs, 5 512 504 state checks, **no violation**".  §2.6:
"transfer matrix | double precision log-sum-exp | relative error of `Z` `≲ 10⁻¹²` … [H: not budgeted formally …]".
§2.7 Lemma R [P] (sample-range bound): "With probability `≥ 1 − δ`: `m_N − (m_N − w_min) ε_N ≤ μ ≤ M_N + (1 − M_N) ε_N`".
§2.8 negative statements N1 ("Analysis alone … certifies third-order constants that are 33–1 400 times the measured
ones"), N2 ("On the helix the recipe fails at every affordable order").  §2.10: "anything about a real peptide in
water | **not claimed**".

Certified populations: `INFERENCE_LIMITS_ADDENDA.md` A17 (13) "What a certified sandwich gives beyond `ln Z`: certified
populations [P, elementary …]" (heading read) and item 88's table (exact range of the mean number of displaced side
chains over the sandwich, e.g. "Val₂₀/PPII, order 5 … **[3.534, 3.550]**").

Certificate format: `03_scientific_translation/docs/science/SANDWICH_CERTIFICATE_FORMAT.md` §1: "**Statement certified by
an accepted file, under the data assumptions (G1)–(G3) of §2:** `m_lower(x) ≤ E(x) ≤ m_upper(x)` at every state x, and
hence `claim.lnZ_lower ≤ ln Z(m_upper) ≤ ln Z(E) ≤ ln Z(m_lower) ≤ claim.lnZ_upper`".  §7, two files in
`03_scientific_translation/experiments/science/sandwich_cert/certs/`: "`sandwich_V6_E_m4_w5.json` (11 kB) | Ace-(Val)₆-NMe,
strand backbone | 6, `3⁶ = 729` | 4, 5 (all pairs) | `198.067925225 ≤ ln Z(E) ≤ 198.068095790`" and
"`sandwich_V20_P2_m5_w8.json` (80 kB) | Ace-(Val)₂₀-NMe, polyproline II | 20, `3²⁰ ≈ 3.5·10⁹` | 5, 8 | `518.255189142 ≤ ln Z(E)
≤ 518.271429999`"; 19+ mutated test vectors in `…/sandwich_cert/vectors/`.  **These two files are banded integer
models `m_lower`, `m_upper` — i.e. a certified weight box `l = e^{−β m_upper}`, `u = e^{−β m_lower}` — usable directly as
S3 test instances (V6 enumerable; V20 samplable exactly by transfer matrix).**

---

## (e) Ensemble division: partial identification

**Definitions** — `04_ensemble_identifiability/docs/ensemble/ENSEMBLE_REPORT.md` §1: "`X` is a compact metric space (often
finite) of configurations, `P(X)` its Borel probability measures (*ensembles*).  `Φ = (φ_1, …, φ_m) : X → ℝ^m` is a
continuous family of observables and `Aν = ∫ Φ dν ∈ ℝ^m` the *data* of `ν`.  The *moment body* is `𝒦 = A(P(X)) = conv
Φ(X)`, compact and convex. … `μ` is **identified** (by `Φ`) if `Aν = Aμ` implies `ν = μ` for every `ν ∈ P(X)`".
Identified interval (E30): "Let `I_A(τ)` be the set of values of `E_νψ` over the ensembles `ν` on `A` with `‖E_νΦ − y‖ ≤ τ`."

**LP/duality certificate** — `SOFTWARE_INTERFACE.md` F3 "(Theorems E2(a), E17(a), §2.2, §4b) — **R3**": "`sup{E_ν ψ : ‖Aν − y‖ ≤
τ} = min_λ { τ‖λ‖_* + λ·y + max_x (ψ − λ·Φ)(x) }`, and symmetrically for the infimum.  *Evidence.*  [P] (linear-programming
duality) … Check T2/F5: duality gap at most `10⁻¹⁴` on 600 instances.  *Input.*  `Φ`, `y`, `τ`, `ψ`.  *Output.*  `INTERVAL [lo,
hi]` with `λ_hi`, `λ_lo`; or `INFEASIBLE` with a Farkas certificate — the data are not within `τ` of the means of **any**
ensemble on `X`, which is a certified statement of model misspecification.  *Checking.*  For each end evaluate `ψ − λ·Φ` at
all `M` configurations: `O(mM)`. … *Trap.*  The interval is for the stated `X`.  It is a worst case over all ensembles, not
a confidence interval".  F6 (inside a first-order/density-ratio class, Theorem E13) "— **R2**": "bounds on means have exact
flow certificates … LP of size `M²` unless the envelope has structure … For a box of weights `l ≤ w ≤ u` … a member is
identified iff, for some `f` in the span, its weights are at the ceiling where `f` exceeds its upper end `t*`, at the floor
below it, and the data determine its weights on the level set `{f = t*}` … (An earlier, stronger sentence — "only
bang-bang members are pinned" — was withdrawn by that division; do not implement it.)"

**Theorem E17 (modulus = dual certificate = estimator)** (`ENSEMBLE_REPORT.md` §4b; register label "P" for (a), "P
(elementary)" for (b,c); novelty "formulation (known technique)"): "Let `𝒫 ⊆ P(X)` be convex and compact … data … `y = Aμ +
σξ` … `R_𝒫(f) = sup_{𝒫} E f − inf_{𝒫} E f` … `ω(ε) = sup{ T(μ₁) − T(μ₀) : μ₀, μ₁ ∈ 𝒫, ‖A(μ₁ − μ₀)‖₂ ≤ ε }`.
(a) `ω(ε) = min_{λ∈ℝ^m} { ε‖λ‖₂ + R_𝒫(ψ − λ·Φ) }` for `ε > 0`.  (b) … The affine estimator `T̂ = λ·y + c` has `sup_{μ∈𝒫} E(T̂ −
T(μ))² ≤ σ²‖λ‖² + R_𝒫(ψ − λ·Φ)²/4 ≤ ω(2σ)²/4`.  (c) Every estimator has `sup_{μ∈𝒫} E(T̂ − T(μ))² ≥ κ·ω(2σ)²/4`, where `κ = E
sech²(1 + Z) = 0.4496`".  Prior art: "**[K]** (Donoho 1994, known to us through P. B. Stark's lecture notes … the
original not read)".  Reading: "The multiplier `λ` of the dual problem is three things at once: the certificate of the
identified interval at tolerance `ε` (its second term is a range of `ψ − λ·Φ` over the class, which is what the kernels
bound: a maximum and a minimum over `X` for the model-free class, two flows with gains for an envelope class, two tilted
partition functions for a divergence ball)".  *For S3:* with `𝒫` = the normalised box class, `R_𝒫(ψ − λ·Φ)` is two
threshold-rule evaluations (a1).

**Proposition E17.2 (error sets that are not boxes) [P, immediate; unreviewed]**: "Let the data satisfy `y − E_μΦ ∈ 𝓔` for a
closed convex set `𝓔 ⊂ ℝ^m` … (a) *Bounds.*  If `a + λ·Φ ≥ ψ` on `X`, then `E_νψ ≤ a + λ·y + σ_𝓔(−λ)` for every ensemble `ν`
compatible with the data; for finite `X` the best such bound is the exact upper end of the range of `E_νψ` (and likewise
below).  (b) *Certificates.*  If `f = c + λ·Φ ≥ 0` has zero set `S ⊇ supp μ` and `f ≥ γ` off `S`, every ensemble `ν` compatible
with the same data has `ν(X ∖ S) ≤ w_𝓔(λ)/γ` … (c) *Cases.*  A box … An ellipsoid … `σ(λ) = ρ‖Σ^{1/2}λ‖₂` … A systematic error
… **the certificate must be orthogonal to every systematic direction**".  Register: "read by nobody but their author".
*For S3:* this is the observation-region version of the dual (for the model-free class; for the box class replace
`max_x (ψ − λΦ)` by the box's support function).

**Proposition E23 (ratios of means … are linear)**: "(a) *Ratios.*  Let `ψ > 0` on `X`.  For every ensemble, `E_μφ/E_μψ ∈ [y
− τ, y + τ]` iff `E_μ(φ − (y + τ)ψ) ≤ 0 ≤ E_μ(φ − (y − τ)ψ)` … (c) *A ratio as target.*  The range of `E_να/E_νβ` (`β > 0`) over
a set of ensembles given by linear constraints is the value of one linear programme (the Charnes–Cooper
transformation, **[K]**)."  Proof remark: "put `w = cν`: the constraints are linear in the positive measure `w` … a target
`E_νψ = Σwψ/Σw` is linear-fractional."  *For S3:* normalised moments `Σwφ/Σw ∈ region` are linear constraints on `w`.

**Proposition E23.1 (several unknown gains and offsets) [P; sufficiency by `eq_of_exposing_certificate`]**: "the
compatible set is convex; determined ⇔ Theorem E1(a) for the features projected off the offset spaces and off the
direction of each group's data; every gain and every offset direction removes one dimension of the certificate space;
with tolerances the constraints are linear in `(ν, 1/gain, offset/gain)` (d)" (register row; "read by nobody but
their author").

**Proposition E28 (an incomplete library is a tolerance; the data bound the missing weight from below) [P,
elementary]**: "(a) … its conditional ensemble `μ_lib = μ(· | X_lib)` has `‖E_{μ_lib}Φ − y‖ ≤ τ + εD` … (b) *Falsification,
with a certificate.*  If `λ·y − ‖λ‖_* τ > h_lib(λ)` for some `λ`, no ensemble on the library is compatible with the data, and
every ensemble `μ` on `X` that is compatible has `μ(X ∖ X_lib) ≥ ( λ·y − ‖λ‖_* τ − h_lib(λ) ) / ( H(λ) − h_lib(λ) )` … (d) No
upper bound on the missing weight follows from the data".  Register: "elementary; unreviewed".  *For S3:* the
"compressed" (sampled) support is an incomplete library; E28 is the model-free analogue of S3's infeasibility certificate.

**Proposition E30 (verdicts do not survive a refinement of the pool; intervals and mass bounds do, at an enlarged
tolerance) [P, elementary]**: "Let `X` be a compact metric space, `Φ` an `L`-Lipschitz map … `X_h ⊂ X` an `h`-net … (a) `I_{X_h}(τ)
⊆ I_X(τ) ⊆ I_{X_h}(τ + Lh) + [−L_ψ h, L_ψ h]` … (c) The verdict "identified" has no such stability: an ensemble identified among
the ensembles on a pool need not be identified among those on a finer pool (Proposition E20c: the verdict can change
under an arbitrarily small displacement; `DEAD_ENDS.md` ED24: a product grid reports identification where there is
none)."  Measured looseness: "in check R3, where `Lh` is between 5 and 40 times `τ`, it is 34 times as wide as the exact
interval (median)."  *For S3:* E30(a) is the deterministic (net) analogue of S3's Hausdorff allowance; E30(c) is the
negative result on refinement.

**`SOFTWARE_INTERFACE.md`** sections: 0 readiness levels; 1 F1–F6 (finite exact layer; F3 = partial identification R3);
2 P0–P2 (product spaces); 3 L1–L2 (laws); 4 T1–T2 (tori); 5 H1 (thermal union bound); 5a N1–N7 (non-mean data, all R1);
6–9 (algorithms, observation models, proof obligations, locations).

**Frozen controls** — `04_ensemble_identifiability/experiments/ensemble/benchmarks/controls_v1.json` (46 kB) and
`docs/ensemble/BENCHMARK_CONTROLS.md`.  Schema (read with a JSON parser): top-level keys `version` (=1), `generated_by`
(`experiments/ensemble/benchmark_controls.py`), `conventions` ("numbers in quotes are exact rationals; unquoted numbers
are decimal approximations"), `controls` (list of **25** instances).  Each instance has keys `id`, `family`, `title`,
`space`, `question`, `expected`, `why`, `source`, and, as applicable, `observables`, `data`, `ensemble`, `tolerance`
(B5-03), `model` (B6-01), `noise` (B7-01).  `space` = `{"type": "finite"|"continuous", "description": …, "states": [list
of labels]}` (states listed explicitly only for some); `observables` = `{"names": […], "table": [[one row per observable,
one exact-rational string per state]]}` (table omitted when shared with an earlier instance); `data` = list of rational
strings (or a dict); `ensemble` = `{"support": [...], "weights": [...]}`.  Ground truth is in `expected`: `verdict` ∈
{`IDENTIFIED`, `NOT IDENTIFIED`, `INTERVAL`, `NO`, `BOUND …`, `LIBRARY_FALSIFIED`, …} with `certificate` (`c`, `lambda`,
`gamma`, `lambda_l1_norm`), `twin`, `interval` (pair of rational strings), `dual certificates`, `closed form`, `stability`.
Example B5-01: space `{±1}³` (8 states), observables `x1,x2,x3`, data `["1/5","1/2","-3/10"]`, question "range of
E[x1*x2]", expected `{"verdict":"INTERVAL","interval":["-3/10","7/10"], "dual certificates": {"upper": "x1*x2 <= 1 + x1 -
x2 on the cube, …", "lower": …}, "closed form": "[|m1 + m2| - 1, 1 - |m1 - m2|]"}`; B5-02 population of `+++`: `["0","7/20"]`;
B5-03 with `"tolerance": {"norm": "max", "tau": "1/20"}`: `["-2/5","4/5"]`.  Pool sizes where `states` are listed: B1-01 8,
B1-02 32, B2-01 4, B2-02 3, B2-03 16, B5-01 8, B7-01 2, B8-01 3, B8-02 4, B8-03 4, B9-01 4, B9-03 4; B4-01 128 (described,
not listed); B3-01 360 (described); B2-04…B2-08 continuous.  Exact identified intervals stored: B5-01/02/03 only (plus
B9-02 missing-weight bound "at least 1/2").  The doc says all 38 claims are verified "in exact rational arithmetic" by
the generator.
`torus_instances_v1.json` (20 kB): keys `version`, `generated_by` (`experiments/ensemble/export_torus_instances.py`),
`conventions`, `six_states_three_angles` (2 instances: `states_t` = 6 triples of rational tangent half-angles, `claim` =
{`lifts_independent`, `rank_of_the_twelve_tangential_conditions`: 12, `dimension_of_span_functions_vanishing_on_the_curve`:
15, `verdict`: "NOT IDENTIFIED (Theorem E20b)"}), `thirteen_states_four_angles` (10 instances: `seed`, `states_phi` = 13
quadruples of decimal-string radians, `claim` = {`functions_of_the_data_span_on_the_curve`, `rank_of_the_26_conditions`,
`candidates`, `verdict`, `dual_margin`}).  Doc: "These verdicts are numerical, and an independent re-implementation has
been asked of the engineering division (ENSEMBLE-REQ-0001)."  None of these instances has a box class or energy
envelope; usable for S3 only as model-free (`l = 0`, `u = ∞`) controls.

---

## (f) Geometry division: stress and reconstruction certificates

`05_geometric_inference/docs/geometry/ENSEMBLE_RIGIDITY.md` §1: "An ensemble is a Borel probability measure `μ` on `𝒞`
… Its **mean squared-distance matrix** is `M(μ)_ij = ∫ |x_i − x_j|² dμ(x)`.  For a configuration `X`, `D(X)_ij = |x_i −
x_j|²`, so `M(δ_X) = D(X)` and `M(μ) = ∫ D dμ`.  The set of all realizable averaged data is `𝒦 = { M(μ) } = conv D(𝒞)`, a
compact convex set." (`𝒞 = { x ∈ (ℝ^d)^n : |x_i − x_j| = ℓ_ij for all ij ∈ E₀ }`, compact modulo translations.)

**Theorem F (stress certificate) [P; core V: `MetricChain.Geometry.stress_certificate`]** (§7.1): "Let `μ = Σ w_k δ_{X_k}`
satisfy (CC), with stacked configuration `z`, and let `F` be a set of pairs such that the vectors `(D(X_k)_ij)_{ij ∈ F}`, `k =
1..K`, are affinely independent.  Suppose there is a symmetric matrix `Ω` with `Ω ⪰ 0, Ω𝟙 = 0, Ω_ij = 0 unless i = j or ij ∈
F ∪ E₀, ker Ω = span(𝟙, columns of z)`.  Then `μ` is identifiable from the averaged squared distances on `F`."  Proof
identity: "`tr(XᵀΩX) = −½ Σ_{i≠j} Ω_ij |x_i − x_j|²`".  "`(Ω, rank of the conic system)` is an independently checkable
certificate: one `LDLᵀ` factorisation and two ranks in exact arithmetic."  Prior art: "For `K = 1` this is the classical
sufficient condition for universal rigidity … Connelly".

**Theorem G (global quantitative rigidity of ensembles) [P]** (§7.2): "Let `Π^⊥` be the orthogonal projection of `ℝ^n` onto
the orthogonal complement of `span(𝟙, columns of z)` and `φ(X) = ‖Π^⊥ X‖_F² = −½ ⟨Π^⊥, D(X)⟩`.  Then (a) `φ ≥ 0` on all
configurations, and on `𝒞` it vanishes exactly on the classes `[X_k]`; (b) `κ := inf_{X ∈ 𝒞} φ(X)/min_k d_P(X, X_k)² > 0`;
(c) for every ensemble `ν` on `𝒞`: `∫ min_k d_P(X, X_k)² dν ≤ (√(n − 1 − dK) / (2κ)) · ‖M(ν) − M(μ)‖_F`; (d) there is a
constant `C_μ` with `W₂([ν], [μ])² ≤ C_μ ‖M(ν) − M(μ)‖_F` …; (e) the exponent cannot be improved".  Limitation (science
consolidation §C): "The Geometry division's stability theorem gives error bars smaller than the object only for distance
errors below `4·10⁻³` to `10⁻⁶` Å".  Geometry consolidation: "No statement about any measured quantity: the observable is
measured by no instrument (labelled scattering gives block sums; FRET, DEER, NOE and PRE data are not averaged squared
distances)".

**Bounded configuration functions usable as φ or f:** `D(X)_ij` (bounded on `𝒞`, which is compact modulo translations);
any linear functional `⟨Ω, D(X)⟩`, e.g. the stress energy `tr(XᵀΩX) = −½ΣΩ_ij D(X)_ij`; `φ(X) = ‖Π^⊥X‖²_F = −½⟨Π^⊥, D(X)⟩`
(Theorem G; vanishes exactly on the states); `min_k d_P(X, X_k)²` (a target bounded through `φ`).  All are means-linear,
so they fit S3's `v(x)`.

**Benchmark suite** — `05_geometric_inference/experiments/geometry/benchmark_suite/` (23 instance files A1–A4, B1–B3,
C1–C6, E1–E2, F1a, F1b, F2, F3, G1–G4, plus `MANIFEST.json` with id, category, title, SHA-256).  `docs/geometry/BENCHMARKS.md`:
"Format of an instance: `chain` (bond length, bond angle, the statewise constraints), `data` (what a tool receives),
`truth` (states, weights), `label`, `expected_behaviour_of_a_correct_tool`, `evidence_for_label`, `reference`, and, where the
label is "not determined", `second_solution`."  A1 keys (read): `category, chain, data, evidence_for_label,
expected_behaviour_of_a_correct_tool, id, label, n_points, n_states, reference, title, truth`; `data.kind` =
"ensemble-averaged squared distances, all pairs, exact", `data.matrix` = floats; `label` = `{"globally_identifiable":
true, "linear_certificate": true, "recoverable_by_linear_algebra": true}`; `evidence_for_label` "P for this instance
(Theorem B with the certificate computed here in floating point …)".  Six classes: uniquely reconstructible; non-unique;
locally only; no efficient certificate; ill-conditioned; violating assumptions.  Not box-class instances.

---

## (g) Complexity division: tractability and impossibility

Register `06_biological_complexity/docs/complexity/THEOREMS.md`:

* **CX-T4** [P]: "`#SSEL` is #P-hard in the same models; the partition function of the `j`-fold magnified model, `j ≤
  poly(N)` part of the input (equivalently the temperature, for a temperature-independent model), is #P-hard by a
  one-call reduction (exact oracle)"; review REV-0001/-0003 correct; "fixed-temperature hardness remains open (A3′)".
* **CX-T12** [P] (exact PF algorithm, multi-strand NN model): "`O(L_0^4 Σ_{d} Π_i C(n_i/d+2,2))` arithmetic operations:
  `O(N^4 3^c)` for distinct strands, polynomial for a bounded number of species"; prior art Boehmer et al. 2025 for the
  base-pair model.
* **CX-T30** [P] (level counts): "For loop energies in `εℤ`: with weights `2^{−K g/ε}`, `K = ⌈N log₂ 24⌉ + 1`, the sums …
  have as base-`2^K` digits the numbers `N_R(m)` of pairs with symmetry exactly `R` and energy `mε` … Same operation count
  as CX-T12, numbers of `O(N·E_max/ε)` bits."  (A density-of-states extraction by one big-integer PF evaluation.)
* **CX-T22** [P]: "**The threshold is a max-flow.** `λ_0 = min_S Σ_{i∈S} ln(1/q_i) / Σ_{U⊆S} max γ_U` is a project-selection
  problem (polynomial for every hypergraph); the exact extremal ratio with state-dependent tables is NP-hard on general
  hypergraphs (MAX-CUT) and polynomial on bands".
* **CX-T23** [P] (thresholded sum): "**Has a floor left its reference?** Deciding `max_x[b(x) + ln π_0(x)] ≥ 0` for
  non-negative tables on `m`-subsets is NP-hard for every fixed `m ≥ 2` … by reductions from MAX-CUT; polynomial for two
  states with a product known part, for windowed tables, for product pair tables with a product known part …, and —
  with a margin `ε` — for exponentially decaying tables".
* **CX-T32** [K for hardness; P for the bijection]: "**Chains: optimising pair data is the Heisenberg ground-state
  problem; hardness.** … strongly NP-hard … Realizability of a complete table of averaged squared distances by an
  ensemble of freely jointed chains is NP-hard in the weak sense under Turing reductions — for an accuracy given in
  binary".
* **CX-T33** [P]: "If the data have range `w` along the chain: exact in `O(n·w·2^w)` for collinear chains, additive error
  `ε·Σ|Q|` in `O(n·w·(πw/ε)^{w−1})` for fixed-angle chains (dynamic programming over torsions); no `2^{o(w)}·poly(n)` exact
  algorithm under ETH".
* **CX-T35** [K in substance; P as written; **unreviewed**] (certified second-order bounds on a tree-decomposable
  reference): "`ln⟨e^{−βV}⟩_0 ≤ −β⟨V⟩_0 + (β²/8)Σ_t R_t²` with `R_t` the range of the `t`-th martingale increment, and `R_t ≤
  Σ_e Γ_{t,e} o_e` with `Γ_{t,e}` total-variation distances between conditional laws of the reference, computable (or
  boundable) by elimination; a column form and a variance (Bennett) form."
* **CX-T36** [P given K; **unreviewed**]: "Unless NP = co-NP there are no polynomial-size certificates of upper bounds on
  `ln Z` within `δ·β·Σ_e o_e` (a constant `δ > 0`) for all instances with trivial reference, binary sites, equal
  antiferromagnetic pairs on a graph of bounded degree and `βJ` a fixed constant".
* **CX-T14, CX-T29** (ETH lower bounds; span problem NP-complete / co-NP-complete) — not S3-relevant except as format.
* **COMPLEXITY-RES-0001** (`06_biological_complexity/docs/collaboration/responses/complexity/COMPLEXITY-RES-0001.md`),
  [P, two lines, given K]: "Deciding whether `Z ≥ 1/2` is W[1]-hard parameterised by `r`, already for `f ≡ 0` (band width
  0), `k = r` states per site, `a_i(x_i) = s_i·e_{x_i}` … and a threshold function `φ` … Consequently no algorithm computes
  `Z`, or approximates it within a factor 2, in time `g(r)·poly(n, R)` unless FPT = W[1] … The exponent `r` of your
  transfer-matrix bound is necessary up to the logarithm."  Limitation: "This is a statement about worst-case instances
  with an adversarial `φ`."  (Its use against item 89(d) was withdrawn by science, see (a2).)
* **Cost of sampling:** no complexity-division statement on sampling cost was found beyond CX-T35/36; the sampling
  cost results are theory's Theorem 11.110(d)–(e), 11.113(d), 11.113b(c), Proposition 11.18e (see (b), (c)).  Exact
  sampling for chain/bounded-width models: `P3_REPORT.md` Theorem 5 item 6 ("`O(n k^{w+1})` … exact independent
  samples of `π_{m₋}` by backward sampling").

---

## (h) Structural biology: certified ln Z and populations (C2)

Modules (`07_structural_biology/src/metricchain_sb/`): `model.py` (`class PairModel`: "Pairwise model with exact dyadic
tables (integers in units of ``2**-scale_bits``)", fields `unary: list`, `pair: dict`, `scale_bits: int = 0`, `meta: dict`;
`from_float(cls, unary, pair, scale_bits=20, meta=None)`; `energy_int`, `energy`, `brute_force_energies`,
`brute_force_min`), `modelio.py` (`save_model(model, path)`, `load_model(path)`: "a :class:`PairModel` stored as a
compressed numpy archive"), `partition.py` (producer; "**Untrusted code.**"), `zcert.py` (format), `zcheck.py` (checker),
`itables.py` (`IntervalTable`, `ExactTables`, `FloatTables`), `expo.py` (`exp_bounds_me(q: Fraction, bits=80)`,
`exp_bounds`, `log_bounds(z: Fraction, bits=40)`), `synthetic.py` (`random_pair_model(seed, n, kmax, density=1.0,
scale_bits=0, amplitude=12, kmin=1)`, `random_contact_model(seed, n, kmax, scale_bits=10, …)`).

Signatures (verbatim):
* `def certify_partition(model: PairModel, beta: Fraction, domains=None, keep=None, tau=None, theta=None, max_entries:
  int = 5_000_000, arithmetic: str = "exact", exp_bits: int = 64, max_leaves: int = 1) -> ZCertificate:` — "A checked
  certificate for `ln Z` over the box (and, with `keep`, for the populations of that site)".
* `def weighted_model(model: PairModel, weights, beta: Fraction) -> PairModel:` — "The model whose partition function is
  `sum_x prod_i w_i(x_i) exp(-beta E(x))`".
* `def check_partition_certificate(cert: ZCertificate, arithmetic: str = "exact", max_entries: int | None = 5_000_000,
  exp_bits: int = 64) -> ZResult:`
* `class ZCertificate`: `model: PairModel`, `beta: Fraction`, `domains: list`, `steps: list`, `order: list`, `keep: int | None`,
  `claim: dict`, `meta: dict`, `branch: int | None`, `children: dict | None`; `dumps(cert) -> str`, `loads(text, model) -> ZCertificate`.
* Returned interval object `ZResult`: `accepted: bool`, `reason`, `ln_z_lo: Fraction | None`, `ln_z_hi: Fraction | None`,
  `slack_lo`, `slack_hi`, `full_box`, `keep`, `populations: dict` ("state -> (lo, hi) for the final domain of `keep`"),
  `removed_upper: Fraction | None`, `stats`; method `population(state)`.  Population rule (zcheck docstring): "`P(x_t = a) >=
  low_a / Z_hi` … `P(x_t = a) <= 1 - sum_{b != a} [lower bound of P(x_t = b)]`".  Claims stored outward-rounded to a `2**-20`
  nats grid (`outward_claim`).

Status (consolidation `07_structural_biology/docs/collaboration/consolidation/structural-biology.md` §B1): "Rule semantics
machine-checked (ours, B3; not reviewed by the theory division) … 40 000 adversarial certificates × 2 tiers without a
miss.  One author wrote producer and checker; no independent implementation (requested: STRUCTBIO-REQ-0004)" (engineering's
X-018 later wrote one; see Part 3).  Assumptions: "The integer tables are the model; rational `β`; float tier: IEEE-754
round-to-nearest products and sums in NumPy (F1–F3, stated and tested, not proved)."  Realistic result: "one structure
(crambin, 26 residues): `ln Z_w ∈ [−71.1574, −71.1499]` in 65 s; 26 population certificates in 13 min."  Limitations: "Ends
near crambin … Population intervals have one width for all states (a tighter ratio bound is known, not implemented).
No baseline has been run."  Negative result 6: "**C2 does not scale past crambin** under this model".  Engineering's X-018:
"**F1: the float tier at `exp_bits` 990–991 accepts an interval 0.31 nats off**".

Stored tables/results usable as test instances:
* `07_structural_biology/experiments/structbio/lnz_dev/results.jsonl` (47 rows, 60 kB; SB-X-004): keys `arithmetic,
  beta_per_kcal, commit, exact_pairs, experiment, full_box, largest_table, ln_z_hi, ln_z_hi_float, ln_z_lo, ln_z_lo_float,
  max_entries, minus_beta_E_min, model_sha256, outcome, pdb_id, prunes, relaxed_pairs, seconds, split, step_slack_nats,
  tau_kcal, theta_kcal, width_nats` (+ `kind: population`, `model: v2-lib` rows); `ln_z_lo/hi` as exact rationals (very long
  strings).  Table R-11 in `docs/structural_biology/RESULTS.md` (crambin, v2-lib: widths 12.1364 → 0.0590 nats).
* `gmec_dev/certs/v2/*.mincert.json`, `v2-lib/` (min-certificates for 1BPI, 1CRN, 1PGA, 2IGD, 5PTI; the 1UBQ files are
  "left out by reference" — 10.0 MB and 15.9 MB, retrievable at the pinned commit per `07_structural_biology/00_DIVISION_INDEX.md`).
* PDB inputs `benchmarks/structbio/pdb/{1CRN,1L2Y,1UBQ,2IGD,1PGA,5PTI,1BPI}.pdb` with `MANIFEST.json`.
* Other result rows: `regime_dev` (18), `gmec_synth` (21), `seed_dev` (66; plus `seed_dev/1CRN_entry_spread.npz`),
  `wellgaps_dev` (1 212), `flipgaps_dev` (264), `nullmethod_dev` (12).
* **The integer `PairModel` instance files (.npz) themselves were not found in the archive** (only checksums
  `model_sha256` in result rows); they are regenerable from the PDB files by the division's pipeline (not run).
  Synthetic instances are reproducible from `synthetic.py` seeds.  Enumerable instances with certified populations:
  the synthetic ones of `test_zcert.py`/X-018 (3 000 enumerable instances in `02_engineering/experiments/eng/sb_zcheck/results/`,
  not opened); crambin is not enumerable.

---

# Part 2 — referee R29 (`03_scientific_translation/docs/science/workstreams/R29_REPORT.md`; message SCI-REV-0030)

Object of the review: Theorem 11.58e of the theory division (export `07cde81`), its certified tops (Z_ADDENDUM A6b,
tables of 11.58e(f)), and the script `z6_certified_tops.py`.  The certified tops are the constants `c_j` (`c_j/a` =
0.500410…, 0.363300…, 0.31279…, 0.29137…, 0.28132… at `u = 1`, j = 2…6).  So "(i) the constants" and "11.58e(f)" overlap:
I classify a concern as (i) when it bears on the computed `c_j` values or their certification, (ii) when it bears on the
statement/proof of 11.58e or its other numbers (τ₂, τ₃, closed forms), (iii) otherwise.

Every concern about a numerical certificate, verbatim:

| # | location | verbatim | severity (referee's) | concerns |
|---|---|---|---|---|
| F1 | R29 §2 F1; SCI-REV-0030 §2 | "**F1 (major — evidence, not numbers).  The script's verdict cannot fail for the errors it is meant to exclude.** `z6_certified_tops.py` lines 320–323: `mono` is true by construction (`next_top` returns `≤ V.c`), `above` compares with a floating `h`. … Mutation study (§3): of 30 mutations, 2 are caught by the script …; 17 break a certificate and still end with "ALL CHECKS PASS" — among them every flipped rounding direction, and **M18 (the two divergences swapped), which prints `c₂ = 0.055481623494 < τ₂ = 0.055517524915` and `c₃/a = 0.360741 < τ₃/a = 0.361184` as "certified"** … So the validity of the tables rests on the code path, not on a check; my independent checker shows that code path is right on the committed runs." | major | (i) — the evidence for the `c_j` (the "ALL CHECKS PASS" line also ends `out_z6_certified_u1_J400.txt`) |
| F2 | §2 F2 | "**F2 (minor).  A13 does not literally cover the cap line.** … The cap line (script lines 257–269) is below the maximum of *two* such lines that meet at the tangent vertex, below neither alone" | minor | (i)/(ii): wording of Proposition A13, on which the validity of the certified lines rests; numbers unaffected |
| F3 | §2 F3 | "**F3 (minor).  Base case and start of the certified sequence.**  A6b line 281 cites "Lemma A1 and Proposition A8", but A8 is for the envelope sequence from `b₀ = a`; the script starts at `c₀ = ā = up(a) > a`, and 11.58e(d) asks for `b₀ ≤ a`." | minor | (i) (justification of the certified sequence) and (ii) (hypothesis of 11.58e(d)) |
| F4 | §2 F4 | "**F4 (minor).  Printed certified numbers are rounded to nearest.**  Script line 318 (`"%.12f"`, `"%.9f"`); the ratio is rounded up as a double (line 308) and then printed to nearest.  All entries of the committed tables stay above the true envelope tops (smallest margin I computed: `2.7·10⁻⁸` of `b_j − h`, against `5·10⁻¹³` of print rounding), so no number is wrong.  *Replacement*: print with a ceiling at the last digit." | minor | (i) |
| F5 | §2 F5 | "**F5 (minor; false as stated for large slopes).** … `τ₂ = min_x a·max(a, x + θ(x))/(a + x)`, and the minimum is at `x*` iff `θ′(x*) ≥ −x*/(a + x*)`.  That holds at `u = ½, 1, 2` (verified with rigorous intervals) and **fails for `u > u₀ = 4.6535196185`** … `τ₂ = b₂` is not affected." (SCI-REV-0030 heads it "F5 (false as stated for large slopes)") | minor (report); "F1 and F5 concern published statements" (message header) | (ii) |
| F6 | §2 F6 | "**F6 (minor; numbers).**  Z_ADDENDUM table after line 235 and `out_z7_exactness_u1.txt`: `τ₃ = 0.361189·a`.  Mine: … `0.361183773·a` … and an upper bound that does not depend on any minimisation being converged, `0.361184025·a`.  Their minimiser of `R[θ]` (a zooming grid) stalls" | minor | (ii) (τ₃ is the exact value, not a certified top; c₃ unaffected) |
| F7 | §2 F7 | "**F7 (minor; status of a claim).**  "From the third level on the recursion is strictly better": a floating-point computation whose errors have no common direction in their script … Still [N]; an interval proof is within reach, not done." | minor | (ii) |
| o1–o4 | §2 "Observations (no change needed)" | "(o1) mpmath's `float(mpf)` truncates, so `up()` returns the least double above the interval end (margins `0.00` ulp); valid in every sign case. … (o3) The four `nextafter` steps on the stored lines cover at most three relative rounding errors: least margins observed `2.20` ulp (slope), `1.83` ulp (beta) over 278 704 lines.  (o4) A cap line with nonpositive slope would be dropped silently by `_hull` (cannot occur: `m ≥ 1/c`)." | "no change needed" | (i) |
| verdict line | §0 | "the code `z6_certified_tops.py` | **sound** on those runs, **with restrictions**: (i) its own final verdict "ALL CHECKS PASS" certifies nothing … (ii) printed decimals are rounded to nearest, not upwards (F4); (iii) other slopes, tiny `K`, the 400-level run not verified by me" | — | (i) |

What R29 established positively for (i): "the three committed runs (`u = 1`: 80 levels; `u = 2, ½`: 40 levels; `K = 3000`)
are **reproduced digit for digit and verified by an independent exact checker: 0 violations** — rigorous upper bounds of
`τ_j` *given* Lemma A1, Corollary A4, Proposition A8 (re-derived).  The 400-level run (`K = 4000`): **NOT FINISHED**".

**Consequence for the constants used by engineering (derived here by reading, not computed):** engineering's comment in
`02_engineering/experiments/eng/twolevel/make_tables_x011.py` cites "`out_z6_certified_u1_J400.txt`" — the `K = 4000`,
400-level run — which is exactly the run R29 did **not** verify.  The file's own values (read here) are `c_j/a` =
0.500410019, 0.363300651, 0.312791457, 0.291376730, 0.281323057 (j = 2…6); the verified `K = 3000` file
`out_z6_certified_u1.txt` has 0.500410024, 0.363300653, 0.312791462, 0.291376787, 0.281323250.  Engineering quotes
`C_UP = {1: 0.5004, 2: 0.3633, 3: 0.3128, 4: 0.2914, 5: 0.2813}` "quoted to four decimals" with `C_UP_ROUNDING = 0.00005`
— rounded to nearest, so 0.5004, 0.3633 and 0.2813 lie **below** the certified upper bounds, and 0.5004 lies below R29's
replicated exact value "`τ₂ = 0.500410018113·a`".  As quoted, three of the five numbers are therefore not upper bounds of
`τ_j` (by ≤ 2.3·10⁻⁵); engineering's script carries the ±0.00005 only in one share computation (line 312).  R29 itself
does not mention engineering.

**What R29 left unfinished** (R29 §6, SCI-REV-0030 §3): the 400-level run (`K = 4000`) — "chunk support written,
**untested**"; Item 5 (the nest) — "nothing run"; Item 6 numbers (size paragraph) — "`r29_i6_crossover.py` … written, never
run"; my tops at `u = 2, ½` — not run; "Odd inputs (`u = 0.3`, `8`; `K < 10`), mutations at other slopes: not run"; §5
comparison with the theory division's three reviews — "**NOT FINISHED**", "was **not opened** (not even listed)"; parts
(b)–(d) of 11.58e — "**not re-derived** (rest on Q2's Lemma U and Proposition T, taken as given)"; "`τ_j` for `j ≥ 4`
(compared with envelope tops only)"; harness XVI.11 "not assessed".  Coordinator's note: "**Checked by me: nothing.**"

---

# Part 3 — certified computation versus evaluation of cost formulas (engineering X-001 … X-019)

Sources: `02_engineering/docs/engineering/EXPERIMENT_REGISTER.md` (the register; X-007 and X-005b/c, X-006b, X-016
continued are separate entries), `02_engineering/docs/engineering/benchmarks/BENCHMARK_RESULTS.md`,
`02_engineering/docs/collaboration/consolidation/engineering.md`.  Kinds: K, C, L, S, F, N, E as defined in the task.
Where an entry has several parts, all kinds are listed, main first.

| exp. | result (short) | kind | register's own words that justify it |
|---|---|---|---|
| X-001 | theory audit replicated: `AUDIT PASSED` at four heads | K (Lean kernel build of the theory proof library; not an instance certificate) + harness tests | "`scripts/audit_all.sh --full`; `experiments/falsify_conjectures.py` …"; "the audit script's self-test (planted violations must be detected) ran and passed" |
| X-002 | lattice chains to 24 torsions: class tables, exact covers, entropy brackets | E (enumeration) + N (LP optima "proved optimal by HiGHS") | "Random seeds | none (exhaustive, deterministic)"; correction: "What holds: proved optimal by HiGHS; 254 of the 263 optima certified independently of any solver by the Scientific Discovery Division" |
| X-003 | exact fractional hitting numbers on the uniform cube | E (exact closed form via a theorem, brute-force validated) | "closed form via Harper's theorem"; "brute force over all `2^{2ⁿ} − 2` proper nonempty subsets for `n = 2, 3, 4`" |
| X-004 | off-lattice chain covers to 12 torsions | E in floating point / N | "classes = sorted truncated squared distances rounded to 8 decimals; cover relation with tolerance `10⁻⁹`; HiGHS"; BENCHMARK_RESULTS: "in floating point … on hold beyond 12 torsions (exact arithmetic first)" |
| X-005 | Algorithm 2L⁺: worst instances, all claims of Thm 11.56 | S | title "(mean runs)"; "differential evolution over 19 instance parameters"; outputs `x005_cost.jsonl` |
| X-005b | non-product instances, classification rule, convergence | S | "Limitation stated up front | uniform inner behaviours … ball level sets; expectation level" |
| X-005c | worst product instance re-examined after R18 | S | "**The search is not converged to the review's `10⁻⁴·na`** after three rounds" |
| X-006 | literal runs with real fluctuations (superseded) | L (oracle inner brackets) | "Limitation stated up front | inner procedures are oracles: the event (V1) … is true by construction and is **not** tested"; "**Superseded by X-006b**" |
| X-006b | 585 000 literal runs, exact sampler; invalid behaviour as control | L | "the 585 cases of X-006 unchanged …"; "oracle inner brackets, so the event (V1) is not tested" |
| X-007 | distance entropy of profile classes; single-flip constants | E | "enumeration of the generic chain by `generic_chain.enumerate_generic`" |
| X-008 | smallest sensitive balls on type classes, `n ≤ 10 000` | E (floating) with exact re-check for `n ≤ 400` | "for `n ≤ 400` (18 cases) the optimum recomputed with exact integer weights and a 60-digit comparison selects the same ball" |
| X-009 | `C_max` of Thm 11.56 vs non-adaptive lower bound: crossover sizes | **F** | "Independent recomputation of the Scientific Discovery Division's table"; "Theorem 11.56 **[P]**, Theorem 11.45(b) **[V given two finite sums]**"; "local, three seconds" |
| X-010 | three nested levels: flat instance and worst outer landscape | S (+F for the middle level's cost bound) | "**no fibre landscape is searched** … represented by the middle level's cost bound (not a certified bound: it is itself searched over outer landscapes)" |
| X-011 | (a) certified bound to six levels; (b) mean-run on searched instances; (f) literal nested runs at 15 sites | **F** (a) + S (b), (c), (e) + L (f) | "costs on instances are in the mean-run model (literal nested runs only at 15 sites); searched worst cases are lower bounds"; consolidation B2: "The certified bounds are computed in floating point from the theorem's formulas, not interval arithmetic." |
| X-012 | exact checker for "shares at the leaves" certificates | C | "a compiled exact checker"; "nine files accepted by both engines with matching checksums"; "tested, not verified" |
| X-013 | exact vertex enumeration of weighted cubes | E (+ interval arithmetic) | "everything else is exact enumeration and interval arithmetic"; "four enumeration methods and … the Parma Polyhedra Library" |
| X-014 | (a) bounds on 75 mixtures of two site types; (b) literal runs on 11–16 sites | **F** (a) + L (b) | "Parts | (a) bounds on 75 mixtures …; (b) literal runs"; "the certified status of (a) is conditional on a proof transfer by one author …; bounds, not runs" |
| X-015 | false certificate under unbounded influence, third implementation | L | "our literal simulator of X-014"; "an invalid bracket in 360 of 360 runs"; "one instance" |
| X-016 | review of structbio `min` certificates and producer (two commits) | C (independent checker) + L (producer vs enumeration/DP) | "an independent checker with a strict loader written from the format description"; "22 472 claims, three checkers, enumeration"; "all six stored certificates accepted by our checker" |
| X-017 | theory's machine-checked kernel executed on six structbio certificates | K | "does the verified function `verify` itself (not a Python mirror of it) accept the six stored certificates"; "Limitation | an execution by Lean's interpreter, not a proof term"; `verifyM` "**proved equal to `verify`**" |
| X-018 | independent checker of C2 partition-function certificates | C | "a checker written from the docstrings and frozen before the implementation was read; differential testing on enumerable instances against a truth in ball arithmetic"; "the checker (982 lines) is unread by the coordinator" |
| X-019 | certified global maximum on the 4-torus; certified 4-D realisation | C (rigorous ball arithmetic; no independent checker of a certificate file) | "Arb ball arithmetic (python-flint): branch and bound …, Krawczyk"; "the coordinator re-ran tests and drivers and did not read the trusted core" |

**Counts (22 distinct experiments; the two X-016 entries counted once; main kind):** K 2 (X-001, X-017); C 4 (X-012,
X-016, X-018, X-019); L 3 (X-006, X-006b, X-015); S 4 (X-005, X-005b, X-005c, X-010); F 3 (X-009, X-011, X-014); N 0 as
main kind (secondary in X-002, X-004, X-008); E 6 (X-002, X-003, X-004, X-007, X-008, X-013).  2+4+3+4+3+0+6 = 22.
Secondary kinds: X-010 +F; X-011 +S +L; X-014 +L; X-016 +L.  Note: X-001's K is a build of a proof library, not a
certificate about a concrete instance; strictly by the task's definition only X-017 is K.

**Places where engineering uses "certified" for something of kind F or S (flagged):**
1. X-009 title: "from which size on is two-level adaptivity **certified** to win?" — F (formula comparison).
2. X-011 title "designed by **certified** cost"; BENCHMARK_RESULTS "the **certified** recursion to six levels"; "best
   **certified** bounds found `0.4221`, `0.3754`, `0.3688` … every one from a search that ran into its time limit" — F
   (floating-point formula evaluation, minimised over a searched design family); consolidation B2: "A **certified**
   recursion for nested runs" while also stating "computed in floating point from the theorem's formulas, not interval
   arithmetic".
3. BENCHMARK_RESULTS / consolidation: "no searched cost above a **certified** bound" — compares S with F.
4. X-010 / BENCHMARK_RESULTS: "charged its **certified** bound it gains nothing" — F; the register itself says the
   middle level's bound is "not a certified bound".
5. X-014 / BENCHMARK_RESULTS "**certified** bounds on 75 mixtures"; consolidation B5 "a **certified** algorithm with
   finite-size constants for cubes whose sites have different slopes" — F, conditional on an unrefereed proof transfer
   (register: "the certified status of (a) is conditional on a proof transfer by one author").
6. `make_tables_x011.py` comment "`C_UP[k]` is the theory division's **certified** upper bound" with values rounded to
   nearest (see Part 2: three of five lie below the certified value) — quotation of an interval computation, but as
   quoted not an upper bound.
7. X-002 BENCHMARK_RESULTS "15 of 25 open brackets **certified** at both ends" — kind not determinable from the files
   read (HiGHS-based optima; the register's correction withdrew "two solvers agree").
8. X-006b BENCHMARK_RESULTS "cost ≤ `C_max` in every run" (L, not called certified) — no flag.
