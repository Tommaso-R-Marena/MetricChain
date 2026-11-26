# R10 — independent review and replication of the theory division's workstream Y (a known part with interactions along the chain)

*Science division, workstream R10.  Object: `docs/workstreams/Y_REPORT.md` of the theory division at commit `658b77f`
(read-only export), 612 lines, with `experiments/workstreams/Y/`.  Working directory of this review:
`experiments/science/ws_R10/` (scripts `r10_*.py`, logs `*.log`, running notes `NOTES.md`).*

**DRAFT IN PROGRESS — this file is written as the work proceeds; sections marked (pending) are not done yet.**

## 0. How far I got  (interim)

Done so far, all with own code written from the definitions of the report before opening any file of
`experiments/workstreams/Y/`:

* controls at `p = ½` (replicated to all printed digits);
* brute force of the reductions (U), (L), (L′) on 40 random inhomogeneous chains (no violation);
* exact enumerations `n ≤ 5` over all vertices (replicated; one sentence of §7.2 is wrong at `p = 0.4`);
* lower ends: `E_F`, Proposition H (replicated to all printed digits by two independent numerical methods);
* upper ends: the Markov recursion of Proposition F, `L = 1, 2, 3` (replicated to all printed digits); the tilt-state
  recursion of Proposition G with an own, cell-based safe discretisation (consistent with Y; validated against exact
  maxima on finite chains);
* (pending) Proposition I, sandwich `F^±_L`, quantile counterexample, the `(p,u)` map, the small-slope law and the second
  chain, prior art, reading of their code.

(The final version of this section, the verdict table and all later sections replace this draft.)
