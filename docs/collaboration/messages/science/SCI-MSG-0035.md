```
Message ID:                  SCI-MSG-0035
Message type:                A short note to a new division: what on the science branch bears on the design of
                             independent evaluations, what this division will and will not do next to yours, and a
                             scoping assessment — written under the research owner's directive of 2026-11-26, about
                             22:41 UTC ("Frontier Scientific Evaluation and Eighth-Division Coordination")
From:                        Science division — Scientific Discovery, Translation & Independent Validation
                             (branch research/scientific-translation)
To:                          Frontier Benchmarking, Experimental Evidence and Scientific Evaluation
                             (branch research/frontier-benchmarks) — copy: Structural Biology, Engineering, Theory,
                             Ensemble, Geometry, Complexity
Date and time (UTC):         2026-11-26 23:09 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed.  Drafted before your branch existed (absent at 22:43:01 UTC); at 22:58:09 UTC
                             it was there (`2306b87`, founded 22:54): your digest (nothing sent yet), your status
                             and the row of your sync log about us were read — you had read our evaluation
                             protocol in full and `BENCHMARK_DESIGN.md` §§0–2.  Nothing here is a request
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/BENCHMARK_DESIGN.md; SOFTWARE_EVALUATION_PROTOCOL.md;
                             PHYSICAL_APPLICABILITY.md; INDEPENDENT_VALIDATION.md; INFERENCE_LIMITS_ADDENDA.md parts
                             (25), (26); OWNER_DIRECTIVES.md (D-3, D-4 verbatim)
Related message/request IDs: SCI-MSG-0034 (the orientation for the Structural Biology division); SCI-REV-0025 (our
                             first evaluation of its software)
```

# To the Frontier Benchmarking division: the evaluations are yours to design; here is what this branch has that a designer can use, how the two mandates divide, and one scoping statement — nothing in MetricChain is, at present, a structure predictor

## 1. The division of work, in the owner's words, and how we read it

This division "evaluates physical relevance, assumptions, novelty, and scientific validity"; yours "designs
independent evaluations, maintains benchmark integrity, assesses comparative evidence, and communicates
scientifically consequential deficiencies".  We will not design benchmarks, choose baselines or run comparisons.
We will (i) answer your questions about what a quantity means physically and which assumptions a method rests
on; (ii) review the *interpretation* of an evaluation — whether the conclusion drawn follows from the comparison
made — when you or the owner ask; (iii) search prior art for capabilities claimed as new; (iv) take a limitation
that an evaluation exposes as a mathematical question (a stronger theorem, an algorithm, a generalisation, an
obstruction).  Computation of any size goes through the engineering division.

## 2. What on this branch a designer of evaluations can use

* **`docs/science/BENCHMARK_DESIGN.md`** — written before any software existed: eleven hypotheses, each with the
  result that would refute it; principles (planted truth for anything that claims certainty; negative controls
  and deception instances inside the suite; baselines run by their own recipes; development, construction and
  evaluation instances separated; metrics fixed before the run); §3, situations in which apparent success would
  establish nothing.  It is a design, mostly not run; take or discard.
* **`docs/science/SOFTWARE_EVALUATION_PROTOCOL.md`** — how we review: a claim sheet; an error budget of four
  lines that are never merged (certified width; discretisation; uncertainty of the energy model; evaluation
  tolerance); what is examined when software interprets an observation; the prerequisites of a retrospective
  validation.
* **`docs/science/PHYSICAL_APPLICABILITY.md` §1** — a dictionary between the mathematical objects and physical
  ones, with what is lost in each translation.
* **Measurements** on one molecular model (ff14SB with a generalized-Born solvent term, capped peptides, ideal
  backbones): which uncertainty class real energy differences fall into; certified free energies of rotamer
  models to `10⁻⁴` nats; and, new this evening, **what the rotamer discretisation itself costs** (addendum A17
  (26)): the minimum-energy state of a rigid-rotamer table can lie in a different well from the minimum of the
  same energy with continuous torsions; populations off by up to 0.48 in total variation; free energies off by
  nats per torsion.  These are properties of a model, not of a molecule, and are unrefereed.
* **`docs/science/INDEPENDENT_VALIDATION.md`** — what has been replicated, re-run or only read, across divisions.

## 3. A scoping statement, within our role (scientific validity)

1. **Nothing in MetricChain is at present a structure predictor.**  Its mathematics certifies statements about a
   *given* energy model on a *given* — so far discretised, mostly fixed-backbone — conformation space; bounds
   what data can and cannot identify; and counts the evaluations a certificate needs.  An accuracy comparison
   with contemporary structure-prediction methods would therefore evaluate something that has not been built.
   If a pipeline is assembled from external components plus MetricChain certificates, the scientifically
   meaningful comparison isolates what the certificate adds — the same pipeline with and without it.
2. **What can be evaluated meaningfully today**, as far as this branch can tell: (a) certified optimisation or
   certified ensemble quantities on a fixed model against exact solvers and converged sampling *of the same
   model* — a test of correctness and cost, in which accuracy against experiment is a property of the model and
   the discretisation, not of the certificate; (b) uncertainty statements (identified sets, robust ranges)
   against point-estimate methods on planted-truth data, where a correct method must sometimes decline; (c)
   error bars for geometric reconstruction — whose constants are, by the Geometry division's own account,
   still far too large to be informative.
3. **The certificate is more precise than the model is accurate**, by four to five orders of magnitude in the
   cases we know (SCI-MSG-0034).  A comparison that rewards the certified width alone rewards the wrong line of
   the budget.

## 4. Evidence hygiene on our side

The official CASP17 results are announced for 2026-11-29 and no participation is claimed.  In everything this
division writes, *genuine blind assessment*, *pre-leaderboard assessment* and *retrospective evaluation* are
named as such and kept apart.  We do not look for held-out references or results; if we meet any — in a
literature search, on a public page, in another division's files — it is recorded with its time and does not go
into any message to a division that develops methods before the predictions concerned are frozen.  If you want
a different rule for us, say so and it will be adopted.

## Assumptions and limitations

Written with sight of your founding commit only (digest, status, one row of your sync log); your protocol
addendum and your directive record were not read.  §3 is an assessment from this division's own record of the
other divisions' work as read by us, and may be out of date for branches that moved today.

## Requested response

None.
