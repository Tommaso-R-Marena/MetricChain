# Software interface — which results of the Ensemble division are computationally effective

*For the Structural & Computational Biology, Software Development and Applications
Division (branch `research/structural-biology`), for the engineering division, which
reviews and benchmarks implementations, and for the science division, which evaluates
assumptions.  Written at the request of the research owner's supplementary directive of
2026-11-26.  Statements and proofs are in `ENSEMBLE_REPORT.md` (section numbers below);
the state of every statement is in `THEOREM_REGISTER.md`.  This file says what each result
means as a computation: inputs, outputs, cost, what must be checked, when a tool must
abstain, and how ready it is.*

**Nothing here is a statement about a molecule or an instrument.**  Every result is about
a probability measure `μ` (an *ensemble*) on a stated configuration space `X`, seen through
means of stated functions `φ_i` on `X` (*observables*), `y_i = ∫ φ_i dμ + ε_i`.  Whether a
measured quantity *is* such a mean of a known function is a modelling assumption that this
division does not assess (§6).

## 0. Readiness levels, and the verdicts a sound tool may give

| level | meaning |
|---|---|
| **R3** | May be implemented as a guarantee.  The theorem has been examined by at least one review other than its author (an internal AI review or another division — not academic peer review), the algorithm is exact on finite data, the output carries a certificate that a separate program can check, and the core inequality is machine-checked where a declaration is named |
| **R2** | May be implemented as a computation whose output states the caveat given in its card (a paper proof that is reviewed but not machine-checked; a solver tolerance; a verification step that is exponential and must be allowed to abstain) |
| **R1** | **Do not implement as a guarantee yet.**  Unreviewed, or true but without the stability modulus that would let it reach noisy data |
| **R0** | Conjectures and numerical thresholds.  Never a guarantee; useful only as hypotheses for benchmarks |

A sound tool returns one of four verdicts, never a bare number:

* `IDENTIFIED` with a certificate (§1) that another program can check;
* `NOT IDENTIFIED` with a *twin*: a second ensemble, given explicitly, with the same data;
* `INTERVAL [lo, hi]` for a stated quantity, with one dual certificate for each end (§1, F3)
  — the normal answer when identification fails;
* `ABSTAIN` with the reason (a margin below the arithmetic's resolution; a verification
  that would need more than the allowed enumeration; a hypothesis that cannot be checked).

"Identified" always means: *among all ensembles on the stated space `X`*, unless a class is
named.  The answer can change when `X` changes — adding one configuration to `X` can turn
`IDENTIFIED` into `NOT IDENTIFIED`.  A tool must therefore record `X` with its verdict.

## 1. Finite, enumerable configuration spaces — the exact layer

`X` has `M` configurations that can be listed; `Φ` is the `m × M` table of observables; `A` maps
an ensemble to its `m` means.  Everything in this section is linear programming plus a
check that needs no solver.  This is the layer that is ready.

### F1 — Is this ensemble determined by these means?  (Theorem E1(a), §2.1) — **R3**

*Statement.*  An ensemble with support `S` is determined by the means of `Φ` among all
ensembles on `X` **iff** (i) the vectors `(1, Φ(x))`, `x ∈ S`, are linearly independent and
(ii) some `f = c + λ·Φ` is non-negative on `X` with zero set exactly `S`.  The answer depends
on `S` only, not on the weights.

*Evidence.*  [P], examined by the internal review ER1; sufficiency is [V]:
`MetricChain.Ensemble.eq_of_exposing_certificate` (witness
`MetricChain.NonVacuity.ensemble_exposing_certificate_witness`).  Check T1: two independent
linear-programming tests agree on 1 500 random instances.

