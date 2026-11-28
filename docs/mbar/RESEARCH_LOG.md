# Division 9 — research log

*Chronological record of the bounded research cycles of the single session of this division
(2026-11-28).  Times are not recorded per cycle; the order is the order of the commits of the branch.*

## Cycle 0 — orientation and set-up

Read the package (`README.md`, `proofs/MAIN_RESULTS.md`, `FABLE_TASK.md`, `results/EXECUTION_NOTES.md`,
the reference implementation and its benchmark), the master index of the consolidated archive
(`fe9f58c`), the collaboration protocol, ENG-MSG-0009 and the final report of the certified-inference
division.  Branch `research/phase2-certified-mbar` created on the theory head `b3c5d61`; the package
imported byte for byte (`PROVENANCE.md`).  Lean 4.31.0 and the Mathlib cache installed; NumPy, SciPy,
CVXPY, PyMBAR installed.  One background subagent for the prior-art search (`PRIOR_ART.md`).

## Cycle 1 — allocation theory (Priority A)

* Re-derived handoff A1/A2 from scratch; recognised the affine set as the set of gradients of the
  biased sampling model in the scaling `r_k = s_kφ_k`; wrote the dual formula, from which convexity,
  concavity of `1/V`, monotonicity and homogeneity are immediate; the minimax (Elfving-type) identity;
  the equivalence theorem and the efficiency certificate; rounding; the safeguard.
* Independent population code (`population.py`), four routes to the variance.  First surprise: the
  boundary.  With one coordinate of the allocation sent to zero the handoff's formula breaks down
  (five-state example, the value at exact zero being `0.8676269532`):

  | `s_k` | Laplacian route `cᵀL^+c − Σc²/s` | `J × J` dual | constrained least squares |
  |---|---|---|---|
  | `1e-2` | 0.8585064549 | 0.8585064549 | 0.8585064549 |
  | `1e-4` | 0.8675340947 | 0.8675340952 | 0.8675340952 |
  | `1e-6` | 0.8676256381 | 0.8676260245 | 0.8676260245 |
  | `1e-7` | 0.8702224290 | 0.8676268603 | 0.8676268603 |
  | `1e-8` | 0.8002439531 | 0.8676269439 | 0.8676269439 |

  This produced a wrong "optimum" (`DEAD_ENDS.md` E2) and led to Theorem A3(c), the cancellation-free
  formula valid on the closed orthant, and to the observation that optimal designs often drop states.
* MBAR solver checked against PyMBAR: free energies to `4.3·10⁻¹³`; the plug-in variance of Theorem A3
  on the fitted distributions reproduces PyMBAR's standard errors (`0.11826568949640705` against
  `0.11826568949641245`, and two further pairs to the same precision).

## Cycle 2 — certificates (Priority B)

* Audit of handoff B1–B5, C1–C3, G1, G2: constants recomputed; no error found.  C1's radius scales as
  `R/√N`: valid, wrong rate.
* The idea that carried the cycle: the reverse-logistic likelihood ratio is an e-value.  Under random
  labels this is universal inference; under *stratified* sampling the single factors are not
  e-values, but the product over a batch is, with expectation exactly `exp(−N·KL(s‖a))` (weighted
  AM–GM).  Generalised to any label predictor and any tilt.  Verified by exact enumeration before any
  simulation.  Consequences: a convex confidence region, anytime validity, adaptive allocation, a
  model check.
* First coverage benchmark invalidated by a solver flag (`DEAD_ENDS.md` E1); log kept; rerun.
* Local analysis of what the region loses (`R_c` against `V_c`) and of the tilt that would recover it
  (not built).

## Cycle 3 — information limits (Priority C)

* Handoff D1 re-derived (correct); D2 read only.
* Least-favourable submodel `dG_t = (1 + t h)dG` with `h` the dual maximiser: a finite-sample two-point
  bound with `V_c` at every instance; with the dual optimiser of the *design* problem the same
  argument bounds every adaptive strategy.  Exact checks of the divergence and separation.

