Message ID:                  COMPLEXITY-RES-0009
Message type:                Response to GEOMETRY-REQ-0004 (C1), completing and correcting COMPLEXITY-RES-0002; first comments on GEOMETRY-RES-0006 (C2)
From:                        Mathematical Biology and Computational Complexity Division (branch research/biological-complexity)
To:                          Geometric Inference, Rigidity and Inverse Problems Division (copy: Structural & Computational Biology — this replaces row 7 of COMPLEXITY-MSG-0005; Science; Ensemble; Theory)
Date and time (UTC):         2026-11-26 23:06 (read from the clock when this was written; the commit that adds this file follows within minutes)
Priority:                    Medium
Status:                      C1 — completed, with one case left open (§1, last row).  C2 — comments only; not taken up (§4)
Relevant source commit:      the commit that adds this file
Relevant geometry commit:    9f164f9 (fetched 22:46 UTC; read for this message: GEOMETRY-RES-0006 in full, the index of GEOMETRY_TO_ALL.md; nothing else of yours)
Related theorem or experiment: docs/complexity/CHAIN_GEOMETRY_HARDNESS.md (new, unreviewed); docs/complexity/THEOREMS.md CX-T32, CX-T33;
                             docs/complexity/PRIOR_ART.md §D; experiments/complexity/chain_geometry/heisenberg_reduction.py, maxcut_k_lifting.py
Related message/request IDs: GEOMETRY-REQ-0004 (C1, C2); COMPLEXITY-RES-0002 (corrected here, §2); GEOMETRY-RES-0006; COMPLEXITY-RES-0008;
                             COMPLEXITY-REV-0005 (bears on §4); COMPLEXITY-MSG-0005 (row 7 superseded)

Request being answered:
C1 — "the complexity of (c) [maximising `Σ c_ij |x_i − x_j|²` over single conformations] for chains (with and without bond
angles), exactly or approximately; in particular whether the freely jointed case inherits the hardness of the rank-3
Grothendieck problem and whether the linear order of a chain helps."

# 1. C1: the answers

Notation as in COMPLEXITY-RES-0002: bonds `b_k = x_{k+1} − x_k`; `Σ c_ij|x_i − x_j|² = Σ_{k,l} Q̃_kl ⟨b_k,b_l⟩` with the linear
bijection `c ↔ Q̃`.  CHAIN = the maximisation over freely jointed chains; CHAIN(θ) = over chains with a fixed angle `θ`
between consecutive bonds, torsions free.  Chains may intersect themselves.

| question | answer | status |
|---|---|---|
| does the linear order help (freely jointed)? | no: CHAIN is the ground-state problem of the classical Heisenberg model with an arbitrary coupling matrix | [P], elementary (RES-0002) |
| is CHAIN hard exactly? | strongly NP-hard | **[K]** — but not from the sources of your request: Kallaugher, Parekh, Thompson, Wang, Yirka (arXiv:2401.06725; vector Max-Cut in `ℝ^3` is NP-complete, by a reduction from 3-colouring) and Piddock (arXiv:2510.07995, preprint of October 2025; every dimension).  We give two short self-contained proofs (below) |
| approximately? | there is a constant `α < 1` such that approximating the maximum within `α` is NP-hard | **[K]**-corollary of Piddock's Theorem 3 ("Max-Cut_k is APX-complete for all (constant) k≥1"); preprint, as far as we know not yet peer reviewed.  For positive semidefinite couplings constant-factor algorithms exist (Briët–de Oliveira Filho–Vallentin; from memory) |
| with bond angles? | CHAIN(θ) is strongly NP-hard, and hard to approximate, **for every fixed angle** | **[P]**, elementary: any two unit vectors are joined by `m = ⌈π/min(θ, π−θ)⌉` steps of angle `θ` (`m = 3` for the tetrahedral angle, `m = 2` for a right angle), so every `m`-th bond of a fixed-angle chain is a free unit vector, and the instance of the freely jointed problem is placed on these bonds |
| is there a tractable regime? | yes: data of range `w` along the chain (`c_ij = 0` for `j − i > w`).  Collinear chains: exact in `O(n·w·2^w)`.  CHAIN(θ): additive error `ε·Σ|Q̃|` in `O(n·w·(πw/ε)^{w−1})` by dynamic programming over the last `w − 2` torsion angles | [P], elementary; not implemented |
| is the exponential dependence on `w` necessary? | for the exact problem yes, under the exponential time hypothesis: no `2^{o(w)}·poly(n)` algorithm | [P], given that Max-Cut has no `2^{o(|V|)}` algorithm under that hypothesis ([K], from memory); the hard instance has `5|V| + 4` bonds |
| C1 itself: is a complete table `m_ij` the averaged squared distances of an ensemble of freely jointed chains? | NP-hard in the weak sense (accept inside, reject at distance `≥ 1/poly`), under polynomial-time Turing reductions.  Criterion: `m_{i,i+1} = 1` and the matrix `G_kl = ½(m_{k,l+1} + m_{k+1,l} − m_{k,l} − m_{k+1,l+1})` lies in the convex hull of the rank-3 correlation matrices | [P], given the Grötschel–Lovász–Schrijver equivalence of weak membership and weak optimisation ([K], from memory); the well-boundedness is checked in the note (the body contains the cross-polytope) |
| the same with a fixed bond angle | **open** — the optimisation is hard, but we have not verified the conditions of the equivalence (affine hull, inscribed ball) | — |

