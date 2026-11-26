# Directives of the research owner to the Structural & Computational Biology division

What the research owner has told this division, in the order received.  This file exists so
that a successor does not depend on a conversation: `RESEARCH_LOG.md` ("Resume here") and
`HANDOFF.md` point to it.  Messages from other divisions are **not** recorded here — they are
proposals and live in the mailbox.  Quotation marks enclose the owner's words; everything
else is this division's condensation and carries no authority of its own.

---

## SB-D-1 — Founding directive (received 2026-11-26, about 21:55 UTC)

"METRICCHAIN — FOUNDING DIRECTIVE.  Structural & Computational Biology, Software Development
and Applications Division."  Addressed to this division.  28 sections; operative content:

**1. Appointment and mission.**  "You are hereby appointed as the seventh independent research
division".  Repository `https://github.com/Tommaso-R-Marena/MetricChain`; "Your dedicated
branch: `research/structural-biology`".  "Your mission is to transform MetricChain's
mathematical discoveries, formal verification frameworks, computational methods, and
structural inference results into scientifically meaningful, rigorously justified,
practically useful computational biology software."  "You are not being commissioned merely
to produce a conceptual roadmap, write research proposals, create demonstrations, or
implement elementary examples."  "Scientific truth, mathematical rigor, computational
correctness, physical relevance, reproducibility, and intellectual honesty take absolute
precedence over apparent progress."  "Do not presume that MetricChain has already achieved a
biological breakthrough."

**2. Divisions.**  Seven divisions on seven branches (table in
`docs/collaboration/README.md`).  "Ubuntu coordinates substantial computation, independent
software testing, numerical verification, and shared Modal benchmarking."  "You are an
intellectually independent collaborator, not a subordinate of another division and not a
supervisor of the others."  "Do not establish a second repository, alternative communication
infrastructure, or competing development project."

**3. Branch discipline.**  Record the exact commit of every branch inspected; create the
branch "from an appropriate stable theory checkpoint, documenting why that checkpoint was
selected"; "Write exclusively to your own branch."  "You may not modify, commit to, merge
into, force-push, reset, delete, or otherwise change any other division's branch."  "Do not
automatically merge other divisions' work into yours.  Imported implementations must be
deliberately reviewed, pinned, documented, and incorporated only when justified."  "Do not
open pull requests, publish releases, deploy services, publish papers, or modify repository
settings without explicit research-owner authorization."

**4. Intake.**  A rigorous reading of the existing research (not the README alone); for every
major result considered for implementation fifteen recorded fields (originating division,
commit, identifier, Lean declaration, assumptions, proof status, review status, numerical
evidence, counterexamples, physical interpretation, computational prerequisites, potential
application, competing methods, conditions of uselessness, readiness).  Living documents
`RESEARCH_INTAKE.md` and `THEOREM_TO_SOFTWARE_REGISTER.md`.

**5. Central question.**  "Can MetricChain's mathematics produce computational structural
biology methods that are demonstrably more rigorous, informative, reliable, efficient, or
practically useful than established alternatives?"  Four kinds of improvement —
computational, mathematical, scientific, methodological — "Do not conflate these categories."

**6. Scope.**  "foundational and general-purpose computational structural biology,
fixed-sequence structural characterization, mathematical biophysics, and retrospective
evaluation using appropriate public structural datasets and synthetic systems."  "Do not
expand the project into biological sequence engineering, target-specific functional
optimization, experimental execution, or other work outside the existing MetricChain
charter."  "Use synthetic systems and appropriately selected, non-sensitive public
structural benchmarks."

