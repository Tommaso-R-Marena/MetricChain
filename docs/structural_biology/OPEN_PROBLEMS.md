# Open problems of the Structural & Computational Biology division

Prioritised; each with the capability it blocks and who could resolve it.  `SB-OP-nn`.

## Mathematical

**SB-OP-01 (highest; blocks C2 at protein size).**  A computable upper bound on
`ln ⟨e^{−βV}⟩₀` for a tree-decomposable reference energy `E₀` and `V` a sum of many weak pair
terms, of second order in the individual oscillations — or a lower bound showing that
polynomial-size certificates must lose first order on such families.  Stated precisely in
STRUCTBIO-REQ-0003 (Q-5) to the theory and complexity divisions.  Known not to work: the range
form of the Hoeffding sandwich; the `Σ c_i²` form without a product reference (theory D14).

**SB-OP-02 (blocks the Lean status of C2).**  Machine-check the four producer rules of
STRUCTBIO-REQ-0003: general elimination on weight functions, pruning before elimination,
product-form relaxation of a pair, the certified exponential with intermediate rounding.
Ours to do (`proofs/StructBio/`), unless the theory division prefers to extend its kernel type.

**SB-OP-03.**  From real numbers to tables: a rigorous enclosure of the floating-point
evaluation error of one table entry of the molecular layer (interval or running-error
analysis of Lennard-Jones, Coulomb and torsion terms as evaluated).  Until then the model is
the rounded tables and the float agreement is evidence [N].  The engineering division names
the same gap (its BM-7, item (ii)); the science division's assumption A9.

**SB-OP-04.**  Discretisation: a certified bound on what the continuous torsional integral
adds to a rotamer-model statement.  The science division's first measurement (toy chain: 1.3
nats per angle at three cells per angle; SCI-MSG-0034 §2.1) says this term dominates every
certified width.  Needs interval evaluation of force-field terms over voxels (theory
blueprint §3.3–§6.3: not built by anyone).

## Software and verification

**SB-OP-05.**  An independent re-implementation of the checker and of the table construction
(requested: STRUCTBIO-REQ-0001).  Until it exists every certified number has one author.

**SB-OP-06.**  Native certificates against pseudo-Boolean proof logging on the same instances
(VeriPB/CakePB, exact SCIP with VIPR): bytes, production time, check time.  Decides whether C1
is more than a re-implementation of established technology.  Not installed here.

**SB-OP-07.**  The `sum` rule of the theory division's kernel is not implemented; no instance
so far needed it (all models are connected and nearly solved by elimination).  Needed for
instances with several independent frustrated components.

**SB-OP-08.**  A stronger producer for frustrated instances (bounds beyond the local polytope;
better branching), or a way to turn an exact solver's search into our certificate.  RESULTS R-5.

**SB-OP-09.**  Cross-machine reproducibility of the instances (hydrogen placement runs a
floating-point minimiser).  If it fails, ship instance archives with the certificates.

## Scientific

**SB-OP-10.**  Does a certified model-relative number change any scientific decision?  (The
science division's open question 8.)  On the development set it changed none.  Candidates
where it could: instances on which exact solvers disagree or time out; statements no
uncertified solver gives (certified per-residue gaps — C1b; certified population intervals —
C2).

**SB-OP-11.**  A defensible, pairwise-decomposable energy model with screened electrostatics
or a pairwise solvation term (the vacuum model places ubiquitin's side chains 139 kcal/mol
below the deposited state).  Any change of model is a new named model, chosen before results.

**SB-OP-12.**  A forward model with stated error for one public experimental observable of
side-chain ensembles (χ1 populations from scalar couplings; alternate conformations in
high-resolution crystal structures), before any level-5 comparison is designed.

**SB-OP-13 (added 2026-11-27).**  Polar hydrogens as part of the state.  In models v1 and v2
hydroxyl and thiol hydrogens ride rigidly on the last χ (v2: anti to the atom towards the
backbone), so a serine, threonine or tyrosine cannot turn its hydrogen towards a partner
(science division, F3; size of the bias unmeasured).  A model v3 with the hydroxyl torsion as
an extra state coordinate (three values for sp3 oxygens, two for tyrosine) is a small change
of `molecular/` and multiplies the states of those residues by three or two.  It is a new
named model and its hypotheses would have to be written before its results.

**SB-OP-14 (added 2026-11-27).**  What the worst-case criterion leaves open.  (a) Exact
per-site robustness: decide whether *every minimiser of every table within `b`* has site `i`
in a given well — our certificate is a sufficient condition (comparison against `x*` alone).
(b) An error model with structure — per energy term, with a cutoff, or correlated across the
entries that share atoms — under which a realistic model error leaves a non-trivial certified
set of wells.  (c) The literature of optimisation with interval data has not been searched by
us; the criterion is classical and nothing is claimed.

**SB-OP-15 (added 2026-11-27).**  The published instance across machines.  The integer tables
are built from floating-point arithmetic (numpy trigonometric functions, OpenMM parameters)
and rounded to `2⁻²⁰` kcal/mol; an entry within one ulp of a rounding boundary can round
differently on another platform, and with `10⁶` entries that is not negligible.  The
checksum comparison of `run.py --check` detects it; it has only been run on one machine.
Until it has been run elsewhere, a held-out run must ship the integer instance itself
(`modelio.save_model`) next to its certificate, so that the statement certified is about a
file and not about a rebuild.

**SB-OP-16 (added 2026-11-27).**  The float tier of the Z checker: assumptions F1–F3 (IEEE-754
round-to-nearest products and sums in numpy, the a-priori factor for sums, the clamps) are
stated and tested against the exact tier, not proved for this platform; and the correspondence
between the Python steps and the Lean statements of `proofs/StructBio/FactorElimination.lean`
is by reading.  An independent checker (STRUCTBIO-REQ-0004) is the remedy for the second.
