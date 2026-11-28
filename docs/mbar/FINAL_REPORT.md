# Division 9 — final report

*Research owner's directive "MetricChain Phase II — Division 9: Certified Statistical Thermodynamics and
Optimal Molecular Simulation" (2026-11-28).  Branch `research/phase2-certified-mbar`.  Written by the
coordinating AI session.  The bounded objectives are complete as far as stated below; the division has
stopped and does not resume without authorisation.  The ten numbered sections are the ten deliverables
of the directive.  Every statement was produced and reviewed by AI sessions only.*

## 0. What to take away

* **The handoff's mathematics is sound.**  A1, A2, E2, B1–B5, C1–C3, D1, E1, E3, G1, G2 were re-derived
  with their constants and no error was found.  Its limits are real: its two observable certificates
  (C1, C2) are valid but far from the right rate, and its allocation evidence was population-level.
* **Allocation.**  The convexity theorem is the tip of a complete optimal-design theory for the biased
  sampling model: a dual formula, a cancellation-free variance formula that covers unsampled states
  and expectations, concave and superadditive precision, an Elfving-type identity for the optimal
  budgeted allocation, an equivalence theorem, a computable efficiency certificate, a monotone
  algorithm.  The ingredients are classical (Bennett; Hahn–Then for two states; Gill–Vardi–Wellner
  posed the design question in 1988); the multistate statements were not found in a bounded search.
  A pilot-based rule realises the predicted reductions of *actual* mean-square error on synthetic
  systems: 24 % (a weak link), 29–52 % (unbalanced overlap), factors 3–6 against equal counts when
  costs differ — and nothing on a well-designed ladder.
* **Certificates.**  A finite-sample confidence region for free energies, valid at every sample size,
  for all contrasts at once, at every round of an adaptive simulation, with no condition on the
  energies: a sublevel set of the MBAR objective.  It rests on one new lemma — the reverse-logistic
  likelihood ratio is an e-value under *stratified* sampling, with expectation `exp(−N·KL(s‖a))`.
  Measured: 100 % coverage in 2200 repetitions, 2.0–3.1 times the width of the asymptotic interval
  for up to ten states, 1.4–8.3 times narrower than the handoff's certificates.  It abstains by
  construction when supports do not connect, and it comes with a model check that detects a sampler
  inconsistent with its neighbours.
* **Limits of information.**  A finite-sample two-point bound of order `√(V_c/N)` at every instance,
  and a proof that no adaptive allocation strategy beats the optimal fixed allocation by more than a
  universal constant factor (locally, for budgets above a threshold): adaptivity is worth, up to a
  constant, the knowledge of the design.  That it is worth nothing more at the level of the leading
  constant is not proved.
* **The internal review changed the work.**  An adversarial AI referee with its own code found no
  false theorem and no wrong constant, but one serious defect in our code — the solver could report
  convergence at its starting point on data whose energies differ by tens of kT between states, giving
  silently wrong free energies and false rejections outside the range of our benchmarks — plus one
  statement false as written, an interface claim that was wrong, several overclaims and six loose
  numbers.  All are corrected and recorded (`REVIEW_A.md`, `DEAD_ENDS.md` E6–E14); the solver was
  rewritten, and the benchmarks were re-run or regression-checked with the final code
  (`VALIDATION.md` §7).  The corrected documents were not refereed again.
* **What it does not do.**  Everything assumes independent equilibrium samples.  Consistent trapping is
  undetectable from samples (a theorem here), an estimated correlation time is not a certificate
  (shown), the region is 5–7 times wider than the asymptotic interval at 26 states, and no experiment
  with a real sampler was run.  **Nothing here is a statement about a molecule.**

## 1. Complete corrected mathematical proofs

`MATHEMATICS.md`: the audit of every handoff statement (§B0, §C0) and proofs of all statements of this
division.  Corrections to the handoff: none to its mathematics.  Two corrections to how it should be
used: its variance formula `cᵀL^+c − Σc_k²/s_k` must not be evaluated near the boundary of the simplex
(it loses all accuracy; Theorem A3(c) replaces it), and its certificates C1 and C2 should be replaced
by the region of Theorem B2.  Handoff D2 was read and not reconstructed.

## 2. New mathematical results and their relation to prior art