*Input.*  `Φ` (exact rationals if possible), the support `S`.
*Output.*  `IDENTIFIED` with `(c, λ, γ, σ)`: `f = 0` on `S`, `f ≥ γ > 0` off `S`, and `σ > 0` the
conditioning of `(1, Φ)` on `S` (F2); or `NOT IDENTIFIED` with a twin; or `ABSTAIN`.
*Algorithm.*  One linear programme — maximise `t` subject to `c + λ·Φ(x) = 0` (`x ∈ S`),
`c + λ·Φ(y) ≥ t` (`y ∉ S`), `|λ_i| ≤ 1` — and a rank computation on `S`.  If `t* = 0`, the dual
solution is a signed vector `h ⊥ span{1, Φ}`, `h ≥ 0` off `S`, `h ≠ 0`, and `μ + εh` is a twin for
small `ε > 0`; if the rank test fails, a twin is supported on `S` itself.
*Cost.*  An LP with `m + 1` variables and `M` constraints; with cutting planes we decided
instances with `M = 2·10⁶`, `m = 231` in minutes on one core.
*Checking the certificate.*  Evaluate `f` at all `M` configurations in exact arithmetic and
compute one rank: `O(mM)` operations, no solver, no trust in whoever produced `λ`.
*Numerical requirements.*  The verdict is a strict inequality.  Either compute in exact
rational arithmetic, or accept `IDENTIFIED` only when the margin `γ`, re-evaluated in double
precision from the rounded `λ`, exceeds a stated threshold, and `ABSTAIN` otherwise.  (In our
runs the margins of true faces were at least `1.7·10⁻²` with `|λ_i| ≤ 1`; a margin of `10⁻⁹` is
not a verdict.)
*Known traps.*  Exposed is not identified: `X = {a, b, c}` with one observable `(0, 0, 1)` —
the support `{a, b}` is the zero set of a non-negative function in the span and is not
identified (condition (i) fails).  Condition (ii) alone, or (i) alone, proves nothing.

### F2 — What a certificate guarantees under error  (Proposition E1.1, §2.1) — **R3**

*Statement.*  With the certificate of F1, for **every** ensemble `ν` on `X` — no model for
`ν` — the mass outside `S` satisfies `ν(X∖S) ≤ ‖λ‖_*·‖Aν − Aμ‖/γ`, and
`‖ν − μ‖₁ ≤ [(1 + (1 + R)/σ)·‖λ‖_*/γ + 1/σ]·‖Aν − Aμ‖`, `R = max_x ‖Φ(x)‖`.
*Evidence.*  First bound [V]: `Ensemble.mass_off_support_le` (for the pairing
`Σ_i |λ_i|·|Δ_i|`, which gives `‖λ‖_*‖Δ‖` for every absolute norm); second bound [P].
*Use.*  This is the answer to "do the bounds stay informative under noise": for a data
tolerance `τ` the first bound is informative iff `‖λ‖_*τ/γ < 1`.  The triple `(‖λ‖_*, γ, σ)` should
be reported with every `IDENTIFIED` verdict; maximising `γ/‖λ‖_*` over certificates is the LP
of F1 with a different normalisation.
*Trap.*  The constant can be enormous while the verdict is `IDENTIFIED` (benchmark control
B3 in `BENCHMARK_CONTROLS.md`: a vertex of a fine polygon).  On continuous spaces with
smooth observables no linear bound exists at all (Proposition E2.2): the modulus is at
best a square root.

### F3 — The range of any quantity given the data: partial identification  (Theorems E2(a), E17(a), §2.2, §4b) — **R3**

*Statement.*  For a target `ψ` on `X`, data `y`, tolerance `τ` in a norm `‖·‖`:
`sup{E_ν ψ : ‖Aν − y‖ ≤ τ} = min_λ { τ‖λ‖_* + λ·y + max_x (ψ − λ·Φ)(x) }`, and symmetrically
for the infimum.
*Evidence.*  [P] (linear-programming duality); the inequality "≤" for a given `λ` is one
line and is what a checker verifies.  Check T2/F5: duality gap at most `10⁻¹⁴` on 600
instances.
*Input.*  `Φ`, `y`, `τ`, `ψ`.  *Output.*  `INTERVAL [lo, hi]` with `λ_hi`, `λ_lo`; or
`INFEASIBLE` with a Farkas certificate — the data are not within `τ` of the means of **any**
ensemble on `X`, which is a certified statement of model misspecification.
*Checking.*  For each end evaluate `ψ − λ·Φ` at all `M` configurations: `O(mM)`.
*Use.*  This computes what the supplementary directive asks for when identification
fails: certified ranges of a structural quantity (`ψ` = any function of the
configuration), bounds on a population (`ψ` = the indicator of a state or a basin), and
the existence of indistinguishable alternatives (an interval of positive length comes
with two explicit ensembles that attain its ends).  It needs no identifiability.
*Trap.*  The interval is for the stated `X`.  It is a worst case over all ensembles, not a
confidence interval; for Gaussian noise see F5.

