# Negative and inconclusive results

*Frontier Benchmarking division.  Kept with the same care as `RESULTS.md`, and listed first
wherever both are cited.  Each entry: what was hoped or assumed, what was found, the failure
attribution (mathematical limitation · physical modelling limitation · numerical instability
· insufficient information · computational intractability · invalid scientific assumption ·
implementation defect · benchmark mismatch), and what it does not show.*

## About MetricChain

**N-1  Nothing in MetricChain could be evaluated on CASP17 before the results.**
No method takes a sequence; no branch has a forward model for the data the ensemble targets
are assessed against; the one route that could touch coordinates in time (repacking public
server models) was rejected as uninformative and derivative.  *Attribution:* benchmark
mismatch — CASP assesses predicted coordinates; MetricChain certifies statements about a
given model.  *Does not show:* that the mathematics is useless for structure; only that it
is not a predictor.  (`CASP17_ASSESSMENT.md`; the software division and science concur.)

**N-2  On public fixed-sequence instances the certified route is one to two-and-a-half orders
of magnitude slower than toulbar2 where both finish, and abstains where toulbar2 finishes in
seconds.**  Pilot of FB-P-01, class A-EXP (`RESULTS.md` §1, with the table and the counts).
*Attribution:* an implementation in Python written within hours, against a solver developed
over two decades — an implementation limitation, **not** a mathematical one; the pilot cannot
separate the two, which is why FRONTIER-REQ-0001 asks for a replication with longer budgets
and for the certified incumbents as comparators.  *Does not show:* that checkable optimality
is intrinsically expensive; nor that it is cheap.