| result | where | status | prior art (`PRIOR_ART.md`) |
|---|---|---|---|
| dual formula; `1/V` concave, superadditive | A2, A4 | [P], cores [V] | follows from known theory (information is additive; design theory); not found stated for MBAR |
| closed-orthant theorem; stable formula for any smooth functional; unsampled states | A3 | [P], [N] | not found |
| Elfving-type identity with costs; equivalence theorem; efficiency certificate | A5, A6 | [P], cores [V], [N] | known for `K = 2` (Bennett; Hahn–Then); the design problem was posed for this model by Gill–Vardi–Wellner 1988; general statement not found |
| iterated Neyman allocation is monotone; rounding; safeguard | A7–A9 | [P], [V] | Fellman's rule for c-optimality, transferred |
| correlated sampling: convexity fails for MBAR; three true statements | A11, A12 | [N], [P] | Hahn–Then note a related non-convexity for `K = 2`; not found for MBAR |
| stratified likelihood-ratio e-value; region; rounds and adaptive allocation; model check | B1–B3, B5 | [P], [V] fixed sample, Ville [X], [N] | random-label case is universal inference; the stratified identity and the application to free energies were not found |
| restriction to a sub-ladder | B2′ | [P] | elementary |
| impossibility under consistent trapping; thinning under β-mixing | B7 | [P] | elementary / known lemma |
| finite-sample two-point bound at every instance | C1 | [P], cores [V], [N] | asymptotic local minimax is known (Gill–Vardi–Wellner); finite-sample form not found |
| no adaptive allocation beats the static optimum by more than a constant factor (two-point, local) | C2 | [P], [N]; leading-constant version [C] | known in other models (treatment assignment, bandits); not found for this model |
| path / thermodynamic-length bound; ladder on the cube class; sampling lower bound | S1, S1′, S1″ | [P]; S1″ conditional on theory's Theorem 11.25 | thermodynamic length is a known heuristic; the non-asymptotic bound for MBAR was not found |
| round hierarchy of allocation (`1/K` for one round; at most a constant factor for any number) | S2 | [P]; two-round optimality [C] | not found |

"Not found" means not found in one bounded search by an AI subagent, with several primary sources not
opened (listed in `PRIOR_ART.md` §4).  The honest summary: **the allocation theory is the
optimal-design theory of a classical model, written out and made computable; the certificate is an
application of e-values with one new lemma; the lower bounds are finite-sample forms of a classical
bound.**  None is a new phenomenon.  What is new, if anything, is that the three fit together and are
usable.

## 3. Lean formalisations and verification logs

`experiments/mbar/lean/` — standalone Lake project, Lean 4.31.0, Mathlib `fabf563a` (the programme's
pins).  Four modules, 50 headline declarations, only `propext`, `Classical.choice`, `Quot.sound`;
`audit.sh` (token scan, build without warnings, axiom audit) passes; logs in `lean/logs/`.
Correspondence with the paper statements, and the list of what is *not* formalised (existence of the
Laplacian solution, measure theory, Sion, Ville, Pinsker, the chain rule, every imported
concentration inequality): `LEAN_CORRESPONDENCE.md`.  Formalised by calculus rather than assumed: the
sharp third-moment bound of handoff B1 (`Softmax.kappa_ge`, `Softmax.curvature_integrated`).  The
formal statements of the allocation theory are for strictly positive allocations and for contrasts;
the boundary cases, where optimal designs often sit, are paper proofs.

## 4. Reproducible implementation and benchmarks

`experiments/mbar/src/d9mbar/` (about 1000 lines), tests, benchmark scripts, stored results, generated
tables; commands in `README.md`.  The handoff's reference implementation is kept unchanged and is run
as a baseline.  The solver agrees with PyMBAR to `10⁻¹³` and, after its rewrite in response to the
review, is exactly equivariant under energy offsets up to 1000 kT per state (tested).

## 5. Genuine pilot-based allocation evidence

`VALIDATION.md` §3, tables T2–T4.  The allocation is computed from pilot data only (MBAR fit of the
pilot, fitted distributions, convex programme, 25 % safeguard); the comparison is of actual
mean-square errors of the final estimate over 2000 independent replicates at matched total cost,
against equal counts (standard PyMBAR practice), equal cost, the one-step Neyman rule, the resistance
criterion and the oracle design.  Result: the predicted gains are realised where they exist
(ratios 0.76, 0.90, 0.48, 0.71 with unit costs; 0.17 and 0.29 with unequal costs), not on the control
(0.92, not significant); the rule beats the one-step Neyman rule and the resistance criterion; with
unequal costs most of the gain is already in the equal-cost rule (0.18 and 0.32), and two variants
added after seeing this — a cost-aware pilot and an equal-cost safeguard — reach 0.14 and 0.23
against the oracle design's 0.12 and 0.21 (post hoc; to be confirmed on a frozen protocol).  No claim of simulation savings is
made beyond these synthetic systems.

## 6. Explicit scientific limitations and counterexamples

`DEAD_ENDS.md` (N1–N17, E1–E5).  The ones that matter most:

0. The first version of our own solver was wrong outside the range we had tested (review finding E1);
   it is corrected and tested, but the episode shows what our benchmarks did not cover: real data
   with large energy offsets were represented by one public data set only.
