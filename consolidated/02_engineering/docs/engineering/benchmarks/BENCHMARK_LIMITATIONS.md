# Benchmark limitations

What the benchmarks of this branch do **not** show.  Kept per campaign; a limitation is
removed only when a recorded result removes it.

## General

* A benchmark is evidence about the instances and sizes that were run.  It proves no
  theorem and refutes one only by an explicit counterexample that satisfies the
  theorem's hypotheses — which is then reported as such, with the instance.
* The internal reviews quoted here (the theory division's referees, the science
  division's reviews, subagents of this division) are reviews by AI systems inside one
  programme, not external peer review.
* One machine and one library version for the local runs; Modal containers for the
  remote ones.
* **A search that stops low looks like a property of the problem.**  When two searches
  over equal or nested families are compared, the maximiser of each is evaluated under
  the other objective before their difference is read; a difference that survives is
  reported with both cross-evaluations.  (Rule adopted after the science division's
  review SCI-REV-0018 showed that a difference we had published was the shortfall of
  one search: ENG-RES-0017.)

## BM-1 — nested adaptive algorithms on `L_u(Q_n)`

* **Model.**  Costs on instances are computed in the *mean-run model*: every random
  count is replaced by its expectation.  Literal runs with real fluctuations exist for
  two levels only (X-006b: no failure in 585 000 runs with the theorem's constant) and
  not at all for nested runs.  A cost in the mean-run model is not a bound on the cost
  of a run; the certified bound `C_max` is.
* **Worst cases are searches.**  "Worst instance found" is the cost of one instance — a
  lower bound on the worst case of a design, within the instance families searched
  (radial outer landscapes with eight knots, monotone or general; fibres flat or cones;
  inner answers of base brackets either their own, or at an end of the promised
  bracket).  ENG-RES-0014 §4 bounds what instances that are not products can add for
  two levels with uniform inner behaviours *in the mean-run model, at the same law and
  the same reference value, inside the range condition* (the qualifications of
  SCI-REV-0018, m3, m4); nothing bounds it for nested runs.  **The search of X-005 was
  not converged at `n ≤ 500`** (shortfalls up to about `0.02` in units of `n a`, found by
  that review; re-searched in X-005c with starting points that place the reference
  point behind a ramp).  The searches of X-010 and X-011 use the same family and the
  earlier starting points and have not been repeated.
* **Design families are finite.**  "The best certified bound with `k` levels" is the
  minimum over the candidate designs listed in `certified.py` (two families) and a grid
  of outer fractions, with the top level fixed (`b = 0.5`, `λ = 0.2`, `η = η′ = θ = 0.05`,
  40 rungs).  A lower value may exist outside the family; no claim of optimality is made.
* **One class.**  The uniform cube, one slope for every coordinate, the uniform
  reference measure, exact evaluations.  Nothing here speaks about heterogeneous slopes,
  other alphabets, dependent reference measures or continuous variables.
* **Accuracy.**  One certified accuracy (`0.8715`) and one failure probability (`0.05`).
* **Sizes.**  The exponent of Theorem 11.58a is approached, if at all, at sizes far
  beyond those where designs can be evaluated; a finite-size table cannot confirm an
  asymptotic law and is not read as doing so.

## BM-2 — certificate kernel for minimisation

* The certificates checked so far were produced by another division for its own
  instances; this branch has no producer yet, hence no statement about production cost.
* An accepted certificate proves a bound for the *published integer instance*; the link
  from that instance to a real-valued model is a separate (paper) lemma of its authors.

## BM-4 — chain covers

* Off-lattice results rest on floating-point comparisons with a tie analysis; they are
  on hold beyond 12 torsions until the chain exists in exact arithmetic (R7-ENG-3).
* Ten of 25 open lattice brackets have a lower end that is a solver's bound, not a
  certified one (ENG-MSG-0004 §4).

## BM-7 — software of the structural-biology division

* Nothing has been received (the branch did not exist on 2026-11-26 22:03 UTC), so
  nothing has been verified.  The procedure is in `BENCHMARK_MASTER_PLAN.md` §3a.
* No component of this branch proves the step from a real-valued energy to the rounded
  integer tables that the certificate kernels check; until one does, "certified" in any
  application statement means "certified for the published integer instance".

## Withdrawn or corrected claims of this branch

Listed, with the messages that corrected them, in `../DEAD_ENDS.md` and ENG-MSG-0004 §4
(five corrections: the sampler of X-006; the two-solver validation; "certified lower
bound"; "decays like `1/√n`"; three numbers computed from rounded entries).  Since then:
**ENG-RES-0017** withdraws the conclusion of ENG-RES-0014 §4 that instances which are not
products cost no more than the worst product instance *found* (the excess was the
shortfall of the product search), and corrects seven sentences of ENG-RES-0014 §§1, 4
and the worst-instance entries of ENG-RES-0008 at `n ≤ 500`.
