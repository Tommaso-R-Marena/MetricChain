# Dead ends, defects and failed approaches of the Structural & Computational Biology division

A register of what turned out false, weaker than stated, broken, or not worth pursuing — kept
so that nobody repeats it and so that corrected claims stay linked to the originals.  Entries
are never deleted.  Identifiers `SB-D-E-nn` (dead end) and `SB-DEF-nn` (software defect).

## Software defects found and fixed

**SB-DEF-01 — recursion along chains of eliminations (found 2026-11-26 on 5PTI, 1UBQ, 1BPI).**
The serialiser `mincert._node_to_json`, its inverse and the converter to `metricchain-cert/1`
recursed once per prune node; certificates with more than about a thousand consecutive
eliminations raised `RecursionError` after the certificate had been produced and checked.
*Cause:* nested representation of a chain.  *Fix (commit c128625):* chains are followed
iteratively; the file format stores a chain as one flat `prunes` node.  *Lesson:* the defect
was invisible in the test suite because importing the theory division's reference checker
raises the interpreter's recursion limit for the whole process (SB-DEF-04).  No certificate
was wrongly accepted or rejected; the failure was a crash.

**SB-DEF-02 — converter crash below an invalid prune node (found by the differential mutation
test).**  Replaying an invalid prune (dominator not in the domain) without checking it can
empty a domain; `to_metricchain_cert1` then took the minimum of an empty set.  *Fix (commit
720e0ec):* an empty minimum is written as 0; both checkers reject at the invalid node and
never read below it.  No soundness consequence.

**SB-DEF-03 — irreproducible hydrogen placement (found by the engineer of the molecular
layer).**  OpenMM's `Modeller.addHydrogens` starts new hydrogens at random positions and then
minimises them; two builds of 1CRN gave one-body energies differing by up to about 70 kcal/mol
for the same rotamer state.  *Fix (commit c128625):* the random source is seeded and the
Reference platform is forced; preparation is reproducible on one machine (tested).  *What
remains:* hydrogen positions are whatever that seeded minimiser produces — a modelling choice
recorded in the assumption register, not a physical determination.

**SB-DEF-04 — a test that could not fail.**  The first regression test for SB-DEF-01 passed
with the defect present, because another test in the same process had loaded the reference
checker, which sets `sys.setrecursionlimit(20000)`.  *Fix:* the test lowers the limit
explicitly.  *Lesson:* a regression test must be watched failing against the defect it is
for.

## Approaches that do not work as hoped

**SB-D-E-01 — exact elimination with first-order relaxation of weak pairs, for the partition
function of a whole protein (2026-11-26; exploratory measurement, RESULTS R-3).**  Idea: keep
the strongly coupled pairs exact (variable elimination on their graph), replace every weak
pair by its additive part with a rigorous `[r_lo, r_hi]` bound on the rest.  On ubiquitin
under the vacuum model the strong graph alone needs an elimination table of about `10¹³`
entries and the weak pairs carry 35 to 113 nats of first-order uncertainty.  The range form of
the free-energy sandwich (`partition_ratio_sandwich`) does not help: its width is
`β²(Σ oscillations)²/8`, worse than first order once the sum exceeds 8.  *Status:* not a
refutation of certified thermodynamics on proteins — a statement that this route, with what
one 15 GB machine can hold, certifies nothing useful beyond roughly the size of crambin.
*What would change it:* a second-order bound for many weak pair terms on a correlated
reference (STRUCTBIO-REQ-0003, Q-5); much larger tables through the engineering division;
conditioning with pruning; or restricting the claim to a local ensemble with a fixed
environment.

**SB-D-E-02 — the plain pairwise dual bound as a general-purpose bound for certified
minimisation (2026-11-26; RESULTS R-5).**  On synthetic instances with random strong
couplings our producer needs hundreds of branch-and-bound nodes at 25 sites and is 600 to
1 700 times slower than toulbar2.  It is adequate on the six real structures (one to four
nodes) and should not be presented as a competitive exact solver.

**SB-D-E-03 — the public side-chain MRF benchmark as a ready-made instance set for certified
thermodynamics (2026-11-26; `BASELINE_REGISTER.md` §G).**  The Yanover–Weiss side-chain
instances store Boltzmann weights with six decimals floored at `10⁻⁶` and no energies or
temperature, and carry no stated licence: usable (with care about the licence) as rational
weight instances for minimisation, not as energy models for a stated temperature.

## Statements of ours that were too strong, with their corrections

**SB-D-E-04 — "checking costs at most 10 % of production"** (hypothesis H3c in the first
version of the benchmark plan, commit 5c241bd).  The development rows already showed 3 to
13 %.  Corrected to 25 % before any held-out run; the original commit stands.

**SB-D-E-05 — "treewidth at least 10" for ubiquitin's strong graph** (a draft of
STRUCTBIO-MSG-0001, never committed).  The number is the width of a min-fill elimination
order, an *upper* bound on the treewidth; the committed text says so.
