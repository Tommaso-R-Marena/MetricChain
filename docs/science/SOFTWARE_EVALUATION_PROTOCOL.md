# How this division evaluates structural-biology software built on MetricChain's mathematics

*Science division.  Version 1 (2026-11-26, after checkpoint 64).  Written under the research owner's directive
"Scientific Evaluation of Structural Biology Software" (`OWNER_DIRECTIVES.md`, D-3) before the Structural &
Computational Biology division had committed anything, so that the standard exists before the first claim does.
It is an instrument for this division's reviews, not a rule for anyone else; a review that departs from it says
where and why.  Every review made with it is an internal review by an AI session, not external peer review.*

## 0. What an evaluation is for, and what it is not

The question is never "is the implementation correct?" — that is the engineering division's — and never "is the
theorem true?" alone.  It is: **does this computation answer a question that matters about a molecule, and how
much of the answer survives the distance between the model and the molecule?**  A correct implementation of a
machine-checked theorem can produce a scientifically empty number; the review says so when it does.  We do not
develop their software, do not tune it, and do not argue for it.  We do not run experiments.  Computations of any
size go to the engineering division as nine-field requests (`docs/collaboration/requests/science/TEMPLATE_BENCHMARK_REQUEST.md`).

## 1. The claim sheet (asked of them once per capability; requests S-1 … S-5 of SCI-MSG-0034)

| field | what we need | why |
|---|---|---|
| claim | one sentence, with the quantity and the accuracy claimed | a review needs a statement that can be false |
| model | energy function; representation (which atoms move with which variable); discretisation; treatment of the backbone; solvent; temperature | every guarantee is relative to this |
| observation model | for anything compared with data: the forward map, its error, the data's error model | §4 |
| certified / estimated | which numbers carry a proof, which a confidence statement, which neither | they are not to be added |
| imports | theorems and constants taken from other divisions, with commits and proof status | imported results are checked, not assumed (D-2) |
| source commit, script, log | — | replication |
| baseline and refutation | the method a practitioner would use; the outcome that would refute the interpretation | §5 |

## 2. Physical applicability: the nine questions of the directive, and what on this branch bears on each

| the method depends on … | what we ask | what this branch has measured or proved (pointers; all model-relative) |
|---|---|---|
| fixed structural assumptions | which degrees of freedom are frozen; what the conclusion becomes if they move by their thermal amplitude | with backbone torsions free nothing is pairwise: vacuum ff14SB mixed differences up to 28 kcal/mol, 12 at separation seven (`PHYSICAL_APPLICABILITY.md` §1) |
| simplified molecular representations | what was coarse-grained; whether the observable is defined on the fine model | lattice chains, bead chains and rotamer models are all on this branch; none is a molecule |
| discretised conformational spaces | the discretisation term, as a number in the units of the result | Proposition A17.24: second order in the cell size; on a toy chain 1.3 nats per angle at three cells per angle (addendum A17 (25)).  **On a real force field (addendum A17 (26)):** the rigid-rotamer table's free energy is off the continuous one by `−3.2` to `+2.0` nats per torsion; for leucine its minimum-energy state is not the well of the continuous minimum; with one-residue cell free energies the coupling between valines is discretised to `4·10⁻⁴`–`4·10⁻²` nats per torsion at three cells |
| inaccessible physical constants | which constants the guarantee needs and how each was obtained: proved, evaluated, measured on a grid, fitted | class constants measured on grids are lower bounds, not bounds; held-out maxima up to ten times fitted ones; by analysis alone a loss of 33 to 1 400 (`PHYSICAL_APPLICABILITY.md` §§0, 2) |
| unjustified independence assumptions | which variables are treated as independent, and the coupling that was dropped | the query-complexity exponents are for independent sites; with a cooperative known part the direction depends on the envelope (SCI-REV-0010; SCI-RES-0033) |
| restricted interaction structures | band width, order, pairwise form: what is outside, and its certified size | the solvent term is pairwise only up to third-order constants of 0.003–0.2 kcal/mol for neutral side chains; compact and charged cases cost orders more (SCI-MSG-0024, -0027) |
| force-field assumptions | the spread between force fields of one lineage in the units of the result | refits change single-residue terms by 0.64–2.6 kcal/mol and reorder helix, strand and polyproline II of a flexible peptide (`PHYSICAL_APPLICABILITY.md` §1) |
| incomplete models of experimental observations | §4 | identified sets; homometric chains; the reflection gap of sequence-local distances (`INFERENCE_LIMITS.md`; SCI-REV-0023 §5) |
| approximations that change the scientific question | state the question before and after the approximation, in words | "the free energy of a peptide" → "the logarithm of a sum over library rotamers on one backbone": the second is what is certified |

