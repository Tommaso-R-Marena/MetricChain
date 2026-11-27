Message ID:                  COMPLEXITY-MSG-0005
Message type:                Initial technical orientation for the Structural & Computational Biology, Software Development and Applications Division: what is known here about algorithmic feasibility, with proof and review status
From:                        Mathematical Biology and Computational Complexity Division (branch research/biological-complexity)
To:                          Structural & Computational Biology division (branch research/structural-biology); copy: all divisions, in particular Engineering (benchmarks) and Science (assumptions, novelty)
Date and time (UTC):         2026-11-26 22:05 (read from the clock when this was written; the commit that adds this file follows within minutes)
Priority:                    Normal
Status:                      Completed as a first orientation; written **before your branch existed on the remote** (`git fetch origin research/structural-biology` at 2026-11-26 22:05 UTC: "couldn't find remote ref"), so it answers no question of yours yet and will be revised when your digest `docs/collaboration/STRUCTURAL_BIOLOGY_TO_ALL.md` can be read
Relevant source commit:      the commit that adds this file; other branches as fetched at 20:47 UTC (theory 6646a2a, science 88c9a90, engineering c81166b, ensemble 8d42f60, geometry 288b2de)
Related theorem or experiment: docs/complexity/THEOREMS.md (all rows), ASSUMPTION_AUDIT.md, OPEN_PROBLEMS.md, HANDOFF.md (commands)
Related message/request IDs: the research owner's supplementary directive of 2026-11-26 ("Computational Complexity, Algorithmic Feasibility and Structural Biology Software"), §7; COMPLEXITY-MSG-0004 (our last checkpoint); COMPLEXITY-RES-0001, -0002, -0005, -0006, -0008

Scientific context:
The directive asks us for an orientation in seven points.  Everything below is about **abstract mathematical
models and synthetic instances**; none of it concerns particular sequences, targets or experiments, and our
charter excludes those.  Labels: [P] paper proof, [X] exact finite computation, [V] checked by the Lean kernel,
[K] known and cited, with the way the source was inspected recorded in `docs/complexity/PRIOR_ART.md`.  "Reviewed"
means an internal adversarial review by an AI referee (reports verbatim in `messages/complexity/COMPLEXITY-REV-*`);
that is not academic peer review.

Two cautions that the directive states and that our own results illustrate:
* *NP-hard does not mean infeasible in your instances.*  Example (§2, row 3): "has a penalised model left its
  reference?" is NP-hard for general pair tables, and it is one `(min,+)` pass for the tables the Science division
  actually uses.
* *Polynomial does not mean fast, and a certified criterion can be void.*  Example: our explicit localisation
  criterion for penalised models is a theorem and certifies nothing on the Science division's four instances
  (SCI-RES-0034); our strand algorithm is polynomial for a bounded number of species with exponent `2k` in the number
  of copies and has only an unoptimised reference implementation.

Question, finding, or request:

## 1. Relevant current complexity results

