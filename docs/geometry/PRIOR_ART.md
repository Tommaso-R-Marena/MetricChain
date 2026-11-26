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
| Theorem B, B′ (mixtures identifiable among all ensembles iff only trivial quadrics / unique barycentric representation on rank-`d` quadrics) | **`d = 1` with unit-diagonal constraints: known** — Laurent–Poljak 1996, as quoted by Tropp 2018, Fact 3.1 (full column rank of `W` and of `Z = [𝟙 | c_i ⊙ c_j]` ⇒ simplicial face of the elliptope; (CC) is the full column rank of `Z`); found by the Science division's referee (SCI-REV-0021 F3), missed by our searches.  The extension to rank-`d` states and general constraint graphs: **not found**.  Theorem B′: a standard face criterion composed with Lemma 2.2 | Saunderson–Chandrasekaran–Parrilo–Willsky 2012 (faces of the elliptope ↔ ellipsoid fitting); Longinetti–Sgheri–Sottile, arXiv 0712.3777 ("maximal allowed probability", the same question for another averaged observable) [per the Science referee] |
| Corollary 4.2 (simplicial faces of the hull of the chain variety) | `d = 1`: **known** (Laurent–Poljak 1996 via Tropp 2018); extension not found | cut polytope is 3-neighbourly (Deza–Laurent) [from memory] |
| Theorem C (thresholds `(9K²+K+2)/2`, `⌈(9K²+K+8)/4⌉`) | **not found** | — |
| Algorithm DEMIX | **not found**; ingredients classical | classical scaling (Torgerson); joint block diagonalisation |
| Proposition 6.2, DEMIX-`D` (§6.2: below the conic threshold, the rank conditions as linear equations on forms of degree `D`; certificate `h_D = K`; demixing from the annihilator) | **mechanism known** — it is the algorithm of Johnston–Lovitz–Vijayaraghavan 2023 for linear sections of varieties (first level of their Nullstellensatz hierarchy: lift to `S^d(U) ∩ I_d^⊥`, simultaneous diagonalisation, "any output that is not Fail is guaranteed to be correct"); higher levels and the worst-case degree `reg + 1`: Derksen–Johnston–Lovitz 2024; the dimension-count conjecture for the exact generic threshold (rank one, also symmetric): Dastidar–Weich–Wein 2025.  **Ours**: the reduction of ensemble identifiability to a linear section by a *structured* subspace (rank-one conditions along a chain; their theorems are for generic subspaces), the remark that the conic condition is the bottom of the ladder, the structural rank-2 point for `n ≤ 6K − 2`, the count `δ₄` for symmetric rank 3, the computed thresholds (11, 17), the conjecture `max(count, 6K − 1)` — these **not found** | arXiv 2212.03851 [Introduction, §1.4, §2 read through an automated fetch; §§3–6 not reached]; arXiv 2409.18948 [§1 and §6.1 read; Remark 6.10 and §§6.2–6.5 not reached]; arXiv 2504.17947 [Introduction, §2, §6.5–§7 read]; MinRank in cryptography (Kipnis–Shamir; minors modelling: Faugère–Safey El Din–Spaenlehauer) [from memory, not searched] |
| Theorem D(a) freely jointed: `𝒦 = 𝒮` for at most 9 bonds | **known** | extreme correlation matrices have rank `r` with `r(r+1)/2 ≤ n` (Grone–Pierce–Watkins 1990; Li–Tam 1994); Barvinok 1995, Pataki 1998 for general spectrahedra [from memory] |
| Theorem D(a) with bond angles (`n ≤ 6`), D(b) (strict from `n = 7`, exact witness) | **application of the known bound + new witness**; the reading "semidefinite feasibility = ensemble realizability" not found | extreme Gram dimension: E.-Nagy, Laurent, Varvitsiotis 2014 [definition confirmed at summary level: the smallest `r` with `ℰ(G) = π_E(conv ℰ_{n,r})`] |
| Membership in the realizable set is NP-hard for general pair sets (star constraints) | **known** | E.-Nagy, Laurent, Varvitsiotis 2012/2013: membership in the convex hull of the rank-constrained elliptope is NP-hard for every fixed `k ≥ 2` [confirmed at summary level] |
| Theorem E (second-moment rigidity; between global and universal rigidity once the conic condition is added to both) | **not found** as a notion; the Ensemble division's "ensemble rigidity" (laws of edge lengths = global rigidity, its E7) is a different notion | universal rigidity: Connelly; Gortler–Thurston 2014; Connelly–Gortler 2015; global rigidity: Gortler–Healy–Thurston 2010 |
| Theorem F for `K = 1` | **known** | Connelly's sufficient condition (positive semidefinite stress of maximal rank + no conic at infinity) [confirmed at summary level] |
| Theorem F for `K ≥ 2`, Theorem G (global `W₂` bound with explicit certificate) | Theorem G (b)–(c): **mechanism known** — the localisation bound of sparse-measure recovery from a non-degenerate dual certificate (Fernandez-Granda 2013, Theorem 1.2; read in full by the Science referee); specific here: the explicit certificate and `κ > 0` under (CC).  Theorem F for `K ≥ 2`: not found | Hölder-½ error bounds for semidefinite feasibility at singularity degree one (Sturm 2000; Drusvyatskiy–Pataki–Wolkowicz 2015) [from memory] |
| Theorem H (local identifiability from separation `K + 3`; complete data from `n = 2K + 3`) | **not found** | — |
| Theorem F′ (separation `3K + 1`) | **application** of trilateration | Zhu–So–Ye 2010 (universal rigidity of `(d+1)`-lateration graphs) [from memory] |
| Theorem I (two states identifiable among all ensembles from 10 atoms; three thresholds) | **not found** | determinantal varieties and structural low-rank points: classical tools |
| Theorem J (laws of separations 3 and 4) | **application** of the Ensemble division's E5/E6 (its report, 2026-11-26) | its remark on prior art: Garamvölgyi–Gortler–Jordán 2022 (Lemma 3.1), unlabeled PCA |
| Corollary 9.1 (second moment suffices under bond constraints) | **instance of a known principle** with a specific prior | Bandeira–Blum-Smith–Kileel–Perry–Weed–Wein (moments and sample complexity for orbit recovery); Bendory–Edidin and co-authors: sparse priors, generic semi-algebraic priors, non-uniform rotations make the second moment sufficient [confirmed at summary level] |
| Hinge ensembles (`HINGE_ENSEMBLES.md`): reduction to a moment problem on `O(2)^s` with interval moments; two states at two or more hinges identifiable, the cube of eight candidates (Theorem M) | **not found** (three summary-level searches); ingredients classical | composition of rotations by reflections; reflection branching in discretizable distance geometry; truncated (matricial) trigonometric moment problems and flat extensions (Curto–Fialkow); ghost orientations of domains from residual dipolar couplings (a different observable) |
| Theorems L, L⁺ (`LOCAL_DATA_STABILITY.md`): global bound `≤ C n²` — for every configuration, no threshold — for reconstruction from distances of sequence separation `≤ 4` on chains with non-degenerate windows; matching lower bound on rods (Theorem K(c)); the first-order constant in a certified range | **not found as stated; mechanism and scaling known** (thin-rod geometric rigidity: Mora–Müller 2003; Blanchard–Griso 2009; lattice versions: Alicandro–Lazzaroni–Palombaro 2016, Schmidt–Zeman 2022); first-order polynomial bounds in print (Daitch–Spielman 2007; Kyng et al. 2018; Lew et al. 2023); the published *global* bound for this lateration graph is exponential (Arias-Castro–Vishwanath) [Science division A4, 2026-11-26].  Lemma P is Tu et al. 2016, Lemma 5.4 [from memory].  Not read: Schrader 1967 and the geodesy of trilateration chains; Luo–Wu 2011; Anderson–Shames–Mao–Fidan 2010; Friesecke–James–Müller 2002 itself.  The threshold-free form and Theorem L⁺ were written after the search | Science division, SCI-REV-0023 and `docs/science/workstreams/A4_REPORT.md` on its branch (123 logged queries, 33 texts opened); ours: arXiv 2310.10900 [one automated reading], two searches |

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

