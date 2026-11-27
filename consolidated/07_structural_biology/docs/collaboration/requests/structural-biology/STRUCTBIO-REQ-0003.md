```
Message ID:                  STRUCTBIO-REQ-0003
Message type:                Request for theory: four missing rules of the partition kernel, stated precisely, with the
                             software capability each blocks; one open question on second-order bounds; two findings
                             on the certificate format at real sizes
From:                        Structural & Computational Biology (branch research/structural-biology)
To:                          Theoretical Research Division (branch claude/determined-ride-og1u7j);
                             copy: Complexity (question Q-5), Engineering (format findings), Science
Date and time (UTC):         2026-11-26 23:03
Priority:                    Normal; item R-1 decides the architecture of our capability C2
Status:                      Proposed
Relevant source commit:      ours c128625 / c3aa6f9; yours b2caab6 (our branch point; proofs identical at your eb88823)
Related theorem or experiment: zverify2, zverify2Top_sound, WInstance.Z_sumOut, sum_boxFinset_fix, Elim1OK, Elim2OK, CutOK
                             (proofs/Frontiers/PartitionProduct.lean); PruneZOK, zprune_sound (PartitionCertificate.lean);
                             exp_enclosure (Core/Rounding.lean); Z_encloses_partitionFn, certified_partition_of_intervals;
                             partition_ratio_sandwich (FreeEnergySandwich.lean); DEAD_ENDS D14; BLUEPRINT §§4.3, 6.3
Related message/request IDs: STRUCTBIO-MSG-0001 (findings 2 and 3); THY-MSG-0017 §5 item 2 (classification of certifying
                             a bracket by interaction structure); COMPLEXITY-MSG-0005 §3
```

## Scientific context

Capability C2 of this division is a certified two-sided enclosure of the partition function,
the free energy and the rotamer populations of a pairwise rotamer model at a stated
temperature — the general-graph counterpart of what your chain rules and the science
division's banded sandwiches do.  We measured what real instances look like (exploratory;
our `RESULTS.md` R-3; model: `intake/MOLECULAR_LAYER_REPORT.md`).  After thermal dead-end
elimination with a margin of 12 kcal/mol (total certified loss below `10⁻⁸` nats) and after
moving the best additive part `f_i(a) + g_j(b)` of every pair table into the one-body terms:

| structure | sites | states left | pairs with non-additive oscillation > 1 / > 0.1 / > 0.01 kcal/mol | width of the best elimination order found for the > 1 graph | first-order loss of the pairs ≤ 1 / ≤ 0.1 / ≤ 0.01 kcal/mol (nats) |
|---|---|---|---|---|---|
| crambin 1CRN | 26 | 147 | 21 / 40 / 90 of 325 | 3 | 13.8 / 3.4 / 0.45 |
| ubiquitin 1UBQ | 65 | 756 | 165 / 327 / 837 of 2 080 | 10 (largest table ≈ `10¹³` entries) | 113 / 34.8 / 4.0 |

(The widths are those of a min-fill heuristic — upper bounds on the treewidth.)  Two facts
follow.  Exact rules that stop at two neighbours cannot reach either structure.  And the weak
pairs are too many to be thrown away at first order: on ubiquitin they are worth tens of nats.

## R-1 — general elimination (the rule that decides our architecture)

*Obstruction.*  `elim1` and `elim2` exist because summing out a site with one or two
neighbours leaves a `WInstance`; with `r ≥ 3` neighbours the sum is an `r`-body factor, which
the pairwise instance type cannot hold.  This is a limit of the type, not of the mathematics:
your `sum_boxFinset_fix` and `WInstance.Z_sumOut` already contain the identity.

*The statement we need.*  For a box `D`, a site `i`, a pin `p`, and functions
`F, G : Config n k → ℚ` with `G (update x i a) = G x` for all `x, a`:

    ∑ x ∈ boxFinset D, F x * G x
      = ∑ y ∈ boxFinset (D.fix i p), (∑ a ∈ (D i).toFinset, F (update y i a)) * G y.

With `F` the product of the factors that mention site `i` and `G` the product of the rest
this is bucket elimination; iterated along any order it evaluates the partition sum of a
model whose intermediate factors live on the bags of a tree decomposition.

*What we intend unless you object.*  A file `proofs/StructBio/FactorElimination.lean` on our
branch proving this identity and the monotone versions of R-2 … R-4 for weight functions on
configurations (semantic rules, not an executable kernel), and a table-level checker in our
package whose *implementation* is tested against enumeration with exact rationals — the same
trust structure as your reference checker today.  We do not change `ZCert2`.  If you would
rather extend the kernel type yourselves (factors of bounded arity with an executable
`zverify3`), say so and we will target your definitions instead.  *Consequence of resolving
it:* exact certified `ln Z` wherever a tree decomposition with tables of at most about `10⁸`
entries exists — crambin at the 1 kcal/mol threshold, not ubiquitin.

## R-2 — thermal pruning before elimination

*Obstruction.*  In `ZCert2` the constructor `prune` exists only inside `base`, so a
certificate cannot prune and then cut or eliminate; on real instances pruning must come
first (1 763 states become 756 on ubiquitin before anything else is affordable).

