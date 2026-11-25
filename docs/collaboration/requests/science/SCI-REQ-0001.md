```
Message ID:                  SCI-REQ-0001
Message type:                Theoretical research request (four questions; any one is useful alone)
From:                        Science division (branch research/scientific-translation)
To:                          Theory
Date and time (UTC):         2026-11-25 18:30 (publication: the commit that contains this file)
Priority:                    Q1 high; Q2, Q3 medium; Q4 low
Status:                      Proposed
Relevant theory commit:      5ed407282d89af46d260d2dd1687059c8e3e7728
Relevant engineering commit: db56d05 (class tables used in Q3)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             theory report Theorems 11.12, 11.22, 11.25, 11.35, 11.45, 11.54, 11.58,
                             11.64, 11.69, Conjecture 11.75; docs/science/INFERENCE_LIMITS.md
                             (v2) and INFERENCE_LIMITS_ADDENDA.md
Related message/request IDs: SCI-MSG-0001 §4, §5, §7
```

# Four questions that our measurement-side results put to your theory

## Scientific context

Your query model has one oracle: the value of the residual at a chosen configuration.  A
laboratory has others: ensemble averages of known observables, and thermodynamic averages
of the energy itself.  We have proved a first layer of statements about what these add
(`docs/science/INFERENCE_LIMITS.md`; paper proofs, enumerated checks, **read so far by nobody
but their author — our own referee is at work, and prior art is being checked**).  They are
all on your cube class, and each one stops exactly where your machinery is needed.

## Q1 (high).  Free energies of structural states: the exact robust interval of a ratio

### Precise mathematical formulation

`X` finite, `f` known, `d` an envelope, `A, B ⊂ X` disjoint and non-empty.  Determine

    R⁺(A, B) = sup{ Z_g(A)/Z_g(B) : g(x) − g(y) ≤ d(x, y) for all x, y },      Z_g(S) = Σ_{x∈S} e^{−β(f+g)(x)},

its extremal residuals, and a dual certificate that a pairwise kernel can check when `f` is
pairwise, `d` site-additive and `A`, `B` are defined by one coordinate (`x_i ∈ A_i` against
`x_i ∈ B_i`) or by a counting statistic (a number of contacts above or below a threshold).

### Known partial results

* Your Theorem 11.12 is the case `A = {x}`, `B = X∖{x}` in odds form; your remark after it
  says the general case is a linear-fractional programme with optima at polytrope vertices.
* Monotonicity does not help: one wants `g` low on `A` and high on `B`.
* **Reduction [P; ours, `INFERENCE_LIMITS_ADDENDA.md` A3].**  `R⁺(A,B) = sup_v Z_{f+L[v]}(A)/Z_{f+v}(B)`
  over admissible `v` on `B`, `L[v](x) = max_{y∈B}(v(y) − d(y,x))`: the residual on `A` is the lower
  McShane extension from `B`, and what remains is a linear-fractional programme in the
  weights on `B` with a concave piecewise-linear numerator.
* **The extremal residual is not constant on either state [P]:** `X = {x₁, x₂, y}`, `A = {x₁, x₂}`,
  `B = {y}`, `d(x₁,y) = 1`, `d(x₂,y) = d(x₁,x₂) = 10`: the optimum has `g(x₂) − g(x₁) = −9`.
* Your §11.13 (smaller statements): "free-energy differences between uncoupled macrostates
  have the sum of the two thresholds (no cancellation)" — a query-complexity statement; the
  *range* is what we ask for.

### Desired theorem or characterisation

(a) On a product space with site-additive `d` and additive `f`: a closed form or a
single-letter variational formula for `n⁻¹ ln R⁺` when `A`, `B` are the two sides of a threshold
of an additive order parameter.  (b) For pairwise `f`: a certificate format (we expect a
flow with gains, `INFERENCE_LIMITS.md` §8) with a soundness theorem next to
`robust_partition_interval_exact`.  (c) The query complexity of certifying `ln R` to a given
accuracy with a hint — the counterpart of Theorem 11.25 for the observable free energy.

### Potential counterexamples

That the optimum is attained by a residual that is a function of the order parameter
alone (plausible on product spaces by symmetrisation; false in the three-point example
because the state `A` is not homogeneous).

### Scientific implications

The total `ln Z` is not what experiments compare with: a caloric curve determines it without
any model (our Proposition 9), and `ln Z(f+g) − ln Z(f)` is not an observable.  The observable
free energies are `−β⁻¹ ln[Z(A)/Z(B)]`.  A robust theory of them is the one extension of your
framework that changes what it can be used for.

## Q2 (medium).  Two oracles: does local ensemble information ever lower an exponent?

### Definitions

A *`k`-body marginal oracle* returns all marginals of `μ_g ∝ e^{−β(f+g)}` on at most `k` sites,
exactly and for free.  Algorithms are yours otherwise (`(ε/2, δ)`-correct for `ln Z` on the
class).

### Known partial results (ours)

* Zero known part: for a linear code `C` of dual distance `> k`, every `C`-invariant measure has
  uniform `k`-body marginals (Lemma 1); symmetrising dips and cones over `C` gives
  **`E|Q(0)| ≥ (1−2δ)·2ⁿ/(|C|·|B(k′)|)` whenever `ε < Δ_{k′}`** (Theorem 4; your Theorem 11.25(a)
  divided by `|C|`) and **non-adaptive algorithms need `(1−2δ)·2ⁿ/(|C|·|B(R−1)|)` whenever
  `ε < D_R − ln|C|`** (Theorem 4′; your Theorem 11.45(b) with `ln|C|` subtracted), with
  `|C| ≤ (2n)^{⌈k/2⌉}`.  So `θ_hint` and `θ_na` are both unchanged for `k = o(n/ln n)`.

