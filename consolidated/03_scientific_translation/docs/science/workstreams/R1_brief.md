# Workstream R1 — independent review SCI-REV-0001: theory report §11.25 ("slices")

Read `docs/science/workstreams/COMMON.md` first.  Your directory:
`experiments/science/ws_R1/`; your report: `docs/science/workstreams/R1_REPORT.md`.

## The object under review

Theory report §11.25 (at commit `5ed4072`; `grep -n '^### 11.25' docs/THEORY_REPORT.md`), about
300 lines: Lemma 11.89 (odds-ratio lemma), Theorem 11.90 (binary centres suffice on a type
class; closed forms; domination by the uniform cube), Corollary 11.91 (**no known part that is
a function of the type is harder than the uniform cube; an interaction without a field
changes no exponent**), Theorem 11.92 (reduction of algorithms to type classes), Lemma 11.93
(random splits), Conjecture 11.94, and the remark that the comparison *fails* for alphabets
with three or more letters.  Status claimed by the authors: "the coordinator's paper proofs,
every step checked numerically with code that shares nothing with the proofs; deterministic
core machine-checked (`proofs/Frontiers/SliceRefinement.lean`); **not refereed**; Corollary
11.91 is an inequality between exponents only through Theorems 11.78, 11.79 of §11.23
(unrefereed)".  The authors' own numerical checks are in
`experiments/coordinator_checks/slices/`; harness block XXI in
`experiments/falsify_conjectures.py`.

You are the first independent referee of this section.  You need §11.23 (Theorems 11.76–11.80)
and the definitions of §11.10, §11.16, §11.20 for context; read what you need, not everything.

## What a review here means

1. **Re-derive, do not re-read.**  For each numbered statement: restate it with all
   quantifiers; find the hypotheses actually used; attempt your own proof before reading
   theirs; then compare.  Classify each as *proved* / *proved with gaps (list them)* /
   *not proved* / *false (counterexample)* / *true but vacuous or weaker than advertised*.
2. **Replicate numerically with your own code** (not theirs): Lemma 11.89 on a fine grid and
   with random search including boundary cases (odds ratio → 1, → 0, → ∞; marginals → 0);
   the closed forms of Theorem 11.90 against direct optimisation; the domination inequality
   near its equality case; the claimed failure for three letters (reproduce a concrete
   counterexample and report its numbers).  State precisely what you replicated.
3. **Hunt for the gap between theorem and headline.**  Corollary 11.91 is advertised in the
   README as "no known part that depends on the configuration only through one order
   parameter … makes certification harder than no known part at all".  Exactly which
   exponents, for which algorithm classes, at which accuracies, under which unrefereed
   inputs (Theorems 11.78/11.79)?  Is "harder" a statement about the hinted exponent of
   symmetric instances only?  About all instances?  What about non-symmetric instances with a
   symmetric known part?  Is there any circularity with §11.23?
4. **Formalisation match.**  Read `proofs/Frontiers/SliceRefinement.lean` (and the Lean
   declarations the section cites): do the Lean statements say what the prose says they say?
   Vacuity, hidden hypotheses, quantifier order.  (You need not compile; if the Mathlib cache
   is present you may check a file with `lake env lean`.)
5. **Originality of Lemma 11.89.**  A short independent search (workstream A1 does the deep
   one): is it a known inequality?  Can you give a shorter proof or a generalisation (e.g. to
   `k` letters with the right notion of "odds ratio", where the authors say it fails)?

## Deliverable

`R1_REPORT.md` in the review format: claim examined; verification method; evidence inspected;
established findings; limitations; **critical / major / minor findings** (numbered, each with
location, what is wrong, why it matters, suggested correction); originality assessment;
reproduction status (what you re-computed, with scripts in your directory); recommended
corrective action; unresolved questions.  If you find a real error, also give the strongest
true statement you can prove in its place.
