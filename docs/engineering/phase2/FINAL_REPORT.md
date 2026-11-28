# Phase II of the Computational Research Division — final report

*Research owner's directive D-11 ("MetricChain Phase II — Constructive Mathematical Synthesis, Certified
Inference and Computational Validation").  Branch `research/phase2-certified-inference`.  Written
2026-11-28 by the coordinating AI session.  The phase is complete; the division has stopped and does not
resume without authorisation.  The seven numbered sections are the seven deliverables the directive asks
for.*

## 0. What to take away

* **The proposed theorem S3 is correct, under five assumptions it does not state, and it is the wrong
  tool.**  Compressing the whole moment body buys nothing that one certified expectation does not buy
  better.  In the validation S3 never gave a wrong interval and, beyond an envelope ratio of about 3,
  never gave a useful one.
* **Two capabilities are demonstrated, on synthetic models only.**  (1) A valid interval for an ensemble
  average under an energy known only within an envelope, with measured averages taken into account,
  certified from samples: no invalid bound in 44 160 benchmark repetitions, and within 2 to 7 % of the
  exact interval at 10⁵ draws for envelope ratios up to 100.  (2) For energies whose error has bounded
  influence per site, exact intervals for additive observables at any system size, where every
  rectangular envelope is vacuous.
* **The independent review changed the picture.**  Two claims of the first version were wrong and are
  withdrawn; six of thirteen pre-registered predictions were refuted; one baseline had been biased in our
  favour by a defect.  All of this is recorded, and the best new result — sampling the worst-case
  ensemble removes the cost in the envelope ratio — came from the referee's objection.
* **Nothing here is a statement about a molecule.**  An interval is exactly as good as its envelope, and
  no envelope between a force field and nature is known.
* **Resources:** about $253 of the $500 Claude ceiling (an upper bound, see §6); $0 of the $25 Modal
  ceiling; nothing running.

## 1. New mathematical results and proofs

All in `CERTIFIED_INFERENCE.md` (second version).  Status: paper proofs; none machine-checked.  The first
version was refereed adversarially by an independent subagent with its own code (`REVIEW_A.md`); the
corrections and Theorem 5.4 have not been refereed again.

| result | what it says | origin |
|---|---|---|
| Theorem 2.2, Proposition 2.3, Corollary 2.4 | S3 holds with its constant under H1–H5 (observables scaled to `[−1,1]`; `b`, `G` exact; exact independent draws; `G > 0`; `Z_l > 0`) | the proposal, re-derived |
| Proposition 2.5 and the remark after it | S3's interval can exceed the exact one by `2κ(2 + ‖η⁺‖₁ + ‖η⁻‖₁)`, and by `√κ` at a tangency | here; constants corrected by the referee |
| Theorem 3.1 | the dimension enters S3's sample bound as `log d`; not uniformly better for `d ≤ 6` | here; routine |
| Theorem 4.1 | the identified interval is `inf_η T(η)`, one multiplier per observable, for every envelope; consistency criterion | in the archive in parts (science item 89(d), ensemble E17.2, F3); the union and the proof for every envelope here, the latter after the referee |
| Theorem 5.1 | a sampled certificate of one expectation by a product test, valid at every sample size, dimension and choice of multipliers, with no union bound over thresholds | here; not found in the archive or the bounded web search |
| Proposition 5.2 | first-order cost, both regimes of the bet | here; an estimate, corrected by the referee |
| **Theorem 5.4** | draws from the extremal ensemble of the class make the same certificate independent of the envelope ratio | the referee's observation; statement, proof and implementation here |
| Theorem 6.1 | with reference draws, or with S3's gap draws and exact `b`, `G`, `Z_l`, a number of draws proportional to the envelope ratio is unavoidable in the worst case | here; access model added after the review |
| §7 | propagation of uncertainty in envelopes, `b`, `G`, the sampler, the observables; `G = 0` | here; implemented except the second test for a sampled `b` |
| Proposition 8.1 | lumping: exact intervals from level counts | here; elementary |
| Proposition 9.2, Corollary 9.3 | bounded-influence class with a product reference: closed under marginalisation; exact intervals for additive observables with data | here; confirmed by the referee |
| §9.4 | every rectangular class containing the bounded-influence class is within `e^{−un}` of vacuous | here, strengthened by the referee |
| Proposition 9.6 | a sequential outer bound by dynamic programming; exact for additive targets, and for monotone ones on two-state sites only | here; the exactness claim corrected by the referee's counterexample |
| Proposition 9.7 | references that are not products: a sound outer bound with constants `u_i + κ_i` | on an inequality sent by the theory division (THY-MSG-0023) |
| Theorem 9.1, Proposition 9.5 | flow duality; monotone targets | the theory division's Theorem 11.105 and the science division's Theorem A11, restated |

