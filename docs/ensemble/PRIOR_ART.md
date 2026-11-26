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
| Donoho–Tanner, "Sparse nonnegative solution of underdetermined linear equations by linear programming", PNAS 102 (2005) 9446–9451; Bruckstein–Elad–Zibulevsky, IEEE Trans. Inform. Theory 54 (2008) 4813–4820 | the face criterion for the unique non-negative solution of an underdetermined linear system — the finite form of E1(a); **pointed out by the science division (SCI-RES-0026 §2(a)), which found them by a search and cites them from summaries** | summary (through the science division) |
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
class was not found in print; its mathematics is two lines given Theorem 2.4, and the
internal review ER1 classes it, rightly, as a formulation.

## 3. Theorem E3

| source | what it has | level |
|---|---|---|
| Chandrasekaran–Recht–Parrilo–Willsky, "The convex geometry of linear inverse problems", Found. Comput. Math. 12 (2012) | recovery error at most `2δ/ε` when `‖Az‖ ≥ ε‖z‖` on the tangent cone (minimum conic gain) | memory (the review ER1's; Proposition 2.2 by its recollection) |
| Hoffman (1952) and the literature on calmness / error bounds of polyhedral systems | the constant of a polyhedral system depends on the active set only | memory |

**Classification.**  Formulation (lowered from "new (not found)" after the internal review
ER1, F11): `1/κ_μ` is the minimum conic gain of the data map on the tangent cone of the
simplex at `μ`, measured in the Kantorovich–Rubinstein norm; that it depends on the support
only is standard in that literature.  What is ours is the sup–min formula over
interpolating majorants in the transport norm.

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

| Boneh–Shaw, "Collusion-secure fingerprinting for digital data" (CRYPTO 1995 / IEEE Trans. Inform. Theory 44 (1998)); Staddon–Stinson–Wei (2001); Fernandez–Urroz, arXiv 2103.02341 | *frameproof codes*: a code of length `ℓ` and minimum distance `d > ℓ − ℓ/c` is `c`-frameproof — the support step of E4 with `d = m − r + 1`, `c = K` | summary (the review ER1's search; the lemma is attributed to Boneh–Shaw by the third source) |

| Dokmanić–Parhizkar–Walther–Lu–Vetterli (2013), echo sorting; Hays–Boland–Kasson (separately acquired distance distributions) | the no-chimera property with the genericity on the sensors; the applied problem without a uniqueness statement | named by the science division's referee (SCI-REV-0020); not opened here |
| Gortler–Healy–Thurston (2010), Definition 1.4 and Corollary 1.15 | the genericity statement used in E7 — opened by the science division's referee (through a fetch), who confirms it is the one we use; Garamvölgyi–Gortler–Jordán Theorem 3.5 likewise, and that its published proof already splices lengths along a separator | read by the science division, not by us |

**Classification.**  E4: a generalisation of Rényi–Heppes whose proof is theirs; the
support step is, in other words, the frameproof-code lemma (found by the internal review
ER1: a splice is a descendant of a coalition, "no chimera" is frameproof).  We have not
found the statement for weights and arbitrary measures over arbitrary features, or the
sharpness for `r > 2`; "generalisation of a known theorem", plus a formalisation.  Heppes'
theorem is for `K + 1` subspaces any two of which determine the point (Fraiman–Moreno–
Ransford, Theorem 1.1, at the level of the review's search); version 1 misquoted it.  E5(a), E6: not found.  E5(b) is the product
lemma of Garamvölgyi–Gortler–Jordán transferred to any polynomial map, with the local
realisability added.  **After the science division's review (SCI-REV-0020, M4):** E5(a) is
a dimension count — elementary, a formulation; E7 is a corollary of the cited theorem of
2022 through E5/E6, and its converse is the case of one conformer; E8 is the classical
`2K`-moment certificate edge by edge.  What was not found — by us or by that review's
eighteen searches — is the reading: a finite mixture of frameworks identified from one
law per edge.  The
identification of a *mixture* of frameworks from per-edge distance laws was searched for
directly (§6, search 7) without a hit; unlabeled PCA is the nearest neighbour and differs
in that its variety (a determinantal variety with an unknown generic subspace) is not
known in advance.  E8.1: a corollary of a known theorem.  The uniqueness of a `K`-atomic
measure on the line among non-negative measures with its first `2K` moments (first step of
E8) is classical (Gauss quadrature; Karlin–Studden).  The converse "identified ⇒ no
chimera" claimed in version 1 is false (counterexamples by the review ER1; report §3.2).

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
| Laurent–Poljak, "On the facial structure of the set of correlation matrices" (1996), as quoted by Tropp (2018, Fact 3.1) | a sufficient condition for a set of cut matrices to span a simplicial face of the elliptope — the `d = 1` case of the Geometric Inference Division's Theorem B, and a stronger conclusion than the face of the cut polytope of our E10 | named by the science division's referee for the geometry division (GEOMETRY-MSG-0007 §2 (b)); not opened here |
| Tropp, "Simplicial faces of the set of correlation matrices", arXiv 1801.00749 (2018), Theorems 2.9–2.11; Laurent–Poljak (1995/1996), Theorem 4.2 | `K` random sign vectors span a simplicial face of the *elliptope* with probability at least `1 − K² e^{−n/K²}`; no simplicial face of the elliptope has more than about `√(2n)` vertices; the linear-independence condition of Laurent–Poljak.  Our E10 concerns the cut polytope, where the range is `n − o(n)` | read by the Complexity division (COMPLEXITY-RES-0008 §§1(b), 2(a)); not opened here |
| The Complexity division's `ISING_GROUND_SETS.md` (its Propositions 5, 13, 13′, Theorem 14) | deciding "exactly the ground states of a pair energy": `2^K·poly(n)`; degree-2 certificates ⇔ no other sign vector in the span; NP-completeness of the span question | COMPLEXITY-RES-0003, -0007, -0008 read in full; the note itself not opened |
| Sheppard (1899); Grothendieck's identity; Goemans–Williamson (1995) | `E sign g_i sign g_j = (2/π) arcsin R_ij` | memory |
| Cover (1965); Schläfli | number of linearly separable dichotomies | memory |
| Gardner, "The space of interactions in neural network models", J. Phys. A 21 (1988); Personnaz–Guyon–Dreyfus (1985); Kanter–Sompolinsky (1987) | capacity `α = 2` of networks with independent couplings per site; the projection (pseudo-inverse) rule, whose energy is the certificate `‖P^⊥x‖²` of E10 | memory (named by the review ER1) |
| Krishnamurthy–Singh (2013); Chen–Epperly–Tropp–Webber (2022/2025, randomly pivoted Cholesky) | adaptive sampling of low-rank / positive semidefinite matrices | memory |

**Classification.**  E9: known.  E10: a synthesis — Odlyzko's theorem (and, for our own
range, his lemma and the Littlewood–Offord inequality) plus the exposure argument; the
reading "resolved by pair-averaged data with any populations, among all ensembles" was not
found (Kueng–Tropp prove uniqueness in the Schur-independent range `K = O(√n)`; the binary
source-separation literature has the span condition for exact factorisations with a known
number of sources).  E11(a): a synthesis — it is the classical capacity bound `α ≤ 2` of
pair-interaction associative memories (Cover; Gardner) read through Theorem E1 (lowered
from "new" after the review ER1, F4).  E11(b): not found; elementary.  The 3-neighbourliness
of E9 is stated in Ziegler's lectures for the correlation polytope ("best possible"); what
exactly Deza–Laurent–Poljak (1992) prove was not verified (obligation OB3).  E12: (b) is the exactness of pivoted
Cholesky for positive semidefinite matrices of finite rank — known; (a) and (c) are
formulations (not found); (c) is Cover's theorem applied to local stability, a standard
argument of the theory of associative memories.

## 5a. Parts IV and V, Theorem E7′ (second checkpoint)

| source | what it has | level |
|---|---|---|
| DeRobertis–Hartigan (1981); Berger, Wasserman and others on density-ratio classes | ranges of posterior expectations over classes `l ≤ dμ/dπ ≤ u` (the separable envelope); threshold rule | memory (also named by the science division for theory report §11.28) |
| Efron–Stein / martingale-difference decompositions; `L¹` Poincaré and isoperimetric inequalities on product spaces (Talagrand 1993; Bobkov–Götze 1999); influences of monotone functions equal their covariances with the coordinates | every analytic ingredient of E15: the proof is an `L¹` martingale decomposition plus monotonicity of the density | memory |
| Holley / FKG inequalities | the population bound of E15T(a) | memory |
| Donoho, "Statistical estimation and optimal recovery", Ann. Statist. 22 (1994) 238–270 | modulus of continuity determines minimax risk of linear functionals over convex classes; affine estimators within about `1.25` | summary (abstract and a set of lecture notes) |
| Stewart–Gough platforms (forward kinematics: up to 40 poses for six legs); Tay (1984), body–bar frameworks; Connelly–Jordán–Whiteley (2013), generic global rigidity of body–bar frameworks | single-pose facts used in E7′ | memory |

*Added by the second internal review (ER2; its list of sources, with the level at which
each was read, is at the end of `reviews/ER2_internal_review.md`):*

| source | what it has | level |
|---|---|---|
| Peres–Winkler, "Can extra updates delay mixing?", arXiv 1112.0603, Lemmas 2.2–2.4 | "monotone likelihood ratio ⇒ stochastic domination" and "the indicator of `{ν > π}` is increasing": the first step of E15/E15T | read by the reviewer (pp. 2–9) |
| Strassen's theorem (monotone couplings of stochastically ordered measures); Harris' inequality; Holley's inequality | the coupling proof of E15(c) and E15T(a) | memory; confirmed in a summary of S. Roch, *Modern Discrete Probability*, ch. 4 |
| Poincaré inequality on the cube and `Inf_i[f] = f̂(i)` for monotone `f` (O'Donnell, *Analysis of Boolean Functions*; arXiv 1205.0314) | the machine-checked inequality `E|r − Er| ≤ 2Σ_i Cov(r, e_i)` is the `L¹` form | summary |
| Farmer (1994); Smarzewski (1997), as cited by arXiv 1905.07547; Bredies–Chirinos Rodriguez–Naldi, arXiv 2304.14039 | extreme points of the Lipschitz unit ball on a finite metric space: E13(a) | summary |
| P. B. Stark, Statistics 210B lecture notes 6 (restating Donoho 1994, Theorems 1–2, Corollaries 1–2) | minimax affine risk `sup_ε (ω(ε)²/4)σ²/(σ² + ε²/4)`; within `1.25` of the minimax risk | read by the reviewer; Donoho's paper: abstract only |
| Connelly–Jordán–Whiteley, "Generic global rigidity of body–bar frameworks" (2013) | generically globally rigid ⇔ redundantly rigid: for two bodies, `m ≥ D_d + 1` legs — the single-pose half of E7′(b) | summary |
| Innocenti (1998), seven in-parallel transducers; Raghavan (1993), Wampler (1996), Dietmaier (1998), Hauenstein–Sottile's certification | seven lengths determine the pose by linear equations; at most 40 poses for six legs, all 40 can be real | summaries |
| Barlow–Proschan (*Statistical Theory of Reliability and Life Testing*, 1975): conditionally increasing in sequence ⇒ associated | the implication used in E15T(b); proved in the report in three lines | memory |

**Classification (after ER2 and SCI-RES-0032).**  E13(a): known in substance (extreme
Lipschitz functions), carried to the weights; E13(b), (c): polyhedral geometry and LP
duality; the flow format is the science division's.  **E15, E15T: formulation** — the
inequality is a union bound over a monotone coupling (Harris or FKG, then Strassen), and
the machine-checked core is the `L¹` Efron–Stein inequality for monotone functions; the
combined inequality "total variation at most the sum of the one-site marginal gaps for
stochastically ordered measures" was not found stated in print in our search (item 10 of
the log) or in the reviewer's three, and the reviewer believes it standard in
mixing-time arguments.  What is ours: the observation that a first-order class lies
stochastically above its most polarised member, and the reading.  The exact statement
on one-body marginals and the closed form for the least scale are the science
division's.  E15(d), E16: not found; elementary.  E17: a formulation of Donoho's theory
with the dual written as a certificate; the constant `0.335` is the exact Bayes risk of
two points (elementary; surely known).  E7′: the single-pose half is known
(Connelly–Jordán–Whiteley; Innocenti); the ensemble statement is a corollary of E5/E6,
not found.  The sandwich `l ≤ w ≤ u` as a first-order class (hub metric) is the science
division's observation; the class itself is the density-ratio class of DeRobertis and
Hartigan (memory).  OB10 is closed at the level "two searches of ours, twelve sources
consulted by the reviewer"; no source was read in the original except Peres–Winkler and
Stark's notes.

## 5b. Part VI (third checkpoint)

| source | what it has | level |
|---|---|---|
| Baldi–Vershynin, "Polynomial threshold functions, hyperplane arrangements, and random tensors", arXiv 1803.10868v3 (2019); first version titled "Boolean polynomial threshold functions and random tensors" | **Theorem 4.2 (resilience of linear independence):** for `dn^{0.02} ≤ t ≤ 0.001n` and `m < C(n − Cn/log n − t, ≤d)`, with probability above `1 − 2^{−t/4}` the span of the lifts `x_i^{≤d}` of `m` random sign vectors contains no `u^{≤d}`, `u ∈ {−1,1}^n`, other than `±x_i^{≤d}`; "for tensors of any order `d > 1`, Theorem 4.2 is new", proved from Theorem 4.1 "using an argument that is inspired by Odlyzko's method".  Theorem 4.1 = Abbe–Shpilka–Wigderson's Theorem 4.5 (linear independence for `m < C(n − log C(n,≤d) − t, ≤d)`, probability `1 − 2^{−t}`).  Theorem 3.3: Cover-type upper bound on the number of polynomial threshold functions.  Main result: `log₂ T(n,d) ≈ n·C(n,≤d)` | **statements read verbatim** in the PDF of v3 (text extracted locally); proofs (Sections 5–6) not read; journal reference not found |
| Abbe–Shpilka–Wigderson, "Reed–Muller codes for random erasures and errors", arXiv 1411.4590 (STOC 2015; IEEE Trans. Inform. Theory 61 (2015) per the previous source's bibliography) | Theorem 1.3 / 4.5: `(1−o(1))C(m,≤r)` random columns of the evaluation matrix of monomials of degree `≤ r` are linearly independent w.h.p., `r = O(√(m/log m))` | partial (abstract and introduction through a fetch; Theorem 4.5 as quoted by Baldi–Vershynin) |
| Chiantini–Coppens, "Grassmannians of secant varieties", arXiv math/0005202 | Corollary 1.3 (generalised trisecant lemma): over `ℂ`, `X ⊂ ℙ^r` integral non-degenerate of dimension `n`; if `k < r − n` a general `(k+1)`-secant `k`-plane meets `X` in exactly `k + 1` points; proof by induction from the classical trisecant lemma | statement read through a fetch (ar5iv); the journal version (Forum Math. 2001, from memory) not checked |
| Curto–Fialkow (flat extensions of moment matrices); Laurent's survey on sums of squares and moment matrices | a positive moment matrix with a flat extension has a unique, rank-atomic representing measure | memory |
| Gardner, "Multiconnected neural network models" (1987); Baldi–Venkatesh (1987); Krotov–Hopfield, "Dense associative memory" (2016) | capacity of order `n^{p−1}` of associative memories with `p`-body interactions (single-flip stability) | memory |
| tensor decomposition: generic identifiability of low-rank tensors (Chiantini–Ciliberto; Chiantini–Ottaviani–Vannieuwenhoven) | uniqueness of the decomposition of a generic tensor of small rank among decompositions of the same rank | memory; **not searched** for the measure-theoretic statement of the torus corollary |

**Classification.**  E18: elementary; a formulation that puts E10, flat extensions and the
Geometric Inference Division's certificate under one statement, plus the observation that
the zero set may exceed the support.  E18′: elementary.  **E19(a) is a published theorem
(Baldi–Vershynin 2019) and our derivation of it is a rediscovery:** on 2026-11-26 we
proved, by revealing coordinates one at a time as Odlyzko does and using
Abbe–Shpilka–Wigderson for the first batch, that the span of the lifted conformers contains
no other lifted vertex up to `(1−ε)n²/2`; a search made before writing it up found the
theorem, with the same method, for every degree.  Nothing of that derivation is claimed.
E19(b)–(d): synthesis — the readings "ground states of an explicit `2d`-body energy,
identified among all ensembles", "pair data with a prior on the number of conformers" and
the Cover-type bound; we did not find the contrast `n²/2` (with the prior) against `2n`
(without) stated.  E19(e), C3: numerical; not searched (the literature on higher-order
associative memories counts stable patterns, not exact ground-state sets).  E20: synthesis
of the trisecant lemma with E18; for moment problems this is classical.  E20′: elementary;
the two-point statement on the torus was not searched (obligation OB16).

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

9. "Donoho Statistical estimation and optimal recovery modulus of continuity 1.25" —
   confirmed at the level of the abstract and of lecture notes.
10. "total variation bounded by sum of one-dimensional marginal deviations monotone
    likelihood ratio FKG influences" — nothing relevant to E15 (results on total variation
    between *two product measures* only).

11–16 (by the internal review ER1, 2026-11-26; sources listed at the end of
`reviews/ER1_internal_review.md`): Irmatov's restatement of Odlyzko's theorem (additive
form, event without linear dependence); the published abstract of Garamvölgyi–Gortler–
Jordán; the frameproof lemma (Fernandez–Urroz, attributing it to Boneh–Shaw); Ziegler's
lectures on 0/1-polytopes (3-neighbourliness); arXiv 1712.08286 quoting Vitushkin–Henkin as
its Theorem 3.3 (nowhere dense in `C(D)` for compact connected `D` with non-empty
interior); Fraiman–Moreno–Ransford (Heppes' theorem for `k + 1` subspaces).  Not settled
by the review: the exact hypotheses of the 1967 text of Vitushkin–Henkin; Odlyzko's
original (the PDF was unreachable); the theorem number of Garamvölgyi–Gortler–Jordán in
the journal version.

16a (by the internal review ER2, 2026-11-26; twelve sources, listed with their reading
level at the end of `reviews/ER2_internal_review.md`): Donoho's theory through Stark's
lecture notes; Peres–Winkler; body–bar global rigidity; Innocenti; the 40 poses of the
Stewart–Gough platform; extreme points of Lipschitz balls; the Poincaré inequality for
monotone Boolean functions; Strassen and Holley.  Three searches for the combined
inequality of E15 ("total variation at most the sum of marginal gaps for ordered
measures"): not found stated.

16b (for Proposition E15U, 2026-11-26).  "variance of increasing event bounded by
covariance with number of ones … non-product measure … positive association weaker
condition" and "total variation distance stochastically ordered measures hypercube
bounded by difference of expected Hamming weight necessary and sufficient condition
monotone density up-sets" — neither returned the criterion `Var(1_U) ≤ Cov(1_U, N)` for
non-product measures nor the equivalence with the bound on a first-order class; nearest:
Harris/FKG for product spaces; van den Berg–Gandolfi on covariances of binary FKG
variables; a 2026 preprint on total variation between Bernoulli products by Hamming
slices.  For product measures the criterion is the Poincaré inequality for monotone
Boolean functions (item 16a).  Classification of E15U: new (not found); elementary.

17. "Abbe Shpilka Wigderson Reed-Muller codes random erasures … linearly independent" —
    found; abstract and introduction fetched (Theorem 1.3).
18. "span of random rank-one sign matrices … contains no other … Odlyzko" — found
    Baldi–Vershynin (the theorem we had just re-derived); PDF text extracted and read.
19. "Chiantini Ciliberto generalized trisecant lemma …" — the statement is Corollary 1.3
    of Chiantini–Coppens (fetched); a real version exists (Ranestad–Seigal–Wang 2024,
    not read).

Not searched yet (obligations): quantitative Heppes (to compare with O4); "random faces of
the cut polytope" (O1); identifiability of secant varieties of measurement varieties (O5);
the literature on maximum-occurrence and ensemble refinement in structural biology for a
uniqueness theorem of the form E7.
