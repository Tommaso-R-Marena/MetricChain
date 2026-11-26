# Baseline specifications

A baseline is fair if it solves the *same task* (same quantity, same accuracy, same
failure probability), has the *same access* to the instance (here: evaluations of the
energy at chosen points, nothing else unless the benchmarked method also has it), and
is charged in the *same unit*.  Weak baselines are not used; where the strongest known
baseline is a lower bound that no algorithm can beat, it is reported as such.

## BM-1 — nested adaptive algorithms on `L_u(Q_n)`

Task: a bracket of `ln Z` of width at most `x` (certified accuracy `0.8715` for the top
design used throughout), valid with probability at least `1 − δ` (`δ = 0.05`) for every
`u`-Lipschitz energy on the `n`-cube; unit of cost: number of evaluations, in every run.

| baseline | definition | status of the number |
|---|---|---|
| **enumeration** | all `2ⁿ` points; `ln cost = n ln 2`, i.e. `ln 2/a = 6.25` in units of `n a` at `u = 1` | exact |
| **non-adaptive base bracket** (Proposition K0 in the whole dimension) | two uniform samples of prescribed size; `certified.k0_lcost(n, u, x, ln(1/δ))` | exact cost of that procedure; its exponent tends to `a` (`1.0` in the units used) |
| **non-adaptive lower bound** | Theorem 11.45(b): `(1 − 2δ)·2ⁿ/|B(n, R − 1)|` (X-009) | a bound for every non-adaptive algorithm |
| **lower bound for every algorithm** | the hinted bound, `alg2l.hinted_lower_bound(n, u, x, δ)`; exponent `h` (`h/a = 0.2626` at `u = 1`) | a bound (machine-checked on the theory branch) |
| **two levels, flat-tuned** | Algorithm 2L⁺ with base brackets, outer fraction chosen at the flat instance | ours (X-005, X-010) |
| **three levels, flat-tuned** (the referee's design) | servers chosen by their cost at the flat fibre (ENG-RES-0014) | ours (X-010); the design the certified-cost designs are compared with |

Not a baseline here: Monte Carlo estimators without a certificate — they solve another
task (no guarantee over the class), and on the hard instances of this class (a hidden
well in a flat landscape) they return a wrong answer with high confidence.  Where a
report mentions them it says so.

## BM-2 — certificate kernel for minimisation

Task: prove `min_x E(x) ≥ L` for a pairwise integer instance on a box.  To be specified
before stage D; candidates, each to be implemented or taken from a maintained solver and
charged *both* its run time and the fact that it leaves no checkable proof:
exhaustive enumeration (exact, the ground truth of stage B); dynamic programming on
chains and trees (exact where it applies); a branch-and-bound with the same LP bound but
no certificate output; CP-SAT (OR-tools 9.15, installed) as an exact solver with a proof
log that is not checkable by our kernel.  The quantities compared: time to produce,
size of the certificate, time to check, against time to solve without a certificate.

## BM-3 — certificate for partition functions

To be specified after stage A.  Ground truth: transfer matrix on chains (exact rational
or interval arithmetic).  Non-certified comparators: annealed importance sampling and
thermodynamic integration with standard error bars — to be reported as *what they
claim* against *what is true*, at matched evaluation counts.

## BM-4 — chain covers

Ground truth: exhaustive enumeration with exact integer covers (lattice).  Comparator
for the limit shape: the closed-form prediction of the theory report §11.22 at the same
`n`, with the finite-size correction it states (if any).

## BM-6 — beyond product measures

Comparator: the same three exponents for the uniform cube (closed forms in
`tables.cube_constants`).
