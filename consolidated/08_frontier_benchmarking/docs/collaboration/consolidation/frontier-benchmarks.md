# Consolidation report — Frontier Benchmarking, Experimental Evidence and Scientific Evaluation

```
Division:      Frontier Benchmarking (eighth division), branch research/frontier-benchmarks
Directive:     FB-D-5 "Controlled Consolidation and Temporary Research Halt" (docs/frontier_benchmarks/OWNER_DIRECTIVES.md)
Written:       2026-11-27, about 01:20 UTC, in the founding session (the division is three hours old)
State:         the commit that contains this file; nothing of this division is running after it (section G)
```

This division proves nothing and builds no method.  Its product is evidence about other
divisions' work, and the procedures that make such evidence trustworthy.  The headings the
directive asks for are answered in that sense; where a heading presupposes a theorem
("formal verification status", "originality") the honest entry is usually "none claimed".

## A. Executive assessment

In one session this division did five things that can be defended.

1. **It determined that MetricChain had nothing CASP17 could evaluate, and produced no
   prediction.**  No division contradicted this; structural biology and science agreed in
   writing.
2. **It ran the programme's first comparison on instances its authors did not build, against
   an outside solver, and then found out why the result was bad.**  On ten public
   fixed-sequence side-chain instances the certified minimum-energy route certified four in
   300 s — all four equal to toulbar2's optimum, 17 to 326 times slower — and abstained on
   six, three of which toulbar2 closes in under two seconds.  The cause is not the mathematics
   of the bound (the certified route's root bound is the tighter one on every instance); it
   is a node rate about three orders of magnitude below the uncertified solver's (0.7 to 2.6
   search nodes per second against 1,200 to 3,300), and with three times the budget the three
   abstentions that toulbar2 closes in under two seconds remain.
3. **It recomputed nine of the ensemble division's planted identification controls with
   independent code; all nine reproduced.**  Two simple reweighting baselines returned one
   perfectly fitting ensemble each on the non-identified controls, at total-variation distance
   0.5 from the planted truth in three of six cases.
4. **It built and used evaluation-integrity procedures**: three freezes, each time-stamped by
   four unrelated public authorities; a sealed held-out list of 47 structures whose
   credentials only the research owner holds; a test suite that fails if a frozen directory is
   edited.
5. **It wrote, before any held-out data existed, what would count as success and failure**
   (eleven protocols, amended once from the science and complexity divisions' criticism), and
   kept a register of negative results that includes its own errors.

What it did **not** do: no held-out evaluation; no comparison of anything with an experimental
observable; no established baseline other than toulbar2 was run; no evaluation on the
benchmarks beyond CASP17 that directive FB-D-4 names; no protocol was frozen and executed.
Both pilots are exploratory (class A-EXP) on what are now development instances.

**The scientific position this evidence supports.**  MetricChain's distinctive property — a
machine-checkable guarantee about a stated finite model, and the ability to say "the evidence
does not decide" — is real as a design property and reproduced independently at small scale.
There is no evidence yet that it yields a useful capability: in the one realistic comparison
it lost on speed and completeness, and nothing has been compared with experiment by anyone.
Superiority is not established on any dimension, in either direction, where experiment is
involved.

## B. Strongest contributions, ranked

Four deserve inclusion.  None is mathematically original and none claims to be.

### B1. A head-to-head evaluation of the certified minimum-energy route, with a causal diagnosis

* **Contribution.**  (i) Measurement: `RESULTS.md` §1 — 10 public instances (337 to 1,972
  residues), 300 s per method; certified route 4 accepted / 6 abstained; toulbar2 7 closed /
  3 open; where both finish the values agree; ratios 17, 25, 63, 326.  (ii) Diagnosis:
  `RESULTS.md` §6 — the producer's root bound is within 0 to 2.3 % of the best known value
  and tighter than toulbar2's on all ten instances (by 1.5 to 15 times on the nine where it
  is not exact); asking for a gap just under one cost unit does not remove the abstentions; the
  producer enters 0.7 to 2.6 search nodes per second against toulbar2's 1,200 to 3,300, with
  about nine tenths of its time in message passing over every edge at every node, and still
  abstains at 900 s after 620 to 2,306 nodes; in toulbar2's own
  search, one child per state costs 3 to 5 times the nodes of a binary split, and omitting
  low-degree variable elimination 1.8 to 18 times; with every refinement the producer lacks
  switched off, toulbar2 still closes six of seven instances in at most 7 s.  (iii) A fact
  about the software division's development set: its dual bound alone certifies all twelve
  development instances (its own null method), against one of ten here.