## 3. The error budget: four lines, never merged

Every certified or estimated number is reviewed as four numbers in the same units:

1. **the certified width** (or the confidence interval) — relative to the model as specified;
2. **the discretisation term** — zero only if the claim is about the discrete model, and then the claim says so;
3. **the uncertainty of the energy model** — with its source;
4. **the evaluation tolerance** — rounding and convergence of every evaluated term, proved or assumed.

*The same exercise on this branch's best certificate* (Lys₁₂ on an ideal helix, `9.5·10¹⁰` rotamer assignments;
SCI-MSG-0028, SCI-RES-0035): line 1: `8·10⁻⁵` nats.  Line 2: not bounded for that instance; measured on small blocks of the same force field
(addendum A17 (26)): nats per torsion in absolute terms, tenths of a nat per torsion in a difference between
backbones, and a different dominant rotamer for leucine.  Line 3: of order `kT` per residue between force fields
of one lineage.  Line 4: `10⁻⁴`–`10⁻³` nats at order 5, from an evaluator tolerance of `10⁻⁷` kcal/mol that is
assumed, not proved.  *Verdict by our own standard:* line 1 is not the headline; what the certificate removes
is sampling error from a model-relative number, and for this model an ordinary estimate already agrees with it
to `10⁻⁴`.  A review of someone else's number ends with the same four lines and the same kind of verdict.

**Scientific weight** of a result, stated in every review, is one of: *changes a decision a practitioner would
make* · *removes sampling error only* · *more precise than the model is accurate* · *not interpretable as a
statement about a molecule*.

## 4. Experimental relevance: what is examined when software interprets an observation

The directive's eight items, as review questions: the **observation model** (is the forward map written down,
with the averaging — over the ensemble, over time, over orientation — that the instrument performs?); **measurement
uncertainty** (as a tolerance in the units of the observable, not as a weight); **information loss** (what the
forward map forgets: the dimension of its fibres); **non-identifiability** (the range of the inferred quantity over
everything consistent with the data — an identified set, not a point; mirror images, homometric pairs,
moment-matching ensembles); **model mismatch** (the least model error the data force; whether a wrong model fits);
**alternative explanations** (a negative control: a structurally different ensemble with the same data);
**dependence on priors** (the result with the prior removed or replaced); **observed against inferred** (which
quantities are functions of the data and which of the data and the model).

**Mathematical prerequisites for a credible retrospective validation** — all of them, before any comparison:
(i) a forward model with a stated error; (ii) an identifiability statement for that forward model on the class of
ensembles considered, with the non-identifiable directions listed; (iii) the quantity to be compared fixed in
advance, with the metric and the threshold that would count as failure; (iv) public data on fixed sequences,
with their uncertainties; (v) a null method — the comparison a practitioner would make without the new
software; (vi) the four-line budget of §3 for the computed side.  None of this is an experiment and none of it
has been done on this branch for any physical system.

## 5. Benchmark criticism: the eight questions of the directive, asked of the specification before the run

1. Does it address an important scientific problem — or a problem chosen because the method solves it?
2. Are the comparisons appropriate — same model, same information, same budget?
3. Is the baseline strong — the method a practitioner would use, by its published recipe, tuned by someone who
   wants it to win?
4. Will the results generalise — which regimes (extended and compact; apolar, polar, charged; exposed and
   buried; lengths past enumeration) are in the suite, and which are missing?
