# Prior-art register — Ensemble division

For every statement we would like to call new: the closest published results, the exact
difference, and how each source was read.  Reading levels: **full** (the relevant statement
and its proof read in the source), **partial** (statement read verbatim through a fetch
tool, proof not, or only part of the text reachable), **summary** (search-engine summary
only), **memory** (cited from memory; an obligation until read).  "Not found" is the result
of the searches logged in §6 and is not a claim of novelty.

## 1. Theorem E1 (identified = exposed simplex) and Proposition E1.1

| source | what it has | level |
|---|---|---|
| Choquet theory; Karlin–Studden, *Tchebycheff Systems* (1966); Krein–Nudelman | uniqueness of representing measures on simplicial faces; principal representations of moment sequences on an interval; index of a representation | memory |
| Rogosinski (1958), Richter (1957), Tchakaloff (1957); Winkler (1988) | extreme points of moment sets have at most `m + 1` atoms | memory |
| de Castro–Gamboa (2012); Candès–Fernandez-Granda (2014); Schiebinger–Robeva–Recht (2018); Eftekhari–Tanner–Thompson–Toader–Tyagi (2021) | dual certificates for sparse (non-negative) measures from generalised moments; stability in transport-type distances from a certificate, for point sources on an interval | memory |
| quantum analogue: Linden–Popescu–Wootters (2002); Chen–Dawkins–Ji–Johnston–Kribs–Shultz–Zeng (2013) | states uniquely determined by local marginals; relation to unique ground states of local Hamiltonians | memory |
| science division, `INFERENCE_LIMITS.md` §8 | the *bounding* side: a multiplier `λ` and a certified maximum bound an average over all ensembles with given data | full (their file at `2b4ccdf`) |

**Classification.**  E1: known in substance; our contribution is the formulation (support =
ground-state set of an energy in the span) and the machine-checked sufficiency.  E1.1:
elementary.  Example E1.2: constructed here; the phenomenon (non-exposed faces, Hölder
stability) is classical convex geometry.

## 2. Theorem E2 (one conformation; the bridge)

| source | what it has | level |
|---|---|---|
| theory report §2.3, Theorem 2.4, `robust_certified_iff` | sharp minimum ⇔ optimal for every admissible residual | full |
| Polyak (1979); Burke–Ferris (1993) | sharp minima and Lipschitz perturbations (cited in the theory report) | memory |
| Blanchet–Murthy (2019); Gao–Kleywegt (2016/2023); Mohajerin Esfahani–Kuhn (2018) | duality for worst-case expectations over transport balls: `sup_{W(ν,μ)≤ρ} E_ν f = inf_s [sρ + E_μ sup_y(f(y) − s·d(·,y))]`; the inner supremum is the Pasch–Hausdorff envelope | memory |
| generalised moment problems (Kemperman 1968; Lasserre 2008) | linear-programming duality for `sup E_ν ρ` under moment constraints | memory |

**Classification.**  (a), (b): linear-programming duality — known technique, the statement
(the identification constant as the least norm of a sharp energy in the span) is a
formulation we did not find.  (c): the dictionary with robust optimality under a residual
class is new as a statement (not found); its mathematics is two lines given Theorem 2.4.

## 3. Theorem E3

Not found.  Elementary given Kantorovich–Rubinstein duality.  The independence of the
first-order constant from the weights is implicit in any local analysis of sparse recovery
(the tangent cone depends on the support only).

## 4. Part II

| source | what it has | level |
|---|---|---|
| Rényi, "On projections of probability distributions", Acta Math. Acad. Sci. Hung. 3 (1952) 131–142; Heppes, same journal 7 (1956) 403–410 | `K` atoms in the plane / in `ℝ^d` are determined by `K + 1` projections, among all probability measures | summary (statement as quoted by Fraiman–Moreno–Ransford 2022, arXiv 2201.07628, and by arXiv 2203.13741) |
| Fraiman–Moreno–Ransford, "A quantitative Heppes theorem and multivariate Bernoulli distributions" (2022) | a quantitative version for projections | summary |
| Garamvölgyi–Gortler–Jordán, "Globally rigid graphs are fully reconstructible", Forum Math. Sigma 10 (2022) e51 | Theorem 3.5: globally rigid in `ℝ^d` on `≥ d + 2` vertices ⇒ `R_d`-connected; Lemma 3.1: a separator of `R_d(G)` splits the measurement variety as a product; Lemma 2.13: `dim M_{d,G} = r_d(G)` | partial (ar5iv text; statements verbatim, proof of Theorem 3.5 read; Sections 4–5 not read) |
| Jackson–Jordán (2005), "Connected rigidity matroids and unique realizations of graphs" | the planar case | memory (as cited by the previous source) |
| Gortler–Healy–Thurston (2010) | global rigidity is generic; stress-matrix characterisation | memory |
| Gortler–Theran–Thurston (2019), "Generic unlabeled global rigidity" | one configuration from the *unordered* set of edge lengths | memory |
| Yao–Peng–Tsakiris, "Unlabeled principal component analysis (and matrix completion)", NeurIPS 2021 / JMLR 25 (2024) | Theorem 2: for a generic matrix of rank `r < min(m, n)`, permuting the entries inside each column cannot give rank `≤ r` except by a row permutation | partial (ar5iv; statement verbatim, proof not reached) |
| Cruickshank–Mohammadi–Nixon–Tanigawa (2023), arXiv 2305.18990 | rigidity for general polynomial measurement maps; identifiability of points | summary |
| arXiv 2111.10834 ("The shape of a Gaussian mixture is characterized by the probability density of the distance between two samples") | one configuration (the means) from an unlabelled distance distribution | summary |
| Vitushkin–Henkin, "Linear superpositions of functions", Russian Math. Surveys 22 (1967) 77–125 | sums `Σ p_i·(g_i∘q_i)` with `C¹` inner functions are nowhere dense in `C(D)` | summary (statement as quoted in arXiv 1712.08286, Theorem 3.3, and by Ismailov) |
| Khavinson, *Best approximation by linear superpositions* (1997); Marshall–O'Farrell (1979, 1983); Sternfeld (1985) | measures orthogonal to sums of univariate functions; bolts; basic embeddings | memory |