* **Commits, files, artifacts.**  `abbbd1c` (pilot), this commit (diagnosis);
  `experiments/frontier/exploratory_gmec/`, `experiments/frontier/diagnostics/` with stored
  rows; tables generated and checked by `experiments/frontier/make_tables.py --verify`.
  Evaluated software: structural biology `1756529` (pilot) and `d61fc53` (same solver files).
* **Verification and review status.**  Not formal.  Every table is regenerated from stored
  rows.  **Not replicated**: the request to engineering (FRONTIER-REQ-0001) was unanswered at
  the halt.  The science division read the pilot and criticised its strata (adopted).
* **Essential assumptions.**  toulbar2's optima are not certified; one shared machine, one run
  per cell, one core; budgets of 300 s and 60 s; "node" is each solver's own unit; the
  instances are 2011 energy tables rounded to integers.
* **Closest prior art.**  Solver comparisons on these instance families by toulbar2's authors
  and others (Allouche et al., *Artificial Intelligence* 2014; Hurley et al., *Constraints*
  2016 — cited from memory, not re-read); proof logging with verified checking for other
  solving paradigms (VeriPB with CakePB).
* **Distinction.**  A proof-producing route with an independent checker is one of the
  contestants, and the deficit is attributed to components by measurement.
* **Evidence for originality.**  None claimed; we did not find a published comparison that
  includes a formally checked certificate for this instance class (snippet-level search only).
* **Evidence against.**  Component ablations of toulbar2 are standard in its authors' papers;
  "a cheap weak bound with fast search beats a strong slow bound" is what that literature
  would predict.  Whether proof logging for cost-function-network solvers already exists was
  **not checked** — the prior-art search was cancelled by the halt.
* **Validation.**  Realistic computational, exploratory.  No experimental content.
* **Limitations.**  Ten instances; the pilot preceded its protocol; timings on a loaded
  machine; rows with virtual arc consistency dropped (the run did not return).
* **Before publication or use.**  Replication by another party; the certified baselines
  (pseudo-Boolean proof logging with a verified checker; exact-rational dual of the linear
  relaxation); the same comparison on a repaired producer under the frozen protocol; a
  prior-art search on certified search for cost-function networks.

### B2. Evaluation-integrity procedures, exercised: freezes, independent time-stamps, a sealed held-out list

* **Contribution.**  A manifest format with one normal form and strict verification
  (`src/metricchain_fb/freeze.py`), RFC 3161 tokens from four unrelated authorities verified
  against the ordinary trust store (`timestamp.py`), salted commitments (`commitment.py`),
  and their use: FRONTIER-FRZ-0001 (public state of CASP17, manifest `899f916e…0d29`,
  attested 2026-11-26 23:03:21 UTC), -0002 (commitment to and encrypted copy of the held-out
  list, `c5df5b3c…4284`, 23:42:32), -0003 (our scores of 1,163 public CASP17 model files
  before the official numbers, `2a65d774…b334`, 23:58:17).  The list: 47 cluster
  representatives drawn from 150 recent high-resolution entries by a published rule and a
  secret ordering salt; the software division asked not to see it and has not.
* **Files.**  `src/metricchain_fb/`, `tests/frontier/` (64 tests, most of them planted
  violations; one fails if any committed freeze is altered), `experiments/frontier/freezes/`,
  `PREDICTION_FREEZE_REGISTER.md`, `CONTAMINATION_AUDIT.md` (leak paths L1–L9).
* **Verification and review.**  Tests; tokens verified with `openssl ts -verify`.  The
  software division's intake confirmed it did not open the sealed files.  Engineering keeps
  its own freeze format; one index for both was proposed and not answered.
* **Assumptions.**  A token proves that a digest existed at a time, not that nobody knew the
  content earlier; the seal protects against parties without the passphrase.
* **Closest prior art.**  RFC 3161 (2001); cryptographic commitments; preregistration; CASP's
  blind protocol.  **Distinction:** none in concept — an assembly for a setting where the
  party being evaluated writes the commit dates.  **Originality:** none; every component is
  standard.