1. No guarantee without independent equilibrium samples; consistent trapping is undetectable (B7).
2. The certified region pays for `K`: 5–7 times the asymptotic width at 26 states (public data).
3. Under correlated sampling MBAR's variance is not convex in the allocation (counterexample stored).
4. With strongly correlated samples treated as independent (`φ = 0.99`) the region's joint coverage
   was 92 % — below nominal; an estimated statistical inefficiency does not repair the asymptotic
   interval (70–83 % coverage).
5. The efficiency certificate is valid but weak far from the optimum.
6. Two benchmark variants are post hoc.
7. The asymptotic efficiency of the two-stage estimator is not proved.

**Resources.**  Ceiling: $350 of Claude credits.  **This session cannot monitor its actual
expenditure**: no usage counter is visible to it.  The work was therefore bounded by construction: one
session; two subagents with one bounded task each (prior-art search; adversarial review); local
computation only, on four cores, a few CPU-hours in total; no Modal job and no external computation;
no request for computation was executed by anyone.  An order-of-magnitude self-estimate cannot be
given responsibly; the research owner's usage counter is the only reliable figure.  The division
stops here and asks for renewed authorisation before any further work (§9).

## 7. Cross-divisional mathematical synthesis

`SYNTHESIS.md`; sent as MBAR-MSG-0001.  Substantive: (S1) every path of states gives a bound on the
variance, because the telescoping tuple is feasible — a non-asymptotic thermodynamic-length bound;
on the programme's cube class a tempering ladder makes the certified free energy cost `O(u²n²/ε²)`
samples, so (conditionally on the theory division's Theorem 11.25) producing those samples costs
`e^{nh}` evaluations: *the exponent of the query model is a cost of sampling, not of estimation*, and
it complements the foundations division's Theorem E (samples of the target alone leave an exponent).
(S2) The round hierarchy of allocation is `1/K` for one round and at most a universal constant factor
for any number of rounds, against an exponential hierarchy in the query model; in both, adaptivity is
worth a hint about the design.
(S3) The envelope-ratio cost `Γ` of the certified-inference division is a χ²-divergence between the
sampled and the target law; a path replaces it by `(ln Γ)²`.  Interfaces only: simultaneous boxes
from our region as data regions for partial identification (S4; a first, stronger form of this claim
was wrong and is withdrawn — MBAR-MSG-0002); intervals for second moments and populations as inputs to
the geometric criteria (S5).

## 8. Publication candidates and outstanding obstacles

| candidate | content | obstacles |
|---|---|---|
| **P1. "Optimal allocation of samples in multistate free-energy estimation"** (methods; J. Chem. Theory Comput. / J. Chem. Phys.) | A1–A10, A11–A12, S1; pilot rule; benchmark | a specialist's prior-art check (design of case-control / multi-phase samples; Tan; Kong et al.); a real-sampler benchmark (MBAR-REQ-0001); a proof or a citation for two-stage efficiency |
| **P2. "Anytime-valid confidence regions for free energies from stratified samples"** (statistics / methods) | B1–B3, B2′, B5, B7; coverage benchmark | the safe-testing literature on fixed group sizes must be checked for the identity; the `K`-dependence (O3); nothing for Markov-chain data (O1) |
| **P3. a short note: "Sampling is the bottleneck"** (inside the programme's mathematics paper, or a remark) | S1′, S1″, S2 | conditional on Theorem 11.25; is the reduction already folklore in the query-complexity literature? |

None is ready.  P2 has the cleanest new lemma; P1 has the most practical content and the most prior
art to clear.

## 9. Recommendations for subsequent computational validation

1. **The decisive experiment** (MBAR-REQ-0001, not authorised, not run): alchemical hydration free
   energies with a real sampler, three allocation arms at matched GPU time, reference from long runs,
   success criterion fixed in advance (MSE ratio ≤ 0.85 with a 90 % interval excluding 1).  Expected
   about $80–$130 of Modal, cap $200; a pipeline pilot under $8.  It needs the research owner's
   separate authorisation.
2. Before it: freeze the protocol, including the cost-aware pilot and equal-cost safeguard that were
   introduced post hoc here, and confirm them once on fresh synthetic seeds.
3. For the certificate: the same runs answer how the region and the model check behave on correlated
   data after thinning; a rejection rate above 5 % in converged runs would be a finding against it.
4. Mathematics worth one more bounded cycle: O1 (a contraction-based e-value for Markov chains), O3
   (a contrast-specific certified interval without the `K`-dependent threshold), and the efficient
   tilted region (O2).

## 10. Consolidated archive

`experiments/mbar/build_zip.sh` builds `division9_certified_mbar.zip` from the tracked files of this
division (documents, mailbox, code, tests, results, data, Lean sources and logs, the handoff package)
with a SHA-256 manifest; the archive is reproducible from the commit and is not committed to the
repository (its manifest is: `experiments/mbar/ZIP_MANIFEST.sha256`).