**N-3  On the three instances where an independent proof would have told us something,
there was none.**  On three of the ten instances (1,060, 1,364 and 1,972 residues) toulbar2
stopped at the time limit with its best value 3–7 % above its own lower bound — the
situation the software division asked us to look for ("only there does an independent proof
carry information").  The certified route abstained on all three.  *Attribution:*
computational intractability at this budget, for both.  *Does not show:* what either does
with an hour.

**N-4  No instance was found on which the certificate changed an answer.**  Wherever both
methods finished, the values agreed exactly.  That is the expected outcome for a sound
solver and a sound checker, and it means that the pilot contains no evidence that
uncertified exact solving is unreliable on this instance class.  *Attribution:* none — it is
a negative about the *need*, on these instances, for what the certificate provides.

**N-5  The accepted certificates contain little or no search.**  They consist of 5,800 to 26,000
eliminations and 1 to 56 dual bounds; the four accepted certificates have 0, 1, 2 and 39
branch nodes.  On
such instances a kernel certificate is, in substance, an exact dual of the linear relaxation
with an elimination trace — established technology.  *Attribution:* benchmark property (the
literature reports the relaxation tight on most fixed-sequence instances); it becomes a
mathematical question for the theory division (T-1).

**N-6  At its founding commit the software division's certificates could not be written to a
file.**  Nesting depth equal to the number of eliminations (5,813 and 25,890 in our two cases)
broke the serialiser, in one case even with a raised recursion limit.  **Repaired by its
authors before we reported it** (at `1756529` the certificate is written, reloaded from text
and accepted again).  *Attribution:* implementation defect, closed.  Kept here because it was
found on the first instance not built by the software's authors.  Found independently by
the engineering division in its review of the same commit (ENG-RES-0018, finding F1: it
"blocks certificate files of realistic size").

**N-7  The certified answer to "is this ensemble determined?" is correct and, alone, not
usable.**  On planted non-identified controls the certified verdict is NOT IDENTIFIED; a
practitioner needs to know *how far apart* the consistent ensembles are.  In the same pilot
two standard baselines each returned one perfectly fitting ensemble, wrong by a
total-variation distance of 0.5 in three of six cases and exactly right in the other three
— "correct by luck is not distinguishable from correct".  *Attribution:* insufficient
information in the data (by construction); for the certified side a missing output (E-3).
*Does not show:* anything about the established reweighting packages, which were not run.

**N-8  Inherited negatives that our protocols assume** (found by other divisions, not by us):
the best certified number is four to five orders of magnitude more precise than its energy
model is accurate; a rigid-rotamer optimum can lie in a different well from the continuous
optimum of the same energy; the software division's own certified optimum for ubiquitin
differs from the deposited conformation at 37 of 65 sites; adaptive algorithms are worse than
plain Monte Carlo at every simulable size; the local-distance stability theorem certifies at
most 10⁻⁵ Å.  References: `RESEARCH_INTAKE.md` §§3 and 6.

**N-17  The certified route's deficit is its node rate; three times the budget does not remove
the abstentions.**  On the three public instances where it abstained at 300 s although
toulbar2 needs under two seconds, the producer enters 0.7 to 2.6 search nodes per second
against toulbar2's 1,200 to 3,300, spends about nine tenths of its time in message passing
over every edge at every node, and **still abstains at 900 s** after 620 to 2,306 nodes
(`RESULTS.md` §6.3).  How large a tree it would need is not known.  Its root bound is not
the problem — it is tighter than toulbar2's on all ten instances (§6.1).  Stripped of every
search refinement the producer lacks, toulbar2 still closes six of seven instances within
seven seconds (§6.4).

**N-18  The software division's development set contains no search.**  By its own null method
(its commit `627a860`; read at the level of the commit subject) the dual bound alone certifies
all twelve of its development instances; on the ten public instances the root bound closes
one.  Its hypothesis that the certified route stays within 1–100 times toulbar2 held on its
set and fails on the public one (N-1, N-2).

## About our own work

**N-9  Our first intake was stale when it was pushed.**  FRONTIER-MSG-0001 and the first
version of the CASP17 maturity table described a commit that had been overtaken within the
hour (a molecular layer and a toulbar2 comparison had appeared).  Corrected by linked message
(FRONTIER-MSG-0002 §1).  *Attribution:* process defect of ours — read, write, and only then
re-fetch.  The rule now: re-fetch immediately before publishing, and evaluate only pinned
releases named by their authors.

**N-10  Our first pilot ran on the wrong commit and labelled a time-out as an optimum.**  The
first run evaluated the founding commit rather than the release offered for evaluation, and
recorded toulbar2's best value at its time limit as "optimum claimed".  Both were caught
before anything was reported; the run was repeated on the release with the solver's own
dual bound recorded.  The superseded rows are kept
(`experiments/frontier/exploratory_gmec/results/scp10_at_720e0ec_partial.jsonl`).

**N-11  A planted test of ours had the wrong sign.**  The test of the torsion-angle sign
convention failed on first run; the code was right and the test wrong, as agreement with an
independent library on a crystal structure showed.  Recorded because a planted answer is
only as good as the person who plants it.

**N-12  Every distance-based score is blind to a mirror image.**  A reflected structure
scores a perfect lDDT in our tests (and must, by definition).  Elementary, and still a
property an evaluation has to remember: chirality errors are invisible to lDDT-type scores
and visible to superposition-based ones.  It also bears on which symmetry group each
identifiability theorem is stated modulo (G-4).

**N-13  The choice of reference chain moves GDT_TS by up to 1.9 units.**  The three scored
CASP17 references each contain two chains of a monomeric target; scoring against chain A or
chain B changes GDT_TS by 0.2–0.4 units on average.  A comparison with official numbers must
know which was used (FRZ-0003 comparison plan).

**N-14  The blind check of our scoring code has little power.**  The only CASP17 monomer
targets with public references are three near-identical easy targets (median GDT_TS about
99).  The check can confirm values; it cannot test discrimination between good and bad
models, and no harder target was available.

**N-15  A literature row was wrong where we could check it.**  The public "ProteinFolding"
category was described to us as fixed-sequence; eleven of its twenty-one instances have
domains up to 350–503, consistent with design instances, and were excluded.  One checked row
in error is a reason to treat unchecked rows — most rows in the geometry, electrostatics and
cavity assessment are search-snippet level — as leads only.

**N-16  What was not done.**  No established packer, no proof-logging solver, no reweighting
package, no partition-function method was run by us; the baselines of the identification
pilot are our own few-line implementations.  No experimental observable was compared with
anything.  No protocol has been frozen and executed as a held-out evaluation.

**N-19  Our auditability count was overstated.**  We reported "A = 3 of 10": toulbar2
returned, at the time limit, values that were not proved optima "without a flag".  The solver
does report an interrupted search — through a status flag (`limited`) that our pilot did not
read; only the return value of its Python call lacks it.  With the flag read, A = 0.  We
learnt this while writing the ablation (in depth-first mode the reported dual bound stays at
the root value even after a completed search, so the flag is the only correct test).  The
protocol's variable is redefined (`ASSESSMENT_PROTOCOLS.md` §6, item 6, correction).

**N-20  Header times of ours were later than the commits that contain them.**  Found by the
software division's intake: FRONTIER-REQ-0001 carries "00:30" and was committed at 00:26:18;
our status file said "about 00:40" in the same commit.  The times were estimates written
before committing.  The commit times and the time-stamp tokens are the record; from
FRONTIER-MSG-0004 on, header times are read from the clock when the file is written.

**N-21  A cross-reference of ours did not resolve.**  `MATHEMATICAL_FEEDBACK.md` sent the
software division to "FRONTIER-MSG-0002 §3" for a list of requirements that existed nowhere
else; that section is about something different.  Found by the same intake; the list is now
stated in the feedback file.

**N-22  Three of our own conjectures were wrong.**  (a) That the abstentions come from a weak
bound: the certified route's root bound is the tighter one (`RESULTS.md` §6.1).  (b) That they
come from the missing integrality step (integer tables, so a bound above U − 1 suffices):
asked for a gap just under one unit the producer abstained on all three instances tried
(§6.2).  (c) That the largest total-variation distance between two fitting ensembles is "a
linear programme with a dual certificate" (our feedback item E-3): it is the maximum of a
convex function over a polytope, and deciding whether it equals one is NP-complete
(ENSEMBLE-RES-0008, Proposition E31; a paper proof read by its author only, not checked by
us).

**N-23  What the consolidation left undone.**  Ordered or planned under directives FB-D-3 and
FB-D-4 and **not done** when FB-D-5 halted the work: any evaluation on validation data (the
side-chain comparison against an established packer and deposited structures; certified
ensemble intervals on public experimental data against maximum-entropy reweighting — both
repositories were fetched and neither was used); any evaluation on the benchmarks beyond
CASP17; the verification of benchmark facts at their sources; the prior-art investigation;
separate request messages to each division.  Within the diagnosis: the oracle run was not
made; the rows with virtual arc consistency were dropped; nothing was replicated by another
party.  The comparison of FRONTIER-FRZ-0003 with the official CASP17 numbers has not been
made and now needs the owner's authorisation.

## Inconclusive

* ~~Whether the certified route's abstentions in N-2 disappear with a longer budget.~~  Answered for
  three of the six at 900 s: they do not (N-17).  For the three instances nobody closes: unknown.
* How many search nodes the certified route would need on the instances where it abstains.
* Whether a native certificate is cheaper than the certified incumbents (not run by anyone).
* Whether our scoring code reproduces the official CASP17 numbers (to be decided after
  2026-11-29 by a plan fixed in advance).