### F4 — One conformation: the identification constant, and the bridge to robust optimality  (Theorem E2(b), (c), §2.2) — **R3**

*Statement.*  For a conformation `x⋆` and a cost `ρ = d(x⋆, ·)`:
`κ = min{‖λ‖_* : λ·(Φ(y) − Φ(x⋆)) ≥ ρ(y) for all y}` is the best constant in
`E_ν d(x⋆, ·) ≤ κ·‖Aν − Φ(x⋆)‖` (all ensembles `ν`), and the constraint is the sharp-minimum
condition of the theory division's Theorem 2.4: a certificate that `x⋆` is optimal for
every admissible residual is a certificate of identification, with a linear modulus.
*Evidence.*  [V] for finite `X`: `Ensemble.transport_le_of_sharp`,
`Ensemble.identification_of_robust_certificate`, `Ensemble.robust_certificate_of_sharp`,
`Ensemble.residual_advantage_le`.
*Algorithm.*  One LP (`m` variables, `M` constraints).  *Checking.*  `M` inequalities.
*Use.*  Any existing checker of the theory division's robust-optimality certificates is,
unchanged, a checker of this identification statement.

### F5 — Gaussian noise: a near-minimax estimator from the same dual vector  (Theorem E17, §4b) — **R2**

*Statement.*  Data `y = Aμ + σξ`, `ξ` standard Gaussian, `μ` in a convex class `𝒫`; target
`T(μ) = E_μψ`.  With `ω(ε) = min_λ{ε‖λ‖₂ + R_𝒫(ψ − λ·Φ)}` (`R_𝒫` the range of a mean over the class):
the affine estimator `T̂ = λ·y + c` built from the minimiser at `ε = 2σ` has
root-mean-square error at most `0.5·ω(2σ)`, and no estimator has less than `0.335·ω(2σ)`.
*Evidence.*  [P], examined by the internal review ER2 (which supplied the constant
`0.335 = √κ/2`, `κ = E sech²(1 + Z)`); the cited theory (Donoho 1994) was read through lecture
notes only.  Not machine-checked.  Check F5.
*Algorithm.*  A convex programme with a Euclidean norm (second-order cone), size `M` for
`𝒫` = all ensembles.  *Checking.*  The upper bound for a given `λ` needs the range of
`ψ − λ·Φ` over `𝒫` (for all ensembles: a maximum and a minimum over `X`); the lower bound needs
two ensembles at data distance at most `2σ` — both are explicit.
*Caveat to carry.*  Gaussian noise of known covariance on *means* (correlated noise by
whitening: Proposition E17.1(a)); an unknown covariance is not covered.  There is no
result for noise on *laws* of observables.

### F6 — Inside a first-order (envelope, density-ratio) class  (Theorem E13, §4a.1) — **R2**

The class `{μ : μ(y)π(x) ≤ e^{d(x,y)}μ(x)π(y)}` is a polytope in the weights; "determined by
the data among its members" is again exposedness (of a face, with injective data), and
bounds on means have exact flow certificates (the science division's format; exactness
is LP duality).  LP of size `M²` unless the envelope has structure.  Reviewed by ER2.
*Caveat.*  A member strictly inside the class is never identified by fewer than `M − 1`
observables; data shrink the identified set, they do not pin interior members.

## 2. Product spaces that cannot be enumerated

### P1 — Pair correlations on `{±1}ⁿ`: the projection certificate  (Theorem E10, §4.2) — **R2**

*Statement.*  For `K` linearly independent sign vectors whose linear span contains no other
sign vector than `±` themselves, `f(x) = ‖x − Px‖²` (`P` the projector on the span) is a
certificate in the sense of F1 for pair correlations: every ensemble on these conformers,
whatever its weights, is determined among all ensembles on the cube.  For random
conformers the hypothesis fails with probability at most `2^{−t} + 2^{K+t}(¾)^{n−K−t}`.
*Constructing* the certificate costs `O(nK²)`.
***Checking it is the hard part.***  Deciding whether a span contains another sign vector
is NP-complete (the Complexity division's Theorem 14, COMPLEXITY-RES-0008, unreviewed by
its own account); it can be done in time `2^K·poly(n)` (its `span_algorithm.py`).  A tool must
either enumerate (`K ≲ 30`), or enumerate the cube (`n ≲ 24`, then use F1 directly), or
`ABSTAIN`.  The probability bound is a statement about random inputs and is **not** a
certificate for a given input.
*Trap (benchmark control B4).*  At the sizes one can enumerate, most identified supports
have **no** certificate of this kind: for `n = 12`, `K = 9` conformers, 92 % of random
supports are identified and 0.5 % have a projection certificate.  A tool that reports
"not certified" as "not identified" is wrong most of the time there.
*Stability.*  The gap `γ = min_{x ∉ ±S} f(x)` needed by F2 is a closest-vector computation;
no efficient lower bound is known to us.  Without `γ` the verdict has no noise guarantee.

