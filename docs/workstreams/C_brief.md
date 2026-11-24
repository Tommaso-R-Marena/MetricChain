# Workstream C — other representations: reduced costs, A*, weak KAM, tropical geometry
Directory: <session scratch>/ws/C/

## Why
The certification geometry was derived from scratch and then found to overlap with several
literatures (difference constraints, L-convexity, optimal recovery).  We suspect at least three
further identifications that could import *theorems* rather than vocabulary:
1. **Reduced costs / Johnson reweighting / A\*.**  The slack `s(a,y) = d(a,y) − g(a) + g(y)` is the
   reduced cost of `d` under the potential `−g`; best-first search with the lower envelope is
   A*-like with a consistent heuristic that improves as evaluations arrive.  Dechter–Pearl (1985)
   proved optimality of A* (every admissible algorithm must expand the nodes with `f < C*`).
   Is there an exact correspondence?  Does the A*/"surely expanded nodes" theory give
   instance-optimality statements for our problem that are stronger than the
   resource-augmentation bound of Theorem 11.11 (theory report §11.5), or explain the "hub"
   counterexample?  Bidirectional/landmark heuristics (ALT) look like the McShane envelopes.
2. **Discrete weak KAM / Aubry–Mather theory; tropical spectral theory.**  Admissible residuals
   are "dominated functions"/sub-solutions for the cost `d`; the contact set of the theory
   report §2.3 and the zero-slack relation look like the Aubry set / static classes; McShane
   envelopes are Lax–Oleinik-type extensions; the admissible class is a polytrope (tropical
   polytope whose generators are the columns of the Kleene star).  What do Peierls barriers,
   static classes, uniqueness sets, tropical rank/generators say about *minimal exact
   certificates* (`ε = 0`), about which evaluations are forced, about asymmetric envelopes?
3. **Optimal transport / LP complementary slackness; metric geometry** (tight spans, injective
   hulls: the set of admissible functions and Isbell's tight span; Funk/Hilbert metrics on the
   polytrope; the slack as a Funk-type distance?).
You are free to pursue whichever of these (or another representation you find) is most
productive.  The deliverable is a *dictionary with consequences*: for each identification, what
is literally the same object, which known theorems transfer and what they say in our language,
and — most valuable — any statement that is new for the certification problem (with proof and
a numerical test), or a cleaner proof of an existing one.  Also say plainly which
identifications are only analogies.