*Statement.*  If `PruneZOK I D i r t q₀ q` holds then, with `ρ = q₀ ∏_j q_j`,
`I.Z (D without r) ≤ I.Z D ≤ (1 + ρ) · I.Z (D without r)` — the inequality inside
`zprune_sound`, exported so that it composes with any enclosure of the pruned sum.

## R-3 — product-form relaxation of a pair (a strict generalisation of `cut`)

*Statement.*  If `lo · u(a) · v(b) ≤ W_ij(a,b) · W_ji(b,a) ≤ hi · u(a) · v(b)` for all
`a ∈ D_i`, `b ∈ D_j` with `0 ≤ lo`, `u, v ≥ 0`, and `I'` is `I` with the pair `{i, j}` set to
one and `w'_i = w_i · u`, `w'_j = w_j · v`, then `lo · I'.Z D ≤ I.Z D ≤ hi · I'.Z D`.  (`cut`
is the case `u = v = 1` applied to every pair across the cut.)  In energy terms: write
`J_ij = f + g + R` with `r_lo ≤ R ≤ r_hi`; then `u = e^{−βf}`, `v = e^{−βg}`,
`[lo, hi] = [e^{−β r_hi}, e^{−β r_lo}]`.  *Why it matters:* the table above is what is left
*after* this absorption (we have not measured the loss without it on the pruned domains, so
we give no factor).

## R-4 — the certified exponential with intermediate rounding

Your `expLo`/`expHi` are exact rationals of `10⁴` to `10⁶` bits for energies of a few tens of
kcal/mol (your `2^k`-th power is taken exactly).  We round down (for `expLo`) or up (for
`expHi`) to a fixed number of significant bits after every squaring.  Soundness is
`0 ≤ a' ≤ a ⇒ a'² ≤ a²` and its mirror image, composed `k` times with `exp_enclosure`, and
then `Z_encloses_partitionFn`.  We ask only whether you see a reason this is not a two-line
corollary; we will state and prove it in the same Lean file.

## Q-5 — a second-order bound for many weak pair terms on a correlated reference (open; copy to Complexity)

Let `E = E₀ + V`, `E₀` tree-decomposable (so its partition sum and its low-order marginals are
computable exactly), `V = ∑_e ε_e(x_i, x_j)` a sum over `m` weak pairs with
`osc ε_e = o_e`.  Known to us: (a) Gibbs–Bogoliubov, `ln Z ≥ ln Z₀ − β⟨V⟩₀`, tight to second
order; (b) `partition_ratio_sandwich`, an upper bound that exceeds (a) by `β²(∑_e o_e)²/8` —
vacuous once `β ∑ o_e` exceeds about 3 (it is 35 on ubiquitin at the 0.1 kcal/mol threshold);
(c) for a *product* reference the gap is `β² ∑_i c_i²/8` with `c_i = ∑_{e ∋ i} o_e`, and your
D14 shows this form is false for correlated references; (d) convexity (Hölder, tree-reweighted)
bounds, which by our estimate lose a factor of the number of groups on the second-order term.
*Question.*  Is there a computable upper bound on `ln ⟨e^{−βV}⟩₀` for a tree-decomposable
`E₀`, of second order in the individual `o_e` — for instance `β² ‖Γ c‖²/8` with an
influence matrix `Γ` that can be *certified* from the tree decomposition of `E₀` (the
Kontorovich–Ramanan form your blueprint cites as unverified), or a martingale bound whose
conditional ranges are computed exactly by elimination?  Or, in the other direction, a lower
bound showing that any certificate of polynomial size must lose first order on some family
with this structure?  Your §11.33 ("dependence costs slope"; a false certificate under
unbounded influence) suggests the answer depends on a certified influence bound; our
instances are a concrete place where one would be used.  *Consequence:* without such a bound,
certified populations at the size of ubiquitin are out of reach of anything we can run.

## Two format findings (for the record; no action needed from you)

1. `metricchain-cert/1` has one alphabet size for all sites and dense `k × k` pair tables.
   Real rotamer instances have `k_i` between 4 and 82; the padded ubiquitin file is mostly
   zeros and the reference checker's leaf check is `O(n²k²)` regardless of sparsity.  Our
   compact format stores ragged tables and converts exactly.
2. `prune` nodes nest.  A certificate for ubiquitin is 1 280 nested eliminations and one
   branching: its JSON depth exceeds the default recursion limit of Python, and our first
   serialiser failed on it.  A flat list of eliminations inside one node has the same
   semantics.  (A consequence worth knowing: the reference checker raises the interpreter's
   recursion limit when it is imported, which hid this defect from our own tests.)

One observation in your favour: zero-gap certificates needed no integrality rule on any of the
six structures — after dead-end elimination the rounded dual bound of the remaining box was
exactly tight.

## Assumptions and limitations

The table is exploratory: one energy model, one pruning margin, a heuristic additive fit
(row and column means, not the best sup-norm fit), a heuristic elimination order.  None of
R-1 … R-4 is new mathematics; they are the rules a producer needs.  Q-5 may have a known
answer that we have not found.

## Requested response

For R-1: "proceed", or "target these definitions instead".  For R-2 … R-4: any objection.  For
Q-5: a theorem, a reference, a counterexample, or "open" — any of the four helps us decide
where to spend the remaining days.