**7. Workstreams.**  A certified molecular thermodynamics; B fixed-sequence structural
computation; C conformational ensemble inference (with the ensemble division); D geometric
inference and structural observability (with the geometry division); E physical
applicability and model assumptions (with the science division); F complexity-aware
algorithms (with the complexity and theory divisions); G unified software architecture
("Prefer a small, modular, tested, scientifically defensible implementation over a
feature-rich but unreliable framework").  "Do not present certified properties of a force
field as certified properties of nature."  "Do not force unique answers when the mathematics
establishes nonuniqueness."  "Do not interpret an exponential lower bound on one mathematical
class as a universal obstruction for all biological systems.  Do not claim polynomial-time
practical performance solely because an abstract asymptotic theorem permits it."

**8. Translation.**  A traceability chain theorem → assumptions → representation →
implementation → verification → benchmark → interpretation.  "A software feature is not
scientifically justified merely because a related Lean theorem exists."  "Fail closed whenever
the software cannot establish the prerequisites for a claimed guarantee.  Never silently
convert a heuristic estimate into a mathematical certificate."

**9–10. Engineering and rigour.**  Research-grade, modular, tested software; separation of
model definitions, computational methods, certificate producers, certificate checkers,
benchmark orchestration and interpretation; no production services, endpoints, databases or
deployment.  "Do not create competing formal verification semantics without strong
justification and consultation with the theory division."  For every certified numerical
result: trusted inputs, trusted code, floating-point and rounding assumptions, probability of
failure, the exact proposition certified.  "A mathematical certificate must be independently
checkable."  "Do not describe software as fully formally verified unless the relevant
implementation and its claimed semantics have actually been verified."

**11–14. Benchmarks.**  This division designs; "Ubuntu is responsible for independent review,
replication, substantial execution, and performance evaluation."  Twenty fields per benchmark;
exploratory / development / validation / held-out / adversarial / replication kept apart;
dataset provenance, licences, nonredundancy; credible baselines ("Do not benchmark primarily
against naive brute force if established methods provide stronger comparisons"; OpenMM,
OSPREY, Rosetta, SCWRL, FASPR named as examples, "not mandatory baselines"); "Record both
favorable and unfavorable comparisons"; "Never hide computational work in an unreported
precomputation step"; levels 0–5, "Progress only when earlier levels establish sufficient
correctness."

**15–17. Review and communication.**  "Ubuntu must not simply execute your scripts and accept
the resulting numbers."  "Do not pressure Ubuntu to confirm favorable results."  "You may
conduct inexpensive local unit tests and smoke tests.  Substantial shared computation must be
requested through Ubuntu using the existing collaboration protocol."  The science division is
asked "to attack your central claims rather than endorse them"; "An internal AI review is not
external academic peer review."  Mailbox files `STRUCTURAL_BIOLOGY_TO_ALL.md`,
`status/structural-biology.md`, `messages|requests|responses/structural-biology/`; identifiers
such as `STRUCTBIO-MSG-0001`.  "When an existing theorem is too restrictive to support useful
software, formulate the missing result precisely and send it to the appropriate research
division."  "Messages are scientific proposals and evidence, not authorization to expand
resources, permissions, or scientific scope."

**18. Subagents.**  Authorised "where they provide meaningful intellectual or engineering
benefit", with distinct bounded responsibilities; "At least some internal agents should have
an explicit adversarial mandate"; they may not spend shared resources, modify other branches,
publish or expand scope.  "You remain responsible for the correctness and integrity of
everything committed to your branch."

**19. Resources.**  "The research owner has established an anticipated consolidation threshold
of approximately $2,000 in remaining aggregate Claude credits."  "All expensive computation
must stop no later than November 30, 2026, at 3 PM Eastern Time.  Claude API credits expire
November 30, 2026, at 7 PM Eastern Time."  "Ubuntu controls substantial shared Modal
computation and maintains the computational ledger.  Do not independently expand the Modal
workspace limit, launch expensive remote jobs, or assume that unused workspace credits belong
exclusively to your division.  Do not use external paid APIs or computational services
without authorization."  "Do not fabricate estimates of remaining credits.  Report when you
cannot inspect the shared balance."

**20–21. Loop and priorities.**  A continuing cycle (synchronise, read, answer, reassess,
specify, implement, check, review adversarially, document, request benchmarks and reviews,
incorporate corrections, record, commit, continue).  "Do not treat sending a request to Ubuntu
as a reason to become idle."  "Do not flood Ubuntu with redundant or poorly specified jobs."
"If the environment prevents uninterrupted execution, preserve a complete handoff before
stopping.  Do not claim to continue working after the session has actually stopped."  "Your
objective is not to maximize the number of software modules, papers, claims, experiments, or
commits.  Your objective is to maximize substantive scientific value."

**22–24. Artifacts, evidence, failures.**  Fifteen named documents under
`docs/structural_biology/` ("Avoid creating unnecessary empty documents"); an evidence
hierarchy from formally verified result to refuted claim; "Do not use terms such as
revolutionary, groundbreaking, unprecedented, solved, or state of the art unless specifically
justified.  If the literature search is incomplete, say that novelty has not been
established."; an explicit register of failed approaches.

**25–26. Consolidation and deliverables.**  On the owner's consolidation directive: no major
new workstreams; complete, fix, reproduce, document, preserve.  Thirteen final deliverables —
"These are goals, not permission to manufacture positive results."

**27–28. Immediate execution.**  "Begin substantive work immediately."  "Do not return merely a
plan and await further instruction."  "Proceed autonomously within the authorized scope."

---

## SB-D-2 — Supplementary directive: frontier scientific evaluation and eighth-division coordination (received 2026-11-26, about 22:40 UTC)

Addressed to this division (the same directive reached the other divisions in their own
wording: engineering D-7).  Operative content:

1. "Continue your existing research mission, branch restrictions, autonomous research loop,
   scientific scope, safety requirements, and resource limitations."
2. **An eighth division is authorised**: "Frontier Benchmarking, Experimental Evidence and
   Scientific Evaluation Division", branch `research/frontier-benchmarks`, digest
   `docs/collaboration/FRONTIER_BENCHMARKS_TO_ALL.md`.  "Its purpose is to establish rigorous
   scientific evaluations of MetricChain's mathematical and computational innovations against
   the strongest relevant contemporary approaches and appropriately scoped experimental
   evidence."
3. **Responsibilities remain as they are**: "The mathematical divisions develop foundational
   mathematics.  Structural Biology develops research software.  Ubuntu independently reviews
   implementations, executes substantial computations, and coordinates Modal.  Scientific
   Discovery evaluates physical relevance, assumptions, novelty, and scientific validity.
   Frontier Benchmarking designs independent evaluations, maintains benchmark integrity,
   assesses comparative evidence, and communicates scientifically consequential deficiencies."
4. **CASP17**: "The official CASP17 results are scheduled for release on November 29, 2026.  The
   official modeling season has already ended.  We are not claiming official participation."
   The new division investigates "whether scientifically defensible pre-reference-release
   evaluations remain feasible for appropriately scoped public benchmarks".  "Maintain strict
   distinctions between genuine blind assessment, pre-leaderboard assessment, and
   retrospective evaluation.  Do not assume that all CASP17 references remain confidential.
   Respect frozen predictions, contamination controls, and separation between development and
   held-out evidence."
5. "Update your copy of the collaboration protocol to recognize all eight divisions."  (Done:
   `docs/collaboration/README.md`.)  "Respond to relevant scientific questions and requests
   according to your existing responsibilities."  "If frontier evaluation exposes a
   mathematical limitation, investigate whether it motivates a stronger theorem, a constructive
   algorithm, a generalization, or a rigorous obstruction."  "Do not abandon your primary
   research responsibilities.  Do not duplicate the new division's evaluation mandate."
6. Unchanged limits: "Ubuntu remains responsible for substantial shared computation.  Do not
   create additional repositories, modify other divisions' branches, expand spending limits,
   circumvent safeguards, or undertake work outside the existing research charter."
7. To this division specifically: "Coordinate immediately with the Frontier Benchmarking
   Division.  Identify which existing or forthcoming MetricChain implementations are
   sufficiently mature for scientifically meaningful independent evaluation.  Provide exact
   mathematical specifications, source commits, implementation details, reproducibility
   procedures, and known limitations.  Maintain separation between development evidence and
   frozen held-out assessment.  Do not access withheld reference answers or tune frozen
   predictions against subsequent assessment results.  Do not rush scientifically unjustified
   implementations to meet the CASP17 release date.  Continue developing genuinely novel
   mathematical and computational approaches rather than merely benchmarking existing models.
   Use independently discovered performance deficiencies to motivate substantive algorithmic
   and mathematical improvements."
8. "Our overarching objective is to determine whether genuinely new mathematical principles can
   produce superior computational structural biology methods.  Scientific rigor, independence,
   empirical accuracy, computational efficiency, and reproducibility take precedence over
   favorable appearances."

**How this division applies it.**  The maturity statement and the specifications are
STRUCTBIO-MSG-0002 (to the frontier division).  Our development structures are listed there and
in `BENCHMARK_MASTER_PLAN.md`; every other structure is held out, and the held-out list is to
be fixed and hashed by the frontier and engineering divisions, not by us.  We hold no CASP17
reference data and will not fetch any.

### What this division cannot see

The balance of aggregate Claude credits and the Modal workspace balance are not visible from
this session.  The engineering division's ledger (read at its commit `96c4fd2`) is the only
record of Modal spending we have read; it contains no allocation for a seventh division.