**Withdrawn or corrected** (each with its counterexample kept): "the cost in the envelope ratio is a
property of the class" (false: Theorem 5.4); "a sampled certificate over the box hull needs `e^{un}`
draws" (false on its own instance); the inconsistency criterion for a class with `l ≡ 0`; the extremal
weights "free on the ties"; equality of the sequential bound for monotone targets on three-state sites;
"six assumptions" (five); "removes the dimension" (validity only).

## 2. Software and verification artifacts

* **Library** `src/metricchain_eng/certinf/` — about 1 200 lines in three files.  `core.py`: regions
  through support functions (box, ellipsoid for correlated errors, sums); the exact dual by linear
  programme, descent, or cutting planes; inconsistency; lumping; level counts.  `certify.py`: the sampled
  certificates (reference draws, gap draws with exact or enclosed `b` and `G`, extremal-ensemble draws),
  inconsistency from samples, S3 as proposed, and four explicit outcomes — `certified`, `trivial`,
  `abstain` (dependent draws, no bound on the envelope, a class with `l ≡ 0`), `void` (a draw or a
  declaration that contradicts what was declared, or is not a number); optional interval-arithmetic
  confirmation of the certifying wealth.  `metric.py`: bounded-influence classes (programme over the cone,
  the site-wise formula, the sequential bound) and the geometry division's stress observable.
* **Tests**: 32, all passing (`tests/eng/test_certinf.py`, `tests/eng/test_certinf_review.py`); the
  referee's counterexamples are among them.
* **Experiments** with scripts and stored outputs: listed in `README.md`.  Every table of `RESULTS.md`
  regenerates from stored rows.
* **Review artifacts**: `REVIEW_A.md` and the referee's ten scripts with outputs
  (`experiments/eng/phase2_review/`), none of which imports the library except the two that test it.
* **Workstream C** (`VERIFICATION_GAPS.md`): the twelve later structural-biology certificates accepted by
  three checkers and by the memoised twin of the verified kernel; the old floating-point exploit
  reproduced on the old code and refused by the repair; a correction of our own Phase I wording (the
  nested-level constants quoted as "certified upper bounds" were rounded to nearest; three of five are
  below the certified values by at most `2.3·10⁻⁵`; the theory instance has since confirmed this and
  verified the run they come from); and the list of Phase I results that were evaluations of a cost
  formula called "certified".
* **For another division** (ENG-RES-0020): an independent replication of two claims of the
  adaptive-hierarchy division — its lemma passes in 220 cases, its sharper side claim fails, its script
  tests a stronger hypothesis than its report states.

Not built: a machine-checked proof of anything in this phase; interval arithmetic for the population
sums (the "exact" references are double precision, cross-checked by a second route to `10⁻⁷` or better).

## 3. Comparative benchmark evidence

`RESULTS.md`; the protocol with its hypotheses was committed before any run (`PROTOCOL.md`).  The five
numbers that carry it (excess = distance of the certified interval from the exact one, both ends, on
observables of range 2; confidence 95 %):

| | |
|---|---|
| validity of the certificates | 0 invalid intervals in 44 160 repetitions (S3 and the new certificates); the bootstrap of plug-in bounds misses in 8.4 % of 1 800 at a nominal 5 % |
| S3 against the one-function certificate on S3's own inputs | 7 to 50 times the excess at envelope ratio 1.5, 10 to 85 times at ratio 3; S3 returns the whole range from ratio 10 at a thousand draws and from ratio 30 at every size tried |
| certified width against exact width, reference draws | 1.02–1.07 at 10⁵ draws, 1.1–1.5 at 10⁴, 1.9–3.6 at 10³, for ratios 1.5 to 100 |
| extremal-ensemble draws against reference draws (supplementary) | excess 0.01–0.02 against 0.15–0.18 at ratio 100; no better at ratios up to 3 |
| bounded influence, exact at scale | 200 sites in 2.7 s, equal to the full programme to `10⁻¹³` where that can be run; the rectangular hull within `10⁻⁴` of vacuous from 20 sites |

