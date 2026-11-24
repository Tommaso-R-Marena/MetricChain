# Workstream D — free-energy estimation in statistical mechanics; general observables
Directory: <session scratch>/ws/D/

## Why
Theorems 11.24–11.26 (soft gaps; randomised lower and upper bounds for `ln Z`; the accuracy
threshold `n ln cosh(βc/2)` on the cube) are minimax statements about estimating a free energy
from pointwise evaluations of an unknown residual.  Computational statistical mechanics has a
large body of practice and theory on exactly this (free-energy perturbation and the
"overlap problem", Bennett acceptance ratio, thermodynamic integration, Jarzynski/annealed
importance sampling, bias of exponential averages, Chatterjee–Diaconis sample sizes) and
theoretical computer science has query lower bounds for normalising constants.

## Questions (choose and extend)
1. Positioning: what is known that overlaps (minimax or information-theoretic lower bounds for
   free-energy differences; sample complexity of FEP/BAR/Jarzynski; Ge–Lee–Lu and successors)?
   Is the threshold phenomenon (bounded cost above the worst-case Jensen gap, exponential cost
   below, for *every* algorithm) known in any form?  Does the soft gap
   `Λ(y) = ln Z(f+g) − ln Z(f + g(y) + d(·,y))` have a physical name (a work, a relative entropy,
   an insertion free energy à la Widom)?
2. Generalise the dip argument and the soft-gap sampling bound to **other observables**:
   Boltzmann averages `⟨O⟩` (linear-fractional in the weights), free-energy *differences*
   between two macrostates or basins (multi-state ranking, theory report §3.6), response
   functions, the Gibbs probability of a state (theory report Theorem 11.12 gives its exact
   range).  For each: the sensitivity radius, lower and upper bounds, thresholds, small-scale
   numerical checks.
3. **Continuous configuration spaces** (a torus of torsion angles with a geodesic-Lipschitz
   residual): the analogues of dips, soft gaps and the threshold; covering numbers become
   metric entropy; what is the scaling in the dimension and in `βL` (`L` the Lipschitz constant)?
4. Can staged protocols (annealing in `β` or in a coupling parameter) beat the lower bound when
   the class has more structure (e.g. bounded second differences, or a residual known to be a
   sum of few-body terms)?  Where exactly does extra structure enter?
Deliver theorems with proofs where possible, numerics on small models, and an honest
known/new table.