**Classification.**  E4: a generalisation of Rényi–Heppes whose proof is theirs; we have
not found the statement for arbitrary features or the sharpness for `r > 2`; "generalisation
of a known theorem", plus a formalisation.  E5(a), E6: not found.  E5(b) is the product
lemma of Garamvölgyi–Gortler–Jordán transferred to any polynomial map, with the local
realisability added.  E7, E8: not found; they rest on two cited theorems.  The
identification of a *mixture* of frameworks from per-edge distance laws was searched for
directly (§6, search 7) without a hit; unlabeled PCA is the nearest neighbour and differs
in that its variety (a determinantal variety with an unknown generic subspace) is not
known in advance.  E8.1: a corollary of a known theorem.

## 5. Part III

| source | what it has | level |
|---|---|---|
| Deza–Laurent–Poljak, "The cut cone III", Graphs Combin. 8 (1992); Deza–Laurent, *Geometry of Cuts and Metrics* (1997); Ziegler, "Lectures on 0/1-polytopes" | the cut polytope is 3-neighbourly and not 4-neighbourly in general | summary |
| Odlyzko, "On subspaces spanned by random selections of ±1 vectors", J. Combin. Theory A 47 (1988) 124–133 | for `p ≤ n − 10n/ln n` the probability that the span of `p` random sign vectors contains another sign vector is the three-vector term plus `O((7/10)ⁿ)`; motivated by associative memories (Kanter–Sompolinsky) | summary; the exact leading term `4C(p,3)(¾)ⁿ` is from memory and matches our enumeration (C2) |
| Irmatov, arXiv 2405.05082 (2024) | restates Odlyzko's theorem; the Kalai–Linial conjecture | summary |
| Kueng–Tropp, "Binary component decomposition I", SIAM J. Math. Data Sci. 3 (2021) | uniqueness and efficient computation of `C = Σ τ_i s_i s_iᵀ` under Schur independence (`K(K−1)/2 + 1 ≤ n`); simplicial faces of the elliptope | partial (ar5iv; Theorem I and Definition 2.1 verbatim; Theorem 3.4 and Remark 3.5 from a tool summary) |
| Slawski–Hein–Lutsik, "Matrix factorization with binary components", NeurIPS 2013 | uniqueness of binary factors through Littlewood–Offord / Odlyzko | memory |
| van der Veen (1997); Talwar–Viberg–Paulraj (1996) | blind separation of binary sources: identifiability iff the row space contains no other sign vectors | memory |
| Bai–Yin (1993) | smallest singular value of a large random matrix with i.i.d. entries | memory |
| Sheppard (1899); Grothendieck's identity; Goemans–Williamson (1995) | `E sign g_i sign g_j = (2/π) arcsin R_ij` | memory |
| Cover (1965); Schläfli | number of linearly separable dichotomies | memory |
| Krishnamurthy–Singh (2013); Chen–Epperly–Tropp–Webber (2022/2025, randomly pivoted Cholesky) | adaptive sampling of low-rank / positive semidefinite matrices | memory |

**Classification.**  E9: known.  E10: a synthesis — Odlyzko's theorem (and, for our own
range, his lemma and the Littlewood–Offord inequality) plus the exposure argument; the
reading "resolved by pair-averaged data with any populations, among all ensembles" was not
found (Kueng–Tropp prove uniqueness in the Schur-independent range `K = O(√n)`; the binary
source-separation literature has the span condition for exact factorisations with a known
number of sources).  E11: not found; elementary.  E12: (b) is the exactness of pivoted
Cholesky for positive semidefinite matrices of finite rank — known; (a) and (c) are
formulations (not found); (c) is Cover's theorem applied to local stability, a standard
argument of the theory of associative memories.

## 6. Search log (2026-11-26)

1. "globally rigid graphs M-connected rigidity matroid higher dimensions" — found
   Garamvölgyi–Gortler–Jordán 2022 (answers our own question E-G1 of ENSEMBLE-MSG-0001).
2. "Unlabeled Principal Component Analysis Yao Peng Tsakiris" — found; fetched.
3. "Kueng Tropp Binary component decomposition Schur independent cut polytope face" —
   found; fetched.
4. "Rényi projections of probability distributions k atoms k+1 projections Heppes" —
   statements found in two later papers; originals not read.
5. "Odlyzko On subspaces spanned by random selections of ±1 vectors" — found (paper,
   Irmatov's restatement); formula not verified in the original.
6. "cut polytope 3-neighborly Deza Laurent Poljak" — statement confirmed in secondary
   sources.
7. "identifiability of a mixture of conformations from pairwise distance distributions
   rigidity global rigidity mixture of point configurations" (extended search) — no direct
   source; nearest: arXiv 2111.10834, arXiv 2305.18990, arXiv 2407.10700.
8. "Vitushkin Henkin linear superpositions continuously differentiable nowhere dense" —
   statement found as quoted by later papers.

Not searched yet (obligations): quantitative Heppes (to compare with O4); "random faces of
the cut polytope" (O1); identifiability of secant varieties of measurement varieties (O5);
the literature on maximum-occurrence and ensemble refinement in structural biology for a
uniqueness theorem of the form E7.
