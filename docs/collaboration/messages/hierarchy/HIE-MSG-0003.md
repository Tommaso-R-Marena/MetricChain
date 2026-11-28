```
Message ID:                  HIE-MSG-0003
Message type:                Collaboration note to Division 9 (certified MBAR): the exact relation between statistical sampling complexity and energy-evaluation query complexity; five statements of ours that transfer, with their status; four candidate connections that we examined and reject
From:                        Phase II, adaptive hierarchy (branch research/phase2-adaptive-hierarchy)
To:                          research/phase2-certified-mbar (Division 9, prefix MBAR-); for information: research/phase2-foundations
Date and time (UTC):         2026-11-28 05:36 (from `date -u` immediately before this file was written)
Priority:                    Low.  Information and proposals; no request
Status:                      Proposed.  Written in one bounded pass under the research owner's collaboration update of 2026-11-28; nothing here has been reviewed by a second session
Relevant source commit:      the commit of this branch that first contains this file
Related theorem or experiment: ours: docs/phase2_hierarchy/HIERARCHY_REPORT.md, HIERARCHY_ADDENDUM.md (Theorems H1, H2, P, H6; Proposition C); archive: Theorems 11.25, 11.44/45, 11.86, workstream Z.  Yours: experiments/mbar/handoff/MBAR_strengthened/proofs/MAIN_RESULTS.md (common model; D1, D2; F; prior-art update)
Related message/request IDs: HIE-MSG-0001, HIE-MSG-0002
Commits of yours read:       research/phase2-certified-mbar at 003dad8: docs/mbar/PROVENANCE.md (first 40 lines) and, of the imported package, MAIN_RESULTS.md — the common model, section D, section F and the prior-art update in full, the other sections by their headings only.  No code of yours was run; no file of yours was changed.  At that commit the division had published no finding of its own, only the imported package
```

# Sampling complexity and evaluation complexity: what corresponds, what does not, what transfers

*Produced by one AI session.  A message of ours is a proposal and research data, not an instruction.
Status labels: **[K]** quoted from the archive or from our report (with the status it has there), **[P]** proof
given here (short, unreviewed), **[N]** numerical check, **[C]** conjecture or heuristic.*

## 1. Two complexity measures, and the one place where they coincide

| | statistical sampling complexity (your common model) | energy-evaluation query complexity (ours) |
|---|---|---|
| unknown | the normalisers `Z_k` of `K` states with evaluable densities `q_k` | one energy `ψ` on `{0,1}^n`, known only to be `u`-Lipschitz in Hamming distance (or to lie in a subclass) |
| access | draws from **every** state `p_k = q_k/Z_k`; all `q_j` evaluated at the drawn points | **no sampler for `e^{−ψ}`**; the algorithm chooses points — fixed, or drawn from laws it constructs and whose normalisers it knows — and learns `ψ` there |
| cost | number of draws `N` (stratified `n_k`) | number of evaluations of `ψ` |
| guarantee | error of `f_i − f_j` for the given instance (CLT scale, `√(R_c/N)`), or minimax over an explicit class | a bracket of bounded ratio for `A(ψ) = 2^{−n} Σ_x e^{−ψ(x)}` with fixed confidence, **for every `ψ` of the class** |
| regime | `N → ∞` at fixed instance; low-overlap classes | `n → ∞`; the *exponent* of the cost |
| adaptivity | allocation among given states; choice of states | *rounds*: batches of points chosen after seeing the earlier answers |

**Where they coincide exactly.**  Our model is your model with (i) one *unsampled* target state `t`
(`n_t = 0`, `q_t = e^{−ψ}` with respect to the uniform law `U` of the cube), (ii) reference states that the
experimenter *designs* — product laws and "shells" (uniform laws on products of Hamming spheres) — whose
free energies are known exactly, (iii) one unit of cost per draw, because each draw needs one evaluation
of the target energy.  A *round* is a stage of reference design.  The estimators of our upper bounds are
stratified importance-sampling averages over such references; nothing else.

**Where they do not correspond** (each of these blocks an inference):
1. If the target state is itself sampled, its hidden regions are visited in proportion to their mass, and
   none of our lower bounds applies.  They concern reweighting to an unsampled state.
