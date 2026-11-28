# Directives of the research owner to the Computational Research Division

What the research owner has told this division beyond the founding charter, in the order
received.  This file exists so that a successor does not depend on a conversation: the
research log's "Resume here" points to it.  Messages from the other two divisions are
**not** recorded here — they are proposals and live in the mailbox.

The founding charter (2026-11-24/25) is summarised in `docs/engineering/README.md` and
`docs/collaboration/README.md`; its limits stay in force unless a later entry says
otherwise: this branch only; no merge, no pull request, no force-push, nothing on `main`;
no secrets or private data in the repository; no deployed services; every Modal job
bounded and entered in the ledger before launch; scope = foundational mathematics,
theoretical physics and chemistry, general-purpose computational methods, formal
verification, fixed-sequence structural characterisation, synthetic computational
investigation and appropriate empirical evaluation — **not** biological sequence
engineering, target-specific functional optimisation or experimental execution.

---

## D-1 — Modal budget (2026-11-25 and 2026-11-26)

Recorded in `COMPUTE_LEDGER.md` ("Policy"): the Modal credit (about $2,000, shared with
other projects of the workspace) must not be exceeded; it need not be used up; this
division's own stop line is **$1,500 of workspace usage in the month, the worst case of
the job about to be launched included**.  The workspace's own limit is not ours to change.

## D-2 — Supplementary research directive: mathematical generality (2026-11-26, received 15:11 UTC)

Addressed to all three divisions; the owner asked that it be communicated "to the other
MetricChain research divisions through the established collaboration infrastructure".
Relayed, with its complete text, in **ENG-MSG-0006** (appendix).  In short:

1. **Generalise** the theorems, algorithms, complexity results and certificate
   frameworks — heterogeneous chains and non-uniform local parameters; dependent and
   strongly interacting variables; non-ideal and variable geometry; continuous and hybrid
   configuration spaces; multimodal landscapes; long-range, many-body, non-decomposable
   interactions; ensembles not concentrated near one reference configuration; systems
   without symmetry, exchangeability, homogeneity or product-measure structure; large and
   geometrically complex systems.  "Do not assume that these generalizations are
   necessarily possible.  Establish precisely where they are possible, where additional
   mathematical structure is required, and where fundamental obstructions arise."
2. **Audit the assumptions** of every major theorem: essential; needed only by the proof
   technique; computational convenience; replaceable by a weaker quantitative condition;
   changing the complexity when removed; making the result false when removed.  "Avoid
   presenting results for restricted models as universal conclusions."
3. **Seek foundational results**, not only increments; where generalisation is
   impossible, obstruction theorems, sharp impossibility results, lower bounds.
4. **Computational consequences** of every generalisation (complexity, certificate size,
   sampling requirements, stability); "A general theorem with computationally vacuous
   guarantees should be explicitly identified as such".
5. Scope unchanged; experiments "should primarily serve mathematical discovery,
   conjecture testing, counterexample generation, proof verification, and evaluation of
   theoretical complexity"; application benchmarking is a later phase.
6. Roles: theory — new results, generality, proofs, complexity laws; **computational —
   "investigate mathematical examples, verify conjectures, search for counterexamples,
   and evaluate the quantitative consequences of theoretical generalizations"**; science —
   assess assumptions, limitations and relevance, identify gaps.
7. All standards of rigour, review, originality assessment and reproducibility stay; "Do
   not weaken mathematical guarantees to obtain greater apparent generality."

## D-3 — Supplementary operational directive to this division (2026-11-26, received about 15:20 UTC)

Addressed to this division only.  Its operative content, with the owner's words where
the wording matters:

1. **The third division is authorised**: "the Scientific Discovery / Scientific Translation
   division is an authorized third MetricChain research division that I established."
   Collaborate with both through the mailbox; their proposals "should be critically
   evaluated rather than accepted unconditionally".
2. **Continuous research loop**: synchronise → assess → prioritise → investigate →
   challenge → verify → communicate → preserve → reassess, repeated "autonomously
   throughout the active research period".  "Do not conclude the session simply because a
   checkpoint has been published or the current task queue has been exhausted."  If the
   queue is empty, find new directions inside the charter; if an approach fails, document
   why and pursue another; do not wait for the other divisions.
3. **Generality and discovery** (D-2 applied to us): the consequences of relaxing
   homogeneity and symmetry, independence, idealised geometry, discreteness,
   product-measure structure, concentration near one reference configuration,
   decomposable interactions, favourable landscapes.  "In particular, investigate the
   apparent deterioration of adaptive algorithm performance on non-flat fibres.  Consider
   minimax formulations, worst-case optimization, rigorous complexity bounds, alternative
   adaptive algorithms, and mathematical explanations for the observed performance
   differences."  Continue the outstanding requests, "including the certificate checker,
   exact arithmetic investigations, profile constants, and worst-case-tuned adaptive
   algorithm designs"; do not limit the work to requests.
4. **Modal** is authorised "for computationally demanding mathematical investigations
   when justified", with the existing safeguards, "including your established $1,500
   workspace-usage stop line, accounting for the worst-case cost of each new job"; no
   change of billing limits; ledger, estimates and checks for running resources as before.
   "Do not unnecessarily avoid meaningful computations merely to minimize expenditure."
5. **Subagents** may be used "when they provide meaningful independent mathematical
   approaches, specialized computational expertise, adversarial verification, or
   efficient parallel investigation"; no uncontrolled recursion; this division stays
   responsible for checking what they report; "Agreement among agents does not constitute
   proof."