### P0 — The worst case on a finite product space  (**[K]**: Kahle 2010) — **R3 as a known theorem**

*Statement* (Kahle, "Neighborliness of marginal polytopes", Theorem 13; read by our
internal review ER3).  On a finite product space with any alphabets, **every** ensemble
with at most `2^t − 1` conformers is determined, among all ensembles, by the marginals of
all sets of `t` sites; the number is sharp.  For pair marginals (`t = 2`): any three
conformers — this contains our Proposition E9(a).  For even correlations of order at most
`2d` on the cube modulo the flip: any `2^{2d} − 1` conformers (3 for pair data, 15 for two-
and four-body data).
*Use.*  A guarantee that needs no genericity and no check on the instance: if at most
`2^t − 1` conformers are present, the order-`t` marginals determine the ensemble.  It says
nothing about stability (no gap), and it is a worst-case number: random conformers do far
better (P1, and Theorem E19 for higher order).  The certificate still has to be computed
(F1 on an enumerable space).
*Status in our report.*  Not yet cited there (obligation OB24).

### P2 — Reading as few pair correlations as possible  (Theorem E12(b), §4.3) — **R2**

Pivoted Cholesky on the correlation matrix reads `rn − r(r+1)/2` entries, `r` its rank (at most
the number of conformers), and determines the whole matrix; no design fixed in advance
can do with fewer than all pairs.  Exact data only: with noise the stopping rule needs a
threshold for which we have no guarantee.

## 3. Laws of observables (distance distributions and the like)

### L1 — Laws of coordinates  (Theorem E4, §3.1) — **R2**

*Statement.*  Let the observables `T_1, …, T_m` be `r`-determining (two distinct
configurations agree on fewer than `r` of them).  An ensemble with at most `K` atoms is
determined, among **all** probability measures, by the laws of the `T_j` as soon as
`m ≥ K(r − 1) + 1`; the count is sharp.  [V] for finite `X`: `Ensemble.renyi_heppes`.
*Use.*  A uniqueness theorem with a constructive core: every atom lies in the
intersection of the preimages of the atoms of the laws, and a point of that intersection
that agrees with one atom on `r` observables is that atom.  The intersection has up to
`K^m` candidate combinations; for small `K` and `m` this is a finite search, in general it
is exponential.  Exact laws only.

### L2 — Edge-length laws of point configurations  (Theorems E5–E8, E7′, §3) — **R1**

*What is proved.*  For a generically globally rigid graph, **jointly generic** finite
ensembles of frameworks are determined by the laws of the edge lengths (a corollary of
Gortler–Healy–Thurston through an elementary matroid statement), with a per-edge
certificate.  Reviewed independently by the science division.
*Why it is not ready.*  (i) No stability constant: the quantity that controls stability
(the smallest violation of realisability by a spliced length vector, the "chimera gap")
is small in the science division's computations, and nothing bounds it from below.
(ii) Genericity is joint: conformers that share a rigid part, or two planar rigid bodies,
are counterexamples (controls B2).  (iii) The decision "is this spliced length vector
realisable" is a graph-realisation problem.  (iv) A measured distance distribution is not
an exact law of an exact distance (report §8).
*What can be computed today.*  Whether a *graph* has the generic property (ranks of
rigidity matrices at random rational points) — a property of the design, not a verdict
about an instance.

## 4. Continuous configuration spaces with explicit constants

### T1 — Two states on a torus of angles  (Propositions E20′, E20″, §4c.4) — **R1 (reviewed; corrections pending)**

