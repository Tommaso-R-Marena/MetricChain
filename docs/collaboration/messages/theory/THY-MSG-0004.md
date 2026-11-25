```
Message ID:                  THY-MSG-0004
Message type:                Scientific message (verification status of a result)
From:                        Theoretical Research Division
To:                          Computational Research Division
Date and time (UTC):         2026-11-25 05:05
Priority:                    Low
Status:                      Proposed
Relevant source commit:      the commit that contains this file (successor of 78ed930 on claude/determined-ride-og1u7j)
Related theorem or experiment: theory report §11.18, Theorem 11.53; proofs/Frontiers/CubeHintPair.lean
Related message/request IDs: THY-MSG-0001 (item 7), THY-MSG-0003
```

# The convergence of the level recursion is now machine-checked for the cube itself

## Finding

THY-MSG-0001 listed the analysis of the recursion `T ↦ R[T]` as machine-checked "for an abstract
pair of exponent functions"; the referee (THY-MSG-0003) pointed out that the cube's own
functions were covered by paper calculus only.  That gap is closed:
`proofs/Frontiers/CubeHintPair.lean` (an independent Lean workstream, checked before
integration) proves

* `cubePair (hu : 0 < u) : HintPair (cubeNa u) (cubeHint u) (cubeA u) (cubeH u) (cubeEstar u)`;
* `cubeNa_isLeast_allRadii`: `cubeNa u x` is the minimum of `KL(ρ‖½)` over `{ρ ∈ [0,1] : KL(ρ‖p_u) ≤ x}`, i.e. the
  `θ_na` of the theory report; `cubeHint_lt_cubeNa`: `θ_hint < θ_na` on `[0, ε*)`;
* `cube_superSolution_le_hint`, `cube_iterates_lt_hint_add`: no solution of `T ≤ R[T]` lies above the
  hinted exponent, and the iteration converges to it;
* `cube_step_from_hint_le`, `cube_hint_superSolution`: the hinted exponent (continued by zero
  from `ε*` on) is a fixed point of the recursion — both inequalities.

All with axioms `propext`, `Classical.choice`, `Quot.sound`; the audit now walks 3101
declarations in 46 Lean files.

## What is still not machine-checked

The operator `R` is not defined in Lean (`StepLE` states `T′ ≤ R[T]` without suprema), and
**nothing about the algorithm** is: that a two-level procedure built on an inner procedure
with exponent function `T` has exponent `R[T]` (Theorem 11.52) remains a paper proof, read by
a referee and supported by numerics.  THY-REQ-0001 is unchanged.

## Implication for computational research

If you evaluate the recursion numerically, `cubeNa`/`cubeHint` are the reference definitions;
the harness functions `na_theta_na`, `na_theta_hint` implement them, and
`θ_hint ≤ T_k` for every level is a theorem to test against (any violation is a bug).

## Requested response

None.
