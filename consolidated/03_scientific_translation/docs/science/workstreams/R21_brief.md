# Workstream R21 (launched 2026-11-26) — adversarial review, asked for by the Ensemble division: "ensemble rigidity = global rigidity" (their Theorems E5, E7, E8), the reading of E1.3, and §5 of their report

*Brief written by the coordinator.  Read `COMMON.md` first (its commit pins are out of date).  The object is the
branch `research/ensemble-identifiability` at commit `a570520` (first checkpoint of the Ensemble Identifiability and
Certified Inference Division, one of three divisions the research owner added on 2026-11-26); a read-only export
is at `/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/ens_ro_a570520/`
(called `<ENS>`: `docs/ensemble/`, `docs/collaboration/messages/ensemble/`, `experiments/ensemble/`,
`proofs/Ensemble/`).  If the agent of this workstream is gone, its notes are in `experiments/science/ws_R21/` and its
draft in `R21_REPORT.md`.*

## What was asked, and by whom

`<ENS>/docs/collaboration/messages/ensemble/ENSEMBLE-MSG-0002.md`, §4, question E-S2 — read the message first:
"Please attack E7/E8 and §5 of the report: novelty (we found no theorem on mixtures of frameworks from per-edge
distance laws; the nearest neighbours are unlabeled PCA and the 2022 product lemma), hidden assumptions (genericity
excludes conformers with common rigid domains; exact laws), and the reading of E1.3 (mean squared distances
determine nothing)."  The report is `<ENS>/docs/ensemble/ENSEMBLE_REPORT.md` (793 lines): §3.2 Theorem E5 (generic
tuples admit no chimera iff the algebraic matroid of the features is connected), §3.3 Theorem E7 (for a graph on at
least `d + 2` vertices: generically globally rigid in `ℝ^d` iff every generic finite ensemble of frameworks, with
any number of conformers and any weights, is determined modulo congruence by the one-dimensional laws of its edge
lengths) and Theorem E8 (`2K` moments of each squared edge length determine a generic `K`-conformer ensemble, with
the certificate `Σ_e Π_i (ℓ_e² − ℓ_e(x_i)²)²`), §2 Proposition E1.3, §5 ("What this says inside the programme"), §8
(limitations).  Their prior-art file and theorem register: `<ENS>/docs/ensemble/PRIOR_ART.md`, `THEOREM_REGISTER.md`.
The coordinator has already sent a note on their Theorems E1/E2 (`docs/collaboration/responses/science/SCI-RES-0026.md`
— read §2 of it so as not to repeat it); E1–E4 and Part III are **not** your object.

## Item 1 — Theorem E7, with E5 as its engine

(i) State E5 and E7 with every hypothesis the text leaves implicit: what "generic" means for a *tuple* of conformers
(jointly generic, or each generic), what "determined modulo congruence" means for an ensemble (each conformer up to
its own congruence; weights), the base field, `N ≥ d + 2`, whether conformers may be congruent to one another.
(ii) The two cited theorems on which E7 rests: which are they, are they quoted correctly, and are their hypotheses
met (open the papers if you can — see "Rules: literature" — and say for each sentence whether it is from the paper
or from memory).  (iii) Re-derive both directions.  For "globally rigid ⇒ determined": the step from "no chimera"
to "every edge-length law pins down the multiset of conformers with weights" — where do weights enter, what if two
conformers share an edge length (non-generic) or all of them, what about a continuum of conformers?  For
"determined ⇒ globally rigid": the construction of two different ensembles with the same edge-length laws when the
graph is not globally rigid — is it a *generic* ensemble?  (iv) E5: "iff the algebraic matroid is connected" — check
the proof and the role of "no `F_e` is constant"; find the smallest example on each side.

## Item 2 — Theorem E8 and its certificate

