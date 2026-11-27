# Directives of the research owner to the Scientific Discovery, Translation & Independent Validation Division

What the research owner has told this division, in the order received, **in the owner's words where they are kept
here**.  This file exists so that a successor does not depend on a conversation: `RESEARCH_SYNTHESIS.md` §0, item 0,
points to it.  Messages from other divisions are *not* recorded here — they are proposals and live in the mailbox.
A later directive does not cancel an earlier one unless it says so; where two seem to pull apart, the limits of the
charter and the explicit resource and authorisation boundaries win.

| # | received (UTC, this division's clock) | what | where the text is |
|---|---|---|---|
| D-0 | before the first commit of this branch (2026-11-25) | the founding charter of the division ("Comprehensive Research Charter", sections 1–28) | **not in the repository in full**; its binding limits are restated in `RESEARCH_SYNTHESIS.md` ("Rules that bind the division") and its mailbox paths and identifiers in `docs/collaboration/SCIENCE_TO_ALL.md` |
| D-1 | 2026-11-26, about 15:11 | "Supplementary Research Directive — Mathematical Generality, Physical Relevance, and Foundational Breakthroughs" | verbatim in `docs/collaboration/messages/science/SCI-MSG-0029.md` §1 (also relayed, with the same words, by the other two divisions: ENG-MSG-0006 appendix, THY-MSG-0016 §1) |
| D-2 | 2026-11-26, about 15:36 | "MetricChain — Authorized Research Expansion and Cross-Division Collaboration Directive" (six divisions) | verbatim below |
| D-3 | 2026-11-26, about 22:00 | "MetricChain — Supplementary Research Directive: Scientific Evaluation of Structural Biology Software" (a seventh division; this division's added duty of independent scientific evaluation) | verbatim below, after D-2 |
| D-4 | 2026-11-26, about 22:41 | "MetricChain — Supplementary Directive: Frontier Scientific Evaluation and Eighth-Division Coordination" (an eighth division, Frontier Benchmarking; the division of responsibilities restated) | verbatim below, after D-3 |

## D-1 in one paragraph (the text is in SCI-MSG-0029 §1)

Keep the programme; move its weight to mathematical generality.  For every major theorem an audit of assumptions
in six classes, and a hierarchy from tractable models outward; obstruction theorems where a generalisation fails;
the computational consequence of every relaxation; experiments in the service of the mathematics, extensive
application-specific benchmarking in a later phase; no biological sequence engineering or target-specific
optimisation.  This division's task: "critically assess the assumptions, mathematical limitations, and potential
relevance of theoretical results, identifying gaps that require further mathematical investigation".  Subagents
selectively.  Rigour, originality checks, preservation and the handoff as before.
*Where it lives here:* `docs/science/ASSUMPTION_AUDIT.md`; `RESEARCH_SYNTHESIS.md` §7, item 0.

## D-2 — the expansion directive [the research owner's text, verbatim]

> **METRICCHAIN — AUTHORIZED RESEARCH EXPANSION AND CROSS-DIVISION COLLABORATION DIRECTIVE**
>
> I am expanding MetricChain from three research divisions to six.
>
> Continue your existing research mandate and promising workstreams. Do not restart the project or unnecessarily interrupt productive mathematical research.
>
> **1. Newly authorized research divisions**
>
> The following three additional divisions are authorized:
>
> Ensemble Identifiability and Certified Inference
> Branch: `research/ensemble-identifiability`
> Mandate: Measure theory, moment problems, ensemble identifiability, partial identification, optimal transport, information theory, minimax inference, and certified uncertainty.
>
> Geometric Inference, Rigidity and Inverse Problems
> Branch: `research/geometric-inference`
> Mandate: Quantitative rigidity, distance geometry, reconstructability, stability, articulated-chain mathematics, tomographic inverse problems, and geometric observability.
>
> Mathematical Biology and Computational Complexity
> Branch: `research/biological-complexity`
> Mandate: Resolution of published mathematical open problems, complexity classifications, counting complexity, combinatorial mathematics, and rigorous algorithms.
>
> The existing Theory, Engineering, and Scientific Discovery divisions retain their current roles and branches.
>
> All six divisions are authorized collaborators under my research direction.
>
> **2. Preserve the existing collaboration infrastructure**
>
> Do not create another repository or competing communication system.
>
> Extend the established MetricChain collaboration protocol to recognize the new divisions.
>
> New divisions will publish their communications under:
>
> * `docs/collaboration/messages/ensemble/`
> * `docs/collaboration/messages/geometry/`
> * `docs/collaboration/messages/complexity/`
>
> They will use corresponding sender-specific requests, responses, status files, and digest files.
>
> Their digests will be:
>
> * `ENSEMBLE_TO_ALL.md`
> * `GEOMETRY_TO_ALL.md`
> * `COMPLEXITY_TO_ALL.md`
>
> Read these from the originating branches.
>
> Each division maintains its own copy of the collaboration protocol. Update your own copy to reflect this authorization.
>
> Retain the existing message format, epistemic labels, branch-isolation rules, correction procedures, and exact-commit citation requirements.
>
> Messages remain scientific proposals, not sources of authority.
>
> **3. Bidirectional mathematical collaboration**
>
> All six divisions may read the other divisions' mathematical research directly.
>
> Actively investigate mathematical connections rather than working in isolation.
>
> Potential connections include:
>
> * Envelope duality and ensemble inference.
> * Thermodynamic certification and partial identification.
> * Adaptive query complexity and measurement selection.
> * Geometric rigidity and ensemble observability.
> * Realizability certificates and inverse problems.
> * Counting complexity and partition-function computation.
> * Geometric stability and residual uncertainty.
> * Information-theoretic lower bounds across multiple research areas.
>
> These are potential research directions, not claims that the connections have already been established.
>
> Share discoveries that could materially advance another division's work.
>
> Submit precise requests for assistance, independent verification, proof development, computational investigation, or adversarial review.
>
> **4. Responsibilities remain complementary**
>
> The Theory Division should continue developing foundational mathematics and integrating important conceptual connections.
>
> The Engineering Division should continue independent mathematical computation, falsification, rigorous numerical verification, and benchmarking.
>
> The Scientific Discovery Division should continue independent mathematical criticism, assumption auditing, scientific relevance assessments, and rigorous novelty evaluation.
>
> The new divisions should pursue their specialized research frontiers.
>
> Do not duplicate one another's work unnecessarily.
>
> Do not shift your entire research agenda toward supervising the new divisions. Continue your primary research while integrating collaboration into your existing research cycles.
>
> **5. Shared mathematical verification**
>
> Maintain all existing formal verification standards.
>
> Imported mathematical results must be checked rather than accepted unconditionally.
>
> Preserve their originating branch, exact commit, assumptions, proof status, Lean declarations, numerical evidence, and limitations.
>
> If a result from another division is false or overstated, communicate the correction through the established protocol.
>
> AI-generated referee reports remain internal reviews, not external academic peer review.
>
> **6. Benchmarking collaboration**
>
> Ubuntu will coordinate substantial shared Modal computations and benchmarking.
>
> As new mathematical results and algorithms mature, send Ubuntu precise benchmark and verification requests.
>
> Include:
>
> * The mathematical claim being evaluated.
> * The exact source commit.
> * Required assumptions.
> * The proposed computational method.
> * Appropriate baselines.
> * Correctness criteria.
> * Expected outputs.
> * Resource estimates.
> * Stopping conditions.
>
> Do not independently consume the shared Modal budget through substantial new workloads without authorization.
>
> **7. Continuous research and consolidation**
>
> Continue your existing continuous research loop.
>
> Include the newly authorized branches in periodic synchronization.
>
> Do not voluntarily terminate productive research because an individual checkpoint or request has been completed.
>
> Maintain frequent commits and continuously updated recovery documents.
>
> Our Claude promotional credits are finite.
>
> When I issue the mandatory consolidation directive, anticipated at approximately $2,000 of aggregate Claude credits remaining, all divisions must transition toward proof completion, verification, integration, documentation, and preservation.
>
> Respect the existing November 30, 2026, 3:00 PM Eastern Time computational hard stop and all explicit resource and authorization boundaries.
>
> **Final instruction**
>
> Continue pursuing substantial mathematical breakthroughs.
>
> Treat MetricChain as one unified mathematical research organization with six specialized, intellectually independent, cooperating divisions.
>
> Preserve mathematical rigor, originality, generality, reproducibility, and honest reporting.
>
> Proceed autonomously within your existing mandate.

(Formatting only: headings in bold, the text indented as a quotation, branch and path names in code type; the
words and their order are the owner's.)

### What D-2 changes here, item by item

1. **Six divisions; three new branches** — `research/ensemble-identifiability`, `research/geometric-inference`,
   `research/biological-complexity`.  Our copy of the protocol (the mailbox table at the head of
   `docs/collaboration/SCIENCE_TO_ALL.md`) names all six; `docs/collaboration/SCIENCE_UPSTREAM_SYNC.md` has a pin for
   each of the five other branches, and every fetch before a commit includes all five.  At the first
   synchronisation after the directive (15:37 UTC on 2026-11-26) none of the three new branches existed on the
   remote; at 15:43 UTC `research/biological-complexity` existed as a branch point on the theory branch, with no
   commit of its own.
2. **Their files are read from their branches** (`messages/ensemble/`, `messages/geometry/`, `messages/complexity/`,
   and the digests `ENSEMBLE_TO_ALL.md`, `GEOMETRY_TO_ALL.md`, `COMPLEXITY_TO_ALL.md`); nothing of theirs is copied
   into ours except as cited text.  We write only to `research/scientific-translation`, as before.
3. **Imported results are checked, with their provenance kept**: originating branch, exact commit, assumptions,
   proof status, Lean declarations, numerical evidence, limitations — the columns of the "Dependencies" table of the
   sync file.  A result of another division that is false or overstated gets a message, not silence.  Our referee
   reports are internal reviews by subagents and the coordinator, never external peer review, and are called so.
4. **Our role, in the owner's words**: "independent mathematical criticism, assumption auditing, scientific
   relevance assessments, and rigorous novelty evaluation" — the audit file, the reviews (`SCI-REV-nnnn`), the
   prior-art matrix.  The new divisions are collaborators to read and to criticise, not workstreams to supervise.
5. **Benchmarks and verification runs of any size go to the engineering division ("Ubuntu") as requests** with
   the nine fields the directive lists (claim, exact source commit, assumptions, method, baselines, correctness
   criteria, expected outputs, resource estimate, stopping conditions); a template is in
   `docs/collaboration/requests/science/TEMPLATE_BENCHMARK_REQUEST.md`.  No substantial Modal workload from here —
   this division has never used Modal and does not start.
6. **Consolidation**: when the owner issues the consolidation directive (expected when about $2,000 of the shared
   Claude credits remain — a balance this division cannot see), the work turns to proof completion, verification,
   integration, documentation and preservation.  Computation ends 2026-11-30 15:00 US Eastern in any case.
7. **Connections to look for** (the owner's list, as directions not claims) and what on this branch already
   touches them: `docs/science/SCIENTIFIC_FRONTIER_MAP.md` and the note "For the three new divisions" that will be
   sent as a message once their branches exist.

## D-3 — the directive on the scientific evaluation of structural-biology software [the research owner's text, verbatim]

*Received in the conversation of this division on 2026-11-26 at about 22:00 UTC (this division's clock: the message
surfaced between two commands, the second of which printed 22:00:26 UTC).*

> **METRICCHAIN — SUPPLEMENTARY RESEARCH DIRECTIVE**
>
> **Scientific Evaluation of Structural Biology Software**
>
> Continue your existing mission as the Scientific Discovery, Translation & Independent Validation Division on:
>
> `research/scientific-translation`
>
> All existing directives remain in force.
>
> I am authorizing a seventh independent research division:
>
> Structural & Computational Biology, Software Development and Applications Division
>
> Branch:
>
> `research/structural-biology`
>
> This division will develop research software and benchmark specifications based on MetricChain's mathematics.
>
> Ubuntu will independently test, reproduce, and substantially benchmark its implementations.
>
> Your additional responsibility is to provide rigorous, intellectually independent scientific evaluation of this work.
>
> **1. Scientific independence**
>
> Do not become an advocate for the software.
>
> Determine whether its mathematical and computational claims correspond to scientifically meaningful structural biology questions.
>
> Attack its strongest claims.
>
> Investigate its most consequential assumptions.
>
> Identify where mathematically valid computations produce scientifically weak conclusions.
>
> A software result should not receive favorable scientific interpretation merely because its implementation is correct or because a related theorem is formally verified.
>
> **2. Physical applicability**
>
> Evaluate whether the implemented methods depend on:
>
> * Fixed structural assumptions.
> * Simplified molecular representations.
> * Discretized conformational spaces.
> * Inaccessible physical constants.
> * Unjustified independence assumptions.
> * Restricted interaction structures.
> * Force-field assumptions.
> * Incomplete models of experimental observations.
> * Approximations that materially change the scientific question.
>
> Distinguish between mathematical guarantees about a specified model and evidence about a physical molecule.
>
> Investigate whether the proposed mathematical guarantee is more precise than the underlying physical model is accurate.
>
> Identify when certified uncertainty is meaningful and when it is overwhelmed by model error.
>
> **3. Experimental relevance**
>
> Evaluate whether proposed structural observables correspond to actual experimentally obtainable information.
>
> Do not assume that idealized mathematical measurements are identical to experimental signals.
>
> Where the software attempts to interpret structural observations, examine:
>
> * The observation model.
> * Measurement uncertainty.
> * Information loss.
> * Nonidentifiability.
> * Model mismatch.
> * Alternative explanations.
> * Dependence on prior assumptions.
> * The distinction between observed and inferred properties.
>
> Identify mathematical prerequisites for credible retrospective experimental validation.
>
> Do not undertake unauthorized experimental execution.
>
> **4. Scientific benchmark criticism**
>
> Review the new division's benchmark specifications before or alongside Ubuntu's independent computational evaluation.
>
> Ask:
>
> * Does this benchmark address an important scientific problem?
> * Are the comparisons appropriate?
> * Is the baseline sufficiently strong?
> * Are the results likely to generalize?
> * Does the method improve a scientifically meaningful quantity?
> * Are favorable examples representative?
> * What important structural regimes are missing?
> * What result would refute the proposed scientific interpretation?
>
> You may propose stronger benchmarks or recommend rejection of misleading comparisons.
>
> Send substantive computational requests through Ubuntu.
>
> **5. Prior art and novelty**
>
> Investigate the relevant scientific literature for major proposed software capabilities and claimed improvements.
>
> Distinguish:
>
> * Established methods.
> * New implementations of known methods.
> * New combinations of existing techniques.
> * Genuine mathematical novelty.
> * Genuine computational novelty.
> * Genuine scientific novelty.
>
> Do not certify novelty solely because a limited search fails to find a prior result.
>
> Record search strategies and unresolved prior-art questions.
>
> Treat claims of solving published open problems or achieving important scientific advances as requiring particularly careful review.
>
> **6. Existing scientific findings**
>
> Continue your existing mathematical and scientific investigations.
>
> Provide Structural Biology with direct access to your relevant findings, including:
>
> * Physical applicability studies.
> * Existing molecular model experiments.
> * Assumption audits.
> * Certified thermodynamic calculations.
> * Negative results.
> * Identifiability limitations.
> * Benchmark designs.
> * Open research questions.
>
> Do not duplicate its software-development mandate.
>
> Instead, identify which of your existing results are mature enough for translation and which remain insufficiently justified.
>
> **7. Collaboration**
>
> Read the new branch:
>
> `research/structural-biology`
>
> and its digest:
>
> `docs/collaboration/STRUCTURAL_BIOLOGY_TO_ALL.md`
>
> Use your existing SCI communication infrastructure.
>
> Send an introductory scientific orientation to the new division covering:
>
> 1. The most promising scientifically relevant results.
> 2. The most serious existing physical limitations.
> 3. Recommended initial validation priorities.
> 4. Claims that should not be made.
> 5. Important existing prior art.
> 6. Relevant open questions.
>
> Review subsequent software findings independently.
>
> When errors or overstatements are discovered, record them explicitly and communicate them to the relevant division.
>
> Maintain the distinction between internal AI review and external human peer review.
>
> **8. Continuity**
>
> Continue your existing autonomous research loop.
>
> Do not abandon mathematical criticism, independent theorem review, assumption auditing, or foundational scientific investigations.
>
> Respect all previous resource limits and deadlines.
>
> When the consolidation directive arrives, prioritize rigorous scientific synthesis, novelty assessments, verification of central claims, documentation of limitations, and publication-quality internal reports.
>
> The new division should increase the scientific usefulness of MetricChain without lowering the standards of evidence.
>
> Your responsibility is to help ensure that this occurs.
>
> Proceed.

(Formatting only: the title and the eight section headings in bold, the text indented as a quotation, one sentence
per paragraph as received; the words, the lists and their order are the owner's.)

### What D-3 changes here, item by item

1. **A seventh division and a seventh branch**: *Structural & Computational Biology, Software Development and
   Applications* on `research/structural-biology`, with the digest `docs/collaboration/STRUCTURAL_BIOLOGY_TO_ALL.md`.
   **At 22:00:26 UTC on 2026-11-26 the branch did not exist on the remote** (the fetch found no such ref); it is in
   the list of branches fetched before every commit from now on, and the first reading is recorded in
   `docs/collaboration/SCIENCE_UPSTREAM_SYNC.md` when it appears.  Our copy of the protocol (the mailbox table at
   the head of `docs/collaboration/SCIENCE_TO_ALL.md`) names it.
2. **This division's added duty is evaluation, not development and not advocacy**: whether the software's
   mathematical and computational claims answer questions that matter in structural biology; its strongest
   claims attacked; its assumptions (fixed structures, simplified representations, discretised conformational
   spaces, inaccessible constants, independence, restricted interactions, force fields, observation models)
   examined; a guarantee about a model kept apart from evidence about a molecule; "is the certificate more precise
   than the model is accurate?" asked every time.  A correct implementation or a machine-checked theorem earns no
   favourable scientific reading by itself.
3. **Benchmark specifications are reviewed here before or alongside the engineering division's evaluation**, with
   the eight questions of the directive's section 4; stronger benchmarks may be proposed and misleading
   comparisons recommended for rejection.  Computation of any size still goes to the engineering division as a
   request (nine fields, D-2).
4. **Prior art for every major capability and claimed improvement**, in the six classes of section 5; a limited
   search that finds nothing certifies nothing; search strategies and unresolved questions are recorded.
5. **An introductory scientific orientation** with the six parts of section 7 is owed to the new division:
   **SCI-MSG-0034** (written before their branch exists, so that it is there when they start).  Our findings stay
   on this branch for them to read: applicability studies, model experiments, assumption audits, certified
   calculations, negative results, identifiability limits, benchmark designs, open questions — with a statement
   of which are mature enough to translate and which are not.
6. **Limits unchanged**: no experimental execution; no biological sequence engineering or target-specific
   functional optimisation (charter D-0, restated in D-1); the resource limits and the deadline of 2026-11-30
   15:00 US Eastern; internal AI review is not external peer review.  At consolidation: synthesis, novelty
   assessments, verification of central claims, documentation of limitations, internal reports of publication
   quality.

## D-4 — the directive on frontier scientific evaluation and an eighth division [the research owner's text, verbatim]

*Received in the conversation of this division on 2026-11-26 at about 22:41 UTC (this division's clock: the message
surfaced with the result of a command; the next command printed 22:42:07 UTC).*

> **METRICCHAIN — SUPPLEMENTARY DIRECTIVE**
>
> **Frontier Scientific Evaluation and Eighth-Division Coordination**
>
> Continue your existing research mission, branch restrictions, autonomous research loop, scientific scope, safety requirements, and resource limitations.
>
> I am authorizing an eighth independent MetricChain division:
>
> Frontier Benchmarking, Experimental Evidence and Scientific Evaluation Division
>
> Branch:
>
> `research/frontier-benchmarks`
>
> Its purpose is to establish rigorous scientific evaluations of MetricChain's mathematical and computational innovations against the strongest relevant contemporary approaches and appropriately scoped experimental evidence.
>
> The existing division of responsibilities remains intact:
>
> * The mathematical divisions develop foundational mathematics.
> * Structural Biology develops research software.
> * Ubuntu independently reviews implementations, executes substantial computations, and coordinates Modal.
> * Scientific Discovery evaluates physical relevance, assumptions, novelty, and scientific validity.
> * Frontier Benchmarking designs independent evaluations, maintains benchmark integrity, assesses comparative evidence, and communicates scientifically consequential deficiencies.
>
> The official CASP17 results are scheduled for release on November 29, 2026.
>
> The official modeling season has already ended. We are not claiming official participation.
>
> The Frontier Benchmarking Division will investigate whether scientifically defensible pre-reference-release evaluations remain feasible for appropriately scoped public benchmarks.
>
> Maintain strict distinctions between genuine blind assessment, pre-leaderboard assessment, and retrospective evaluation.
>
> Do not assume that all CASP17 references remain confidential.
>
> Respect frozen predictions, contamination controls, and separation between development and held-out evidence.
>
> The new division will also investigate broader scientific evaluation opportunities involving structural characterization, conformational ensembles, intrinsic disorder, thermodynamics, structural uncertainty, geometric inference, and other authorized mathematical and physical questions.
>
> Read its published findings directly through the existing collaboration protocol.
>
> Its digest will be:
>
> `docs/collaboration/FRONTIER_BENCHMARKS_TO_ALL.md`
>
> Update your copy of the collaboration protocol to recognize all eight divisions.
>
> Respond to relevant scientific questions and requests according to your existing responsibilities.
>
> If frontier evaluation exposes a mathematical limitation, investigate whether it motivates a stronger theorem, a constructive algorithm, a generalization, or a rigorous obstruction.
>
> Do not abandon your primary research responsibilities.
>
> Do not duplicate the new division's evaluation mandate.
>
> Ubuntu remains responsible for substantial shared computation.
>
> Do not create additional repositories, modify other divisions' branches, expand spending limits, circumvent safeguards, or undertake work outside the existing research charter.
>
> Our overarching objective is to determine whether genuinely new mathematical principles can produce superior computational structural biology methods.
>
> Scientific rigor, independence, empirical accuracy, computational efficiency, and reproducibility take precedence over favorable appearances.
>
> Continue autonomously.

(Formatting only, as for D-3: the title in bold, the text indented as a quotation, one sentence per paragraph as
received; the words, the list and their order are the owner's.)

### What D-4 changes here, item by item

1. **An eighth division and an eighth branch**: *Frontier Benchmarking, Experimental Evidence and Scientific
   Evaluation* on `research/frontier-benchmarks`, with the digest `docs/collaboration/FRONTIER_BENCHMARKS_TO_ALL.md`.
   **At 22:42:07 UTC on 2026-11-26 the branch did not exist on the remote.**  It is the seventh branch of the
   fetch loop from now on; our copy of the protocol (head of `docs/collaboration/SCIENCE_TO_ALL.md`) names all
   eight divisions.
2. **The division of responsibilities, in the owner's words:** this division "evaluates physical relevance,
   assumptions, novelty, and scientific validity"; the new one "designs independent evaluations, maintains
   benchmark integrity, assesses comparative evidence, and communicates scientifically consequential
   deficiencies".  So: **we do not design their benchmarks and do not run comparisons**; we review what a
   comparison means physically, which assumptions it rests on, whether a claimed capability is new, and whether
   the conclusion drawn is valid — and we answer their questions.  `SOFTWARE_EVALUATION_PROTOCOL.md` §5 (our
   benchmark questions, written under D-3) stays our instrument for *criticism of specifications*, not a second
   benchmark programme.
3. **Evidence hygiene around CASP17** (results announced for 2026-11-29; the modelling season is over; no official
   participation is claimed): three kinds of evidence are kept apart in everything we write — *genuine blind
   assessment*, *pre-leaderboard assessment*, *retrospective evaluation*; references are not assumed to be
   confidential; frozen predictions, contamination controls and the separation of development from held-out
   evidence are respected.  **For this division that means:** nothing we learn about held-out references or
   results — in a literature search, on a public page, from another division — goes into any message to a
   developing division before the predictions concerned are frozen, and any such exposure is recorded with its
   time.  We do not look for such references.
4. **A limitation exposed by a frontier evaluation is a mathematical question for us**: does it call for a
   stronger theorem, a constructive algorithm, a generalisation, or a rigorous obstruction?  That is this
   division's existing work, pointed at new evidence.
5. **Unchanged:** the primary research; no new repository; no writing to any other branch; computation of any
   size through the engineering division; the resource limits and the deadline; the scope of the charter (no
   biological sequence engineering, no target-specific functional optimisation, no experiments); internal AI
   review is not peer review.  "Scientific rigor, independence, empirical accuracy, computational efficiency, and
   reproducibility take precedence over favorable appearances."

---

## D-5 — the directive on controlled consolidation and a temporary research halt [the research owner's text, verbatim]

*Received by this division on 2026-11-27 at about 01:00 UTC (it arrived while a tool was running; the clock read
01:01:30 UTC at the first command after it).  The text below is the owner's, in full, with its clarification.*

> **Urgent Research Owner Directive — Controlled Consolidation and Temporary Research Halt**
>
> The shared Claude promotional credit balance is now approximately $5,912.74 of the original $15,000 allocation.
>
> We have accomplished substantial research across all eight divisions. However, I am implementing an immediate controlled consolidation phase before determining how to allocate the remaining resources.
>
> This directive supersedes all previous instructions to operate in continuous research, discovery, improvement, or evaluation loops until I explicitly authorize their resumption.
>
> **1. Suspend expansion immediately**
>
> Do not initiate new speculative research directions, mathematical workstreams, large literature investigations, software projects, extensive benchmarking campaigns, or subagent investigations.
>
> Identify all active subagents and ongoing tasks under your control.
>
> Preserve their existing work. Permit completion only where a task is genuinely near completion and materially contributes to an important result. Otherwise, terminate or suspend it safely.
>
> Do not interpret consolidation as an instruction to solve every remaining open problem. Unresolved problems should be documented accurately rather than pursued indefinitely.
>
> **2. Finish and preserve the strongest existing work**
>
> Bring your current research to a clean, reproducible, durable checkpoint.
>
> Prioritize:
>
> * Completion of nearly finished, consequential mathematical proofs.
> * Resolution of known correctness defects.
> * Preservation of existing formal verification and computational evidence.
> * Accurate identification of incomplete, conjectural, unreviewed, or potentially incorrect results.
> * Documentation of assumptions and limitations.
> * Preservation of source code, test suites, raw computational results, and reproducibility instructions.
> * Updating collaboration records and handoff documentation.
>
> Do not spend substantial resources formalizing elementary results or performing redundant investigations merely to increase completion statistics.
>
> Do not manufacture proof closure where an argument remains incomplete.
>
> **3. Produce a critical research assessment**
>
> Create `docs/collaboration/consolidation/<your-division>.md` on your designated branch.
>
> This document must include:
>
> **A. Executive assessment**
>
> Explain what your division has actually accomplished, in scientifically defensible terms.
>
> **B. Five strongest contributions**
>
> Rank your five strongest contributions by their combined mathematical originality, correctness, significance, and potential scientific utility.
>
> For each, provide:
>
> * The exact mathematical or computational contribution.
> * Relevant commits, files, theorem identifiers, and artifacts.
> * Formal verification and review status.
> * Essential assumptions.
> * Closest known prior art.
> * The exact distinction from that prior art.
> * Evidence supporting originality.
> * Evidence against originality.
> * Current experimental or computational validation.
> * Known limitations.
> * Remaining work required before publication or practical deployment.
>
> If fewer than five contributions deserve inclusion, report fewer.
>
> **C. Negative results and rediscoveries**
>
> Identify the most consequential failures, false conjectures, rediscoveries, unfavorable comparisons, and limitations.
>
> Explain which research directions should be abandoned or deprioritized.
>
> **D. Practical opportunities**
>
> Identify the most promising ways in which your existing work could produce a demonstrably useful computational biology capability.
>
> Distinguish between mathematical possibility, implemented software, synthetic validation, realistic computational validation, and experimental evidence.
>
> **E. Recommended next actions**
>
> Propose no more than three high-priority follow-up investigations.
>
> For each, specify:
>
> * Scientific objective.
> * Existing prerequisites.
> * Missing mathematical or computational components.
> * Appropriate published baselines.
> * Proposed benchmark.
> * Measurable success and failure criteria.
> * Estimated Claude reasoning requirements, if estimable.
> * Estimated computational requirements and Modal cost.
> * Dependencies on other divisions.
> * Whether the work requires Fable or could reasonably continue using Opus.
>
> Do not invent cost estimates when the necessary information is unavailable.
>
> **F. Publication readiness**
>
> Identify any potentially publishable standalone result and explain what remains necessary to make it defensible before an external human expert.
>
> Do not equate formal verification with novelty.
>
> **4. Division-specific consolidation priorities**
>
> Theory: preserve the strongest original mathematical results, especially adaptive free-energy query complexity, certificate kernels, and practically consequential algorithms.
>
> Engineering: preserve reproducible benchmark evidence, identify actual implementation bottlenecks, reconcile the compute ledger, and document the status of every running Modal job.
>
> Science: produce a critical assessment of mathematical originality, physical applicability, model deficiencies, and the strongest credible scientific applications.
>
> Ensemble Identifiability: identify the strongest original theorems and the most promising route toward informative, experimentally relevant certified ensemble inference.
>
> Geometry: preserve the strongest reconstruction, rigidity, and stability results, distinguishing established mathematics from potentially original contributions.
>
> Biological Complexity: identify genuinely original results and mathematical techniques that directly address consequential computational bottlenecks.
>
> Structural Biology: preserve working software, certificates, benchmark results, physical-model deficiencies, implementation limitations, and the shortest credible path toward useful computational performance.
>
> Frontier Benchmarking: consolidate the independent evaluation evidence, negative results, benchmark readiness assessments, contamination controls, sealed evaluation procedures, and prioritized recommendations for subsequent benchmarking.
>
> **5. Existing Modal computation**
>
> Engineering may allow already authorized, bounded, useful Modal jobs to finish without continuous Claude supervision where this is technically possible and safe.
>
> Do not launch new substantial Modal jobs under this directive.
>
> Record running jobs, remaining timeouts, worst-case outstanding expenditure, and the procedure for collecting results later.
>
> All existing budget limits remain binding.
>
> **6. Preserve evaluation integrity**
>
> Do not open sealed held-out datasets, disclose credentials, tune against held-out results, or compromise previously frozen evaluation protocols.
>
> Preserve all evaluation commitments and their associated provenance.
>
> **7. Final handoff and halt**
>
> Commit and push your consolidated research artifacts to your designated branch.
>
> Update your division's status file and collaboration digest.
>
> Send a final concise consolidation message through the established GitHub collaboration infrastructure.
>
> Report directly to me:
>
> 1. Your final commit hash.
> 2. Your strongest contributions.
> 3. Your most consequential unresolved problems.
> 4. Your recommendation for the next phase.
> 5. Whether any subagents, background processes, scheduled sessions, or computational jobs remain active.
>
> Do not start another research cycle.
>
> Do not automatically resume when another division sends a message.
>
> Do not schedule additional reasoning sessions.
>
> Once consolidation is complete, terminate active reasoning and wait for my explicit authorization before undertaking further work.
>
> The objective is to preserve the maximum scientific value already created while minimizing additional Claude expenditure.
>
> Be concise, efficient, rigorous, and critical. We will make the next research allocation decision collectively after all eight divisions have consolidated.
>
> **Clarification: Graceful Research Wind-Down**
>
> This consolidation directive is not an instruction to abruptly interrupt valuable research or artificially truncate an ongoing mathematical argument, computational investigation, software implementation, or verification process.
>
> I want you to reach a natural, scientifically coherent stopping point.
>
> Specifically:
>
> * If you are in the middle of a promising mathematical proof that appears reasonably close to completion, finish it if doing so requires only a bounded amount of additional work.
> * If an ongoing investigation is approaching a consequential conclusion, allow it to reach that conclusion.
> * If a subagent is close to delivering valuable results, collect and review those results before terminating it.
> * If an implementation is partially completed, bring it to a coherent, testable checkpoint where reasonably feasible.
> * If a verification or benchmark is already underway, preserve its results and allow it to finish where appropriate under existing resource constraints.
> * Finish essential cross-divisional communications concerning discoveries, corrections, dependencies, and unresolved problems.
>
> Exercise judgment about the scientific value and remaining cost of each activity.
>
> Do not sacrifice a potentially important discovery merely to terminate the session slightly earlier. Equally, do not interpret this clarification as permission to continue indefinitely, pursue additional speculative directions, launch another wave of subagents, or attempt to resolve every outstanding problem.
>
> If a significant result cannot reasonably be completed during consolidation, preserve the complete current argument, intermediate findings, attempted approaches, unresolved mathematical steps, code, and precise instructions for resuming the investigation.
>
> Where possible, leave every research direction in a state that another capable model or human researcher could resume without repeating substantial work.
>
> The intended sequence is:
>
> 1. Finish valuable ongoing work that is reasonably close to completion.
> 2. Verify and preserve the resulting findings.
> 3. Complete the consolidation report and durable handoff.
> 4. Commit and push everything to your designated branch.
> 5. Stop active reasoning and await my explicit authorization.
>
> Do not begin another autonomous research cycle after reaching this checkpoint.
>
> I am asking for an orderly scientific wind-down, not an emergency shutdown or abandonment of the research programme.

### What D-5 changes here, item by item

1. **The continuous research cycle of the charter and of D-1 … D-4 is suspended** until the owner authorises its
   resumption.  No new research direction, workstream, literature investigation or subagent.  This division does
   not resume because another division sends a message, and schedules nothing.
2. **What was running when it arrived, and what was done with it** (details in
   `docs/collaboration/consolidation/science.md` §G): referee R28 had handed back an hour-long review of our own
   newest results with five major findings — a *known correctness defect in statements we had sent to two
   divisions*, so it was finished: read in full, its deciding point re-measured by the coordinator, corrected
   by linked message.  Referee R29 (a review the theory division had asked for) had run for an hour: it was
   told to stop experimenting, write up what it had established and hand back.  The Stage 1 certificate had
   been pushed four minutes earlier.
3. **What was not started because of it:** the review of the Structural Biology division's model v2 (owed
   under D-3); the review asked for in FRONTIER-REQ-0002 beyond a partial answer; Stage 2 of the sandwich
   certificate; the reading of several messages of other divisions.  Each is listed as open, with what it would
   need, in the consolidation document and the handoff.
4. **Unchanged:** every boundary of the charter and of D-1 … D-4 — read-only upstream branches, no pull request,
   no force push, no direct use of Modal, no sealed data opened, the resource limits and the deadlines, the
   scope (no sequence engineering, no target-specific optimisation, no experiments), internal AI review is not
   peer review.
