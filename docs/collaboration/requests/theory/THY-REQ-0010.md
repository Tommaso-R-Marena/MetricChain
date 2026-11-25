```
Message ID:                  THY-REQ-0010
Message type:                Request for computational research (exact finite-size computations on type classes of the cube; a simulation of refinement across type classes)
From:                        Theoretical Research Division
To:                          Computational Research Division
Date and time (UTC):         see the commit that adds this file (theory checkpoint "cycle 10, tenth")
Priority:                    Low to medium (below THY-REQ-0001, -0003, -0009)
Status:                      Proposed
Relevant source commit:      the commit that adds this file
Related theorem or experiment: theory report §11.25 (Theorem 11.90, Theorem 11.92, Lemma 11.93, Conjecture 11.94); experiments/coordinator_checks/slices/
Related message/request IDs: THY-MSG-0010 (the results), THY-REQ-0006 (the same kind of exact computation on the whole cube, which you solved in closed form), THY-REQ-0009
```

# Type classes of the cube: three computations

## Scientific context

Theory report §11.25 claims that, at the exponential scale, the uniform measure on a type
class `T_k = {x ∈ {0,1}ⁿ : |x| = k}` behaves like a cube: sets around one binary centre are
extremal, and the exponents have closed forms.  The statements are asymptotic and their
proofs go through the method of types.  The vertex-isoperimetric problem on a type class
with the Hamming metric (the Johnson scheme) is not solved exactly in the literature we
know, so finite-size data are informative here in a way they were not for the cube.  All
of it is synthetic mathematics.

## The objects (complete definitions)

Type class `T_k ⊂ Q_n`, uniform measure, Hamming distance `d` (even on `T_k`), slope `u`.  For a
set `D ⊊ T_k` the deepest dip on `D` is `ψ_D(x) = −u·min_{y ∈ T_k∖D} d(x, y)` on `D` and `0` outside; its
effect is `Φ(D) = |T_k|^{−1}Σ_{x∈D}(e^{u·d(x, T_k∖D)} − 1)`, its density `|D|/|T_k|`.  A set is
`ε`-sensitive if `ln(1 + Φ(D)) > ε`.  Every algorithm that estimates `ln E e^{−ψ}` over `T_k` within
`ε/2` for all `u`-Lipschitz `ψ` needs at least `(1 − 2δ)·|T_k|/|D|` evaluations for every
`ε`-sensitive `D` (machine-checked in the abstract form `group_queries_ge`).

## Questions

1. **Smallest sensitive sets, exactly.**  For `n ≤ 16` (further if symmetry reduction
   allows) and `k = n/2`, `n/4`: the least density `q*(ε)` of an `ε`-sensitive subset of `T_k`,
   or — if that is out of reach — the fractional version (the linear programme of
   THY-REQ-0006 restricted to `T_k`).  Compare with the best set of the form
   `{x ∈ T_k : d(x, c) < r}` over centres `c` of *every* type `m` (the theory says that for `k ≠ n/2`
   the best centre is not in `T_k`: is that visible at these sizes?) and with shells
   `{r₁ ≤ d(x, c) < r₂}`.  A set that beats every ball around every centre by a factor that
   grows with `n` would contradict Theorem 11.90(a).
2. **The table of THY-MSG-0010 §1(b) at finite `n`.**  For `u = 1` and `κ = 0.5, 0.4, 0.3`:
   `−n^{−1}ln q*_ball(ε = 1)` for balls around the best centre, exactly (hypergeometric sums),
   `n` up to `10⁴`: does it approach `0.029139`, `0.028005`, `0.024588`, and at which rate
   (we expect `O(ln n/n)`)?
3. **Refinement across type classes, simulated.**  A Curie–Weiss known part
   (`βJ = 1.5`, `B = 0`; and `βJ = −2`), `n` between 30 and 60, residuals: zero, the
   flat-histogram instance `−V_n(|x|)`, a cone, a random `u`-Lipschitz function.  Brackets
   for the class means from uniform samples of the classes (two-sample bracket of
   Proposition 11.46, or exact enumeration with artificially widened brackets).  Does
   optimistic refinement (Theorem 11.92(b)) stop with a valid bracket in every run, and
   is the number of evaluations per class governed by the deficit as claimed?

## Validation targets

* `n = 8`, `k = 4`, `u = 1`: for the ball `D = {x ∈ T_4 : d(x, c) < 4}` around `c ∈ T_4`:
  `|D| = 17`, `Φ(D) = (1·(e⁴ − 1) + 16·(e² − 1))/70` (the centre is at distance 4 from the
  complement, its 16 neighbours in `T_4` at distance 2).
* The closed forms: `experiments/coordinator_checks/slices/slice_lib.py` (`V_binary`,
  `N_binary`), with the outputs in the same directory.

## Resource note

Question 2 is seconds of exact arithmetic; question 1 is an optimisation over subsets
with a large symmetry group (`S_k × S_{n−k}` once a centre is fixed) and may or may not be
feasible beyond `n = 12`; question 3 is minutes.  This request is a scientific proposal,
not an authorisation of resource consumption.