`2K` moments of each squared edge length; the polynomial `Σ_e Π_i (ℓ_e² − ℓ_e(x_i)²)²` vanishes exactly on the
configurations each of whose edge lengths is that of some conformer — the chimeras; so its mean is zero for an
ensemble iff the ensemble lives on chimeras, and by E7 the chimeras of a generic ensemble are its conformers.
Re-derive; then: does "determine" include the weights (which moments fix them); is the count `2K|E|` right and can
it be lowered; **what is the stability** — the certificate has a `K`-fold product of squared differences, so its
growth near a conformer is quadratic and its value between two close conformers tiny: say what error of the
moments is tolerated, at least in order of magnitude, for a small example (this is the "hidden assumption: exact
laws" in numbers).

## Item 3 — replication with your own code

Small frameworks in the plane (`d = 2`): (a) a globally rigid graph on 5 or 6 vertices and generic ensembles of
`K = 2, 3` conformers: search numerically for a chimera (a framework whose every edge length is taken from one of
the conformers, not all from the same one) by nonlinear least squares from many random starts — none should
exist — with a **control that must find one**: a graph that is rigid but not globally rigid (a flip ambiguity), or
conformers that share a rigid part; (b) for E8, the mean of the certificate polynomial under a generic ensemble
and under a perturbed one.  Do not import their scripts before yours are final; then re-run
`<ENS>/experiments/ensemble/run_all.py` from a scratch copy (`python3 -I -B`) and compare with their `output.txt`.

## Item 4 — the reading of E1.3 and of §5; hidden assumptions; what the statements mean for data

E1.3: "mean squared distances — on any graph — determine no ensemble of frameworks, not even a single
conformation."  Check the proof (the coordinator's guess: affine images `xA_k` with `Σ p_k A_kᵀA_k = I` have the same
mean squared distances; is that their argument, and does it need the mixture to be non-congruent?).  Then say what
a reader may and may not conclude from Part II for measured data: laws versus moments versus means of nonlinear
functions of a distance; exact laws versus laws with a band; one law per edge measured on separate samples; point
conformers versus conformers that are themselves distributions; genericity versus conformers that share rigid
domains (their own limitation — how restrictive is it for articulated chains, where most conformers share most
rigid parts?).  Is anything in §5 or in the message's headline ("ensemble rigidity = global rigidity") stated more
generally than the theorem?

## Item 5 — novelty

Their claim: "no theorem on mixtures of frameworks from per-edge distance laws".  Search (generic queries only):
identifiability of mixtures of point configurations from distance distributions; unlabeled distance geometry;
"beltway" and "turnpike" problems for the union of distances; reconstruction of several conformations from pooled
distance data.  Say for each statement E5, E7, E8, E1.3 whether, as far as you can see, it is new, a formulation of
something known, a corollary of the cited theorems, or a rediscovery — with what you opened.

## Rules

Write only in `experiments/science/ws_R21/` and `docs/science/workstreams/R21_REPORT.md`.  No state-changing git;
no subagents; no `lake`; `<ENS>` stays untouched (copy what you run into `ws_R21/rerun_copy/`, which will not be
committed).  **Literature:** web search and fetch for published papers and their definitions only, with generic
queries; put no name, file or text of this project into a query; upload nothing; cite only what you opened and
say "from memory" or "from a search summary" otherwise; never invent a bibliographic detail.  Keep four kinds of
checking apart: **review**, **replication** (own code), **re-run** (their code), **read only**.  A finding is
*critical*, *major* or *minor*; give a replacement text for each.  Report what you did not check, and your own
errors.  Machine: 4 cores and 15 GB shared with other jobs — `OMP_NUM_THREADS=1`, at most two processes, no process
above 2 GB, no run longer than 20 minutes; before any run of more than five minutes write its cost into `NOTES.md`.
Keep `NOTES.md` from the first minute.  A log is cited only if its run reached its last line; logs of stopped or
failed runs go into `not_cited/`; fresh names instead of overwriting.  A time written into a file is read from the
clock.  Every check is reported with the violations of its control.  **If a tool declines an action, do not work
around it: keep everything in `NOTES.md` and return the findings as text in your hand-back.  Do not delete files
with wildcards or `rm -r`.**  This is an internal review, not external peer review; say so in the report.

## The report

(0) Verdict in ten lines: are E5, E7, E8, E1.3 proved as stated; the findings by class.  (1) The statements with
their implicit hypotheses.  (2) Findings, each with the line that decides it and a replacement text.  (3) Your
numerical tests, with their controls.  (4) Re-runs.  (5) What the statements mean for data (Item 4).  (6) Novelty
(Item 5), with what you opened.  (7) Requests to the Ensemble division that can be sent as they stand.  (8) What
you did not check; your own errors; files.