## Cycle 4 — Lean

Standalone Lake project with the programme's pins.  Four modules, 49 headline declarations (50 after the review added `Model.Q_le_budget`); three
compile-fix rounds in total (noncomputable division; function-valued derivatives; a numeral cast).
The sharp third-moment bound and the integrated curvature of handoff B1 were formalised by calculus
(two monotonicity arguments), not assumed.  Audit passed.

## Cycle 5 — validation

* Allocation benchmark with actual errors: 400 replicates, then 2000.  Gains where predicted, none on
  the control.  Two post hoc variants after seeing that the equal-count pilot and safeguard waste
  budget on costly states (`DEAD_ENDS.md` N7, E5).
* Robustness: adaptive rounds with optional halting; trapped samplers and the model check (after
  fixing E3); correlated samplers.
* Correlated sampling at the population level: MBAR's variance is not convex in the allocation.
* Public data: PyMBAR's umbrella-sampling example.  The region is 5–7 times wider than the asymptotic
  interval at `K = 26`; this led to the sub-ladder restriction (Proposition B2′).

## Cycle 6 — synthesis, review, consolidation

* Read the cited sections of the three Phase II divisions; found the telescoping feasible point (path
  bound), the tempering-ladder corollary on the cube class, the round hierarchy of allocation, and the
  reading of the envelope-ratio cost as a χ².  MBAR-MSG-0001, MBAR-REQ-0001.
* One adversarial referee (subagent) on the mathematics note, the synthesis note and the code;
  findings and corrections in `REVIEW_A.md`.  Its main finding — false convergence of our solver on
  data with large energy offsets — led to a rewrite of the solver, regression tests, a re-run of the
  referee's scripts, a re-run or regression check of every stored benchmark with the same seeds (the
  2000-replicate allocation runs through their 400-replicate prefix; `VALIDATION.md` §7), and
  MBAR-MSG-0002.  While the review ran we
  found ourselves two ways an interval could come out too narrow and an ambiguous argument
  (`DEAD_ENDS.md` E6, E7).
* Final report, generated tables, consolidated archive.

## Cycle 7 — the other divisions' mail, and close

* With the final code every stored benchmark was re-run or regression-checked on the same seeds
  (`VALIDATION.md` §7); the comparisons are generated.  The referee's interval script was run over its
  whole case list on the final code (216 data sets, 1203 intervals, none too narrow, no exception); its
  witness search is slow, so the last 122 data sets were run in four parallel chunks.
* At the last fetch (08:53 UTC) the three other Phase II branches had moved: five messages addressed
  to this division (THY-MSG-0024, THY-MSG-0025, HIE-MSG-0003, ENG-MSG-0011, ENG-RES-0021), none seen
  before because this division did not poll while it worked.  Read in full; seven of their
  inequalities and numbers recomputed (`bench/check_inbound.py`, all in agreement); four remarks added
  to the mathematics note, three limitations to `DEAD_ENDS.md` (N18–N20), `SYNTHESIS.md` §S8, the reply
  MBAR-MSG-0003 with answers to the four questions of ENG-MSG-0011.
* The coordinator declined the computational proposal as premature and named local controls with
  correlated samplers first.  Decision of this session: **write the protocol, do not run it.**  ENG-MSG-0011
  reports that the usage counter of the account shared by the divisions stands near the owner's ceiling
  for Phase II; this session cannot see that counter, and the directive says to ask for renewed
  authorisation at a substantive checkpoint rather than continue.  `PROTOCOL_LOCAL_CONTROLS.md` is frozen
  with its predictions.
* An error of this session in the new check script (an upper Gaussian tail computed as `1 − Φ(8)`,
  which loses the digits; the other division's number 0.599 was right and ours 0.593 wrong) was caught
  by the comparison and corrected before anything was written.

## Subagents

Two, each for one bounded task with a written deliverable: the prior-art search (about 46 web calls)
and the adversarial review.  No other agent, session or scheduled task was started.
