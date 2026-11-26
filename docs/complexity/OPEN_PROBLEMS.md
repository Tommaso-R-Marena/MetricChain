# Open-problem register (complexity division)

Status vocabulary: **OPEN** (no resolution found by the searches listed in `PRIOR_ART.md`) ·
**SOLVED-ELSEWHERE** (a source resolves it; cited) · **CLAIMED-ELSEWHERE** (a resolution is claimed
in a source that is not peer reviewed and that we could not verify) · **OURS-[label]** (our result,
with the epistemic label of `THEOREMS.md`) · **PARTIAL** · **ILL-POSED** (the source's statement
needs a formalisation before it has a truth value; ours is given).

"Verified on" is the date of the last prior-art check.  A status is never upgraded on the basis of
internal review alone.

---

## A. Nearest-neighbour nucleic-acid folding models

Source A-I: G. Ducloz, A. Shalaby, D. Woods, *Algorithmic Hardness of the Partition Function for
Nucleic Acid Strands*, DNA 31 (2025), LIPIcs 347, 1:1–1:23, doi:10.4230/LIPIcs.DNA.31.1 (full
version arXiv:2506.19756).  Read in full (conference PDF) on 2026-11-26.

Source A-II: A. Shalaby, D. Woods, *One partition function call to rule them all: Efficiently
computing the equilibrium energy landscape of multiple nucleic acid strands*, arXiv:2611.27945v2
(23 Nov 2026), **preprint, not peer reviewed**.  Sections 1–3 read on 2026-11-26.

Source A-III: K. Boehmer, S. J. Berkemer, S. Will, Y. Ponty, *RNA Triplet Repeats: Improved
Algorithms for Structure Prediction and Interactions*, WABI 2024, LIPIcs 312, 18:1–18:23
(journal version: Algorithms Mol. Biol. 2025).  Sections 1, 2, 4, 6 read on 2026-11-26.

### Definitions (as in A-I §2, A-II §2; reproduced because every statement below depends on them)

* A *strand* is a word over `{A,C,G,T}`; base pairs are `A–T`, `C–G`.  A *secondary structure* of a
  multiset of `c` strands with `N` bases in total is a set of base pairs in which every base occurs
  at most once.  It is *unpseudoknotted* if for some circular ordering `π` of the strands the
  polymer graph (strands placed 5′→3′ around a circle in the order `π`, base pairs as chords) has no
  crossing chords; it is *connected* if the graph of backbone bonds and base pairs is connected.
* *BPM model:* `ΔG(S) = −|S|`.  *BPS model:* `ΔG(S) = −#{(i,j) ∈ S : (i+1,j−1) ∈ S}`.
* *NN model* (A-I Def. 11, A-II Def. 7): for unpseudoknotted **connected** `S` on `c` strands, with
  strands of equal sequence indistinguishable,
  `ΔG(S) = Σ_{loops l of S} ΔG(l) + (c−1)·ΔG_assoc + k_B T · log R_max(S)`,
  where `R_max(S)` is the maximum degree of rotational symmetry of `S` (A-II Def. 11).
* Problems (A-I Defs 14–18): `MFE` (minimum of `ΔG`), `PF` (`Σ_S e^{−ΔG(S)/k_BT}`), their decision
  versions `dMFE`, `dPF`, and `#SSEL(k)` (number of structures with `ΔG(S) = k`).  The energy model is
  part of the input.  *Magnification* by `α`: replace `ΔG` by `α·ΔG`.  A model is
  *PF-polynomially magnifiable* (A-I Def. 25) if the `j`-magnified PF is polynomial-time computable
  for all `j ∈ poly(n)`.

### A1 — NP-hardness of MFE in the NN model (A-I, "Future work" 1)

> "MFE hardness in two settings is still an open question: Is MFE NP-hard for NN single-strand
> pseudoknotted, or NN O(n)-strands unpseudoknotted? If so, can the reduction map be leveraged to
> show hardness results for PF and #SSEL in the NN model?"