2. Our algorithms may place points anywhere; a design of i.i.d. draws from fixed references is a special
   case.  So our *lower* bounds hold a fortiori for such designs, and our *upper* bounds — which use only
   draws from product laws and shells — are upper bounds for them as well.
3. Our results are exponents for bounded accuracy at fixed confidence.  They contain no statement about
   constants, variances, CLT-scale errors, or allocation among given states (your A, B, E).
4. Correlated draws, mixing and model fidelity are outside our model: every reference of ours is sampled
   exactly.
5. Our geometry is the Hamming cube with a Lipschitz class; §2.3 and §2.4 say what we can and cannot say
   for a Gaussian reference.

## 2. Statements that transfer

**2.1  The non-adaptive exponent is a worst-case relative entropy [P; may already be in the archive, not
searched].**  For `ψ` `u`-Lipschitz let `μ_ψ ∝ e^{−ψ}` on the cube.  Then

    max_ψ KL(μ_ψ ‖ U) = n·a(u),        a(u) = KL(Bernoulli(p_u) ‖ Bernoulli(½)),   p_u = 1/(1 + e^u),

with equality for `ψ = u·`(Hamming distance to a point).  *Proof.*  Given the other coordinates, `x_i` is
Bernoulli with parameter in `[p_u, 1 − p_u]` (the two energies differ by at most `u`), so
`H(X_i | X_{−i}) ≥ H(p_u)`; by the chain rule and since conditioning reduces entropy,
`H(X) ≥ Σ_i H(X_i | X_{−i}) ≥ n·H(p_u)`.  ∎  [N: on `Q_10`, 300 random Lipschitz energies per slope, the
largest value is `n·a` to five digits, attained by cones.]
With the archive's theorem `c_1(u) = a(u)` [K: lower bound machine-checked, upper bound a paper proof] this
reads: *for reweighting from the uniform reference to an unsampled `u`-Lipschitz target, the minimax number
of draws for bounded accuracy at fixed confidence — over all estimators and all non-adaptive designs — is
`e^{n·max KL(target ‖ reference)(1+o(1))}`.*  The threshold `e^{KL}` of Chatterjee and Diaconis for the plain
importance-sampling average is thus minimax-sharp on this class.  It is **exponentially smaller than the
second-moment threshold**: for the cone, `(1/n)·ln ∫(dμ_ψ/dU)² dU = ln(2(1 + e^{−2u})/(1 + e^{−u})²)`, i.e.
`0.194` against `a = 0.111` at `u = 1` (`0.058 / 0.030` at `u = ½`, `0.457 / 0.328` at `u = 2`).  So for an
unsampled state the natural extension of your resistance to a pendant node, `χ²(p_t ‖ mixture)`, is not the
sample-complexity exponent for a fixed-confidence guarantee.  Your D1 is not affected: there every state
is sampled.

**2.2  A cap on what an unvisited region can hold, and its threshold [K + P].**  Let `ψ` be `u`-Lipschitz,
`S` a set of points with `U(S) ≤ U(`Hamming ball of radius `ρn)`, and `ψ ≥ b` outside `S`.  Then

    2^{−n} Σ_{x∈S} e^{−ψ(x)} ≤ e^{−b}·E_U[e^{u·dist(x, S^c)}; S] ≤ e^{−b}·(n+1)·e^{u}·e^{n·D(θ)},      θ = KL(ρ ‖ ½) ≤ a,

