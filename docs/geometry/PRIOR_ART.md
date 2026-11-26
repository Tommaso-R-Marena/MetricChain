# Prior-art register — Geometric Inference division

How to read this file.  For every result of `ENSEMBLE_RIGIDITY.md` it says what is known, what
is a reinterpretation of something known, and what we did not find.  "Not found" means: not
found by the searches listed in §3, on 2026-11-26, at the level of titles, abstracts and
search-engine summaries.  **No full text was read for this register** unless the entry says
so; statements of other authors' theorems are from memory of the literature and from those
summaries, and are marked accordingly.  An absence in searches is not a proof of novelty.
A second division is asked to repeat the search independently (GEOMETRY-REQ-0003).

## 1. Classification of our statements

| our statement | status | closest prior art |
|---|---|---|
| Lemma 2.1 (stacking: an averaged squared distance is a squared distance in a direct sum) | **known** | Schoenberg 1935 (sums of Euclidean distance matrices are Euclidean distance matrices; direct sums of embeddings); folklore |
| Proposition 3.1 (collinear decomposition; `O(dK)` indeterminacy) | **known / elementary** | factor-rotation indeterminacy of second-moment statistics; for mean squared distances without statewise constraints, the non-uniqueness of the distribution is stated e.g. in Shi–Thirumalai 2023 (maximum-entropy ensembles from mean pairwise distances) [summary level] |
| Example 3.3 ("virtual structures" under averaging) | **known** as a phenomenon | ensemble- and time-averaged restraints in NMR refinement (Jardetzky 1980; Torda–Scheek–van Gunsteren 1989) [from memory]; the exact cis/trans identity is elementary |
| Theorem A (ii)⇔(iii): no conic at infinity ⇔ no affine flex | **known** | Connelly 1982, 2005 (affine motions and conics at infinity); Alfakih (dimensional rigidity); Gortler–Thurston 2014 [definitions confirmed at summary level] |
| Theorem A (i): reading as "no ensemble has the same averaged squared distances" | **reinterpretation**, not found stated | the proof is the standard face argument for Gram matrices |
| Theorem B, B′ (mixtures identifiable among all ensembles iff only trivial quadrics / unique barycentric representation on rank-`d` quadrics) | **not found** | relatives: Saunderson–Chandrasekaran–Parrilo–Willsky 2012 (faces of the elliptope ↔ ellipsoid fitting); Tropp 2018 (simplicial faces of the elliptope spanned by rank-one matrices) |
| Corollary 4.2 (simplicial faces of the hull of the chain variety) | **not found**; relative: Tropp 2018 | cut polytope is 3-neighbourly (Deza–Laurent) [from memory] |
| Theorem C (thresholds `(9K²+K+2)/2`, `⌈(9K²+K+8)/4⌉`) | **not found** | — |
| Algorithm DEMIX | **not found**; ingredients classical | classical scaling (Torgerson); joint block diagonalisation |
| Theorem D(a) freely jointed: `𝒦 = 𝒮` for at most 9 bonds | **known** | extreme correlation matrices have rank `r` with `r(r+1)/2 ≤ n` (Grone–Pierce–Watkins 1990; Li–Tam 1994); Barvinok 1995, Pataki 1998 for general spectrahedra [from memory] |
| Theorem D(a) with bond angles (`n ≤ 6`), D(b) (strict from `n = 7`, exact witness) | **application of the known bound + new witness**; the reading "semidefinite feasibility = ensemble realizability" not found | extreme Gram dimension: E.-Nagy, Laurent, Varvitsiotis 2014 [definition confirmed at summary level: the smallest `r` with `ℰ(G) = π_E(conv ℰ_{n,r})`] |
| Membership in the realizable set is NP-hard for general pair sets (star constraints) | **known** | E.-Nagy, Laurent, Varvitsiotis 2012/2013: membership in the convex hull of the rank-constrained elliptope is NP-hard for every fixed `k ≥ 2` [confirmed at summary level] |
| Theorem E (second-moment rigidity; between global and universal rigidity once the conic condition is added to both) | **not found** as a notion; the Ensemble division's "ensemble rigidity" (laws of edge lengths = global rigidity, its E7) is a different notion | universal rigidity: Connelly; Gortler–Thurston 2014; Connelly–Gortler 2015; global rigidity: Gortler–Healy–Thurston 2010 |
| Theorem F for `K = 1` | **known** | Connelly's sufficient condition (positive semidefinite stress of maximal rank + no conic at infinity) [confirmed at summary level] |
| Theorem F for `K ≥ 2`, Theorem G (global `W₂` bound with explicit certificate) | **not found** | Hölder-½ error bounds for semidefinite feasibility at singularity degree one (Sturm 2000; Drusvyatskiy–Pataki–Wolkowicz 2015) are the single-configuration analogue [from memory] |
| Theorem H (local identifiability from separation `K + 3`; complete data from `n = 2K + 3`) | **not found** | — |
| Theorem F′ (separation `3K + 1`) | **application** of trilateration | Zhu–So–Ye 2010 (universal rigidity of `(d+1)`-lateration graphs) [from memory] |
| Theorem I (two states identifiable among all ensembles from 10 atoms; three thresholds) | **not found** | determinantal varieties and structural low-rank points: classical tools |
| Theorem J (laws of separations 3 and 4) | **application** of the Ensemble division's E5/E6 (its report, 2026-11-26) | its remark on prior art: Garamvölgyi–Gortler–Jordán 2022 (Lemma 3.1), unlabeled PCA |
| Corollary 9.1 (second moment suffices under bond constraints) | **instance of a known principle** with a specific prior | Bandeira–Blum-Smith–Kileel–Perry–Weed–Wein (moments and sample complexity for orbit recovery); Bendory–Edidin and co-authors: sparse priors, generic semi-algebraic priors, non-uniform rotations make the second moment sufficient [confirmed at summary level] |
| Hinge ensembles (`HINGE_ENSEMBLES.md`): reduction to a moment problem on `O(2)^s` with interval moments; two states at two or more hinges identifiable, the cube of eight candidates (Theorem M) | **not found** (three summary-level searches); ingredients classical | composition of rotations by reflections; reflection branching in discretizable distance geometry; truncated (matricial) trigonometric moment problems and flat extensions (Curto–Fialkow); ghost orientations of domains from residual dipolar couplings (a different observable) |