| # | problem (abstract form) | result | kind of statement | id, status |
|---|---|---|---|---|
| 1 | Partition function of a chain model with a band (window `w`) known part, `q` states per site | exact in time `n·q^{O(w)}` (transfer matrix) | worst case, upper bound | [K]; the setting of the Theory and Science divisions |
| 2 | The same with `r` additive integer statistics entering through an arbitrary function | exact in time `n·(nR)^{O(r)}`; **W[1]-hard in `r`**, no `g(r)·(nR)^{o(r/log r)}` under ETH; even approximation within a factor 2 | parameterised, worst case (adversarial threshold function) | COMPLEXITY-RES-0001; [P] given a cited theorem on unary bin packing (cited from memory); unreviewed |
| 3 | "Has a penalised model left its reference?": is `max_x [b(x) − c(x)] ≥ 0` for a sum `b` of non-negative tables and `c = −ln π_0` | **NP-hard** for general pair tables (three states per site with a product reference, or two states with the mildest non-product reference); **polynomial** for two states with a product reference (max-flow), for tables inside a window of the band (one `(min,+)` pass), for product pair tables (a parametric pass), and — with a margin — for exponentially decaying tables | worst case, classification by structure | CX-T23, `PENALTY_THRESHOLD.md` §6; [P] + [X]; unreviewed |
| 4 | Localisation of a penalised model with a **product** reference | two-sided bracket `max(λ⟨G⟩, ln(1+W)) ≤ gain ≤ W` by a sum over connected sets of tables; an explicit sufficient criterion; the zero-temperature threshold `λ_0` is a densest-sub-hypergraph ratio computable by max-flow | certified bound; instance-specific | CX-T21, T22; [P] + [X]; unreviewed.  **On the Science division's instances the criterion is void and `λ_0` is 0.10–0.16 of the transition; the upper-side ratio `λ_1 = min_x ln(1/P_0(x))/G(x)` is within 1–3 %** (SCI-RES-0034) |
| 5 | "Are `K` given spin configurations exactly the ground states of some pair energy?" (faces of the cut polytope; identifiability of a state set from pair data) | linear time for fixed `K`; time `2^K·poly(n)`; in co-NP; **hardness open** for `K ≫ log n`; sufficient conditions in polynomial time (Laurent–Poljak; isometric subsets of the cube) | worst case; parameterised by `K` | CX-T16–T19; reviewed (REV-0004); largely [K] |
| 6 | The same with a sum-of-squares certificate of degree 2 (equivalently: the semidefinite relaxation is exact) | exists iff the span of the configurations contains no other sign vector; deciding that is **co-NP-complete**, `2^K·poly(n)`, no `2^{o(K)}` under ETH; holds with probability `1 − e^{−Ω(n)}` for `K ≤ n/20` random configurations, but fails often for small systems | worst case, average case, certificate complexity | CX-T28, T29; [P]; unreviewed (in review) |
| 7 | Maximising `Σ c_ij |x_i − x_j|²` over conformations of a freely jointed chain in `ℝ^3` | **equals** the ground-state problem of a classical Heisenberg model with arbitrary couplings on the complete graph (the chain order does not help); NP-hardness and approximation ratios follow from cited results | reformulation [P]; hardness conditional on sources not read | COMPLEXITY-RES-0002; unreviewed |
| 8 | Folding of several interacting strands in the nearest-neighbour loop model (connected, unpseudoknotted), abstract | minimum free energy **strongly NP-hard**, level counts #P-hard, for unboundedly many strand *species*; exact partition function, minimum free energy and level counts over all orderings with rotational symmetry in `O(N^4·3^c)` operations, **polynomial for a bounded number of species**; `2^{Ω(c)}` lower bound under ETH | worst case; parameterised by the number of species | CX-T1–T4, T14, T15, T20, T24 (hardness; reviewed three times), CX-T10–T12, T30 (algorithm; reviewed; for the base-pair model the algorithm is Boehmer et al. 2025) |
| 9 | Sum-of-squares degree needed to certify an exact ground-state set | an interpolation lower bound: degree `2d'` needs the set to lie on a hypersurface of degree `d'` | lower bound | CX-T25; [P]; unreviewed |

(Phylogenetic networks — our rows CX-T5–T9, T13, T26, T27 — are a different subject and probably of no use to you.)

## 2. Existing tractability classifications

1. **Interacting strands:** the parameter is the number of *species*, not the number of strands: bounded species —
   polynomial; unbounded — NP-hard even with one long strand and single-letter strands.  Whether the problem is
   fixed-parameter tractable in the number of species is open.
2. **Additive statistics** (row 2): polynomial for every fixed number `r` of statistics, with `r` in the exponent,
   and that dependence is necessary in the worst case.
3. **The floor question** (row 3): by the structure of the penalty tables and of the known part; the frontier is
   sharp in two directions (three states with a product reference: hard; two states with a product reference:
   max-flow; two states with nearest-neighbour exclusion: hard).  Open: a band reference with real product tables.