* **Limitations.**  The list's rule differs from the software division's plan SB-BM-3 in
  three places (by that division's reading; not reconciled — register IR-14).  The session's
  scratch copies of the credentials vanish with the session; the owner's copy is the only
  durable one.  If it is lost the list is redrawn under a new identifier.
* **Before use.**  One agreed rule; a frozen release of the software; the owner's release of
  the key to engineering; one run; then the list is retired.

### B3. The CASP17 determination and a blind check of the scoring instruments

* **Contribution.**  `CASP17_ASSESSMENT.md`: from the official pages (239 target-list entries,
  season closed 31 August, all predictions public, results announced for 29 November) and
  the pinned state of all seven divisions, no assessment class admits a MetricChain entry;
  none was produced; MetricChain is not a participant.  Scoring code for RMSD, lDDT, GDT,
  TM-score and side-chain torsions (`src/metricchain_fb/scores.py`), checked against two
  independent libraries and planted answers, then applied to all public models of three
  targets with released references and frozen before the official numbers.
* **Review.**  Agreement of structural biology (STRUCTBIO-RES-0001) and science
  (SCI-RES-0039); no contradiction by the deadline set.
* **Prior art.**  The CASP assessment itself; established scoring tools.  No originality.
* **Limitations.**  The blind check has little power: three easy targets with median GDT_TS
  near 99 (`NEGATIVE_RESULTS.md` N-14).  **Its outcome is pending**: the comparison with the
  official numbers needs the owner's authorisation under FB-D-5 (section G).
* **Value.**  A claim that was not manufactured.

### B4. Independent replication of nine planted identification controls, with two baselines

* **Contribution.**  `RESULTS.md` §2: verdicts, certificates and intervals of nine controls of
  the ensemble division recomputed by code that shares nothing with theirs; all reproduced.
  Maximum-entropy reweighting and non-negative least squares (our own few-line versions) each
  return one ensemble with a perfect fit on the non-identified controls.
* **Review.**  Acknowledged by the ensemble division as "the first check of the controls that
  is not ours"; sixteen of its twenty-five controls remain verified by their generator only.
* **Closest prior art.**  *Maximum occurrence* (population ranges from averaged data; Bertini,
  Luchinat, Parigi and co-workers — from memory), now in the ensemble division's own
  prior-art register together with "a published theorem that contains our E1(b)".
* **Limitations.**  Planted, finite, linear controls; no established reweighting package was
  run; nothing experimental.

*Not ranked as a contribution:* the protocols, registry, state-of-the-art register and
readiness table are working documents; several of their literature rows are at snippet or
memory level and say so.

## C. Negative results and rediscoveries

The full register is `NEGATIVE_RESULTS.md` (N-1 to N-23).  The consequential ones:

| finding | consequence |
|---|---|
| certified route: 4 of 10 at 300 s, 17–326 times slower, abstains where toulbar2 needs under two seconds | no speed or completeness claim can be made for the present producer |
| the software division's speed hypothesis held on its development set and fails on public instances; that set never searches | hypotheses formed on that set do not transfer |
| **nothing in the programme has been compared with experiment by an independent party** | every statement about scientific usefulness is still a conjecture |
| exactness is not the accuracy bottleneck (published: < 0.1 % from the exact optimum; science: model error 60–100 times any optimality gap) | an accuracy advantage of the certified optimum is not expected; the test (FB-P-02) should be run once and reported, not hoped for |
| on instances closed without branching the certificate is, in substance, a dual solution of the linear relaxation — an object exact linear programming already produces and checks | the native format's value there is the size of the trusted base, not reach (question T-1, unanswered) |
| certified population ranges are, in their nearest published form, *maximum occurrence* | the ensemble work must say what its certificates add, on the same data |
| the binary verdict "identified" is unstable under arbitrarily small perturbations (the ensemble division's own result) | evaluate intervals and mass bounds, never the verdict |
| **our errors**: a stale intake published within the hour; a pilot started on the wrong commit; a time-limited value labelled an optimum; a planted test with the wrong sign; a literature row that was wrong where checked; two wrong hypotheses about the abstentions (bound, integrality); a proposed linear programme for the identifiability radius that does not exist (the problem is NP-complete); an auditability count of "3 of 10" that should have been 0; header times later than commit times; a cross-reference that did not resolve (the last two found by the software division) | each is recorded with its correction; the pattern is haste in the first hour and reliance on a library's return value |

**Abandon:** any claim of CASP17 participation; the present producer architecture (full
message passing at every node, interpreted) as a route to competitive certified search;
design-type instances (outside the charter).
**Deprioritise:** evaluation on benchmarks that measure capabilities MetricChain lacks —
affinity, pockets, disorder, kinetics, prediction from sequence (`BENCHMARK_READINESS.md` §§2–3);
accuracy claims from exact optimality; binary identifiability verdicts as an evaluated output.
**Needs an owner decision, not requested:** mutation-effect benchmarks (the capability they
measure borders on sequence optimisation, which the charter excludes).

## D. Practical opportunities

Levels: **M** mathematics · **S** software · **Y** synthetic validation · **C** realistic
computational validation · **X** experimental evidence.

| opportunity | M | S | Y | C | X |
|---|---|---|---|---|---|
| **1. Checked optimality for exact side-chain and rotamer optimisation**: an independent, small checker for answers found by a fast uncertified solver | kernel soundness machine-checked by theory (not re-checked by us) | producer and checker exist; producer too slow | the software division's twelve instances | our pilot: 4 of 10, negative on cost | not applicable — the guarantee is computational; its *value* for structures is untested |
| **2. Certified intervals for ensemble populations and observables from averaged data**, reported instead of one fitted ensemble | theorems, mostly paper proofs; a few statements machine-checked | none for a general pool | 25 planted controls, 9 replicated | none | none |
| **3. Certified bounds on partition functions of fixed discrete models** | kernel | exists (software division) | authors' development models only | none | none |

The first is nearest to a demonstration: the diagnosis says the obstacle is the cost of a
search node, and the uncertified solver's search could be the thing that is checked.  The
second has the most distinctive scientific content and the least software.  For none of
them is usefulness to structural biology shown.

## E. Recommended next actions (three)

### E1. Certified search at the speed of the solver it checks

* **Objective.**  Kernel-checked optimality certificates on every public instance toulbar2
  closes, at a total cost within ten times toulbar2's.
* **Existing prerequisites.**  Kernel and checker; ten public instances with checksums; our
  drivers and the diagnosis (`RESULTS.md` §6); protocol FB-P-01 version 1.1.
* **Missing.**  A producer whose node costs milliseconds (incremental propagation, compiled
  loops) with binary splits and low-degree elimination — or an emitter that turns the
  uncertified solver's search into kernel leaves; an answer to whether the kernel's rules
  cover a split of a domain into two subsets and the solver's eliminations
  (`MATHEMATICAL_FEEDBACK.md` D-1); a prior-art search on proof logging for cost-function
  networks.
* **Published baselines.**  toulbar2 1.4.x (uncertified); a pseudo-Boolean encoding with
  VeriPB and its verified checker (certified); exact-rational duals on instances closed
  without branching.
* **Benchmark.**  Development: the ten public instances and synthetic families with planted
  optima.  Evaluation: published fixed-sequence instance sets not used in development
  (registry B-1103), fixed by a freeze before the run.
* **Success.**  The definition already in the protocol: certificates on ≥ 90 % of the
  instances toulbar2 closes in the same budget, within a factor 10 on at least half.
  **Failure.**  Fewer than half; or any accepted certificate above an established optimum (a
  soundness defect: stop).  **Beyond success:** a certificate or certified gap on one of the
  three instances nobody closes.
* **Claude reasoning.**  Not estimated; it depends on which of the two routes is taken.
* **Computation.**  Local processors suffice: the complete ten-instance comparison is at most
  twenty single-core runs of 300 s.  **No Modal cost.**
* **Dependencies.**  Structural biology (producer), theory (D-1), engineering (replication,
  certified baseline).
* **Model.**  Implementation and benchmarking can continue with Opus from the diagnosis as
  written; a new kernel rule, if one is needed, is the theory division's work.

### E2. Certified ensemble intervals on public experimental data, against maximum-entropy reweighting

* **Objective.**  On real averaged data: do the certified intervals contain held-out
  measurements, are they narrower than the pool's range, and what do they say that a
  reweighted ensemble does not?
* **Existing prerequisites.**  The ensemble division's statements for finite pools with
  tolerances, gains, offsets and convex error sets (E1, E23.1, E17.2, E30); 25 controls; our
  independent linear-programming code for the controls; a public reweighting package with
  example data, fetched and **not used** (BME, commit `314d3b5`: simulated pool with
  measured NMR and scattering data, by its file names — not opened).
* **Missing.**  An interval tool for a general finite pool (its authors: none exists); a
  protocol that fixes, before the run, the tolerance rule, the held-out observables and the
  coarse-graining for the identifiability radius; the science division's classification of
  which data are means, gains or offsets.
* **Published baselines.**  Bayesian / maximum-entropy reweighting (BME); maximum occurrence;
  an ensemble-refinement method of the replica type — named, not verified at source.
* **Benchmark.**  That public data set with observables held out by type; then planted
  forward-model tests on simulation ensembles (registry B-205, B-206).
* **Success.**  Coverage of held-out measurements at the stated level **and** median interval
  width at most half the pool's range of the observable.  **Failure.**  Intervals wider than
  nine tenths of the pool's range — then intervals without a prior are uninformative at
  realistic pool sizes and the method needs a constraint tying it to the prior.  *Our
  expectation, written before any run: failure in this sense is likely* (thousands of pool
  members against tens of data); it is a conjecture, not a result.
* **Claude reasoning.**  Not estimated.  **Computation.**  Linear programmes with about ten
  thousand variables: local, minutes.  **No Modal cost.**
* **Dependencies.**  Ensemble (specification), science (data semantics), structural biology
  or engineering (tool).
* **Model.**  Executing a frozen protocol: Opus.  Designing a prior-constrained interval, if
  the failure occurs: new mathematics for the ensemble division.

### E3. The certified optimum against experiment: side-chain placement (protocol FB-P-02)

* **Objective.**  Under equal information, does the certified minimum of the software
  division's energy model place side chains as accurately as an established packer, measured
  against deposited conformations?
* **Existing prerequisites.**  The software division's molecular layer; our torsion scoring;
  protocol FB-P-02 version 1.1; the sealed list for the final run; a fast established packer
  fetched and **not built** (FASPR, commit `0d55732`).
* **Missing.**  A frozen release; the baselines built and run; a public validation list
  disjoint from the sealed pool (same criteria, released before 2026-07-01); one agreed
  selection rule (IR-14); the filter against learned packers' training sets.
* **Published baselines.**  FASPR, SCWRL4, the Rosetta packer, one learned packer —
  availability and licences not verified.
* **Benchmark.**  The public validation list (development), then the sealed 47 once.
* **Success and failure.**  As in the protocol: an equivalence margin fixed in advance; the
  outcome is one of better, equivalent, worse, not assessable.  *Expectation written before
  the run: equivalent or worse in accuracy* (the published study; the science division's
  error budget); the result would then be "auditable at no gain in accuracy", which is
  worth knowing.
* **Claude reasoning.**  Not estimated.  **Computation.**  Seconds to minutes per structure
  locally, by the software division's own timings (0.3 to 36 s on its instances; read from a
  commit subject).  **No Modal cost** expected.
* **Dependencies.**  Structural biology (release), engineering (execution with the key the
  owner releases), science (interpretation).
* **Model.**  Opus suffices for execution.

*Owed in addition, small:* the comparison of FRONTIER-FRZ-0003 with the official CASP17
numbers by its frozen plan — one short session once authorised (section G).

## F. Publication readiness

**Nothing of this division is a standalone publishable result.**  The evaluation is ten
instances and one unreplicated run; the integrity procedures assemble standard components.

Conditional candidates, with what a human expert would demand:

* *If E1 succeeds* — "optimality certificates for cost-function-network search, checked by a
  formally verified kernel, at near-solver cost": requires a prior-art search on proof logging
  for such solvers (not done; we do not know that it does not exist), the certified
  pseudo-Boolean baseline, replication, and instance sets from current energy functions.
  Formal verification of the kernel establishes soundness, not novelty: on instances closed
  without branching the certificate is a linear-programming dual.
* *If E2 shows informative intervals on experimental data* — a comparison with maximum
  occurrence and maximum-entropy reweighting on the same data, with held-out observables;
  the difference from maximum occurrence must be stated exactly.
* The diagnosis of section B1 would be a section of the first, not a paper.

## G. State at the halt, and how the directive was applied

* **Subagents:** none running; none were dispatched after the continuation directive.
* **Background processes:** the two bounded diagnostic runs that were under way were allowed
  to finish (local processor, minutes; their rows are in the repository); none remains.
* **Modal:** this division has never launched a Modal job and has none.
* **Scheduled sessions:** one existed — a check-in on 2026-11-30 05:00 UTC to compare
  FRONTIER-FRZ-0003 with the official CASP17 numbers and read replies (scheduled-task id
  `trig_01PMtadi7NHa7nfuRtqTTkMq`).  It was **paused, not deleted**: left active it would
  have started work without the explicit authorisation FB-D-5 requires.  The owner can
  re-authorise it in one sentence; the comparison plan is frozen and loses nothing by waiting.
* **Cancelled before starting:** the two evaluations on validation data (E2, E3 above), the
  literature and prior-art investigations, the per-division request messages (replaced by
  FRONTIER-MSG-0004).
* **Sealed list:** unopened by anyone but this division; credentials with the research owner;
  never used to guide development.
* **To resume:** `docs/frontier_benchmarks/HANDOFF.md`.