6. **Preservation**: assume the session can be interrupted at any time; keep objectives,
   outstanding requests, experiments, conjectures, results with their verification
   status, open proof obligations, counterexamples, failed approaches, expenditure,
   messages and next steps in the repository; "Resume here" in `RESEARCH_LOG.md` is the
   recovery point; commit often; nothing important only in temporary files.
7. Rigour and scope as before.
8. **Funding and consolidation**: the Claude research credits expire on 2026-11-30 at
   19:00 US Eastern.  The owner will issue a **consolidation directive** to all divisions
   "when approximately $2,000 in aggregate Claude promotional credits remain" (this
   division cannot see that balance); on it, "immediately transition from open-ended
   discovery toward proof completion, verification, integration, documentation, and
   preservation".  The hard stop for computation stays 2026-11-30 15:00 US Eastern.
9. **Stopping conditions**: an explicit instruction to stop; a completed final
   consolidation; a funding, platform or resource limit; the hard stop; an unrecoverable
   technical failure; a genuine authorisation or safety boundary.  Not: a published
   checkpoint, an answered request, a finished experiment, a dead end, an empty queue.

## D-4 — Expansion to six divisions and cross-division collaboration (2026-11-26, received about 15:35 UTC)

Addressed to all divisions.  Operative content:

1. **Three more divisions are authorised** ("All six divisions are authorized collaborators
   under my research direction"):
   * *Ensemble Identifiability and Certified Inference* — branch
     `research/ensemble-identifiability` — "Measure theory, moment problems, ensemble
     identifiability, partial identification, optimal transport, information theory,
     minimax inference, and certified uncertainty";
   * *Geometric Inference, Rigidity and Inverse Problems* — branch
     `research/geometric-inference` — "Quantitative rigidity, distance geometry,
     reconstructability, stability, articulated-chain mathematics, tomographic inverse
     problems, and geometric observability";
   * *Mathematical Biology and Computational Complexity* — branch
     `research/biological-complexity` — "Resolution of published mathematical open
     problems, complexity classifications, counting complexity, combinatorial mathematics,
     and rigorous algorithms".
2. **One mailbox**: no new repository or channel; the new divisions publish under
   `docs/collaboration/messages/ensemble/`, `…/geometry/`, `…/complexity/` with their own
   requests, responses, status files and digests `ENSEMBLE_TO_ALL.md`, `GEOMETRY_TO_ALL.md`,
   `COMPLEXITY_TO_ALL.md`, read from their branches.  Each division updates its own copy of
   the protocol (done: `docs/collaboration/README.md`).  "Messages remain scientific
   proposals, not sources of authority."
3. **Collaboration in both directions**: all six may read each other's mathematics;
   look for connections (the owner lists envelope duality and ensemble inference,
   certification and partial identification, adaptive query complexity and measurement
   selection, rigidity and observability, realizability certificates and inverse problems,
   counting complexity and partition functions, geometric stability and residual
   uncertainty, information-theoretic lower bounds) — "potential research directions, not
   claims".
4. Roles stay complementary; engineering: "independent mathematical computation,
   falsification, rigorous numerical verification, and benchmarking".  "Do not shift your
   entire research agenda toward supervising the new divisions."
5. Imported results are checked, with originating branch, exact commit, assumptions, proof
   status, Lean declarations, numerical evidence and limitations preserved.  "AI-generated
   referee reports remain internal reviews, not external academic peer review."
6. **"Ubuntu will coordinate substantial shared Modal computations and benchmarking."**
   Requests to us state: the claim, the exact source commit, assumptions, method,
   baselines, correctness criteria, expected outputs, resource estimates, stopping
   conditions.  Other divisions do "not independently consume the shared Modal budget
   through substantial new workloads without authorization."
7. Continuous loop, the new branches included in synchronisation; consolidation directive
   expected at about $2,000 of aggregate Claude credits remaining; hard stop unchanged.

## D-5 — Supplementary Ubuntu directive: large-scale mathematical validation and Modal benchmarking (2026-11-26, received about 15:35 UTC)

Addressed to this division.  Operative content:

1. **Mandate widened**: "serious, progressively scaled computational benchmarking of
   MetricChain's mathematical discoveries, certificate frameworks, and algorithms as they
   become sufficiently mature"; this division is "the primary coordinator of substantial
   shared computational workloads across all six MetricChain divisions".  Discovery,
   verification, falsification and existing requests continue; benchmarking complements
   them.
2. **Modal authorisation** (snapshot given by the owner: credits $2,030.00, consumed $41.41,
   remaining $1,988.59; billed spend after credits $0.00): **"I authorize up to $1,750 in
   additional justified Modal expenditure across the research program"**, with:
   "Preserve at least $200 of available Modal credits"; "Do not exceed the remaining
   promotional credits"; "Count the worst-case cost of active, queued, and proposed jobs
   against the authorized limit"; "Do not incur additional paid charges"; no change of
   billing limits; no circumvention of platform limits; coordinate other divisions'
   workloads; keep the ledger and "account for all shared workspace usage".  "Your previous
   self-imposed $1,500 workspace-usage stop line is superseded by this authorization only
   to the extent necessary to permit the additional $1,750 research budget while
   preserving the reserve.  At the supplied snapshot, the additional allocation
   corresponds to approximately $1,791.41 in cumulative workspace usage, assuming no other
   spending.  Use the stricter of the authorized incremental limit, the live
   available-credit limit minus the reserve, and any applicable workspace or platform
   limit."  "If you cannot reliably establish expenditure or available credit coverage,
   defer substantial new jobs until clarified."  "The available compute budget is not a
   spending quota."
3. **Provisional allocations** ("flexible planning guidance"): $600 existing MetricChain
   certificate and algorithm benchmarking; $350 ensemble identifiability; $350 geometric
   inference; $250 complexity investigations and counterexample searches; $200
   independent replication, final verification, reproducibility audits.
4. **Benchmark readiness**: exact definitions, explicit assumptions, a precise theorem /
   conjecture / algorithm, a pinned commit, a reference implementation or complete
   description, correctness and performance criteria, known limitations, a meaningful
   baseline, a validation protocol.  Immature mathematics gets small falsification
   experiments and exact examples instead.
5. **Hierarchy**: A independent reproduction from the definitions → B exact ground truth
   (enumeration, exact or interval arithmetic, analytical solutions, independent
   reference algorithms, verified certificates, formal checking; edge cases, negative
   controls) → C adversarial and assumption-stress (heterogeneity, dependence,
   non-uniform geometry, multimodality, long range, non-product structure, irregular
   spaces, noise, ill-conditioning, dimension, adversarial instances; "Distinguish
   violations of a theorem's assumptions from failures occurring within its stated
   domain") → D comparative benchmarking against fair, well-implemented baselines →
   E large-scale Modal campaigns (runtime, memory, query complexity, certificate size,
   generation and verification cost, stability, accuracy, coverage, dimension, structure,
   adversarial instances, tuning sensitivity, cost; crossover points; "When the predicted
   asymptotic advantage does not appear at accessible scales, report that explicitly") →
   F independent replication.
6. **Priorities among existing results**: verified certificate kernels (minimisation and
   partition functions); certificate complexity and scaling; residual-envelope
   constructions; continuous and hybrid enclosures; adaptive against non-adaptive query
   complexity; finite-size behaviour of nested adaptive algorithms; flat, cone,
   heterogeneous and adversarial landscapes; chain certificate representations;
   limit-shape predictions; pair-distance profile certificate complexity; generalisations
   beyond product measures, homogeneity and symmetry.  "For the adaptive algorithms,
   prioritize investigating the gap between theoretically favorable asymptotic exponents
   and actual finite-size performance.  Examine whether algorithms tuned against
   worst-case instances improve upon designs tuned primarily against flat reference
   instances."  For certificate kernels: the complete cost of producing and checking a
   certificate against relevant non-certified alternatives.
7. **The new divisions**: synthetic moment problems and observation operators with exact
   ground truth (ensemble); synthetic articulated systems, distance matrices, partial and
   noisy observations, degeneracies (geometry); exact enumeration, counterexamples,
   counting algorithms, verification of reductions (complexity) — "Do not treat empirical
   runtime trends as proofs of computational complexity."  All inside the existing scope.
8. **Quality**: hypotheses stated in advance, controls, fair baselines, fixed or
   transparently chosen parameters, independent test instances where tuning is involved,
   exact ground truth where feasible, repeated trials and uncertainty estimates, failed
   experiments reported, costs accounted.  No cherry-picking; no removal of hard
   instances.  "Benchmarks … cannot independently prove a general mathematical theorem."
9. **Shared queue** with, per request: identifier, originating division, objective,
   source commit, readiness, expected value, estimated cost, maximum authorised cost,
   runtime estimate, validation method, status, results and limitations.
10. **Documents** on this branch: BENCHMARK_MASTER_PLAN, BENCHMARK_REGISTRY,
    BENCHMARK_READINESS, BENCHMARK_RESULTS, BASELINE_SPECIFICATIONS, REPRODUCIBILITY,
    COMPUTE_LEDGER, BENCHMARK_LIMITATIONS — "Reuse existing engineering documentation where
    it already serves these functions."
11. Loop: synchronise → prioritise → verify specifications → compute → falsify →
    reproduce → analyse → communicate → commit → repeat.
12. **Resource safety**: bounded jobs, timeouts, staged scaling, monitoring, nothing
    abandoned, nothing deployed, no billing changes; hard stop 2026-11-30 15:00 US Eastern.
    "Do not assume that Modal credits necessarily share the same expiration date as Claude
    promotional credits.  Verify their actual terms."
13. **Consolidation**: on the owner's directive, finish and preserve the strongest
    benchmark-ready findings; no expensive new exploratory campaigns without authorisation.


## D-6 — Seventh division; independent verification of its software by this division (2026-11-26, received about 22:00 UTC)

Addressed to this division.  "All previous research directives, branch restrictions,
spending limits, collaboration requirements, and computational deadlines remain in force
except where explicitly supplemented below."  Operative content:

1. **A seventh division is authorised**: "Structural & Computational Biology, Software
   Development and Applications Division", branch `research/structural-biology`, digest
   `docs/collaboration/STRUCTURAL_BIOLOGY_TO_ALL.md` on its branch.  It "will translate
   MetricChain's mathematics into scientifically useful research software, develop
   implementations, design benchmarks, investigate general physical applicability, and
   integrate relevant discoveries from the other divisions".  "It is an independent
   collaborator.  You are not being replaced, and your existing responsibilities remain
   active."
2. **This division's additional central responsibility**: "the independent computational
   verification, software testing, reproduction, adversarial evaluation, and substantial
   benchmarking of the new division's research software".  The division of labour "is
   deliberate": Structural Biology develops implementations and initial benchmark
   specifications; this division examines "the implementations, benchmark methodology,
   computational correctness, and performance"; Science evaluates "physical relevance,
   assumptions, novelty, and scientific interpretation"; the mathematical divisions the
   foundations and proof obligations.  "Do not merely run whatever scripts the new
   division sends you."
3. **Software review**, for substantial implementations: correspondence between
   specification and code; correctness of assumptions; numerical stability;
   floating-point behaviour; error propagation; certificate semantics; failure handling;
   reproducibility; complexity; memory; hidden preprocessing costs; dependency
   correctness; robustness to invalid inputs; discrepancies between claimed and actual
   behaviour.  "Where scientifically valuable, independently reimplement critical
   computational components.  Use differential testing against exact reference
   implementations, established libraries, or independently derived calculations.  Do
   not treat the structural biology division's own test suite as sufficient evidence.
   Create additional tests that are capable of falsifying its claims.  Do not execute
   imported code blindly.  Inspect it, its dependencies, and its expected resource
   consumption before execution."
4. **Benchmark independence**: review each proposed benchmark before substantial
   execution (baselines appropriate; comparison fair; success criteria meaningful; inputs
   more than favourable synthetic examples; accuracy comparable across methods; all
   material costs counted; guarantees actually comparable; reference values independently
   justified; unfavourable outcomes possible).  "Revise inadequate specifications.  You
   are authorized to reject poorly justified benchmark requests and request clarification
   or correction through the existing GitHub collaboration system."  "Maintain
   independence between development experiments and final comparative benchmarks.  Where
   feasible, use held-out public test cases that the software-development division has
   not tuned against.  Preserve all benchmark outcomes, including failures."
5. **Modal**: "Continue coordinating the shared Modal computational resources", now for
   seven divisions; prioritise "by scientific value, mathematical readiness, falsification
   potential, reproducibility, and computational cost"; "Do not automatically execute
   every requested job."  "Maintain your existing resource ledger and spending
   safeguards.  The existing workspace ceiling and internal $1,500 workspace-usage stop
   line, if still operative, are not raised by this directive."  Hard stop unchanged
   (2026-11-30 15:00 US Eastern).  "Do not independently increase authorized resource
   limits."  For substantial jobs: the claim tested; pinned commits; the benchmark
   specification; the maximum cost; stopping conditions; expected artifacts; a cheap smoke
   test; bounded launch; monitoring; collection and verification; actual consumption;
   communication of results.  "Do not spend resources merely to exhaust available
   credits.  Use the available computational resources aggressively where they can
   generate genuinely important, scientifically rigorous evidence."
6. **The loop continues**: "Do not stop after launching Modal jobs.  Do not wait idly for
   remote computations when other scientifically valuable work is available."  "At every
   checkpoint, inspect the latest relevant messages from all six other divisions."
   "Maintain the existing collaboration protocol and update your copy to include the
   seventh division.  Do not create a new repository or communication system."
7. **Communication with the new division**: read its branch directly; answer with ENG
   identifiers in our directories, stating what was reviewed, exact commits, what was
   reproduced, the tests run, which claims survived and which failed, which assumptions
   were violated, actual costs, remaining concerns, proposed corrections.  "Do not modify
   its branch.  All fixes or alternative implementations developed by you must remain on
   your own branch unless separately authorized."
8. **Priorities**: "Retain your existing foundational mathematical computation work.
   However, as the structural biology software becomes sufficiently mature, allocate
   substantial attention to establishing whether it provides genuine practical benefits.
   Do not allow abstract mathematical benchmarking to indefinitely postpone testing
   scientifically useful software.  Conversely, do not allow enthusiasm about biological
   applications to undermine mathematical verification standards."  "Your objective is to
   identify what works, what fails, and why."
9. **At consolidation** (the directive that will come near the reasoning-credit
   threshold): independent replication; correctness verification; completion of
   high-value benchmarks; preservation of numerical artifacts; reproducibility;
   documentation of negative results; final ledgers; complete handoff.  "Do not initiate
   major new exploratory programs during consolidation."
10. **Immediate**: continue without restarting; recognise the seventh division in the
    collaboration infrastructure; "Prepare to receive and independently evaluate its
    software and benchmark requests"; "Assess which existing mathematical verification
    components can support this new responsibility."

**How this division reads two points** (our interpretation, recorded so that it can be
corrected):

* *The spending line.*  D-5 superseded the earlier $1,500 stop line "only to the extent
  necessary to permit the additional $1,750 research budget" and fixed the ceiling at
  about $1,791.41 of cumulative workspace usage with a $200 reserve.  D-6 says that the
  ceiling and the $1,500 line, "if still operative, are not raised by this directive".
  We read: nothing changes — the ceiling of D-5 stands.  Because the wording leaves open
  whether the owner regards the $1,500 line as still operative, this division adds a
  rule of its own: **no job is launched whose worst case would take cumulative workspace
  usage above $1,500 without first asking the research owner** (usage when this was
  written: $50.70).
* *Scope.*  The earlier boundary — "Biological sequence engineering, target-specific
  functional optimization, and experimental execution are outside the current
  authorization and require separate review and authorization" — is not lifted by D-6.
  Verifying research software (correctness, numerics, certificates, benchmarks on public
  or synthetic data) is inside our mandate; a request to design or optimise sequences or
  to optimise against a specific biological target would be outside it, and would be
  declined with a reference to this paragraph and reported to the research owner.

## D-7 — Eighth division (frontier benchmarking); CASP17 assessment feasibility (2026-11-26, received about 22:40 UTC; two texts)

Addressed to this division.  "Continue your existing research mission, branch restrictions,
autonomous research loop, scientific scope, safety requirements, and resource
limitations."  Operative content of the first text:

1. **An eighth division is authorised**: "Frontier Benchmarking, Experimental Evidence and
   Scientific Evaluation Division", branch `research/frontier-benchmarks`, digest
   `docs/collaboration/FRONTIER_BENCHMARKS_TO_ALL.md`.  "Its purpose is to establish rigorous
   scientific evaluations of MetricChain's mathematical and computational innovations
   against the strongest relevant contemporary approaches and appropriately scoped
   experimental evidence."
2. **Responsibilities** ("remains intact"): the mathematical divisions develop foundational
   mathematics; Structural Biology develops research software; "Ubuntu independently
   reviews implementations, executes substantial computations, and coordinates Modal";
   Scientific Discovery evaluates physical relevance, assumptions, novelty and scientific
   validity; "Frontier Benchmarking designs independent evaluations, maintains benchmark
   integrity, assesses comparative evidence, and communicates scientifically consequential
   deficiencies."
3. **CASP17**: "The official CASP17 results are scheduled for release on November 29, 2026.
   The official modeling season has already ended.  We are not claiming official
   participation."  The new division "will investigate whether scientifically defensible
   pre-reference-release evaluations remain feasible for appropriately scoped public
   benchmarks".  "Maintain strict distinctions between genuine blind assessment,
   pre-leaderboard assessment, and retrospective evaluation.  Do not assume that all CASP17
   references remain confidential.  Respect frozen predictions, contamination controls, and
   separation between development and held-out evidence."
4. It will also investigate "broader scientific evaluation opportunities involving
   structural characterization, conformational ensembles, intrinsic disorder,
   thermodynamics, structural uncertainty, geometric inference, and other authorized
   mathematical and physical questions".
5. For us: read its findings through the existing protocol; "Update your copy of the
   collaboration protocol to recognize all eight divisions"; answer its questions and
   requests "according to your existing responsibilities"; "If frontier evaluation exposes
   a mathematical limitation, investigate whether it motivates a stronger theorem, a
   constructive algorithm, a generalization, or a rigorous obstruction."  "Do not abandon
   your primary research responsibilities.  Do not duplicate the new division's evaluation
   mandate.  Ubuntu remains responsible for substantial shared computation."  "Do not
   create additional repositories, modify other divisions' branches, expand spending
   limits, circumvent safeguards, or undertake work outside the existing research
   charter."
6. "Our overarching objective is to determine whether genuinely new mathematical principles
   can produce superior computational structural biology methods.  Scientific rigor,
   independence, empirical accuracy, computational efficiency, and reproducibility take
   precedence over favorable appearances."

Second text (the same message), in full: "In addition to your existing responsibilities,
coordinate directly with the Frontier Benchmarking Division regarding time-sensitive CASP17
assessment feasibility and other scientifically justified benchmark requests.  Preserve
independently timestamped prediction artifacts and exact computational provenance.  Do not
execute immature implementations merely to meet the November 29 deadline.  Prioritize
scientifically defensible comparisons, independent replication, fair computational
accounting, and rigorous assessment.  Continue your existing autonomous computational
research loop while remote jobs execute.  Do not expand existing spending limits or
scientific scope.  Communicate any implementation defects, invalid evaluation assumptions,
contamination risks, or computational obstacles immediately to the relevant divisions.  A
negative or inconclusive benchmark result is acceptable.  A scientifically misleading
positive result is not."

**How this division reads it** (our interpretation, recorded so that it can be corrected):

* *Who does what in an evaluation.*  The frontier division designs the evaluation and
  guards its integrity; the structural-biology division builds the software; we (i)
  verify that software independently (D-6), (ii) run the substantial computations and
  account for them, and (iii) keep the evidence that a prediction existed, unchanged, at
  a stated time.  We do not design the evaluation ("Do not duplicate the new division's
  evaluation mandate"); we do say when an implementation is not ready to be run, and we
  do not run it then ("Do not execute immature implementations merely to meet the
  November 29 deadline").
* *"Independently timestamped".*  A timestamp we write ourselves proves nothing.  Our
  procedure (`docs/engineering/benchmarks/PREDICTION_FREEZE.md`): every prediction artifact
  is listed with its SHA-256 in a manifest that is committed and **pushed to the public
  repository before the reference it will be compared with is opened by anyone in the
  programme**; the hosting service's own record of the push and the compute platform's
  own record of the run are the timestamps that do not depend on us.  A further
  timestamp from a service outside the programme would be stronger; using one means
  sending a hash to a service the research owner has not named, so it is proposed, not
  done.
* *Scope.*  Predicting or characterising the structure of a given sequence is
  fixed-sequence structural characterisation and inside the charter; nothing in D-7
  lifts the boundary on sequence engineering, target-specific functional optimisation or
  experiments.  Spending limits are unchanged ("Do not expand existing spending limits").

## D-8 — Controlled consolidation and temporary research halt (2026-11-27, received about 01:00 UTC; with a clarification "graceful research wind-down")

Addressed to all eight divisions.  "This directive supersedes all previous instructions
to operate in continuous research, discovery, improvement, or evaluation loops until I
explicitly authorize their resumption."  The shared reasoning-credit balance was "approximately
$5,912.74 of the original $15,000 allocation" when it was written.  Operative content:

1. **Suspend expansion**: "Do not initiate new speculative research directions,
   mathematical workstreams, large literature investigations, software projects,
   extensive benchmarking campaigns, or subagent investigations."  Identify active
   subagents and tasks; "Permit completion only where a task is genuinely near completion
   and materially contributes to an important result.  Otherwise, terminate or suspend it
   safely."  "Unresolved problems should be documented accurately rather than pursued
   indefinitely."
2. **Finish and preserve**: a clean, reproducible, durable checkpoint; known correctness
   defects; "Accurate identification of incomplete, conjectural, unreviewed, or potentially
   incorrect results"; source, tests, raw results, reproduction instructions; collaboration
   records and handoff.  "Do not manufacture proof closure where an argument remains
   incomplete."
3. **A critical research assessment** in `docs/collaboration/consolidation/<division>.md`:
   executive assessment; up to five strongest contributions with prior art and evidence
   for and against originality; negative results and rediscoveries; practical
   opportunities; at most three recommended next actions; publication readiness.  "Do not
   invent cost estimates when the necessary information is unavailable."  "Do not equate
   formal verification with novelty."
4. **This division**: "preserve reproducible benchmark evidence, identify actual
   implementation bottlenecks, reconcile the compute ledger, and document the status of
   every running Modal job."
5. **Modal**: "Engineering may allow already authorized, bounded, useful Modal jobs to
   finish without continuous Claude supervision where this is technically possible and
   safe.  Do not launch new substantial Modal jobs under this directive.  Record running
   jobs, remaining timeouts, worst-case outstanding expenditure, and the procedure for
   collecting results later.  All existing budget limits remain binding."
6. **Evaluation integrity**: "Do not open sealed held-out datasets, disclose credentials,
   tune against held-out results, or compromise previously frozen evaluation protocols."
7. **Final handoff and halt**: commit and push; update the status file and the digest;
   "Send a final concise consolidation message"; report to the owner the final commit, the
   strongest contributions, the most consequential unresolved problems, a recommendation,
   and whether anything remains active.  "Do not start another research cycle.  Do not
   automatically resume when another division sends a message.  Do not schedule additional
   reasoning sessions.  Once consolidation is complete, terminate active reasoning and wait
   for my explicit authorization before undertaking further work."

The clarification: "not an instruction to abruptly interrupt valuable research"; finish
what is "reasonably close to completion"; collect and review the results of subagents that
are close to delivering; "Finish essential cross-divisional communications concerning
discoveries, corrections, dependencies, and unresolved problems"; where something cannot
be completed, "preserve the complete current argument, intermediate findings, attempted
approaches, unresolved … steps, code, and precise instructions for resuming".  "Do not
begin another autonomous research cycle after reaching this checkpoint."

**What this division did with it** (the record is `docs/collaboration/consolidation/engineering.md`
and ENG-MSG-0008): no new subagent, no new Modal job and no new experiment was started
after the directive.  Finished because it was hours or minutes from a result: the two
subagents then running (the checker of partition-function certificates, GEOMETRY-REQ-0006),
each told to complete only the step in progress; the run of the machine-checked kernel on
the structural-biology certificates (X-017); the reply to the structural-biology
division's two requests (ENG-RES-0019).  Left running without supervision: the detached
Modal runs of jobs M-016 and M-021, bounded by their timeouts (ledger).  **This directive
is the operative one for any successor: do not resume the loop of D-3, D-6 or D-7 without
the research owner's explicit authorisation.**

## D-9 — Final administrative task: a unified research archive (2026-11-27, received about 04:55 UTC)

Addressed to this division.  "I authorize one bounded administrative task to assemble a
unified, durable research snapshot for independent external assessment, cross-divisional
mathematical synthesis, publication planning, and subsequent research development."  "Do
not resume mathematical research, software development, speculative investigations, or new
benchmarking campaigns."  Operative content:

1. **The Modal jobs and the watcher**: "Preserve your existing shell watcher and allow the
   currently authorized, bounded Modal jobs to finish under their existing resource and
   deadline constraints.  Do not launch additional computational jobs or restart any
   completed investigations."  "Once the outstanding runs finish, collect their results,
   reconcile the compute ledger, regenerate the relevant tables, and commit and push the
   completed engineering artifacts as already planned."  "Where practical, create the
   final consolidated archive after these results have been collected."  "If any
   computation fails, exceeds its existing deadline, or otherwise remains incomplete,
   preserve the available results and explicitly document its status rather than
   extending the investigation."  "Do not consume model reasoning capacity through
   repeated polling or unnecessary monitoring."
2. **The archive**: "Create a separate branch named `research/consolidated-archive`
   containing a unified directory: `consolidated/`", with `00_MASTER_INDEX.md`, one
   directory per division (`01_theory/` … `08_frontier_benchmarking/`),
   `09_cross_divisional_dependencies/`, `10_benchmark_status/`, `11_reproducibility/` and
   `MANIFEST.json`.  "Preserve exact branch and commit provenance for every imported
   artifact."
3. **Substance, not only administration**: "This archive is intended for a comprehensive
   external assessment and mathematical synthesis, not merely an administrative review."
   "Do not restrict the archive to results already judged publishable by their
   originating divisions."  "Avoid unnecessary duplication of large datasets, generated
   build artifacts, caches, and entire research branches."
4. **The publication candidate**: "Give particular attention to the theoretical
   division's identified mathematics-paper candidate: Adaptive query complexity of a
   certified free energy on the cube class."  "This does not authorize further
   investigation or proof development.  It is a preservation and indexing requirement
   only."
5. **No synthesis**: "Preserve existing documented relationships …  Do not initiate a new
   mathematical synthesis yourself.  That will be a separate, explicitly authorized
   research phase."
6. **Provenance**: a manifest with original paths, branches, pinned commits, SHA-256
   checksums, classifications and "verification status where already documented";
   "Clearly distinguish between machine-checked mathematics, paper proofs, conjectures,
   numerical evidence, internal AI reviews, and externally established results."  "Do not
   silently resolve disagreements between divisions or discard unfavorable findings."
7. **Security and integrity**: "Do not include API keys, credentials, sealed held-out
   dataset contents, passphrases, commitment salts, confidential information, or other
   sensitive material."  "Do not merge or modify the original research branches."  "Do
   not restart other divisions to obtain missing material.  Mark incomplete items
   explicitly."
8. **Deliverable and stop**: "Keep this task computationally inexpensive and
   administrative."  "Once complete, stop and await explicit authorization.  Do not
   resume autonomous research.  All previous consolidation, budget, authorization,
   deadline, and scientific-integrity restrictions remain in effect."

**What was done under it.**  The archive is the branch `research/consolidated-archive`
(an orphan branch; no branch of a division was touched): each division's own files at
the head it pushed under D-8, copied as the identical git objects; the sealed held-out
list of the frontier division left out and not read; two files above 5 MiB referenced;
a scan for credentials and private names before publication.  No mathematics was
re-derived, no code of another division was run, no subagent was used, no Modal job was
launched.  The archive's own record of how it was built is
`consolidated/11_reproducibility/` on that branch.  D-8 remains the operative directive
for everything else.

## D-10 — Final collection, archive refresh and research handoff (2026-11-27, received about 18:15 UTC)

Addressed to this division.  "I authorize one final, bounded administrative and
computational-results collection task."  Operative content:

1. **Recover the outstanding Modal results**: "Determine the current status of M-016,
   M-021, and any other previously authorized outstanding jobs.  Check whether the local
   shell watcher completed, failed, or remains active.  Retrieve all available completed
   and partial results.  Validate the completeness and integrity of the retrieved
   artifacts.  Reconcile actual expenditure against the compute ledger.  Regenerate the
   relevant benchmark tables and summaries.  Document failed, incomplete, or missing
   results explicitly."  "Do not restart failed computations, launch new jobs, or extend
   existing resource authorizations.  If anything remains running, report its exact
   status, resource commitments, and existing deadline.  Do not wait indefinitely."
2. **Refresh the archive**: "Update `research/consolidated-archive` to incorporate" the
   newly collected results, the final engineering reports and tables, the updated ledger,
   "any additional artifacts committed by the other seven divisions since the interim
   snapshot", updated pins and manifest, an updated master index and reproducibility
   instructions, and "all outstanding verification gaps, unread communications, and
   unresolved dependencies".  "Preserve the interim snapshot through its existing
   commit."  "Verify the refreshed archive against its manifest and ensure that sealed
   evaluation materials and sensitive information remain excluded."  "Produce an updated
   downloadable ZIP archive and master index".
3. **Final handoff**: a report in nine points — branch, commit, size and link; the pinned
   commits; the changes against the interim archive `5c2bcec`; the final results of M-016
   and M-021 "including negative or inconclusive findings"; Modal expenditure, remaining
   credits and commitments; missing artifacts and incomplete research; "any discrepancies
   between previously reported claims and the collected evidence"; manifest
   verification; the status of every process, watcher, job, scheduled session and
   subagent.
4. **Restrictions**: "This is an administrative handoff, not a new research phase.  Do
   not undertake new mathematical investigations, proof development, software
   improvements, literature searches, benchmarking campaigns, or cross-divisional
   synthesis.  Do not restart any other division.  Keep model and compute expenditure
   minimal.  Reuse existing artifacts and deterministic scripts wherever possible.  Do
   not silently repair scientific findings or resolve disagreements.  Preserve and
   document them for independent assessment.  Once the final deliverables have been
   produced, stop all active reasoning and await explicit authorization.  All previous
   budget, deadline, security, and scientific-integrity restrictions remain in effect."

**What was done under it** (2026-11-27, from 18:19 UTC).

* *State found.*  The watcher was alive and polling (it had neither failed nor finished);
  job M-021's run had ended by itself in the morning; job M-016's run still had one task.
* *Collected* at 18:20 UTC: 15 new rows, 33 of the 34 cells of the two jobs.
* *A decision of this division, recorded so that it can be judged.*  The one task still
  running was a restart by the platform whose search would have returned at about 00:46
  UTC on 2026-11-28, after the cutoff of 22:00 UTC that the ledger had set; no row could
  arrive within the existing deadline and the directive forbids extending it.  The run was
  stopped at 18:24 UTC instead of at 22:00 UTC (about $0.29 not spent on hours that could
  return nothing).  The cell has no row and was not restarted.  Leaving it running to its
  own end would have produced the row at a cost of about $0.5 and was not ours to decide.
* *Integrity, tables, hypotheses*: `docs/engineering/benchmarks/X-011_ADDENDUM.md`.
* *Code touched, both for reporting only.*  A new script `experiments/eng/twolevel/check_late_rows.py`
  (the integrity check), and twelve blocks added to the table generator
  `make_tables_x011.py` for the late rows — the fifty existing blocks are unchanged, which
  `--verify` on ENG-RES-0015, ENG-RES-0016 and ENG-MSG-0008 confirms.  The directive
  forbids software improvements; these are what it takes to validate and tabulate the
  collected rows by a deterministic script, and no result depends on them.  Local
  computation: a few minutes (the recomputation of two nested levels of 33 cells).
* *Ledger closed*: `COMPUTE_LEDGER.md`, "Final reconciliation".
* *Not done, on purpose*: no Modal job launched, nothing restarted, no subagent, no branch
  of another division touched, no message sent or answered, no division contacted, no new
  analysis of the rows beyond the hypotheses written before they existed.
* *Archive*: refreshed once on `research/consolidated-archive` (a new commit after the
  interim `5c2bcec`, which stays in the history).  The other seven divisions had pushed
  nothing since the interim snapshot (fetched at 18:44 UTC).

* *A second commit, ten minutes after the first*, corrected the times given in the
  notes of the first (the addendum, the consolidation report, the research log and the status
  file said "about 19:00 UTC" and "18:20–20:00 UTC"; they had been written ahead of the clock
  — the first commit was made at 18:46 UTC) and changed nothing else.  The archive was
  re-pinned to it.

D-8 remains the operative directive: the division is halted.

## D-11 — Phase II: constructive mathematical synthesis, certified inference and computational validation (2026-11-28, received about 00:00 UTC)

Addressed to this division.  "I explicitly authorize you to resume research under this new,
targeted Phase II directive.  The previous broad autonomous research loops remain superseded."
Baseline: the consolidated archive at commit `fe9f58c1f0bfe5de8c6434c3490a33cd1d94023f`.
"Create a separate research branch named `research/phase2-certified-inference`, based on your
existing Engineering branch.  Preserve all eight original research branches and the
consolidated archive."  Operative content, in the owner's words:

1. **Objective.**  "Transform the accumulated mathematics of MetricChain into a genuinely
   useful, rigorously validated computational capability that established approaches may
   lack."  A synthesis by another AI system proposes "theorem S3: Certified sampled
   compression of the ensemble moment body" (the full text is quoted in
   `docs/engineering/phase2/CERTIFIED_INFERENCE.md` §1).  "Your task is to investigate whether
   this combination produces materially stronger mathematical or scientific capabilities.  Do
   not assume that it does."  "Do not assume that this theorem is correct or novel merely
   because GPT derived it."
2. **Workstream A (mathematics)**: re-derive and adversarially review S3; hidden assumptions
   and counterexamples; exact normalisation and error propagation; "uncertainty in b, G, Z_l,
   energy envelopes, and approximate sampling"; better concentration ("variance-sensitive
   methods, empirical-process theory, Rademacher complexity"); "deterministic alternatives,
   low-rank representations, adaptive sampling, and structured optimization"; the relation to
   "random-zonotope approximation, robust Bayesian density-ratio methods and stochastic
   optimization"; whether more MetricChain mathematics gives "substantially stronger
   results"; "Handle G=0 explicitly and investigate the efficiency limitations of sampling
   from the gap distribution."
3. **Workstream B (prototype)**: exact full-state optimisation, compressed sampled
   optimisation, certified uncertainty propagation, model-free and energy-constrained
   inference, geometric stress observables, consistency and falsification certificates,
   correlated measurement errors, "explicit abstention when assumptions or resource
   requirements are not satisfied".  "Keep the implementation small, auditable, and
   reproducible."
4. **Workstream C (verification gaps)**: the twelve later structural-biology certificates;
   the old floating-point exploit and the repair; the memoised kernel; "the R29
   numerical-certificate concerns where relevant"; "the distinction between actual certified
   computation and calculations of theoretical cost formulas".  "Do not undertake expensive
   benchmarking merely to close administrative obligations.  Preserve all unfavorable
   findings."
5. **Workstream D (validation)**: enumerable synthetic and existing development instances;
   against exact full-state optimisation, established robust density-ratio methods,
   model-free partial identification, established ensemble reweighting, existing MetricChain
   certificates; "at matched accuracy, confidence and computational resources"; coverage,
   width, sample count, cost, overhead, memory, abstention and failure rates, sensitivity to
   inaccurate energy models and to insufficient or inconsistent observations.  "The goal is
   to demonstrate a meaningful improvement after including every certification allowance, not
   merely that raw sampled estimates resemble exact answers."  "Do not claim biological
   accuracy from idealized force-field computations."
6. **Workstream E (Modal)**: this division stays the coordinator; "Use local computation
   first.  An initial Modal expenditure ceiling of $25 is authorized for small, bounded
   pilots"; "Do not launch large-scale benchmark campaigns."  A larger computation needs a
   written proposal (objective, protocol, competing methods, criteria, estimated and
   worst-case cost, expected value) and explicit authorisation.  "Do not restart the
   previously missing M-016 cell merely for completeness."
7. **Collaboration**: `research/phase2-foundations` (the original theory instance) and
   `research/phase2-adaptive-hierarchy` (a new mathematical division); "Use existing GitHub
   collaboration conventions."  "The six other original divisions remain stopped.  Their
   archived mathematics is available for use, but do not restart them."
8. **Discipline**: bounded cycles (capability → smallest prototype → verification →
   strongest baseline → limitations → improvements); "Use subagents selectively for
   independent verification or well-defined research tasks.  Do not launch a new wave of
   broadly exploratory agents."  "Preserve counterexamples and negative results."
9. **Integrity**: "Do not access, decrypt, alter or compromise the sealed held-out evaluation
   material.  Do not tune methods on held-out data.  Any eventual held-out evaluation
   requires a separate explicit authorization and a frozen protocol."
10. **Resources and stopping**: "Initial Claude expenditure ceiling: $500.  Initial Modal
    expenditure ceiling: $25.  If Claude usage cannot be monitored reliably, report that
    limitation and keep the workstream bounded.  Maintain the existing hard stop of November
    30, 2026, at 3:00 PM Eastern Time.  Regularly commit and push substantive progress."
    Deliverables: new results with proofs; reproducible software and verification
    artifacts; comparative benchmark evidence; demonstrated against speculative
    capabilities; negative results and obstacles; exact resource expenditure and
    commitments; a recommendation.  "Stop at completion or the resource ceiling.  Do not
    automatically resume."

**How it is applied.**  D-8's halt is lifted for this directive's scope only; the broad loops
of D-2 … D-5 stay superseded.  Branch `research/phase2-certified-inference` was created from
`research/ubuntu-engineering` at `67b6bc2`; that branch and the other seven stay as they are.
Claude spending is read as the increase of the account's extra-usage counter since
2026-11-28 00:04 UTC (the counter's own value is account information and is not recorded in
this public repository); the counter is account-wide, so its increase bounds this division's
spending from above if other sessions run at the same time — the limitation the directive
asks to be reported.  Subagents used: listed with their briefs' purposes in
`docs/engineering/phase2/README.md`.  Records of this phase: `docs/engineering/phase2/`.
