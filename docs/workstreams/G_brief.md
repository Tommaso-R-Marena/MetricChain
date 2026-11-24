# Workstream G — what the theory says for articulated chains: envelopes from geometry
Directory: <session scratch>/ws/G/

## Why
The complexity theory of theory report §11 is abstract (a known part `f`, an envelope `d`).  The
program is about fixed-sequence articulated chains whose degrees of freedom are torsion
angles; the first research phase derived envelopes for SE(3)-invariant residuals from geometry
(theory report §4.4: torsion changes → RMSD bounds through reduced moments of inertia;
`proofs/Frontiers/TorsionRMSD.lean`, `InvariantEnvelope.lean`; blueprint §7).  Nobody has yet
asked what §11 *predicts* when the envelope constants come from that geometry.

## Questions (synthetic models only — idealised chains with made-up parameters)
1. For a model chain of `n` torsions, each with `k` rotameric states, and a residual that is
   `L`-Lipschitz in RMSD (or in another invariant distance), compute the bounded-difference
   constants `c_i` that the verified torsion-to-RMSD bounds give (they depend on the position
   along the chain: lever arms), for a few synthetic geometries (extended, helical, compact).
2. With a simple synthetic known part (local torsional terms, optionally nearest-neighbour
   couplings), which sites are *sharp* (`c_i ≤` excitation energies), what are the predicted
   exponents `R*`, the soft gaps and the randomised thresholds as functions of chain length,
   `L`, temperature?  Is certification with a first-order RMSD-Lipschitz envelope hopeless for
   long chains (lever arms grow), and which *other* envelope (local frames, contact-based
   distances, internal-coordinate metrics, second-order structure) would make sites sharp?
3. Is there a better invariant metric for the envelope — one in which realistic synthetic
   residuals (e.g. sums of pair terms of bounded range) have small Lipschitz constants and the
   induced `c_i` do not grow with chain length?  Prove what you can (e.g. `c_i` for
   contact-map or local-frame metrics), and quantify the gain in the exponents.
4. Anything about the geometry–complexity interface we have not anticipated.
Deliver formulas, small numerical studies with the code, and a clear statement of which
regimes are certifiable according to the theory and which are not.