* Known: NP-hard in BPS for one strand with pseudoknots (Lyngsø 2004), NP-hard/APX-hard in BPM for
  unboundedly many strands without pseudoknots (Condon–Hajiaghayi–Thachuk, DNA 27, 2021); #P-hard PF
  in the same two settings (A-I Thms 33, 38); hardness at the *domain* level for 2-domain strands
  (Demaine et al., DNA 30, 2024 — abstract read only).  A-II Table 1 (Nov 2026) still lists the
  unbounded-strand hardness results "in the simpler base pair matching (BPM) model".
* **Status: OPEN, and partly ILL-POSED** — "the NN model" has no pseudoknot energy rule in A-I's
  Definition 11, and the hardness of the multi-strand case depends on whether the loop-energy function
  is part of the input (then BPS is a special case, as A-I's footnote 2 notes) or is a fixed table.
  Verified on 2026-11-26.
* Our position: **OURS-[P], internally reviewed twice (COMPLEXITY-REV-0001; SCI-REV-0019, independent of
  it) — not peer reviewed** for the multi-strand unpseudoknotted half: `THEOREMS.md` CX-T1–CX-T4, CX-T14,
  CX-T15, CX-T20, `STRANDS_NN_HARDNESS.md`.  In the formal model of the question (a loop with a nick is an
  exterior loop of energy 0): strongly NP-hard for *every fixed* loop-energy function with the `GG/CC` stack
  negative and bulge/interior loops less favourable than the stacks they displace (hypothesis (H2′); so also
  when the energy function is part of the input); #SSEL #P-hard; partition function #P-hard with the
  magnification (or the temperature of a temperature-independent model) as input; no `2^{o(c)}` algorithm
  under ETH.  Extensions: a reward for flush coaxial stacks (Theorem 1c), dangles of total strength below
  `|σ|` (Theorem 1d), several complexes (Remark 5).  The gadget is Lyngsø's (2004) with the `C`-runs cut into
  strands — "apparently unpublished", no more is claimed.  **Not covered:** dangles and coaxial stacking
  together or any published table as implemented; the single-strand pseudoknotted half (ill-posed, see
  above); the partition function at a fixed temperature (A3′).

### A2 — Is the NN model PF-polynomially magnifiable? (A-I, "Future work" 2)

> "Is the NN model PF-polynomially magnifiable (see Definition 25)? (The existing algorithm by Dirks
> et al. [8] does not handle rotational symmetry in a magnification adaptable way.) A positive answer,
> and the reduction map would immediately imply a polynomial time algorithm for #SSEL."

* **Status: SOLVED-ELSEWHERE** (preprint).  A-II Theorem 1: "There is an O(N³(c−1)!) time and O(N²)
  space magnifiable partition function algorithm for c = O(1) DNA/RNA strands with N bases, in the
  unpseudoknotted nearest neighbour model."  A-II Theorems 2, 3: MFE and #SSEL within the same bounds.
  Verified on 2026-11-26.  Not pursued (`DEAD_ENDS.md` CX-D1).

### A3 — Reductions without magnification (A-I, "Future work" 3)

> "Figure 2 has arrows of two colours: red that means the reduction uses our magnification trick, and
> grey does not. Can all red arrows be made grey? This involves replacing our magnification trick with
> a completely different strategy."

* The red arrows are `#SSEL ≤_T PF` (Thm 22), `dMFE ≤_T dPF` (Thm 23), `PF ≤_T dPF` (Thm 24); each
  calls the oracle on a *magnified* model (for temperature-independent models: at other temperatures).
* **Status: OPEN, partly ILL-POSED** ("for any energy model" has no content without a class of
  models).  Our formalisation **A3′** (fixed-temperature hardness): *for a fixed model (BPM or BPS)
  and a fixed temperature, i.e. a fixed weight `x = e^{1/k_BT} > 1` per base pair / stack, is the
  function "strand multiset ↦ Σ_S x^{−ΔG(S)}" #P-hard?*  A-I proves #P-hardness only for the problem
  in which the temperature (equivalently the magnification) is part of the input.
  Verified on 2026-11-26.
* Our position: **active (2026-11-26)**.

### A4 — Dropping the logarithmic-precision assumption (A-I, "Future work" 4)

> "In Note 13, we assume in the NN model that loops are specified using at most logarithmic precision.
> […] Mathematically, some loop free energies, namely, hairpin, interior and bulge loops, are a
> logarithmic function of their size and thus may be irrational. Hence we ask: Can this logarithmic
> precision assumption be dropped?"