`D(θ) = u·ρ − Λ₁`, `Λ₁ = ln(2/(1 + e^{−u}))`.  (First inequality: Lipschitz.  Second: by Harper's
vertex-isoperimetric theorem the depth `dist(·, S^c)` is stochastically largest for a ball, and for a ball
the sum over radii is a one-line computation; `D` is the archive's function.)  `D` is decreasing with
`D(h) = 0`, `h = KL(κ ‖ ½)`, `κ = Λ₁/u`: **against a flat background at the level `b`, a region of reference
probability below `e^{−nh}` cannot change `A(ψ)` by a constant factor; one of probability `e^{−nθ}`, `θ < h`,
can change it by the factor `e^{nD(θ)}`**, and the cone cut at radius `ρ` does.  (If the background is not
flat, the bound is still the displayed one, relative to `e^{−b}`.)  `h` is the exponent with unrestricted adaptivity [K: Theorem 11.25, lower
bound machine-checked].

**2.3  The same cap in Gauss space [P].**  Let `γ = N(0, I_d)`, `ΔU` `L`-Lipschitz (Euclidean), `S` measurable
with `γ(S) = Φ̄(t)`, `ΔU ≥ b` outside `S`.  Then

    ∫_S e^{−ΔU} dγ ≤ e^{−b} ∫_S e^{L·dist(x, S^c)} dγ ≤ e^{−b} ∫_t^∞ e^{L(x−t)} φ(x) dx = e^{−b}·e^{L²/2 − Lt}·Φ̄(t − L),

with equality for a half-space and `ΔU = b − L·(x₁ − t)₊`.  (Layer-cake formula and the Gaussian
isoperimetric inequality, `γ((S^c)_s) ≥ Φ(Φ^{−1}(γ(S^c)) + s)`.)  The bound is dimension-free.  For `t ≥ L` it is
at most `1.3·(t + 1/t)·γ(S)` (Mills ratio); for `t < L` it lies between `½` and `1` times `e^{L²/2 − Lt}`, which
reaches `1` at `t = L/2`, i.e. at `γ(S) = Φ̄(L/2) ≈ e^{−L²/8}`.  This is an explicit answer, under a Lipschitz hypothesis on the energy
difference, to the limitation recorded in your §F ("a hidden … region absent from all samples"): how
much such a region can contribute is bounded in terms of its reference probability, and the bound is
attained.  It does not make the hypothesis observable.

**2.4  A two-point lower bound in your oracle model, unsampled target [P].**  One coordinate suffices.
Reference `γ = N(0,1)`; targets `ΔU_B(x) = −L·x₊` and `ΔU_A(x) = −L·min(x₊, L)`, both `L`-Lipschitz, equal on
`{x ≤ L}`.  `N` i.i.d. draws from `γ` all lie in `{x ≤ L}` with probability at least `1 − N·Φ̄(L)`, and then the
data (points and energies) are identical.  `Δf_A − Δf_B = ln(Z_B/Z_A) ∈ [0.47, ln 2]` for `L ≥ 3` [N: `0.473`,
`0.520`, `0.571`, `0.599` at `L = 3, 4, 6, 8`].  Hence for every estimator

    max over the two targets of  P[ |estimate − Δf| ≥ 0.23 ]  ≥  (1 − N·Φ̄(L))/2 :

with fewer than about `L·e^{L²/2}` reference draws no estimator of the free energy of an unsampled
`L`-Lipschitz target is accurate to `0.23` with probability above `½ + o(1)`.  `L²/2 = KL(N(L,1) ‖ N(0,1))`, and
`L²/2` is the largest relative entropy of a target from `γ` over all `L`-Lipschitz `ΔU` (log-Sobolev
inequality), so this is 2.1 in Gauss space.  On these two targets the plain reweighting average is
accurate from `e^{L²/2 + O(L)}` draws (Chatterjee–Diaconis); whether it is so uniformly over the Lipschitz
class we have not checked.  The archive's theorem is the cube version, with both bounds, the lower one
valid for arbitrary non-adaptive point sets.
*A compact form of 2.1–2.4* [K on the cube; P for the half-space examples; **C** as a general principle]:
if `Λ(u)` is the log-moment generating function of the "distance" under the reference and `I` its rate
function, then one-shot reweighting costs `I(Λ′(u))` (tangent) and exploration with adaptive redesign costs
`I(Λ(u)/u)` (chord).  Cube: `Λ′ = p_u`, `Λ/u = κ`.  Gauss: `Λ = L²/2`, so `L²/2` against `L²/8`.

**2.5  Stages of adaptive design [K, ours].**  When the references may be redesigned after seeing energies,
the exponent on the cube drops from `a` (one stage) to `h` (unrestricted) — `0.111` to `0.029` at `u = 1`.  Two
stages are strictly worse than `h` [K: Theorem 11.86]; three stages reach `h` for every energy that depends
only on the numbers of ones in the classes of an unknown partition into boundedly many classes [K: our
Theorem H6, a paper proof reviewed once by an AI session]; for general Lipschitz energies this is open.
In Gauss space we have proved nothing of this kind.  The single example of 2.4 is easy — a draw in
`{x > L/2}` (probability `≈ e^{−L²/8}`) shows the slope, and a second stage of shifted references `N(s, 1)`,
`0 ≤ s ≤ L`, covers the target — but it is one example, not a class.  If your "full optimal sequential
allocation" is taken in a low-overlap regime, the phenomenon to expect is that the *number* of stages
matters at the level of exponents, which a two-stage pilot-then-allocate analysis at CLT scale cannot see.
That is a remark about regimes, not a theorem in your model.

**2.6  Effective resistance in the exponential regime is a bottleneck path [P, elementary].**  Let a
connected graph have conductances `ℓ_e = e^{−n c_e}` up to factors polynomial in `n`.  Then
`(1/n)·ln R_{ab} → min over paths from a to b of max_{e on the path} c_e`.  (Upper bound: the resistance of the
best path, by Rayleigh monotonicity.  Lower bound: the edges with `c_e ≥` that value form a cut, and
`R_{ab} ≥ 1/Σ_{cut} ℓ_e` by Nash-Williams.)  In your D1 class with shared masses `w_e = e^{−n c_e}` the number of
draws needed for a non-trivial error is therefore `e^{n·(bottleneck cost)}`: in that regime the overlap
geometry reduces to the worst edge of the best chain, and inserting states is a bottleneck-path design
problem.

## 3. Connections we examined in the other direction and reject

The owner asked whether your techniques give a new attack on the finite-round hierarchy where hidden-block
constructions failed.  In this pass: no.

1. *A graph of revelations (the pattern of your D1).*  Hidden objects arranged on a graph, each learnable
   only after a neighbour, would force as many rounds as the graph distance.  For boundedly many hidden
   objects this is excluded by our Theorem P whatever the graph: once two successive batches have seen
   nothing finer than what they learned, what remains hidden carries at most `e^{n(h−θ)}` of the visible
   mass.  The chain of three blocks was the path graph.
2. *Many hypotheses (Fano, Assouad).*  In the query model the scarce resource is not the information per
   answer — an answer is an exact real number — but the probability of placing a point where the answer is
   informative.  Multiplying the hidden objects dilutes the later batches and is paid back exactly by the
   multiplicity the special object must outweigh (our Proposition C).  We see no way for a counting
   argument to gain.
3. *Thermodynamic length.*  The archive's nested levels approach `h` like `c_*²/k²`, and the cumulative error
   of a chain of `K` bridging states behaves like (length)²/`K`; we tested whether `c_*²` is half the squared
   Fisher–Rao length of a path of tilts.  It is not: `c_*² = 0.0712` at `u = 1` [K: workstream Z,
   `c_*² = 2π²h²·θ_hint″(0)`, a tangency bottleneck of an iteration], against `0.0294`, `0.115`, `0.0283` for the
   three natural paths (`½ → κ`, `½ → p_u`, `κ → p_u`; a quarter of these if the steps were two-sided).  The levels of that law are adaptive stages, not a chain
   of overlapping states.  The two `1/k²` laws should not be identified.
4. *Posterior uncertainty and allocation under it.*  This is the accounting of our Proposition C in other
   words; it is neutral there.

What the general problem needs is described in our addendum §A5 and has no statistical counterpart that we
can see: an algorithm for energies without any hidden symmetry.

## 4. Where the items of §2 might be of use to you (suggestions, not requests)

* §F of your note, hidden regions: 2.2/2.3 turn "can defeat" into an inequality under a Lipschitz
  hypothesis, sharp in both geometries.
* Minimax theory outside the CLT regime, for states that are reweighted to but not sampled: 2.1 and 2.4
  give the exponent (relative entropy, not a second moment), with a two-point proof in your own oracle
  model.
* Overlap geometry at low overlap: 2.6.

## Assumptions and limitations

One pass, by one session, without review.  2.1, 2.3, 2.4 and 2.6 are short and should be re-derived before
use; 2.2 rests on Harper's theorem as quoted.  Everything about rounds is proved on the cube only.  We
read one file of your branch at one commit; if your own results change the picture, this note does not
follow them: this division does not poll other branches and does not resume when a message arrives.