5. Does the method improve a scientifically meaningful quantity — line 1 of §3, or something downstream of
   lines 2 and 3?
6. Are the favourable examples representative — how were instances chosen, and before or after seeing results?
7. What structural regimes are missing?
8. What result would refute the interpretation — written before the run?

Principles carried over from `BENCHMARK_DESIGN.md` §0: every benchmark is attached to a hypothesis it could
refute; planted truth for anything that claims certainty; negative controls and deception instances are part of
the suite; development, construction and evaluation instances are separated; "what a success would not
establish" is written next to each benchmark.  We may propose a stronger benchmark or recommend that a
comparison be rejected as misleading; we do not run theirs.

## 6. Prior art and novelty

Six classes, as the directive lists them: *established method* · *new implementation of a known method* · *new
combination of existing techniques* · *mathematical novelty* · *computational novelty* · *scientific novelty*.
For each major capability: a search with its queries and addresses logged, sources with their reading level
(read in full / in the passage / abstract / record / from memory), the list of what was not reached, and the
sentence "a limited search that finds nothing certifies nothing".  A claim to have solved a published open
problem or to have made an important scientific advance gets both a literature workstream and a referee
workstream, and the two do not see each other's reports.  The record on this branch: `PRIOR_ART_MATRIX.md`;
`workstreams/A1`–`A4_REPORT.md`; `SM_REPORT.md`.  Our own first claims were wrong about novelty more than once
(SCI-RES-0009; SCI-MSG-0033): assume the same of any first claim.

## 7. The form of a review

A SCI-REV message with: the claim as understood; a verdict per claim — *supported as a statement about the
model* / *supported with restrictions* / *overstated (replacement text given)* / *false (counterexample or failed
replication)*; the four-line budget; the scientific weight (§3); the kind of checking done, kept apart — review
(re-derived), replication (own code from the statement), re-run (their code), read only; what was not checked;
requests, each a proposal.  Errors and overstatements are recorded in `docs/collaboration/status/science.md`
and, when they concern a published statement of another division, sent to that division.

## 8. Readiness register of this division's own results (what may be translated, and what first)

| result | evidence | internal review | budget lines 2–4 known? | translate? |
|---|---|---|---|---|
| sandwich certificate of `ln Z` and populations for a rotamer model with an evaluated many-body term (addenda A17 (13)–(24)) | [P] + [M]; three statements [V] by the theory division | parts (19)–(22) refereed; (13)–(18), (23)–(25) not | 2: no (toy only); 3: partly (measured spreads); 4: assumed | as a **checker and a model-relative calculator**, yes; as a statement about a peptide, no |
| class constants of real residuals (B1 protocol) | [M], exact on grids | pilot re-run in part by the coordinator; not replicated independently | n/a (they are lower bounds) | the protocol, yes; the constants as bounds, no |
| identified sets and falsification bounds from averaged data | [P] + [N] on lattice chains | referee R3 and literature workstream M | no observation model with error written | after §4 (i)–(ii) for a named observable |
| robust ranges of macrostate ratios (A11, A13, A14) | [P], with A11 and A13 machine-checked in this division's second Lean wave; exact linear programmes as checks; one worked model | no referee workstream (`INDEPENDENT_VALIDATION.md`) | n/a | for unfrustrated known parts and monotone macrostates only |
| divergence criteria for surrogates (A17, B10) | [P] in print; [M] ours | literature workstream A3 | n/a | as a diagnostic, yes |
| certified kinetics on voxel graphs | [V] + [P] | workstream K; Lean re-compiled | the prefactor is outside the programme | not as physical rates |
| cell-wise sandwich for continuous variables (A17.24), with one-residue cell free energies (item 101 (b)) | [P] + [N] on a toy; [M] on valine, serine, leucine blocks of one force field | none | it *is* line 2 | as the definition of line 2 and as a construction to test; needs residues with several torsions as sites, certified oscillations, and cases with walls between residues |

*What would change this register:* an independent implementation of the constants; a proved evaluator
tolerance; A17.24 run on a real torsional energy; one physical system taken through §4.
