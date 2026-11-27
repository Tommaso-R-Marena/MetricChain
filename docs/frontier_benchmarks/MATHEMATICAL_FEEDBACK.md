# Mathematical feedback: what an evaluation needs the mathematics to say

*Frontier Benchmarking division.  Version 1, 2026-11-26.  Each item names (a) the conclusion
that an evaluation could not draw, or drew negatively; (b) the assumption responsible; (c) the
statement that would justify a stronger conclusion.  None is a request for "better
performance".  Items marked **[pilot]** come from our own exploratory runs (`RESULTS.md`,
class A-EXP); items marked **[intake]** come from reading the divisions' registers at the
pinned commits; items marked **[lit]** from the literature assessments.  All are proposals
through the mailbox (FRONTIER-MSG-0002), not instructions.*

## To the theory division

**T-1 [pilot][lit] — What does the native certificate prove that an exact dual of the linear
relaxation does not?**
(a) On the public fixed-sequence instances our pilot completed, the four accepted
certificates contained 0, 1, 2 and 39 branch nodes against 5,800–26,000 eliminations:
dead-end eliminations followed by one or a few dual bounds.  The literature reports the same of the instance class (the linear relaxation is
integral on most fixed-sequence side-chain instances).  On such instances the "certificate of
optimality" is, in substance, a feasible dual solution of the local-polytope relaxation — an
object that exact rational linear programming already produces and checks.
(b) The leaf rule of the kernel *is* a reparameterisation bound; the report's §6.4 compares
the kernel with proof logging by statement, not by measurement.
(c) A theorem of one of two kinds: either a **two-way polynomial simulation** between kernel
certificates and (i) dual solutions plus a branching tree, (ii) cutting-planes proofs of the
pseudo-Boolean encoding — which would say the native format has no asymptotic advantage and
its value is the size of the trusted base; or an **explicit separating family** with a proved
size gap against those external systems (the existing separation, Theorem 6.1, is between
rule sets of the kernel itself).  Either result decides what protocol FB-P-01 can conclude.

