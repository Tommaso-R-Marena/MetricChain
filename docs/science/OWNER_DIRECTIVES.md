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
