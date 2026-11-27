# Workstream P — physical applicability: do the envelope classes describe any real residual?

Read `docs/science/workstreams/COMMON.md` first.  Your directory:
`experiments/science/ws_P/`; your report: `docs/science/workstreams/SP_REPORT.md`
(named `SP` because the theory division already has a `P_REPORT.md`).

## The question

Every guarantee of MetricChain is relative to an *input*: a known part `f`, and an envelope
class for the residual `g = E_true − f` (per-site bounded differences `c_i`; torsion-space
Lipschitz constants; mixed second differences `c_ij`; or "linear in pair-distance profiles
with `L`-Lipschitz radial functions").  The theory report says in three places that the
interface is "hypothetical until one instance is certified" (§8, §12 items 4, 7, 9(f)); the
theory division's request THY-REQ-0003 and the engineering division's agenda item E-3 ask
"which class do residuals live in" for synthetic or learned residuals on enumerable domains
(accepted, not started; see `eng_ro/docs/collaboration/responses/engineering/ENG-RES-0003.md`).

Nobody has yet put a **real molecular energy model** next to these classes.  That is your
job: a first *measured* data point, plus a precise physical reading of every assumption.

## Part 1 — measurement on a real force field (the pilot)

Use a public, standard molecular mechanics implementation (suggestion: `pip install openmm`;
OpenMM ships Amber ff14SB and GBn2 implicit solvent; if OpenMM cannot be installed, fall
back to your own implementation of a published small force field, and say so).  Fixed
sequences only — small capped peptides are the natural choice (alanine dipeptide
Ace-Ala-NMe; Ace-(Ala)_n-NMe for n = 2…8 or as far as is cheap; one or two with side-chain
torsions if easy).  Build conformations on a torsion grid (backbone φ, ψ on a coarse grid
or rotamer-like wells), with fixed bond lengths and angles; decide and state how you treat
clashes.

Physically meaningful residuals `g` to examine — each is a real instance of "explicit
pairwise-decomposable part + correction":

* (a) **implicit-solvent polarisation energy** (generalised Born: many-body through the Born
  radii) relative to the vacuum force field — the classic non-pairwise term of provable
  side-chain-placement work;
* (b) **difference between two force fields** (e.g. two Amber generations, or Amber vs
  CHARMM if available) — a proxy for "model error";
* (c) optionally a difference between two solvent models, or a nonbonded cutoff error.

For each residual, on each chain length, measure **exactly on the enumerated grid** (and by
sampling where enumeration is impossible), and report with units (kcal/mol and `k_BT` at
300 K):

1. per-torsion bounded-difference constants `c_i = max |g(x) − g(x')|` over pairs differing in
   torsion `i` only, and their dependence on the position `i` along the chain and on the
   chain length — the theory predicts growth with the distance to the chain end for
   contact-type residuals (lever arm; theory report §11.14, Theorem 11.37, `DEAD_ENDS.md`
   D42).  Does a real residual show it?  How do `βc_i` compare with the scale `u = βc ~ 1`
   where the theory's exponents are computed?
2. the same for mixed second differences `c_ij` (second-order class, §11.7/§11.12): sparse or
   dense in `|i − j|`?
3. the best approximation of `g` in the **pair-distance-profile class** of §11.17 (pair-additive
   with radial functions of bounded slope; several atom/bead types allowed — say which), and
   in simpler linear classes (sum of single-torsion terms; sum of torsion-pair terms): the
   sup-norm and RMS remainder `η`, and the Lipschitz constant `L` of the fitted radial
   functions.  Is `βη` small compared with 1?
4. the **sharpness** of sites for the known part: at how many torsions is the energy gap to
   the second-best well larger than `c_i`?  (By Theorem 11.6/§11.4 the certificate cost is
   exponential in the number of non-sharp sites.)  Plug your measured numbers into the
   theory's formulas (exponent `R*`; accuracy threshold `Σ ln cosh(βc_i/2)`) and say what
   they predict for a 10-residue and a 100-residue chain.

Keep the pilot small and exact rather than large and vague.  Report every modelling choice.
A negative outcome ("no real residual is near any cheap class; the constants are tens of
`k_BT`") is a main result if that is what the numbers say.

## Part 2 — the physical reading of the mathematics (analysis, not computation)

A table, one row per mathematical object of the programme, with columns *object — physical
counterpart — when the identification is valid — what is lost — what would have to be
measured or certified to use it*.  Rows at least for: the finite configuration space
(rotamer / voxel discretisation; what the continuous integral needs: theory report §3.4);
the known part `f` (pairwise decomposability in which variables? torsion-space energies are
*not* pairwise in torsions for backbone flexibility — say exactly where pairwise
decomposability holds: fixed-backbone side-chain placement, coarse-grained contact models,
lattice models); the residual `g` (solvation, polarisation, quantum corrections, learned
corrections); the envelope `d`; anchors (single-point quantum-chemistry or expensive-model
evaluations); `min E` (a global minimum-energy conformation: when is it physically
meaningful at all, given that the model uncertainty is of the order of the gaps?);
`ln Z` (which free energies are observable — differences between macrostates or
thermodynamic states — and which are not: the absolute `ln Z(f+g) − ln Z(f)` is a
model-correction free energy, not an observable); inverse temperature (`βc` in real units);
the "hint"; the product-landscape and cube idealisations (which physical systems are
product-like?); the lattice chain of §11.22.

Then answer in prose, with precise conditions rather than adjectives:

* For which physical question, system size and accuracy could a MetricChain certificate be
  produced *today*, with constants one could actually certify?  (Candidates: fixed-backbone
  side-chain placement with a pairwise force field and no residual — where the comparison is
  with existing provable solvers; small-molecule conformer ranking with a quantum-chemical
  residual; coarse-grained chains.)
* Which results of the theory are *resolution statements about models* rather than
  algorithms — e.g. "with model uncertainty `c_i` per site, a unique global minimum is not a
  meaningful prediction unless every site is sharp" — and do the measured numbers of Part 1
  say that typical sites are sharp or not?
* What is the smallest set of additional *physical* assumptions under which the exponential
  lower bounds stop applying (locality along the chain, finite interaction range, low
  interaction order, smoothness), and does the real residual of Part 1 satisfy them?