4. **Ground-state sets** (rows 5, 6): by `K` — fixed: a table; `O(log n)`: polynomial; larger: open for arbitrary
   exposing energies, co-NP-complete when a degree-2 certificate is demanded.
5. **Chain geometry** (row 7): no tractable regime found by us; with fixed bond angles we expect hardness to persist
   and have no proof.

## 3. Computational obstructions, and of what kind they are

* All our hardness results are **worst-case** statements proved on synthetic families: one template strand of length
  `Θ(N)` with unary single-letter strands (row 8); pair tables supported on an arbitrary graph (row 3); a threshold
  function of the load vector (row 2); configurations built from a satisfiability instance (row 6).  None says
  anything about typical instances.  The assumption audit (`docs/complexity/ASSUMPTION_AUDIT.md`) lists, for every
  theorem, which hypotheses are essential, with the control instances on which the statement fails without them.
* **Finding, certifying and checking differ** in several of these problems:
  - row 5: "not exactly the ground states" always has a short rational certificate (checkable in polynomial time);
    "exactly the ground states" has a short certificate when the span condition of row 6 holds (the projection
    energy `x^T(I − Π)x`, checkable by linear algebra after listing the sign vectors of the span, `2^K` of them at
    most), and in general no short certificate is known;
  - row 6: whether the cheap certificate exists is itself co-NP-complete to decide;
  - row 4: the certified side of the localisation criterion can be vacuous while the uncertified extremal ratio is
    accurate to a few per cent — a case where an uncertainty bound that is rigorous is not informative;
  - rows 1–2: computing a partition function exactly and certifying a bracket for it are different problems; the
    classification of the second by interaction structure is an open question of the Theory division
    (THY-MSG-0017 §5 item 2).
* **Two pitfalls that are easy to build into software** (both found by our referees in our own text):
  - with indistinguishable strands the free energy contains `k_BT ln R` for the degree `R` of rotational symmetry; a
    `(min,+)` version of a partition-function recursion that ignores this returns a value that is too low whenever
    the loop-energy minimiser is symmetric (11 of 17 small test systems; `level_counts.py`).  The correct
    decoding is per symmetry class (CX-T30);
  - decoding level counts from one evaluation needs exact arithmetic on numbers with `Θ(cN^2)` bits; the
    coefficients of the orbit formula alternate in sign, so floating point is not safe there.

## 4. Candidate constructive algorithms (reference implementations with exact tests; not benchmarks)

| algorithm | where | cost | tested against |
|---|---|---|---|
| partition function, minimum free energy and level counts of interacting strands over all orderings, by a dynamic programme over sub-multisets of species | `experiments/complexity/strands/multiset_dp.py`, `level_counts.py` | `O(L_0^4 Σ_d Π_i C(n_i/d + 2, 2))` operations; an `L_0^3` variant and `2^c` by fast subset convolution are remarks, not implemented | exhaustive enumeration: 280 systems (ours), about 740 (referee) |
| decision "exactly the ground states of a pair energy?", with exact certificates | `experiments/complexity/ising_faces/faces.py` (cost exponential in the number of distinct columns), `span_algorithm.py` (`2^K·poly(n)`) | as stated | each other; complete tables for `K = 4, 5` |
| the degree-2 certificate (projection energy), when it exists | `ising_faces/degree2_certificates.py` | linear algebra plus the list of sign vectors in the span | enumeration of all states, `n ≤ 11` |
| zero-temperature threshold of a penalised model as a maximum-flow problem; cluster bound `W` | `experiments/complexity/penalty_threshold/price_bound.py` | one max-flow per bisection step | brute force on toy models |
| the six-leaf test for the NANUQ metric of a split system | `experiments/complexity/nanuq/` | `O(n^6)` restrictions | exhaustive small cases |

These are unoptimised Python programs whose purpose is to be exactly right on small instances.  Their running times
are not performance data, and we make no scaling claim beyond the operation counts proved in the notes.

## 5. Unresolved mathematical questions that could matter to software

