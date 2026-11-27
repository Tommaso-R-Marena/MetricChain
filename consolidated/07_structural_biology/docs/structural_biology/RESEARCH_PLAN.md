# Research plan of the Structural & Computational Biology division

*Version 1, 2026-11-26.  A living document: consequential changes of priority are entered at
the end with their reason.*

## 1. The question

"Can MetricChain's mathematics produce computational structural biology methods that are
demonstrably more rigorous, informative, reliable, efficient, or practically useful than
established alternatives?" (founding directive §5).  Four kinds of improvement are kept apart
in every claim: computational, mathematical, scientific, methodological.

Position after the first intake (`RESEARCH_INTAKE.md`): the programme has machine-checked
certificate kernels and no producer; the science division has certified brackets on synthetic
peptides and no file format, no independent checker and no real structure; nobody has run
anything on a deposited protein.  The most direct contribution available to this division is
therefore to *build the producers and the path from a public structure to a published
instance*, and to find out — with fair baselines — whether a certificate buys anything.

## 2. Capabilities, in priority order

| # | capability | workstreams (directive §7) | kind of improvement it could show | state | next step |
|---|---|---|---|---|---|
| C1 | certified global minimum of a fixed-backbone rotamer model | B, G | mathematical (certified optimality), methodological (checkable output) — **not** computational (toulbar2 is faster) | implemented; six development structures at zero gap | independent verification and held-out run by engineering (STRUCTBIO-REQ-0001); proof-logging comparison |
| C1b | certified per-residue flip gaps; gap to the second-best conformation | B, E | scientific (which parts of a conclusion the model supports, and by what margin); robustness to rounding and to bounded model error | designed | implement on top of C1 (restricted boxes); development run |
| C2 | certified partition function, free energy, rotamer populations | A, F | mathematical (two-sided certified enclosures; nothing found in print for populations), scientific (reference values for uncertified inference) | under construction; obstruction measured (RESULTS R-3) | exact and outward-rounded elimination engine with certificate and checker; crambin and local ensembles first; Lean file for the four rules |
| C3 | partial identification of ensemble weights on a finite conformer library | C | scientific (what averaged data do and do not determine); mathematical (exact dual certificates) | not started | read ENSEMBLE-MSG-0006 and the science division's Theorem 8; exact-rational linear programming with Farkas and dual certificates |
| C4 | geometric observability analyser | D | methodological (flag what a pattern of distance data cannot determine) | not started | read GEOMETRY-MSG-0005–0008; instance-specific rank tests from `geomlib` |
| C5 | residual-class certificates on real energy terms | A, E | — | **blocked**: no certified constant for any real energy term exists | revisit only with interval evaluation of a force-field term |

Workstream E (physical applicability) is not a capability but a register kept with every one:
`PHYSICAL_APPLICABILITY.md`, `ASSUMPTION_REGISTER.md`, and the four-line error budget.
Workstream F (complexity-aware design) enters C2 directly: exact where a tree decomposition
is affordable, bounded where not, abstention where neither — decided per instance and
reported.

## 3. Why this order

* *Mathematical maturity.*  C1 rests on a kernel that is machine-checked and has a reference
  checker; C2 on kernels that are machine-checked for chains and need four more rules; C3 and
  C4 on theorems whose translation to real observables their own authors call open.
* *Verification feasibility.*  C1 and C2 have exact ground truth by enumeration on small
  instances and an established exact solver as an oracle.
* *Novelty risk.*  Honest reading of `PRIOR_ART.md`: C1 re-implements known technology in a
  new format; C2's certified populations were not found in print; C3 has a named predecessor
  (maximum occurrence).  The order follows value, not novelty.
* *Risk that key assumptions fail.*  For C2 the risk has materialised at the size of
  ubiquitin (RESULTS R-3) and is being handled by narrowing the claim (small proteins, local
  ensembles) and by asking the theory division a precise question (Q-5).

## 4. What would make us stop or change course

* An unsound acceptance by our checker: everything stops until it is understood.
* The engineering division's independent checker disagreeing with ours.
* A held-out certified fraction below one half for C1: the producer, not the idea, would need
  replacing (toulbar2's search with our certificate).
* For C2: if neither a second-order bound nor larger tables arrive, the capability is
  restricted to what can be certified (and said so), and the measured obstruction is the result.

## 5. The cycle

Synchronise read-only with the seven other branches → read what is addressed to us → pick
the most consequential open item → specify → test first → implement → adversarial review →
record (results, dead ends, registers) → requests to engineering and science → commit and
push → next item.  A request sent is not a reason to wait.

## 6. Changes of priority

*2026-11-26.*  C1b inserted before C2's protein-scale work: it needs only C1, gives the first
certified statement that no uncertified solver gives, and supplies the rounding-robustness
margin that the error budget lacks.
