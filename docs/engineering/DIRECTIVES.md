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

## D-3 — Supplementary operational directive to this division (2026-11-26, received about 15:40 UTC)

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

## D-4 — Expansion to six divisions and cross-division collaboration (2026-11-26, received about 16:40 UTC)

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

## D-5 — Supplementary Ubuntu directive: large-scale mathematical validation and Modal benchmarking (2026-11-26, received about 16:40 UTC)

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