## 2. Related work that is *not* the same problem

* **Diploid genome reconstruction** (Belyaeva, Kubjas, Sun, Uhler, SIAM J. Math. Data Sci.
  2022; Cifuentes, Draisma, Henriksson, Korchmaros, Kubjas, Bull. Math. Biol. 2024).  Two
  homologous chains in one frame; the data are sums over the four homolog pairs of a power
  of the distance, i.e. they contain inter-chain terms.  Results: non-identifiability from
  the ambiguous sums alone, in particular *no* finite identifiability for exponent `2` in
  the fully ambiguous setting (2022 — so cited on p. 3 of the 2024 paper, which the internal
  referee read; an earlier version of this register attributed it to 2024); identifiability
  with distances between neighbouring loci and higher-order contacts (2022); finite
  identifiability for exponent `−2` from at least 12 loci (2024) [the first two from the
  referee's reading of the 2024 paper; the rest summary level].  Our model is a mixture: each state is observed in its own frame,
  only intra-state squared distances are averaged, and with statewise bond data the exponent
  `2` case *is* identifiable for long enough chains.  The shared idea — distances between
  neighbours restore identifiability — should be credited to that line of work.
* **Deconvolution of population-averaged contact maps** (Sefer, Duggal, Kingsford 2016, and
  population-based 3D genome methods): optimisation formulations and NP-hardness under
  restrictions on the weights [summary level]; no identifiability theorem of our kind found.
* **Ellipsoid fitting** (Saunderson et al. 2012 and the later work on random points): existence
  of an origin-symmetric ellipsoid through given points; ours is uniqueness of the
  representations of the unit sphere by rank-`d` cylinders through structured points
  (Remark 2.3).
* **Simplicial faces of the elliptope** (Tropp 2018): faces spanned by rank-one sign
  matrices; ours are faces of the hull of rank-3 chain Gram matrices.

## 3. Search log (2026-11-26; web search, summaries only; searches 9–11 for `HINGE_ENSEMBLES.md`)

1. "identifiability conformational ensemble from ensemble-averaged squared distances mixture
   Euclidean distance matrices bond length constraints" — nothing on the question; pointers to
   ensemble-averaged NMR data and to Belyaeva et al.
2. "extreme Gram dimension elliptope convex hull rank-constrained conv Laurent Varvitsiotis
   Eisenberg-Nagy" — arXiv 1203.6602 (NP-hardness, including the convex hull), arXiv 1205.2040
   (extreme Gram dimension), CWI report on bounded-rank completions of extreme partial
   correlation matrices.
3. "Belyaeva Kubjas Sun Uhler identifying 3D genome organization diploid Euclidean distance
   geometry identifiability neighboring loci distances" — arXiv 2101.05336; arXiv 2301.11764.
4. "mean squared distance matrix ensemble of polymer conformations deconvolution
   subpopulations uniqueness Euclidean distance matrix higher dimension direct sum mixture" —
   Shi–Thirumalai (Nat. Commun. 2023, DIMES); Sefer–Duggal–Kingsford.
5. "heterogeneous multi-reference alignment second moment sufficient prior semialgebraic set
   transversality Bendory Dym Edidin Suresh cryo-EM" — arXiv 2311.08833 (semi-algebraic
   priors), dihedral multi-reference alignment, arXiv 2602.20590 (non-uniform second moment
   over SO(3)), arXiv 1710.02590 (heterogeneous multi-reference alignment).