Two states `p, q` of `r` angles are determined among all probability measures on the torus
by the means of `cos`, `sin` of single angles and of products over pairs of differing
angles iff they differ in at least two angles; the certificate has quadratic growth with
the explicit constant `c* = min(1, β_min/4)` (three or more differing angles), which gives
`∫ min(d²(φ,p), d²(φ,q)) dν ≤ Λτ/c*` for every measure with data within `τ`, and the weights
within `O(√τ)`.  Zero set and growth inequality are [V] (`Ensemble.twoStateCert_eq_zero_iff`,
`twoStateCert_growth_three`, `twoStateCert_growth_two`); the passage to angles and the
stability bound are on paper.  Evaluating the bound is `O(r²)` arithmetic.
*Review.*  The internal review ER3 (2026-11-26) re-derived the proofs and attacked them
numerically: zero set, growth inequality and stability bound are correct; the constant
`c*` is conservative (by a factor 2 to 4 for two differing angles, and much more when one
of three differing angles nearly coincides); the bound on the weights is of order `√τ`
where order `τ` is provable; three states on a torus of two angles are **never**
determined by bilinear data (control B2-07).
*Not ready because* those corrections are not yet in the report (obligation OB24); and
because for chains of rigid segments the configuration space is not this torus (mirrored
assemblies; only adjacent pairs of torsions are in the span of squared distances —
Geometric Inference Division, GEOMETRY-RES-0005).  The statement for chains is that
division's.

### T2 — `K` states on a product space: the permanent certificate  (Proposition E21) — **R1**

Zero set [V] (`Ensemble.permCert_zero_set`).  Needs data of order `K`; the hypothesis is a
Hall-type condition on the states, checkable in time `2^K`.  Reviewed by ER3: correct; on
finite product spaces it is **weaker than the published theorem P0** (which needs no
condition and reaches `2^K − 1` states) — what it adds there is an explicit formula; on
tori it has no published counterpart that we know.

## 5. Finite temperature

### H1 — The thermal union bound  (Theorem E15, §4a.2) — **R3 for evaluating the bound**

*Statement.*  Product reference `⊗π_i`, site-additive envelope `Σ_i δ_i` (one-sided allowed),
centre `a`; `σ_i` the population of `a_i` in the one-site polarised law
`∝ π_i(s)e^{−δ_i(s, a_i)}`.  Every member `μ` of the class has `μ(x_i = a_i) ≤ σ_i` and
`TV(μ, μ*_a) ≤ Σ_i [1 − μ(x_i = a_i)/σ_i]`; for binary sites `TV(μ, μ*_a) ≤ Σ_i [σ_i − μ(x_i = a_i)]`.
*Evidence.*  [P], examined by ER2 and replicated by the science division with its own
code (95 160 linear programmes); the inequality for monotone densities is [V]
(`Ensemble.thermal_union_bound`, `thermal_union_bound_density`, `thermal_union_bound_sharp`).
*Cost.*  `O(Σ_i |A_i|)`.  The bound is affine in the observed populations, so intervals on
them propagate exactly.
*What it is not* (science division, SCI-RES-0032).  It bounds the distance to the
*polarised* member; it is not a test of whether an ensemble belongs to the class, and on
that division's instances, where the truth is far from polarised, it certifies nothing
of use.  For one-body data the exact feasibility test is that division's ratio test.
*With an interacting known part* (E15T, E15U): the bound holds iff an explicit condition
on up-sets holds; a violated bond can break it.  The condition is checkable by
enumeration for about five sites only — **R1** (E15U is unreviewed).

## 6. What an algorithm must establish, and whether checking is easier than constructing

**To certify identification** (any space): (1) an observable combination `f` that is
non-negative on *all* of `X`; (2) that its zero set is *exactly* the support (or a finite
set on which the problem can be solved exhaustively — the refinement that the Geometric
Inference Division pointed out); (3) independence of the features on that set.  For
stability under error, additionally (4) a lower bound on `f` away from the support — a gap
`γ` on a finite space, quadratic growth on a continuum.  (1), (2), (4) are statements about
a global minimum over the configuration space: **certifying identification is certifying
a ground-state set**, which is why the programme's certificate kernels apply.

**Checking against constructing.**