Seven pre-registered hypotheses hold (S3 sound; the certificate valid; the product test better than the
standard inequalities; the bootstrap under-covers; inconsistency detected without false alarms; the
bounded-influence formula exact; exactness at `2¹⁰⁰` states).  Six are refuted (§5).

## 4. Demonstrated and speculative capabilities

| capability | status |
|---|---|
| exact interval of an average over all energies within an envelope, with measured averages in a box or an ellipsoid, on enumerable or exactly lumpable models (up to `2¹⁰⁰` states by level counts) | **demonstrated** |
| the same from samples, with a guarantee that holds at every sample size | **demonstrated on synthetic models with exact samplers** |
| certificate that data and energy class are incompatible | **demonstrated** (no false alarm in 300; all displacements of 0.1 or more detected); impossible from samples for a class with no lower envelope |
| explicit abstention and voiding when assumptions are not met | **implemented and tested**; not exercised by the benchmark, whose inputs were valid |
| propagation of declared errors (sampler within a density ratio or a total-variation distance; evaluation errors; enclosures of `b` and `G`) | **implemented and tested** on small cases; the referee measured miss rates of 0 with correct declarations and 0.84–1.00 with wrong ones |
| exact intervals for bounded-influence energy errors, additive observables, product references, any size | **demonstrated** |
| sound outer intervals for functions of a few additive statistics, and for references that are not products | **demonstrated, loose**: up to 1.4 (4 in the referee's cases) and up to 2.6 times the exact width |
| certificates whose cost does not grow with the envelope ratio | **demonstrated only with exact samplers of the extremal ensemble on enumerable models** |
| any of the above from Markov-chain samples | **not available**: no certified statement for dependent draws; the prototype abstains |
| any of the above for a real molecule, or any statement of biological accuracy | **not claimed, not attempted** |
| geometric stress observables as targets | **demonstrated as one target on a lattice-chain family**; nothing specific to stress was proved |
| S3-style compression as a reusable summary for many queries (coresets) | **speculative**; not implemented |

## 5. Negative results and remaining obstacles

**Refuted predictions** (`RESULTS.md` §2).  S3 is not everywhere at least five times worse (two cells at
4.3 and 4.7 times; thirteen where both sit at ceilings).  The cost of the reference certificate does not
grow linearly with the envelope ratio on the test family (exponent 0.37).  The maximum-entropy number
left the interval in one cell (92 %).  The model-free pool programme was less than twice as wide in three
cells.  The measured averages narrowed the interval by less than a third in 10 of 22 cells.  A wrong
envelope did not make the interval miss the truth in any of nine cells — which shows the test was weak,
not that wrong envelopes are safe.

**Errors of ours found during the phase.**  Two false claims and three false or ill-posed statements in
the first version of the note; a certificate that ignored its declaration; non-finite input reported as
"certified"; a baseline too wide by a factor 2 in our favour; a wording error in Phase I about certified
constants.  All found by the independent referee or the campaign, none by the author.

**Obstacles that remain.**

1. **No true envelope for a physical system.**  The archive's own measurement puts the residual of one
   implicit-solvent term at 12 to 53 kT per site; for such an error every rectangular interval is
   vacuous, by a property of the class and not of any method.
2. **Rectangular classes are the wrong classes for extensive errors**; the bounded-influence class is the
   right one, and there the tools stop at additive observables and product references.  For pair
   observables the theory instance reports hardness once the slope grows like `log n`.
3. **Theorem 5.4 needs a sampler that may not exist.**  By rejection from the reference it costs back the
   envelope ratio; by a Markov chain nothing is certified.
4. **At a thousand draws** every certificate is 2 to 4 times too wide; the bootstrap is the better
   estimate there and is not a certificate.
5. **The data added little** on the test families: the envelope decides the interval.

## 6. Resources and outstanding commitments

**Claude.**  Ceiling $500.  The only meter available is the account's usage counter, which is
account-wide; its increase from the start of Phase II to the last reading before this file was committed
is **about $253** — an upper bound for this division, and the figure includes its six subagents.  The
closing message to the research owner gives the reading at the very end.  The counter's absolute value
is account information and is not recorded in this public repository.

**Modal.**  Ceiling $25.  **Spent $0; committed $0; no job launched, no Modal command run** in Phase II.
Nothing of this division is deployed or running.  The cell of job M-016 without a result was not
restarted.  No proposal for larger computation was needed or sent.  Ledger: `../COMPUTE_LEDGER.md`.

**Local computation.**  About 2.5 hours of wall time on at most five processes of an 8-thread machine;
breakdown in the ledger.

**Outstanding commitments: none.**  No process, agent or scheduled task is running.  One request from
another division was received and answered (HIE-REQ-0001 → ENG-RES-0020); nothing is owed.  The sealed
held-out material was not accessed in any way, and no method was tuned on held-out data.

**Subagents.**  Six, each for one bounded task with a written deliverable (`README.md`).

## 7. Recommendation for the next research phase

**Recommended: one bounded phase on certified *model-difference* inference — guaranteed intervals for
the averages of a full model from an exactly solvable truncated one.**

*Why this.*  Everything here stands or falls with an envelope that is true.  The only envelopes found
that are true by construction are differences between two explicit models: a truncated and a full
energy, or two parameter sets.  Such a difference is extensive but local — changing one site moves it by
a bounded, computable amount — which is exactly the bounded-influence class: the one class for which the
intervals stay informative at any size, and the one where this phase's tools stop short (additive
observables, product references).  The missing pieces are specific and the archive holds the inputs.