* **Status: OPEN.**  Verified on 2026-11-26.  Our position: queued (a model-of-computation question;
  candidate approach: Boltzmann factors of logarithmic loop terms are algebraic, `L^{-γ}`).

### A5 — Returning MFE structures (A-I "Future work" 5; A-II "Future work" 1)

> A-I: "We studied the MFE problem, which aims to compute the minimum free energy value. A natural
> variant is to ask for its corresponding secondary structures. How does this version relate to our
> five other problems?"
> A-II: "Our MFE algorithm gives the MFE value but not the MFE secondary structure(s). Can the
> algorithm be modified to return the MFE structure with the same time/space bound? More broadly, in
> the context of reductions from problem A to B, where we have only a dynamic programming algorithm
> for B, can we use the matrices for B to construct the optimal solution of A?"

* **Status: OPEN.**  Verified on 2026-11-26.  Our position: queued.

### A6 — The dependence on the number of strands (A-II, "Future work" 3 and 4)

> "3. Checking all cyclic permutations of c strands yields the (c − 1)! factor in the multi-stranded
> running times in Table 1. Boehmer, Berkemer, Will, and Ponty [3] reduce that to 3^c, but for the
> simple BPM model. Can we make such improvements in the nearest neighbour model?
> 4. Can we increase the number of strands c beyond O(1) and still have a polynomial time partition
> function or MFE algorithm? We know “not by much”, since for c = Θ(N) partition function is #P-hard
> [16] and MFE is NP-complete [5] in the simple BPM model."