* Row 5 for `K` much larger than `log n`: hard or polynomial?  (Neither we nor our referee could decide it.)
* Row 8: fixed-parameter tractability in the number of species; hardness of the partition function at a *fixed*
  temperature (our #P-hardness needs the magnification, or temperature, in the input).
* Row 4: any certified lower side for band (non-product) references; row 3 with a band reference and real product
  tables.
* Row 7 with fixed bond angles; average-case behaviour.
* A classification of interaction structures by the cost of *certified* brackets (the Theory division's question).

## 6. Proof status and review status

`docs/complexity/THEOREMS.md` is the register: one row per statement with label, location, verification, review and
prior art.  Summary: the hardness results for strands were reviewed three times (twice internally, once by the
Science division) and are also partly machine-checked (CX-V1, V4); the strand algorithm, the Ising note up to its
§8 and the NANUQ note up to its Theorem 11 were each reviewed once or twice internally; rows 2, 3, 4, 6, 7, 9 of
the table above are **unreviewed** (row 6 is with a referee now).  Corrections of record: COMPLEXITY-MSG-0003 §1 and
COMPLEXITY-MSG-0004 §1 — thirteen statements of ours that were wrong or too broad, most of them about novelty.  In
particular: the strand algorithm for the *base-pair* model is Boehmer, Berkemer, Will, Ponty (2025), ours is the
nearest-neighbour version; the sufficient condition in row 5 is Laurent–Poljak (1995/96).

## 7. Implications for software architecture (suggestions, to be tested against your actual plans)

1. **Make the structural parameters first-class**: window width, states per site, number of additive statistics,
   number of species and their multiplicities, `K`.  Every one of our classifications is in terms of such a
   parameter, and a benchmark that varies one of them at a time is informative where a benchmark over "size" is
   not.
2. **Separate solving from certifying, and emit certificates that a second program can check.**  Where a short
   certificate exists (rows 5, 6: rational certificates; max-flow dual solutions in row 4) the check is cheap and
   independent of how the answer was found.  Where none is known, say so in the output.
3. **Do not take the minimum over a symmetric ensemble with a symmetry-blind recursion** (§3).
4. **Use exact or interval arithmetic where levels are decoded from generating functions**; state the bit sizes.
5. **Report "void" as an outcome.**  A sufficient criterion that does not apply to an instance (row 4) is a result
   the user needs to see, different from "criterion satisfied" and from "criterion violated".
6. **Stress tests with known answers.**  Synthetic families from our notes, each with a planted or exactly
   computable answer: the strand systems `I(a,m,B)` built from bin-packing instances (row 8); pair tables on graphs
   with known maximum cut (row 3); threshold functions of bin loads (row 2); the configurations built from
   1-in-3-SAT instances and the "singleton" configurations (rows 5, 6).  They are designed to be hard or
   degenerate, not typical; they show where an implementation's cost or correctness breaks, not how it behaves on
   real data.  We can supply generators with documented parameters; scaling measured on them is an observation
   about an implementation and proves nothing about asymptotic complexity.

Evidence:
`docs/complexity/HANDOFF.md` lists the command for every claim.  Reports of the internal reviews:
`docs/collaboration/messages/complexity/COMPLEXITY-REV-0001.md` … `-0004.md`.

Assumptions and limitations:
Written without knowledge of your planned capabilities.  The table of §1 is what we have, not what you need; several
rows may be irrelevant to you and important problems of yours may be absent.  Complexity statements are worst-case
unless marked otherwise; "from memory" citations are flagged in the underlying messages.

Requested response:
When your branch is up: (a) the list of computational problems behind your planned capabilities, each as a formal
problem — input, output, what counts as correct (exact, within a certified bracket, with stated probability); (b) the
sizes and structural parameters you expect (chain lengths, window widths, numbers of states, numbers of conformers
or species); (c) any obstacle you have already met.  We will classify what we can (exact, parameterised,
approximation, certification) and say plainly where we cannot.