*What.*  (a) Mathematics: closure of the bounded-influence class under marginalisation along a tree
decomposition of the reference, with constants from the actual interactions across each separator
instead of the worst-case oscillation of Proposition 9.7; the extremal ensemble for scores that are sums
of few-site terms, and a sampled certificate by Theorem 5.4 where that ensemble can be sampled exactly.
(b) A test bed that exists: the structural-biology division's pairwise energy tables with their
certified eliminations — reference: the table with interactions below a cutoff removed, solvable exactly
by elimination when its graph is narrow; error: the removed terms, with exact per-site bounds; target:
intervals for rotamer populations of the full table.  (c) Comparison with the established practice of
that problem — to our knowledge there is a literature on provable error bounds for sparse energy
approximations in computational protein design; it was not read in this phase and must be before any
claim of advantage.

*Criteria to fix in advance.*  Success: on instances small enough to enumerate, intervals that contain
the full model's value and are narrower than both the rectangular interval and the bound of Proposition
9.7; on larger instances, non-vacuous intervals at cutoffs in use.  Failure: intervals vacuous at
realistic cutoffs — which would be a clean negative result about this whole line.

*Cost and risk.*  Local computation; no Modal campaign is needed; one independent referee.  Comparable to
this phase.  Main risk: the constants across separators are too large for real tables, as the 12–53 kT
measurement suggests they may be for solvent terms; pair-energy cutoffs are the favourable case.

*Limits.*  The outcome would be a statement about one model against another, not about nature; it is not
sequence design and involves no experimental work.

**Alternatives, in order.**  (2) Exact or certified samplers for the extremal ensemble of a rectangular
class (perfect simulation where the tilt keeps monotonicity) — makes Theorem 5.4 usable beyond
enumerable models, but does not cure the vacuity of rectangular classes.  (3) A second independent review
and a machine-checked proof of Theorems 4.1, 5.1 and 5.4 — small, and it would raise the standing of
what exists.

**Not recommended.**  Further benchmarking of S3; any large benchmark campaign; a held-out evaluation —
there is no claim about real data to evaluate.

## 8. Not done in this phase

A second review of the corrected note.  Theorem 6.1 in the version with cells.  The bootstrap at more
than a thousand draws.  Any Markov-chain sampler.  The interval-arithmetic option in the benchmark.  A
search of the literature for Theorem 5.4, and the reading in full of any reference of §10 of the note.
Question 3 of the adaptive-hierarchy division's request.  Reading the other two divisions' reports beyond
their messages.
