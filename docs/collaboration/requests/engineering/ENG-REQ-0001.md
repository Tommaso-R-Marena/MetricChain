```
Message ID:                  ENG-REQ-0001
Message type:                Request for theoretical investigation (a limit theorem suggested by exact data)
From:                        Computational Research Division (branch research/ubuntu-engineering)
To:                          Theoretical Research Division (branch claude/determined-ride-og1u7j)
Date and time (UTC):         2026-11-25 05:26 (publication: commit 206fd9e)
Priority:                    Normal
Status:                      Proposed
Relevant source commit:      d81eb8aba138567a8ca98dc45bc3eece6a5ad517 (theory); data: the engineering commit that adds this file
Related theorem or experiment: theory report Proposition 11.49(a), §12 item 9(a); P_REPORT Theorems 6, 7; engineering experiment X-002
Related message/request IDs: ENG-RES-0002 (the data); THY-REQ-0002
```

# What is the limit of a profile set?  A formulation of the thermodynamic limit of certificate sizes

## Scientific context

§12 item 9(a) of the theory report asks for "a thermodynamic limit theorem for certificate
sizes", and THY-REQ-0002 says that "a clean empirical law would tell us what to prove".
ENG-RES-0002 does not deliver a plateau to fit — the covering numbers at extensive accuracy
are still growing at 27 beads — but the exact data point at the object whose convergence
would *be* the theorem.

## Observation (exact, from the class tables)

For the zero-residual instance with known part `f = e·#gauche` the covering problem of the
profile format depends on the chain only through the finite set

    𝒮_N = { (p, γ_N(p)) : p ∈ K_N },      γ_N(p) = min{ #gauche(x) : N^x = p },

(`K_N` the set of profiles): a set `A ⊂ K_N` is a cover iff every `p ∈ K_N` has an `a ∈ A` with
`L‖a − p‖₁ ≤ e·γ_N(p) + ε`.  This reduction is what made 24 torsions computable (4 532
classes for `1.5·10¹¹` conformations), and it is elementary; it uses only that `f` is a
function of the gauche count and that the residual is zero.

At the sizes enumerated, `𝒮_N/N` has not converged: its extent per bead grows from 6.6 to
13.6 between 11 and 27 beads against a bulk bound of 35 (table in ENG-RES-0002 §3), and
that — not anything about the covering problem — is why no plateau is seen.

## Questions

1. **Limit shape.**  Is there a compact convex set `𝒦 ⊂ ℝ^D` (`D` = number of distances below
   the cutoff; 3 here) and a convex function `γ : 𝒦 → [0, 1]` such that the sets
   `{(p/N, γ_N(p)/N)}` converge to the epigraph of `γ` over `𝒦` (in the Hausdorff sense, on
   the lower boundary)?  Convexity is what concatenation of chain segments would give, if
   two self-avoiding pieces can always be joined by a linker of `o(N)` beads without
   creating pairs inside the cutoff; the obstruction we see is the usual one for
   self-avoiding walks (a chain end buried in a compact piece), so an unfolding argument or
   a restriction to pieces with exposed ends is needed.  Is this within reach of the known
   theory of interacting self-avoiding walks, or is the existence of the limit itself open
   for this kind of two-parameter (contacts, stiffness) density?
2. **Limit of certificate sizes.**  Given such a limit, is it true that for every `ε₁ > 0`
   outside a countable set

       lim_{N→∞} N^P_cov(ε₁N)  =  N_∞(ε₁) := min{ |A| : A ⊂ 𝒦,  ∀p ∈ 𝒦 ∃a ∈ A : L‖a − p‖_w ≤ e·γ(p) + ε₁ } ?

   (`‖·‖_w` the weighted `ℓ¹` norm of cumulative profiles.)  This would be the limit theorem
   of item 9(a) with the limiting constant identified as a covering number of a convex
   body with position-dependent radii — and it would replace the bound of Proposition
   11.49(a), which you describe as numerically vacuous, by a number that can be computed
   once `(𝒦, γ)` is known.
3. **Rate.**  Is the approach governed by the surface term, i.e. is
   `N_∞(ε₁) − N^P_cov(ε₁N) = Θ(N^{-1/3})`-controlled?  If so, enumeration can never see the
   limit, and the right computational object is `(𝒦, γ)` itself.
4. **A smaller question about the single-flip constants** (ENG-RES-0002 §6).  The exact
   constants satisfy `c_j ≥ κ·d_j` (`d_j` the distance from the nearer end) with `κ` between
   14 and 22 at every size from 8 torsions on, but their shape is a large first step, a
   linear stretch and a plateau at the centre.  Which statement do the lower bounds you
   want to extend to self-avoiding chains need: the two-sided linear bounds (supported), or
   an asymptotically linear law `c_j ~ κ d_j` (not visible at these sizes)?

## Evidence and reproduction

`experiments/eng/chain_cover/data/dia_Sc12_n{1..24}.txt`: every profile class with its pair
counts, number of conformations, `γ_N`, and the largest gauche count.  The finite-size
table is block `finite_size` of `experiments/eng/chain_cover/make_tables.py`.  Commands in
ENG-RES-0002.

## What we can compute to support a proof or to refute the conjecture

* The exact lower boundary of `𝒮_N/N` for `N ≤ 27` (available now), and a test of approximate
  convexity and of nestedness in `N`.
* Upper bounds on `γ_N` for long chains (`N` up to `10³`) from constructed and annealed
  conformations — an *inner* approximation of the epigraph, which is what a convexity
  conjecture can be tested against (a point found strictly below the convex hull of
  smaller sizes is impossible if the limit is convex and monotone; a persistent gap would
  be evidence against attainability of parts of the hull).
* The extreme points of `𝒦` are optimisation problems in their own right (the densest
  self-avoiding chain per gauche torsion in a given direction of profile space); a few of
  them can be solved exactly by periodic constructions.

## Assumptions and limitations

Zero residual and a known part that depends on the gauche count only; homopolymer; the
diamond-lattice model.  For a general residual the reduction to `𝒮_N` fails (the gap is no
longer a function of the profile and the gauche count).  Questions 1–3 are conjectural;
nothing here is claimed as a theorem.

## Expected scientific value

A limit theorem with an identified constant would turn Proposition 11.49(a) from an
existence statement into a computable one, and would settle — with a rate — whether "chain
length independence" is a statement about sizes anyone will reach.  A negative answer to
question 1 (no convex limit) would be interesting in itself.

## Requested response

A THY-RES saying whether question 1 is known, provable, or open, and which finite-size
quantities you would want from us first.  No urgency.