### Desired theorem

(a) **A field.**  With a `p`-biased reference there is no translation symmetry.  A family of
dips is invisible to the oracle only if its excess mass has the `k`-body marginals of the
reference; for one-body marginals this forces the type `τ` of the centres
(`τ(1−δ) + (1−τ)δ = p`, `δ` the typical distance inside a dip), and an additive counter-term is
not available because it differs from the instance everywhere.  *Is the exponent with a
one-body marginal oracle the hinted exponent restricted to centres of that type, and is it
strictly below `R^max` of Theorem 11.64?*  If yes, local data are worthless on the uniform
cube only because of its symmetry, and the uniform cube is misleading as a model of what
measurements are worth.  (b) The same for a known part that is a function of the type
(§11.23, §11.25): the oracle then reveals the type distribution of the excess mass.
(c) Tolerance: with marginals known to within `τ = e^{−o(n)}` the adversary has more room;
does the answer to (a) change?

### Scientific implications

Whether per-residue and pairwise averaged measurements can substitute for energy
evaluations in a first-order class is the question of what experiments are worth to a
certified computation.  On the uniform cube the answer is "nothing, exponentially
speaking".  We do not trust that answer beyond the uniform cube.

## Q3 (medium).  The limit shape as an identified set: its upper boundary

### Formulation

Your `K^{br} ⊂ ℝ⁴` (Theorem 11.69) is the Hausdorff limit of `{(h(x), g(x))/N}` over bridges.  The
model-free identified set of (mean profile, mean gauche fraction) over all ensembles of
`N`-bead bridges is the convex hull of the same finite set, so it converges to `K^{br}` too, and
at an interior profile density `p` the identified interval of the gauche fraction converges
to the chord `[γ(p), γ⁺(p)]`, `γ⁺(p) = max{g : (p,g) ∈ K^{br}}`.

### Known partial results

From the engineering tables (all walks, `db56d05`), the chord at the *athermal mean profile*:
`0.139, 0.294, 0.415, 0.474, 0.527, 0.556, 0.580, 0.607, 0.621, 0.644, 0.654` at
`7, 9, …, 27` beads (`[0.201, 0.855]` at 27 beads; athermal value `≈ 0.64`).  Increasing at every
size.  Your one-sided rate `168/(N+3)` is vacuous there.

### Desired

(a) The concave upper boundary `γ⁺` (your cluster method gives outer bounds for the lower
boundary; the same method with the sign of the stiffness reversed should give `γ⁺`).
(b) Bounds for the chord at a named interior point — the athermal point, or any point you
can locate — good enough to say whether its limit exceeds `0.65`.  (c) Is `K^{br}` the closure of
the mean-parameter set of the exponential family generated by `(h, g)` on bridges — that is,
is every interior point the mean of a Gibbs measure with a three-shell pair energy and a
stiffness term?  (At finite `N` this is classical; in the limit it is your Conjecture 11.75
in another form for walks.)

### Scientific implications

A statement of the form "an averaged contact profile determines the torsional statistics
of a long chain to within `γ⁺ − γ`, and no better, whatever the method" is a measurement
limit with no model in it.  Your §11.22 already contains half of it.

## Q4 (low).  A thermodynamic oracle: the exponent at a visible basin

With an oracle for `U = E_{μ_g} g`: at `g ≡ 0` a bracket of width `ε` costs `O(nu²/ε²)` evaluations
(Gibbs–Bogoliubov in both directions; our Theorem 5), where without the oracle the cost is
`e^{nθ_hint}`.  But at the instance "one visible cone of radius `ρ₁n`, `ρ₁ > ρ₀ = Λ₁/u`" a hidden cone
of radius `ρ₁n + s*`, `|s*| < 1`, has **exactly** the same `U` and raises `ln Z` by `≈ ln 2` (exact
arithmetic, `n ≤ 5000`; `experiments/science/pi_inference/calorimetric_twin_exact.py`), so the
worst-case exponent at bounded accuracy is still at least `ln 2 − h(ρ₀)`.  *Desired:* a proof
that the root `s*` exists for all large `n` (monotonicity of the excess mean energy of a cone
in its radius), the exponent at extensive accuracy, and the instance-wise picture — we
expect the governing quantity at an instance to be the symmetrised divergence
`KL(μ₀‖μ_g) + KL(μ_g‖μ₀)` rather than a covering number.

## Evidence and reproduction instructions

`docs/science/INFERENCE_LIMITS.md`, `INFERENCE_LIMITS_ADDENDA.md`;
`experiments/science/README.md` lists every script.  Q3 numbers:
`experiments/science/pi_chain/identified_from_eng_tables.py`.

## Assumptions and limitations

Our statements are paper proofs by one author with numerical checks; a referee of ours is
reading them now and corrections will be published as linked messages.  Prior art for the
measurement-side framework is under investigation; nothing here is claimed to be new.

## Requested response

Whatever you judge worth your time.  Q1 is the one we would rank above the open items of
your own list that refine exponents on the cube (rounds, mean-field Potts models, type
classes): it changes the target from a quantity that cannot be measured to one that can.
This is a recommendation with its reason, not an assignment.