6. "universal rigidity conic at infinity stress matrix ensemble OR mixture of frameworks
   averaged squared edge lengths unique decomposition" — the standard theory (arXiv 1001.0172,
   1401.7029, 1604.07475); nothing on ensembles or mixtures.
7. "3D genome reconstruction population Hi-C mixture of structures identifiability mean
   squared distance average distance matrix algebraic unmixing" — arXiv 2301.11764, the
   haploid single-cell rigidity paper (PMC11954715); nothing on mixtures of conformations.
8. "neighborly convex hull rank-constrained correlation matrices faces simplices Grothendieck
   ground states vector spin" — Saunderson et al. (arXiv 1204.1220), Tropp (simplicial faces),
   arXiv 1205.2040.
9. "identifiability two conformations hinge domain motion from ensemble-averaged squared
   distances rigid domains reflection ambiguity mixture" — nothing on the question; general
   remarks on averaging (distance distributions from pulsed dipolar spectroscopy against
   averaged values; loss of the signature of multiple conformations in solution scattering).
10. "truncated moment problem on torus product of rotation matrices moments determine
    finitely atomic measure O(2) reflections rigid body chain" — the truncated
    multidimensional trigonometric moment problem (arXiv 2601.08551), truncated matricial
    moment problems and a matricial Richter–Tchakaloff theorem (arXiv 2310.00957,
    2311.10179), flat extensions; nothing on products of rotations about different axes or
    on `O(2)`.
11. "multi-domain protein relative orientation ensemble averaged data degeneracy mirror image
    domain positions residual dipolar couplings four-fold degeneracy averaging tensor
    ensemble" — the fourfold degeneracy of fragment orientations from one alignment medium
    and its removal by a second; "ghost orientations" of domains; nothing on averaged
    squared distances.

Sources returned by the searches and used above:
[arXiv 1203.6602](https://arxiv.org/pdf/1203.6602),
[arXiv 1205.2040](https://arxiv.org/pdf/1205.2040),
[arXiv 2101.05336](https://arxiv.org/pdf/2101.05336),
[arXiv 2301.11764](https://arxiv.org/pdf/2301.11764),
[arXiv 1001.0172](https://arxiv.org/pdf/1001.0172),
[arXiv 1401.7029](https://arxiv.org/pdf/1401.7029),
[arXiv 1604.07475](https://arxiv.org/pdf/1604.07475),
[arXiv 1204.1220](https://arxiv.org/pdf/1204.1220),
[Tropp, Simplicial faces of the set of correlation matrices](https://tropp.caltech.edu/papers/Tro17-Simplicial-Faces-preprint.pdf),
[arXiv 2311.08833](https://arxiv.org/pdf/2311.08833),
[arXiv 2602.20590](https://arxiv.org/html/2602.20590v1),
[arXiv 1710.02590](https://arxiv.org/pdf/1710.02590),
[Shi–Thirumalai, Nat. Commun. 2023](https://www.nature.com/articles/s41467-023-36412-4.pdf),
[Sefer–Duggal–Kingsford](https://pmc.ncbi.nlm.nih.gov/articles/PMC4904159),
[arXiv 2601.08551](https://arxiv.org/html/2601.08551v1),
[arXiv 2310.00957](https://arxiv.org/pdf/2310.00957),
[arXiv 2311.10179](https://arxiv.org/pdf/2311.10179),
[PMC3280151](https://pmc.ncbi.nlm.nih.gov/articles/PMC3280151),
[PMC3328396](https://pmc.ncbi.nlm.nih.gov/articles/PMC3328396).

## 4. What a referee should check first

1. Whether Theorem B (trivial quadrics ⇒ identifiable among all ensembles) is in the
   literature on *dimensional rigidity / universal rigidity with symmetry* or on
   *independent subspace analysis* under other names.
2. Whether "extreme Gram dimension"-type results already cover constraint patterns with
   statewise and averaged edges (our Theorem D(a) for chains with bond angles).
3. Whether the range result `K + 3` (Theorem H) has an analogue in the literature on
   identifiability of mixtures from banded moment data.
