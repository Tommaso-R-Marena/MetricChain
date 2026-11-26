# Assumption audit (AA1, AA2) — every major theorem, six categories, adversarially

*Brief written by the coordinator on 2026-11-26, in response to the research owner's
supplementary directive of the same day (its text: `docs/collaboration/messages/theory/THY-MSG-0016.md`
§1; item 2 is the mandate of this task).  Two readers, one brief; each reader is told
its part in the dispatch message.*

## 1. The task

For **every major theorem** of your part of `docs/THEORY_REPORT.md` — every row of the
tables "Results at a glance" (§0.2) and "The later phases at a glance" (§0.3) that falls
in your sections, and every numbered Theorem; Propositions, Lemmas and Corollaries only
where a later result or a recommendation rests on them — write one entry:

1. **Statement in one or two lines**, with its label in the report ([V] machine-checked,
   [P] paper, [N] numerical, …) and whether it has been refereed (the research log's
   "Resume here" section lists what has).
2. **Setting**: the model it is proved for (space, measure, class of functions or
   residuals, what the algorithm may query, accuracy regime).
3. **Assumptions**, each classified — with its evidence — as
   * **E** mathematically essential (the statement is false or meaningless without it:
     say why);
   * **P** required only by the present proof (say what a different proof would need);
   * **C** introduced for computational or expository convenience;
   * **Q** replaceable by a weaker *quantitative* condition (state the condition and
     what the conclusion becomes);
   * **X** its removal changes the computational complexity (state from what to what,
     and whether that is proved);
   * **F** its removal makes the claimed result false (give the counterexample: one in
     the repository — a harness test, an entry of `docs/DEAD_ENDS.md`, a later theorem —
     or a new one that you construct and check with a short script);
   * **?** not known.
   Evidence is a pointer (section, theorem, harness test id, dead-end number, file) or
   a new argument written out.  "Obviously essential" is not evidence.
4. **Where it generalises**: the later result of the report that relaxes an assumption
   (heterogeneous sites, alphabets, a field, interactions, slices, sup-norm classes, …),
   so that the entries form a hierarchy; and what is *not* covered by any result
   (continuous spaces, non-product measures, long-range or many-body interactions,
   ensembles without a single reference configuration, …) — say "open" or "obstructed
   by …".
5. **Computational reading**: is the guarantee quantitatively useful in the stated
   regime, or vacuous (exponential cost, constants that swamp the bound, a regime that
   no instance of the report reaches)?  Quote the report's own numbers where it has
   them.
6. **Overstatement check**: any sentence of the report (summary tables, section titles,
   remarks, README) that presents the result more generally than it is proved.  Quote
   it with its line number.  This is the adversarial part: assume there is at least one
   per section until you have looked.

At the end of your report: (a) the **hierarchy** for your part as a diagram or a nested
list (tractable model → broader classes → what fails), (b) the ten assumptions whose
classification matters most for anyone who wants to apply the theory outside the
models of the report, (c) every place where you could not classify (the "?"s), ranked
by how much hangs on them, (d) errors found in the report on the way.

## 2. How to work

* Read the statements and their labels in full; read proofs where a classification
  depends on them.  `docs/DEAD_ENDS.md` (65 entries of failed claims and why they failed),
  §8 (limitations) and §12 (open questions) of the report already contain much of the
  evidence — use them, with their numbers.
* Be adversarial and concrete.  For an **F** or **X** classification that the report does
  not already support, construct the example and check it numerically (small exact
  enumeration; a seeded script with stored output).  For a **P**, name the step of the
  proof.
* Do not soften: a theorem for a restricted model is a theorem for a restricted model.
  Do not inflate either: where a result is already general (an abstract statement in
  Lean about arbitrary finite types, say), record that.
* Scope: mathematics of certified computation; synthetic examples only.  No biological
  sequence engineering, no target-specific optimisation.

## 3. Rules

* Create only your report (`docs/audit/AA1_REPORT.md` or `docs/audit/AA2_REPORT.md`) and
  files under `experiments/audit/AA1/` or `experiments/audit/AA2/` (scripts with stored
  outputs; commands in the report).  Do not edit any existing file.  Do not run `lake`
  or `scripts/audit_all.sh`.  No git command that changes state.  Do not start further
  agents.
* One Python process at a time, under about 1 GB; the machine (4 cores) is shared.
  Foreground `sleep` is not available.

## 4. What to report back

At most 40 lines: the number of theorems audited, counts per category, the hierarchy in
five lines, the five most consequential classifications, the overstatements found
(count, and the three worst with line numbers), new counterexamples constructed, the
"?"s that matter most, errors found, files created.
