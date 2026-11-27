# Workstream F — the two-oracle model with a field: are local measurements worth anything once the symmetry of the uniform cube is gone?

Read `docs/science/workstreams/COMMON.md` first.  Your directory:
`experiments/science/ws_F/`; your report: `docs/science/workstreams/SF_REPORT.md` (the theory
division already has an `F_REPORT.md`).  Second wave.

## The question (the most important open limitation of our own results)

`docs/science/INFERENCE_LIMITS.md` (version 3; read §§0–4, §13, §14) and its addenda (A1, A8,
A10 in `INFERENCE_LIMITS_ADDENDA.md`) prove, **on the uniform cube with zero known part**:
giving an algorithm, free and exact, all `k`-body marginals of the Gibbs measure `μ_g`
changes neither the adaptive nor the non-adaptive worst-case exponent of certifying
`ln Z` (Theorem 4, Theorem 4′ = theory report Proposition 11.104); with error bars the
same for correlations of every order (Theorem 4-τ).  The proof symmetrises a hidden dip
over a linear code: translation invariance makes every `k`-body marginal *exactly*
uniform.  **With a field — a `p`-biased reference measure, `p ≠ ½` — there is no translation
symmetry, and we have said in every message that we do not trust "local data are worth
nothing" beyond the uniform cube** (SCI-REQ-0001 Q2; our referee's finding M6; open
problem A2 of `docs/science/OPEN_PROBLEMS.md`).  Settle it, for one-body marginals first.

Setting (theory report §11.20, `grep -n '^### 11.20' docs/THEORY_REPORT.md`, lines 4197–4617;
§11.26 for the general formulas, readable in the checkout
`/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro`
at commit `89ac710`): `X = {0,1}ⁿ`, reference `π = Bernoulli(p)ⁿ`, class `L_u` of functions `ψ`
with `|ψ(x) − ψ(y)| ≤ u·d_H(x,y)`, target `ln E_π e^{−ψ}`, Gibbs measure `μ_ψ ∝ π e^{−ψ}`.  Known
without an oracle (Theorem 11.64): adaptive exponent `R^max(ε₁) = max_{|γ|≤u} R_γ(ε₁)`, the
hinted exponent of the hardest *additive* instance `γ*|x|`, which partly cancels the field;
non-adaptive exponent `θ_na`; a field always helps (Proposition 11.65(b)).  The general
formulas (Theorem 11.99, reviewed by us in `R5_REPORT.md`): the site function is a Rényi
capacity of the "vertex channel" `φ ↦ π_φ` (for a binary site: two vertices, the full tilts
towards 1 and towards 0), `F*(t) = min_Q max_φ (1−t)D_t(π_φ‖Q)`, and the hardest additive
instance at slope `t` has the Rényi centre `Q*` as its Gibbs law.

**Oracle.**  For the instance `ψ` the algorithm receives, free and exact, the one-body
marginals `μ_ψ(x_i = 1)`, `i = 1…n` (later: all `k`-body marginals; later: with a tolerance).

## The coordinator's conjecture and sketch (to be tested, not assumed)

**Conjecture.**  The one-body oracle does **not** lower either exponent, with or without
a field — for a structural reason: *the hardest instance is self-consistent*.

*Sketch.*  (1) At the saddle point `(M*, Q*)` of the site game at slope `t`, the Rényi centre
satisfies Augustin's fixed-point identity

    Q*  =  Σ_φ M*(φ) V_φ ,        V_φ ∝ π_φ^t · Q*^{1−t} ,

and `V_φ` is the conditional type that carries the mass that matters in a hidden dip (it
is the minimiser in `(1−t)D_t(π_φ‖Q) = min_V[t·D(V‖π_φ) + (1−t)·D(V‖Q)]`).  So the excess mass of
dips whose centres have label law `M*` has, in aggregate, **the one-body statistics of the
hardest instance itself**.  For `t → 1` this is the textbook fact that the
capacity-achieving output law is the mixture of the channel's outputs.
(2) A single dip (or cone) reveals its centre through the one-body marginals.  Average
the *weights* over the `n` cyclic shifts of the centre (the weight cone is convex; `π` and
additive instances are permutation invariant, so `Z` is unchanged): the result is
invariant under cyclic shifts, so all `n` one-body marginals are equal — one number.
(3) Exactness: one scalar equation.  A continuous parameter (a mixture of two centre
types `m`, `m+1`; or a partial flattening level) lets the intermediate-value theorem hit
the base instance's marginal exactly, if the two ends bracket it — which (1) says they
do near the optimal label law.
(4) Then the counting argument of Theorem 4 with orbits in place of cosets: the lower
bounds are divided by at most `n`.
*What can go wrong, and would be as interesting:* (a) the pair of instances that the
non-adaptive lower bound compares (a cone and its truncation — theory report Theorems
11.45, 11.98(d)) must have **identical** oracle answers *and* coincide outside a small
set: the removed mass must itself have the base's one-body marginals — check whether the
truncation can be shaped so (one more scalar equation); (b) at slopes `t < 1` the fixed
point holds at the saddle only — away from it the constraint may bind, and then the
oracle **does** lower the lower bound: the constrained problem is "the hinted exponent
restricted to centre label laws `M` with `Σ_φ M(φ)V_φ = ` the base's site law" — compute it
and compare with the unconstrained one over the whole range of accuracies; (c) for
`k ≥ 2` exact symmetrisation needs `k`-transitive permutation groups of polynomial size
(`AGL(1,q)` for `k = 2`, `PGL(2,q)` for `k = 3`, none for `k ≥ 6`): there the natural statement
is with a tolerance, using centre sets that are approximately `k`-wise independent with
the biased label law — say what you can prove; (d) instance-wise the oracle certainly
helps somewhere (at a cone instance it reveals the centre): an *upper* bound that uses
the oracle at favourable instances would show where measurements are worth an
exponential factor.

## What to do

1. **Numerics before theory.**  (i) Implement the single-letter formulas for the binary
   `p`-biased cube (`F*(t)`, `R_γ`, `R^max`, `θ_na`, the saddle `(M*, Q*, t*)`) from the theory
   report and check them against its printed numbers (e.g. §11.20's tables; `u = 1`).
   Verify the fixed-point identity numerically, and compute how far the one-body
   marginal of the relevant excess mass is from the base's site law *away* from the
   saddle.  (ii) Exact finite-`n` computations with type-class sums (`n` up to several
   hundred) and exhaustive enumeration (`n ≤ 16`): cyclically symmetrised dips and cones
   on the biased cube, their exact one-body marginals, the root of the matching equation,
   the resulting lower bound, and its exponent against `R^max` and `θ_na`.  (iii) If the
   constraint binds anywhere: the constrained exponent as a function of `(p, u, ε₁)`.
2. **Theorems.**  State and prove the cleanest true statement you can reach — for
   example "for every `p`, `u`, the non-adaptive exponent at vanishing accuracy (the Shannon
   capacity `a`) is unchanged by a free exact one-body marginal oracle", then the adaptive
   exponent, then extensive accuracies — with every quantifier, in the style of Theorem 4
   and addendum A1.  Or the opposite, with the constrained formula and an algorithm.
3. **`k = 2`** and the tolerance version, as far as you get.
4. **Reading (label it [H] and keep it apart from the statements):** what this says
   about per-residue averaged measurements for a molecule whose reference ensemble is
   not symmetric.

## Deliverable

`docs/science/workstreams/SF_REPORT.md` in the format of COMMON.  Final message: at most 600
words — the verdict on the conjecture (true / false / true in which regime), the precise
strongest statement with its status, the numbers, and the absolute path of the report.