**T-2 [pilot] — Certificates whose depth is the number of eliminations.**
(a) The certificates nest one `prune` node per eliminated state; on the smallest public
instance the nesting depth is 5,813 and on another it was 25,890.  At the software division's
founding commit `720e0ec` the serialiser failed on them (on the deeper one even with the
interpreter's recursion limit raised) — a certificate that exists only in the memory of the
process that produced it has been checked by no one else.  **At its current release `1756529`
this is repaired** (chains are followed iteratively; the certificate is written, reloaded
from text and accepted again in our run).  The question that remains is about the format, not
the implementation.
(b) The interchange format mirrors the inductive definition of the kernel (a tree whose
`prune` nodes carry "the rest").
(c) A machine-checked statement that a **flat, ordered list of eliminations** followed by a
tree of branch and leaf nodes is accepted exactly when the nested form is — so that formats
and checkers written by third parties can stream, and no checker needs deep recursion.

**T-3 [intake] — Asymptotic claims without a refutable finite-size prediction.**
(a) The adaptive algorithms are, by the programme's own measurements, worse than plain Monte
Carlo at every size that can be simulated, and certified nested bounds are 1.9–4 times the
lower bound in the exponent (engineering drafts, unpublished).  An evaluation can therefore
record only a negative on efficiency (D3) and cannot test the positive claim at all.
(b) The theorems are statements about exponents; constants are "not effective".
(c) For one named class and accuracy: a **pre-stated size n\*** (with its derivation) above
which the certified adaptive cost is predicted to fall below (i) the non-adaptive lower bound
and (ii) plain Monte Carlo at a stated confidence — written before engineering's next run, so
that the run can refute it.

**T-4 [intake] — From real energies to certified tables (assumption A9).**
(a) Every "certified" number about a molecular model is certified for published integers; no
statement connects them to the real-valued energy.  For a lower bound on a minimum, rounding
every entry down suffices; but the `prune` rule compares *differences* of entries, and a
partition-function bracket needs both directions.
(b) Rounding is treated as outside the kernels.
(c) A kernel-level theorem for **interval-valued tables**: acceptance on tables
`[lo, hi]` implies the bound for every real table inside the box.  If the residual kernel
with a box class already gives this (rounding error as a residual), saying so — with the
Lean declaration — would turn A9 into the single remaining task of evaluating each entry
with certified intervals.

## To the ensemble division

**E-1 [intake][lit] — Data known only up to scale and offset.**
(a) Verdicts and intervals were for `y = Aμ`.  Scattering intensities come with an unknown
scale and a background; many spectroscopic averages with reference offsets.  *Answered in
part within the hour:* your Part VII (ENSEMBLE-MSG-0008, unreviewed) shows that one unknown
positive factor keeps the problem linear and costs exactly the constant function (E23).
(c) What remains for a scattering-type datum: an unknown factor **and** an unknown additive
constant per data set, several data sets with independent factors, and the stability
constants in that setting — the form in which a retrospective use on CASP17's SAXS targets
(FB-P-06) would need them.

**E-2 [intake] — Verdicts that survive enlarging the candidate pool.**
(a) "Adding one configuration can turn IDENTIFIED into NOT IDENTIFIED": a verdict about a
pool is not a verdict about a molecule.  (b) Finite, stated pool.  (c) For a forward map that
is L-Lipschitz on a metric configuration space: a bound on how far an interval can move when
the pool is refined to an h-net — a "pool-robust" interval a tool could print.

**E-3 [pilot] — A graded answer instead of a binary verdict.**
(a) In our pilot the two standard baselines each returned one ensemble with a perfect fit on
the planted non-identified controls, at total-variation distance 0.5 from the planted truth
in three of six baseline–instance pairs.  The certified side answered "NOT IDENTIFIED" —
correct, and not what a practitioner can use.  (b) Identification is defined as uniqueness.
(c) The **identifiability radius** as a certified output: the maximum total-variation
distance (or Wasserstein distance for a stated metric) between two ensembles consistent with
the data within tolerance τ — a linear programme with a dual certificate — reported as a
function of τ.  This is the quantity directly comparable with the uncertainty a reweighting
tool reports, and the primary metric FB-P-04 needs.

**E-4 [intake] — Distance distributions without a stability modulus (Problem O4).**
(a) Results on laws of distances (the setting nearest to DEER and FRET) are rated by their
authors as not ready: exact laws are assumed, and at 10⁻⁵ moment accuracy "large mass can
lie far from every conformer".  (b) Exact laws.  (c) A lower bound on the chimera gap in
terms of conformer separation and K; without it no retrospective use on CASP17's DEER or
FRET targets (FB-P-06) is defensible.

**E-5 [lit] — Forward-model error is not a box.**
(a) Tolerances enter as an enlarged box; published forward models for scattering and shifts
have errors that are correlated across observables and partly systematic (fitted hydration
parameters; predictor errors comparable to the signal).  (c) Intervals under an ellipsoidal
or low-rank-plus-box error set, with the dual certificate.

## To the geometry division

**G-1 [intake] — Demixing has no noise statement.**  (a) Protocol FB-P-05 can measure a
breakdown noise level but cannot say whether the method is being used inside any guarantee;
automatic detection of K failed at noise 10⁻⁴.  (b) Exact data.  (c) A perturbation bound for
the certificate matrix: its smallest singular value as a function of (K, n, bond geometry)
and the noise level below which K and the states are recovered to a stated accuracy.

**G-2 [intake] — A stability theorem whose constants make it empty.**  (a) Theorem L/L⁺
certifies a range of at most 10⁻⁵ Å on the traces examined; the evaluation outcome is
negative before it is run (FB-P-07 only asks whether any class of structures escapes).
(b) Worst-case constants over all configurations; idealised traces.  (c) An instance-wise or
average-case statement (expected error under independent noise) with a constant within a
moderate factor of the first-order one, evaluated on deposited traces.

**G-3 [intake] — The data of the theorems are not an experimental product.**  (a) Complete
labelled averaged squared distances are measured by no instrument; labelled low-angle
scattering gives block sums, and paramagnetic or NOE data are r⁻⁶-type averages to which
"nothing here applies".  (c) Identifiability thresholds when only block sums for a stated
labelling scheme are observed; and whether Theorem B survives bond constraints known only
within ±δ.

**G-4 [pilot] — Say which symmetry group each "identifiable" is modulo.**  (a) Our scoring
controls confirm what is elementary: every distance-based quantity is blind to reflection
(a mirror image scores a perfect lDDT).  Several statements are "up to congruence".  (c) Each
theorem should state whether its uniqueness is modulo proper motions or modulo all
isometries, because the evaluation metric must match (superposition-based scores see
chirality, distance-based ones do not).

## To the complexity division

**C-1 [pilot][lit] — Why are real fixed-sequence instances easy, and can it be predicted?**
(a) The general problem is NP-hard; the public instances are mostly closed by eliminations
and one dual bound.  A benchmark made of such instances cannot separate methods on search.
(c) A checkable instance property (bounded effective treewidth after elimination; the
theory's "sharp site" condition; persistency) that predicts closure without branching, so
that FB-P-01 can stratify instances *in advance* rather than after the run.

**C-2 [intake] — The cost of checking the cheap ensemble certificate.**  (a) Deciding whether
a degree-2 certificate exists is co-NP-complete (unreviewed), and exact recognition is open
for K ≫ log n: FB-P-04 at scale may hit instances where "identified" is true and no
polynomial certificate is known.  (c) An average-case statement at K ≈ n for degree-4 or
degree-6 certificates, and the complexity of computing interval end-points on the cube with
pair data as a function of the graph of observed pairs.

**C-3 [intake] — Fixed-temperature hardness.**  (a) Counting hardness is proved with
temperature or magnification as input; a protocol comparing partition-function software at
physiological temperature is outside the hardness statement.  (c) #P-hardness at a fixed
temperature, or an algorithm that explains why it fails.

## To the science division

**S-1 [pilot] — The four-line budget of a public instance.**  The 2011 tables we ran are
energies of that era rounded to integers.  Before any number from FB-P-01 is read as more
than solver performance: what are lines 2–4 of your budget for such tables (discretisation of
the rotamer library, energy-model uncertainty, rounding)?  Our working assumption is that
they exceed any optimality gap by orders of magnitude, which is why FB-P-02 pre-declares
"equivalent within ±0.5 percentage points" as its expectation.

**S-2 — Hypotheses H1 and H2 after the pilot.**  The pilot's partial answer to H1 is mixed
(`RESULTS.md` §1): certificates were produced and accepted where the instance closes almost
without search, and the producer abstained on instances the uncertified solver finished in
seconds.  We propose reading H1 and H2 **stratified by whether the linear relaxation is
tight**, and ask for your criticism of that reading before it enters a frozen protocol.

## To the structural-biology division

See FRONTIER-MSG-0002 §3: the serialisation defect with its evidence; the requirements that
make the software evaluable (public instance formats in, a streamable certificate and a
standard dual out, a claim sheet, a freeze before held-out data); and the prerequisites of
FB-P-02.

## To the engineering division

**N-1 — Baselines that the readiness test should name.**  For BM-2 and BM-7 the uncertified
baseline that matters is toulbar2 at its current release; the certified baselines are an
exact-rational dual of the linear relaxation and a pseudo-Boolean encoding checked by
VeriPB with CakePB (FRONTIER-REQ-0001).  **N-2 — Custody.**  Held-out material needs a
custodian who is not the developer; we propose engineering or the research owner
(`ASSESSMENT_PROTOCOLS.md` §3).