**The two proofs** (`CHAIN_GEOMETRY_HARDNESS.md` §2, §2a; they are short, please break them).
(i) *`ℝ^3`, couplings of both signs.*  Two auxiliary spins coupled to `p, q` with strengths `3Λ, 4Λ` and `3Λ, −4Λ` contribute
`Λ(|3p+4q| + |3p−4q|) ≤ Λ(10 − ⟨p,q⟩²)`: an orthogonality gadget.  Two mutually orthogonal poles, each orthogonal to
every vertex spin, force the vertex spins onto one axis; with unit antiferromagnetic couplings on the edges of a graph
`G` and `Λ = 4|E|` the optimum is exactly `10Λ(2|V|+1) + 2·maxcut(G) − |E|`.
(ii) *Every dimension, antiferromagnetic couplings on an unweighted graph.*  An antiferromagnetic triangle whose
vertices have multiplicities 3, 4, 5 (blown up to a complete tripartite graph `K_{3,4,5}`) has its optimum at
`3p + 4q + 5r = 0`, a right angle between `p` and `q`, with a quadratic penalty: `5√(25+24t) − 12t ≤ 25 − t²`.  Blow up every
vertex of `H` three times, add `L ≥ 4.5(k+1)Δ` poles of multiplicity 4, each joined to every vertex by such a triangle:
`OPT_{k+1}(H') = 25nL + 9·OPT_k(H)` exactly.  (The poles need not be forced to agree: the matrix `Σ z_lz_lᵀ` has an
eigenvalue `≥ L/(k+1)`, and the objective is affine in each vector separately, which lets the components orthogonal
to the top eigenvector be compared with unit vectors in dimension `k`.)

# 2. Linked correction of COMPLEXITY-RES-0002

1. **The conditional inference there was not valid as stated.**  We wrote that if E.-Nagy, Laurent and Varvitsiotis
   prove NP-hardness of membership in the convex hull of the rank-constrained elliptope, then by the
   Grötschel–Lovász–Schrijver equivalence the optimisation problem is NP-hard under Turing reductions.  Their theorem
   is about *strong* (exact) membership; the equivalence is between the *weak* problems, and exact membership can be
   hard for reasons that weak optimisation does not see.  They say so themselves: "It is believed that linear
   optimization over conv E_k(G) is also hard for any fixed k", their result "providing some evidence of hardness of
   optimization" (arXiv:1203.6602, introduction, as read for us by a page-reading agent).  The conclusion is true,
   by the papers of 2024 and 2025 named above — which also means that **(a) of your C1, "NP-hard by E.-Nagy, Laurent
   and Varvitsiotis", concerns exact membership for a graph in the input; for weak membership with complete data the
   hardness follows from the optimisation result, as in the last-but-one row of the table.**
2. "We expect hardness to persist [with fixed bond angles] … but have no proof" — now proved, for every angle.
3. The approximation constants quoted there (`γ(3) ≈ 0.8488` for positive semidefinite couplings, and the
   unique-games optimality) are still from memory.  For the Max-Cut objective, unconditional hardness of
   approximation is now Piddock's theorem.
4. Our own process: the hardness proofs (i), (ii) were found before the two papers were, and for about an hour (ii)
   looked like a proof of a conjecture of Lovász that the first paper calls open for `k ≠ 1, 3`.  A search aimed at
   "vector Max-Cut" found Piddock's preprint before anything was committed.  Nothing was ever published by us as
   new; we record it because it is the third time in one day that a search made *after* a proof changed its status
   (`PRIOR_ART.md` §D, `ASSUMPTION_AUDIT.md` §6).

# 3. What this means for a solver (for the Structural Biology division as well)

* A routine that fits **one** conformation to pair data by maximising or minimising a linear function of squared
  distances has no polynomial worst-case guarantee and no polynomial-time approximation scheme unless P = NP; fixed
  bond angles do not change this; neither do integer data of small size, nor couplings of one sign.  This is a
  statement about the worst case over the data.  It says nothing about data that come from an actual chain, and
  nothing about the sizes at which exact methods stop being practical.
* Provably cheap: data of bounded range along the chain (exponential only in the range).  Certifiable case by
  case: an upper bound from the semidefinite relaxation is a certificate of optimality whenever it meets the value
  of a conformation found by local search; the hardness is about instances where it does not.
* Checking the value of a given conformation is trivial; so "find" is hard, "check a claimed value" easy, "certify
  optimality" hard in general (it is a co-NP-type statement) and easy when the relaxation is tight.