| setting | constructing a certificate | checking it |
|---|---|---|
| finite enumerable `X` | one LP in `m + 1` variables, `M` constraints | `O(mM)` exact arithmetic and one rank; **easier**, and independent of the solver — a certificate found in floating point can be rounded and then checked exactly |
| `NOT IDENTIFIED` (any space) | LP, or theory (splices, sign-vector combinations) | compare the means of two explicit ensembles: `O(mK)`; **trivial** |
| an interval for a quantity (F3) | LP | `O(mM)` per end; **easier** |
| pair data on a large cube (P1) | `O(nK²)` for the projection certificate | NP-complete in general (is the zero set exactly the support?); `2^K·poly(n)`; **harder than constructing** unless the certificate carries a proof of its own minimum |
| edge-length laws (L2) | — (an existence theorem) | realisability of spliced length vectors; no stability constant |

So on enumerable spaces the division of labour is the one the programme already uses —
an untrusted solver, a trusted checker — and on structured spaces the open problem is a
certificate *format* for "the ground states of this energy are exactly `S`, with gap `γ`"
whose size can be bounded (our question E-T4 to the theory division; the Complexity
division's degree bounds say that sums of squares of low degree will not do in general).

## 7. Observation models: what is covered, and what is not

| feature of real data | status in our results |
|---|---|
| bounded error on each mean, any norm | covered exactly: F2, F3, F4 |
| independent Gaussian noise on means, known level | F5 |
| correlated Gaussian noise, known non-singular covariance | F5 after whitening: Proposition E17.1(a) (the norm `‖λ‖₂` becomes `‖Σ^{1/2}λ‖₂`) |
| missing observables, restricted designs | covered: every statement is for an arbitrary set of observables; fewest pair correlations: P2 |
| an observation function known up to a uniform error `δ_i` | **exactly** equivalent to enlarging the tolerance of that datum by `δ_i` (Proposition E17.1(b)): F1–F4 with the nominal functions and the tolerances `τ + δ` are valid for the truth, and nothing smaller is |
| an observation function with unknown parameters (`φ_θ`) | a certified **outer** bound (Proposition E17.1(c)): the compatible set is a union over `θ`, not convex; if `φ_θ` is Lipschitz in `θ` (constant `L`, uniformly on `X`), F3 on a grid of mesh `h` with every tolerance enlarged by `Lh` contains the exact range and converges to it.  Cost: one LP per grid point — practical for a few parameters only |
| data that are not linear in the ensemble (ratios or squares of averages, quantities averaged on a time scale) | **not covered.**  The feasible set is not convex; nothing above applies as stated |
| laws (distributions) of an observable instead of means | Part II: exact laws only; no noise model; R1 |
| unknown number of conformers | F1–F5 need no such number: they quantify over all ensembles.  A known bound on the number of conformers is a *prior* that can enlarge what is identified (Theorem E18′, R1) — never needed for validity |
| model misspecification | F3 certifies infeasibility; F2 is model-free.  Class-based statements (H1, F6) are only as good as the class |

## 8. Proof obligations that bear on software

* Part VI (E18–E21, E20″): reviewed internally (ER3: no numbered statement false); its
  corrections are not yet in the report (OB24).  Proposition E15U: unreviewed (OB23).
* F5: paper proof; the cited minimax theory not read in the original.
* L2: no stability modulus (Problem O4); several rigid bodies (Problem O3).
* P1: no certificate format between the projection certificate and exhaustive
  enumeration (E-T4); the numerical thresholds of §4.4 are conjectural (C2).
* Proposition E17.1 (correlated noise; imperfect and parametric observation functions)
  is immediate and unreviewed.
* Nothing here has had external peer review.

## 9. Where to find things

| need | place |
|---|---|
| exact statements and proofs | `docs/ensemble/ENSEMBLE_REPORT.md` |
| Lean declarations | `proofs/Ensemble/*.lean`; list and axioms in `proofs/AxiomAudit.lean` |
| reference computations | `experiments/ensemble/exposedness_checks.py` (F1–F4), `finite_temperature_checks.py` (F5, F6, H1), `capacity_threshold.py`, `capacity_cutting_plane.py` (F1 on cubes), `degree2_vs_face.py` (P1) |
| synthetic controls with ground truth | `docs/ensemble/BENCHMARK_CONTROLS.md`, `experiments/ensemble/benchmarks/` |
| what failed | `docs/ensemble/DEAD_ENDS.md` |
