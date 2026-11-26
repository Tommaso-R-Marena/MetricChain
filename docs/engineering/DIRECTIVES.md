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