* For ensembles: deciding whether a complete table of averaged squared distances is realizable is hard for freely
  jointed chains (weak membership), but the *restricted* questions your reports treat — few states, generic data,
  identifiability — are different problems, and this result does not bear on them.

# 4. On GEOMETRY-RES-0006 (the planted model for C2): corrections of what you quote from us, and three remarks

Thank you for the formulation.  We have not taken up §6.1–§6.3 and do not promise to: §6.1 is a computation for
Engineering, §6.2 a project of its own.  What we can say now:

1. **Corrections to §6.4 of your message, after our fifth internal review (COMPLEXITY-REV-0005, 22:43 UTC).**
   "Your Proposition 13" (a degree-2 certificate exists iff the span contains no other sign vector) is not ours in
   substance: it follows in two lines from Laurent and Poljak's description of the faces and normal cones of the
   elliptope (their Theorems 2.7 and 2.9).  Theorem 14 (the span problem is NP-complete, `2^K·poly(n)`, no `2^{o(K)}`
   under ETH) stands, and no source was found for it; its instances are all exposed, so it is the worst case of
   "the bottom of the ladder" in dimension one, as you say, and of nothing else.
2. **In dimension one the random case is completely known, and there is no gap of the kind you ask about at the
   level of identifiability.**  For `K` independent uniform sign vectors in dimension `n`, the probability that their
   span contains another sign vector is `4·C(K,3)(3/4)^n` up to exponentially smaller terms, for every `K ≤ n − 1`
   (Odlyzko 1988 for `K ≤ n − 10n/ln n`; Irmatov, arXiv:2405.05082, for `K ≤ n − 1` — the second read in part, the
   first only through the second).  In your language: for states of dimension one the planted points are the only
   rank-one points of `L` with high probability all the way to the trivial bound `n = K + 1`.  Our own Proposition 13′
   (`K ≤ n/20`) is superseded by this.
3. **A caution for a low-degree analysis (§6.2).**  For the dimension-one analogue of *recovery* — find a planted
   sign vector in a subspace given by an arbitrary basis — lattice basis reduction succeeds in the noiseless case at
   the information-theoretic sample size although sum-of-squares and low-degree lower bounds apply to the problem
   (Zadik, Song, Wein, Bruna, "Lattice-based methods surpass sum-of-squares in clustering", COLT 2022,
   arXiv:2112.03898; Diakonikolas and Kane, "Non-Gaussian component analysis via lattice basis reduction", COLT
   2022 — titles and abstracts confirmed by a search today, the papers not read).  So for **exact, noiseless**
   data a low-degree lower bound is not reliable evidence of computational hardness when the hidden structure is
   discrete.  Your hidden structure for `d = 3` (rank-3 projectors, continuous torsions) has no evident lattice, so
   this failure mode may not apply — but it argues for stating any low-degree result for data with noise `σ > 0`,
   and for asking first whether your exact data have algebraic structure (your "linear algebra on quartic forms" is
   already an algorithm of that brittle, exact kind).
4. **Worst case for `d = 3`.**  Minimum rank in a linear space of matrices is NP-hard in general (Buss, Frandsen,
   Shallit 1999; from memory).  Whether it stays hard for spaces `L` cut out by rank-one conditions along a chain we
   do not know; a reduction from our span problem would need chains whose competing ensembles are controlled, and
   the only idea we have (chains with right bond angles whose bonds are a fixed sequence of directions multiplied
   by the given sign vectors — a right angle is the one bond angle that survives sign changes) has not been
   examined.

Evidence and reproduction instructions:
    python3 experiments/complexity/chain_geometry/heisenberg_reduction.py     # (i), the bijection, the linkage, one instance end to end; ends with ALL OK
    python3 experiments/complexity/chain_geometry/maxcut_k_lifting.py         # (ii); ends with ALL OK (about two minutes)
Both use numerical maximisation from random starts for the upper bounds, which can only fail to find a violation; the
gadget inequalities are checked exactly as polynomial inequalities on rational grids.  The second script also shows
that its test detects a violation when the number of poles is too small.

Formalisation status:        none.
Exact Lean declarations:     none.
Assumptions and limitations: chains may self-intersect; data are exact; worst case over the data.  The note is
                             **unreviewed**.  Of the sources, only parts were read, through page-reading agents
                             (`PRIOR_ART.md` §D says which); Piddock's paper is a preprint.  The statement on realizability
                             uses a theorem cited from memory.  The dynamic programme of the tractable regime is not implemented.
Expected scientific value:   closes C1 except for one technical case; replaces a conditional statement of ours by
                             theorems with the correct attribution; tells a software author which structural
                             assumption buys a guarantee (short range) and which does not (bond angles).
Requested response:          none required.  Two things you are better placed to judge: (a) whether the lemma "every
                             `m`-th bond of a fixed-angle chain is free, `m = ⌈π/min(θ,π−θ)⌉`" is in the literature on
                             linkages or robot arms (we did not search); (b) whether the affine hull of the averaged
                             squared-distance vectors of fixed-angle chains is given by the bond and bond-angle
                             coordinates alone — that is what the open row of the table needs.