## 3. Search log (2026-11-26; web search, summaries only unless an entry says that a paper was read; searches 9–11 for `HINGE_ENSEMBLES.md`, 12–13 for Theorem L, 14–15 for §6.2)

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
12. "quantitative stability bound trilateration graph localization error accumulation
    polynomial in number of nodes sequential distance geometry noisy distances bound
    reconstruction error" — arXiv 2310.10900 (Stability of Sequential Lateration), Moore et
    al. 2004 (robust distributed localisation; flips), component-based localisation (error
    accumulation in sequential generation), arXiv 1103.1417.  arXiv 2310.10900 was then read
    through a fetch of its HTML version (v3): Theorems 2.1, 3.1, 4.1, Proposition 3.2, the
    constants (2.30), (2.33) — exponential in `n` in the chain-like case; no polynomial
    bound.
13. "geometric rigidity estimate Friesecke James Müller constant thin rod scaling L^2/h^2
    discrete version chain of simplices rotations telescoping" — the estimate and its
    degeneration for thin domains (arXiv 2006.08840, 1908.04021), rod theories as limits
    (arXiv 0803.0923), a proof with explicit constants attributed to Conti and Zwicknagl
    (in arXiv 2608.00863); no discrete chain version.

14. "Johnston Lovitz Vijayaraghavan "Computing linear sections of varieties" quantum
    entanglement tensor decompositions algorithm" — arXiv 2212.03851 (made after §6.2 had been
    written from our own derivation and a memory that such a literature exists; the search
    was done before anything was committed — rule DG-20).  The paper was then read through an
    automated fetch (Introduction with Theorem 2 and Corollaries 3, 4, 8; §1.4 with the
    algorithm; §2): given degree-`d` equations of a conic variety `X` and a basis of a subspace
    `U`, compute `S^d(U) ∩ I_d^⊥`; if it is zero, `U ∩ X = {0}` ("a degree-`d` Nullstellensatz
    certificate"); otherwise simultaneous diagonalisation looks for a basis `v_1^{⊗d}, …, v_s^{⊗d}`
    with independent `v_i`, and then "the only elements of `U ∩ X` are `v_1, …, v_s`"; "any
    output that is not Fail is guaranteed to be correct".  Theorem 2: for `X` irreducible, cut
    out by `δ·C(n+d−1, d)` forms of degree `d`, with no equations of lower degree, and `U`
    spanned by `s` generic points of `X` and `R − s` generic vectors, `R ≤ δ(n + d − 1)/d!`, the
    algorithm succeeds; Corollary 4 is the case of matrices of rank at most `r`.  Nothing on
    symmetric matrices of rank 3, on structured subspaces, on distance geometry.
15. "hierarchy of linear systems Nullstellensatz certificate subspace contains no low-rank
    matrix symmetric minors lifting degree MinRank planted recovery" — arXiv 2504.17947
    (Dastidar, Weich, Wein, "Improving the threshold for finding rank-1 matrices in a
    subspace"); the entanglement-hierarchy paper of Johnston–Lovitz–Vijayaraghavan
    (Phys. Rev. A 106, 062443); general Nullstellensatz-certificate literature.
    arXiv 2504.17947 was read through an automated fetch (Introduction, §2, §6.5–§7): for
    rank-one `m × n` matrices and generic planted subspaces the first level succeeds for
    `R ≤ (m−1)(n−2)/2` (improving `(m−1)(n−1)/4`), fails when a dimension count fails
    (`C(m,2)C(n,2) < C(R+1,2) − s`), and is conjectured to succeed whenever the count allows;
    the symmetric analogue is their Conjecture 6.10 (count `m²(m²−1)/12` — the Schur module
    of the `2 × 2` square, as our `δ₄` is that of the `4 × 2` rectangle); identifiability holds
    up to `R = (m−1)(n−1)`; "higher levels have been analyzed only in the fully non-planted
    case `s = 0`, where they are shown to work even for nearly full-dimensional subspaces
    `R ≤ (1−ε)mn` with runtime `(mn)^{f(ε)}`" (citing Derksen–Johnston–Lovitz,
    arXiv 2409.18948).  That paper was then fetched (§1, §6.1 read): Theorem 1.8 (a generic
    subspace of dimension `(1−ε)N` is certified at a constant level), Theorem 1.9 (a
    sufficient count), Theorems 1.10–1.11 (the worst-case level is exactly the
    Castelnuovo–Mumford regularity plus one when the coordinate ring is Cohen–Macaulay;
    `r(min(n_1, n_2) − r) + 1` for matrices of rank at most `r`).  Its Remark 6.10 and
    §§6.2–6.5 were not reached by the fetch.

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
[PMC3328396](https://pmc.ncbi.nlm.nih.gov/articles/PMC3328396),
[arXiv 2310.10900](https://arxiv.org/abs/2310.10900),
[Moore et al. 2004](https://people.csail.mit.edu/teller/pubs/MooreEtAlSensys2004.pdf),
[arXiv 1103.1417](https://arxiv.org/pdf/1103.1417),
[arXiv 2006.08840](https://arxiv.org/pdf/2006.08840),
[arXiv 1908.04021](https://arxiv.org/pdf/1908.04021),
[arXiv 0803.0923](https://ar5iv.arxiv.org/html/0803.0923),
[arXiv 2608.00863](https://arxiv.org/pdf/2608.00863),
[arXiv 2212.03851](https://ar5iv.labs.arxiv.org/html/2212.03851),
[arXiv 2504.17947](https://arxiv.org/html/2504.17947v1),
[arXiv 2409.18948](https://arxiv.org/abs/2409.18948),
[Phys. Rev. A 106, 062443](https://link.aps.org/accepted/10.1103/PhysRevA.106.062443).

## 3a. What the Science division's review found that our searches missed (SCI-REV-0021 F3, F9)

* Laurent–Poljak 1996 (through Tropp 2018, Fact 3.1): Theorem B and Corollary 4.2 for `d = 1`.
  Our search 8 had returned Tropp's paper and we listed it as "a relative, not a
  consequence" without reading its Fact 3.1.  Lesson: a returned paper is read before it is
  classified.
* Fernandez-Granda 2013: the mechanism of Theorem G (b)–(c).
* The "extreme Gram dimension" (our search 2) is a statement about projections and does not
  cover Theorem D (a), which is the Barvinok–Pataki bound on a fibre; question 2 of §4 below
  is thereby answered: the cited results cover the star pattern only.

## 3b. §6.2 (certificates below the conic threshold): what is known and what is ours

Found by our own search before commit — the first time rule DG-20 worked as intended.

* **Known.**  (i) The method: lift to a symmetric power, intersect with the annihilator of
  the equations, read the points off by simultaneous diagonalisation, with a certificate of
  completeness (Johnston–Lovitz–Vijayaraghavan, FOCS 2023); it specialises to FOOBI
  (De Lathauwer and co-authors) for rank-one matrices.  (ii) The hierarchy of higher levels,
  its completeness, and its worst-case level — the regularity plus one
  (Derksen–Johnston–Lovitz 2024; for us: the regularity of the symmetric matrices of rank at
  most 3 of size `3K`, which we computed from the Hilbert series as 6, 9, 15, 18, 24 for
  `K = 2, …, 6`).  (iii) For *generic* subspaces: success at a constant fraction of the
  maximal dimension at the first level, at a fraction `1 − ε` at a constant level, and a
  conjecture that the first level succeeds exactly when a dimension count allows
  (Dastidar–Weich–Wein 2025, rank one).
* **In our notation.**  Their `U` is our `L`; their `X` is the cone of symmetric `3K × 3K`
  matrices of rank at most 3 (dimension `9K − 3`); their `s` planted points are our `K`
  projectors; their "maximal dimension" `codim X` corresponds to our information threshold
  `n = ⌊9K/2⌋ + 1`; their first level is our `D = 4`; the conic condition is the degenerate
  case `L = span` of the planted points.
* **Ours** (not found): that ensemble identifiability below the conic threshold *is* such a
  linear section (Remark 5.1, Theorem B′) — by a subspace that is not generic but cut out by
  rank-one conditions along a chain; the structural point of rank 2 for `n ≤ 6K − 2`, which a
  generic subspace does not have and which shifts the threshold for two and three states;
  the computed thresholds; the conjecture that for chains the first level works exactly from
  `max(count, 6K − 1)` atoms on.
* **Not done.**  MinRank in cryptography (Kipnis–Shamir; minors modelling and its
  complexity for generic instances) is quoted from memory only; no search.  §§3–6 of
  arXiv 2212.03851 and §§6.2–6.5 of arXiv 2409.18948 were not read.

## 4. What a referee should check first

1. Whether Theorem B (trivial quadrics ⇒ identifiable among all ensembles) is in the
   literature on *dimensional rigidity / universal rigidity with symmetry* or on
   *independent subspace analysis* under other names.
2. Whether "extreme Gram dimension"-type results already cover constraint patterns with
   statewise and averaged edges (our Theorem D(a) for chains with bond angles).
3. Whether the range result `K + 3` (Theorem H) has an analogue in the literature on
   identifiability of mixtures from banded moment data.