* Known (A-III): Theorem 14 "MFE Strand Interaction can be solved in time O(3^m · n³)" for a
  base-pair energy model **without** the rotational-symmetry term ("If we want to give a penalty for
  rotational symmetries […] the DP will not necessarily compute the MFE value"); Remark 15 sketches a
  partition-function variant with per-symmetry partition functions; Theorem 16 is an XP algorithm in
  the number of distinct strands for triplet repeats, with the remark that "the parameter then becomes
  the number of non-identical strands"; Theorem 19: NP-completeness for triplet repeats of one pattern
  in a model with disconnected complexes.
* **Status: OPEN** as posed (preprint of 23 Nov 2026).  Verified on 2026-11-26.
* Our position: **OURS-[P], validated [X], unreviewed (2026-11-26)** — `STRANDS_ALGORITHM.md`, CX-T10–T12:
  the magnified partition function of the full NN model (connectedness, rotational symmetry, all
  orderings) in `O(N^4 · Π_i C(n_i+2,2))` arithmetic operations: `3^c` instead of `(c−1)!` for distinct
  strands (question 3), and polynomial time for unboundedly many strands of a bounded number of species
  (a partial answer to question 4; with CX-T2 the picture is "bounded species: polynomial; unbounded
  species: NP-hard").  MFE and #SSEL follow by A-II's decoding, which we cite and have not re-derived.
  Open: `2^c` by fast subset convolution (remark only); FPT in the number of species.  ETH-tightness: conditional statement CX-T14.

### A7 — Pathways through the landscape (A-II, "Future work" 2)

> "is there a polynomial time algorithm outputting an efficient description of all pathways through
> the energy landscape? Such a description would somehow efficiently encode an exponential size graph,
> where each edge is the formation or breakage of a base pair."

* **Status: OPEN, ILL-POSED** (no definition of "efficient description").  Not pursued.

---

## B. Phylogenetic networks: quartet distances

Source B-I: N. Holtgrefe, E. S. Allman, H. Baños, L. van Iersel, V. Moulton, J. A. Rhodes,
K. Wicke, *Distinguishing Phylogenetic Level-2 Networks with Quartets and Inter-Taxon Quartet
Distances*, Bull. Math. Biol. (2025), doi:10.1007/s11538-025-01549-4; read in full in the version
arXiv:2507.17308v2 (13 Oct 2025) on 2026-11-26.

### Definitions (B-I §§2–4)

* A (binary) *semi-directed network* `N` on `X` is obtained from a binary rooted phylogenetic LSA
  network by undirecting all non-hybrid edges and suppressing the root.  *Blob*: maximal connected
  subgraph without cut edges; *level-k*: at most `k` hybrid nodes in each blob; *bloblet*: a single
  non-leaf blob; *outer-labeled planar*: a planar embedding with the leaves on the unbounded face;
  *galled*: for every hybrid node and its two hybrid edges some cycle contains them and no other hybrid
  edge.  `N_k` = outer-labeled planar, galled, level-`k` semi-directed networks; `B_k` = bloblets of `N_k`.
* `T(N)` = trees displayed by `N` (delete one hybrid edge per hybrid node, clean up); a *displayed
  quartet* of `N` is a quartet tree displayed by a quarnet `N|_{xyzw}`.
* For a quartet tree `T` on `{x,y,z,w}`: `ρ_xy(T) = 0` if `x,y` form a cherry, `1` otherwise.  For a
  quarnet `Q`: `ρ_xy(Q) = (1/|T(Q)|) Σ_{T ∈ T(Q)} ρ_xy(T)` (unweighted average; Eq. (10)).
* *NANUQ metric* (Def. 4.1): `d_N(x,y) = Σ_{z,w ≠ x,y} 2·ρ_xy(N|_{xyzw}) + 2n − 4` for `x ≠ y`, `d_N(x,x) = 0`.
* A metric is *circular decomposable* if it is a non-negative combination of split metrics of a
  circular split system; by Chepoi–Fichet (Prop. 2.8) this holds for the circular order
  `(x_1,…,x_n)` iff all `α_ij = d(x_i,x_j) + d(x_{i+1},x_{j+1}) − d(x_i,x_{j+1}) − d(x_{i+1},x_j) ≥ 0`,
  and then the support is `{S_ij : α_ij > 0}`.
* B-I Theorem 4.7: for `N ∈ B_2` on at least four leaves, `d_N` is circular decomposable and its
  support is `Split(T(N))`.

### B1 — Extension of Theorem 4.7 to all of `N_2`

> (before Thm 4.7) "We conjecture that this theorem can be extended to the class N2 (for some more
> details, see the discussion in Section 6)."
> (§6) "First, we conjecture that one of our main results (Theorem 4.7) can be extended to more general
> classes of networks. Specifically, supported by exploratory simulations, we conjecture that this
> theorem extends to all level-2 outer-labeled planar galled networks (not just bloblets within this
> class), as is the case for level-1 networks [ABR19]."

### B2 — Level-3 bloblets

> (§6) "In addition, we conjecture that the NANUQ metric of outer-labeled planar, galled, level-3,
> bloblet networks is also circular decomposable. Proving this will either require an even more
> extensive case analysis than in Lemma 4.6, or a different technique."

### B3 — Parametric family

> (§6) "A final related open problem is whether some of our results can be extended to a parametric
> family of distances, as introduced in [All+25a]."

* **Status of B1, B2 (and, as far as the public summary says, B3): CLAIMED-ELSEWHERE.**  A community
  record (vibemathed.com, entry "All-level NANUQ circularity and exact displayed-split support",
  submitted 30 Sep 2026, labelled there "Verification: Unreviewed", "Publication: Preprint",
  model "OpenAI Codex") states: "Original NANUQ is circular decomposable at every finite level and
  with any number of blobs in the binary semi-directed LSA, galled, outer-labeled planar class (at
  least four taxa). Its positive split support equals the union of displayed-tree splits. […] A
  six-label reduction, exact finite certificate and composition identity remove the level bound. […]
  Planarity cannot be dropped for exact support. Full all-level Lean verification, network uniqueness,
  statistical inference and unrestricted ARGs are not claimed."  The proof artefacts are in a
  third-party GitHub repository **which this session was not authorised to read** (the request to
  attach it was denied on 2026-11-26); we have read the public summary page only.  No peer-reviewed
  or arXiv source resolving B1–B3 was found.  Verified on 2026-11-26.
* What we have established ourselves so far (2026-11-26):
  - [X] `d_N` depends on `N` only through the circular split system `Split(T(N))`; for *arbitrary*
    circular split systems, and even for unions of binary-tree split systems, the statement fails on
    6 points (`DEAD_ENDS.md` CX-D2).
  - [X] B2 holds for every network in `B_3` with at most 8 leaves, and Theorem 4.7 is reproduced for
    `B_1`, `B_2` up to 7 leaves (`experiments/complexity/nanuq/test_bloblets.py`).
* Our position (2026-11-26, after the internal review COMPLEXITY-REV-0002): **OURS-[P]+[X], finite inputs
  [V], internally reviewed once — not peer reviewed** — `NANUQ_LOCAL_CRITERION.md`, `THEOREMS.md` CX-T5–CX-T9,
  CX-V3:
  - B1 and B2 hold, as special cases of a statement for every level and any number of blobs (CX-T6).
    **In all likelihood a rediscovery**: the third-party summary counts "122 distinct quartet systems", and
    122 = 1 + 3 + 16 + 102 is the number of systems of our class 𝒜 on 3–6 leaves, so the method probably
    coincides.  Ours was derived independently and later; priority, if the third-party proof is correct, is
    theirs; neither is peer reviewed.
  - For which we found no prior art (ours: 2 searches; the referee: 9): **"galled" cannot be dropped** — an
    explicit 7-leaf level-2 outer-labeled planar bloblet that is not galled and whose NANUQ metric is not
    circular decomposable, with exact weights `2 − C(s+t,2)` in a family (CX-T7); the criterion is sharp for
    "Kalmanson with exact support" among classes of split systems (CX-T8); for "Kalmanson" alone the sharp
    class is given by a forbidden six-leaf pattern — three 3-splits without all six 2-splits (CX-T26,
    unreviewed); and **for level 2 the scope of B1 is determined exactly** (CX-T27, unreviewed): an
    outer-labeled planar network of level ≤ 2 satisfies the conclusion iff, for each of its *nested* blobs
    (the only kind that is not galled), `β_1·G + ξ_1·R > Σ_{j<l∈M} β_jβ_l` in the numbers of leaves hanging at
    the positions of the blob; for bloblets `k_1 + k_2 > C(k_B − 1, 2)`.
  - B3 (parametric family): **OURS-[P]+[X], not reviewed** (CX-T13; the referee only spot-checked it): for
    **our** extension of the NANUQ⁺ family beyond level 1, the conclusion of Theorem 4.7 holds on the whole
    class exactly when `ρ_o = ρ_s` and `ρ_c + ρ_s ≤ 2ρ_a < 2ρ_s`; the Modified NANUQ distance `(½,1,½,1)` is
    outside and fails on an explicit level-1 network, although it works when every hybrid node has a leaf
    child.

---

## C. Further candidates (reconnaissance; none active yet)

| id | problem | source | status |
|---|---|---|---|
| C1 | Approximation complexity of the partition functions shown #P-hard in A-I (FPRAS or inapproximability at fixed temperature) | not posed in A-I; natural | to be checked |
| C2 | Parameterised complexity of multi-strand MFE/PF in the number of distinct strand species (A-III Thm 16 is XP; is it W[1]-hard?) | implicit in A-III §4.3 ("the parametrized approach […] is the best we can hope for") | to be checked |
| C3 | Encoding of level-3 semi-directed networks (arXiv:2610.07855) — open questions of that paper | not yet read | to be read |

This table is extended as reconnaissance proceeds; entries are promoted to sections only when the
exact statement and status have been verified.

---

## D. Questions received from other divisions

### D1 — E-C1 (Ensemble division, ENSEMBLE-MSG-0003 §4)

> "Deciding whether `K` given sign vectors are exactly the ground states of some Ising energy with
> independent pair features is a linear programme with exponentially many constraints whose separation
> problem is a ground-state problem.  Is the decision problem co-NP-hard for `K ≥ 4`?  (For `K ≤ 3` the
> answer is always yes.)"

* Reformulation: do `K` given vertices of the cut polytope form a face?
* **Status:** for fixed `K`: **OURS-[P], unreviewed** — linear time, because the answer depends only on the set
  of column types (`ISING_GROUND_SETS.md` Theorem 2, CX-T16); the `K = 4` rule is very probably classical.
  For `K` part of the input: in co-NP (Theorem 1); **hardness OPEN** (we found neither a reduction nor an
  algorithm; structure in CX-T18, CX-T19).  No systematic prior-art search.  Verified on 2026-11-26.

