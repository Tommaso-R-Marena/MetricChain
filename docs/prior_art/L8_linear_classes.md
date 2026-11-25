# L8 — Classes that are linear in features; pair-distance profiles (theory report §11.17)

Compiled in cycle 10 from the search logs of workstream P (`workstreams/P_REPORT.md`, §4: sixteen
searches, one full-text extraction) and of the sixth referee (`reviews/R6_referee_report.md`, §4
and Q6).  The coordinator read none of these sources; the column "read by / depth" says what
was read by whom.  Nothing here was read in a printed original.

| statement in §11.17 | what it is | source | read by / depth | verdict |
|---|---|---|---|---|
| Theorem 11.47(b), worst case over the data: the bracket half-width is the dual-norm distance to the span, attained by an affine rule at the zero information | optimal recovery of a linear functional from linear information on a balanced convex set | Smolyak (1965, thesis); Micchelli & Rivlin (1977); Traub & Woźniakowski (1980); Sukharev for classes that are not symmetric | P, R6: search summaries (papers of Foucart–Liao citing Smolyak and Micchelli–Rivlin); originals not read | **known**; the first version of §11.17 attached Smolyak's name to the data-dependent range, which is plain linear-programming duality (R6, m2) |
| Theorem 11.47(b), given data: the exact range as two linear programs | feasible-parameter-set intervals of set-membership (unknown-but-bounded) estimation; robust counterpart of a linear program with box uncertainty | Milanese & Vicino, Automatica 27 (1991); Soyster (1973); Ben-Tal & Nemirovski | P: search summaries | **known** |
| Theorem 11.48(a): a pair-additive energy is linear in the pair-distance histogram | the energy equation; in discretised form the feature map of linear ("LP") contact potentials | Maiorov & Crippen, J. Mol. Biol. 227 (1992) 876; Tobi, Shafran, Linial, Elber, Proteins 40 (2000) | P: summary/abstract of Maiorov–Crippen; R6: could not open Maiorov–Crippen (HTTP 403), read Tobi et al. pp. 71–73, which credit Maiorov–Crippen with the first use of inequalities over decoys and use contact counts per type and distance segment as linear features | **known**; Tobi et al. is the closer reference for the features |
| Theorem 11.48(b): `L¹` distance of cumulative distance counts = Wasserstein-1 distance | Kantorovich–Rubinstein duality on the line; the cutoff as a boundary reservoir | Figalli & Gigli (2010) for the reservoir | P, R6: search summaries | **known** mathematics |
| the same distance as a structural dissimilarity | earth mover's distance between shape distributions; sorted pair descriptors compared in `ℓ¹` | Osada, Funkhouser, Chazelle, Dobkin, ACM TOG 21 (2002), p. 815, footnote 1; Hansen et al., J. Phys. Chem. Lett. 6 (2015) ("bag of bonds"); several 2021–2026 papers using `W₁` between radial distribution functions | R6: Osada et al. footnote read; bag of bonds through a full-text summary; the others as search summaries; P: abstracts | **known as a score**; its reading as the exact envelope (support function) of the class of unknown Lipschitz pair potentials next to a known part was **not found** and is immediate |
| Proposition 11.49(a): metric entropy `≍ 1/δ` of bounded monotone functions in `L¹` | classical | Birman & Solomyak (1967); van de Geer (1991; 2000); van der Vaart & Wellner, Thm 2.7.5; Gao & Wellner (2007) | P, R6: secondary sources only — which is why the proposition is proved in the report with its own constant | **known**; the application is immediate |
| Proposition 11.49(b), continuous distances: polynomially many span evaluations | greedy reduced bases against Kolmogorov widths | Binev, Cohen, Dahmen, DeVore, Petrova, Wojtaszczyk (2011); DeVore, Petrova, Wojtaszczyk, Constr. Approx. 37 (2013), arXiv:1204.2290, Cor. 3.3(ii) (Hilbert space, exact greedy: `d_n ≤ C₀ n^{−α}` implies `σ_n ≤ 2^{5α+1} γ^{−2} C₀ n^{−α}`) and Cor. 4.2(ii) (Banach space: rate `n^{−α+1/2+β}`) | P: statements extracted by a tool from the ar5iv full text, PDF not read; R6: tool summary | **known** theorem; **the corollary was not read by a person in this project** — the two derivations (P, Theorem 8; R6, Appendix C) agree with each other |
| coefficients as a measure of extrapolation | D-optimality / MaxVol active learning for potentials that are linear in features; "extrapolation grade" `max_k |C_k|` | Podryabinkin & Shapeev (2017), arXiv:1611.09346 | R6: full text through a fetch tool (quotations in its Q6); P: summaries | **known**; the grade is the `ℓ^∞` size of the multipliers of Theorem 11.47(b), the transport term of (d) a weighted `ℓ¹` size |
| Theorem 11.47(d): remainder in sup norm → `ℓ¹`-penalised regression | optimal recovery with noisy information | not located in this exact form | P | certainly known in that literature (P's assessment) |
| the pair potential is determined by the pair distribution | Henderson's theorem (1974) | — | P: search summaries | context only |
| general setting: a utility linear in unknown parameters constrained by queries, minimax regret | decision theory | Boutilier et al. (2006) | R6: abstract | context only |

Not searched by anyone (stated by P): optimal recovery for *nonlinear* functionals such as a
minimum over a known part; Lebesgue constants of `L¹` greedy bases; the statistical-mechanics
literature on realisable pair-correlation functions.

Assessment (R6 and P, accepted).  Known: Theorem 11.47(a)–(c), 11.48(a), the duality of
11.48(b), the entropy behind 11.49(a), the greedy theorem behind 11.49(b).  Routine: 11.47(d)
with one transport plan, 11.49(b) on lattices.  Not found in print and immediate once named:
the profile distance as the exact envelope of a residual class next to a known part; the
count of evaluations that follows; certificates of a linear class for a minimum as covers by
subspaces with asymmetric gauges (workstream P, Theorem 4); the constant / polynomial /
exponential trichotomy of the three formats on lattices (P, Theorem 6); the lower bound "one
evaluation per torsion" for the span format of pair-specific classes (P, Proposition 12 —
an application of the classical width of a box in `ℓ¹`, see below); the statement that the
slack of a linear part plus a first-order remainder is at least the sum of the two slacks
(P, Corollary 15).

**Addendum (review of workstream P, `reviews/R_P_review.md`).**

| statement | where it is known | read how |
|---|---|---|
| Corollary 3.3(ii) of DeVore–Petrova–Wojtaszczyk (weak greedy algorithm in a Hilbert space: `d_n ≤ C₀n^{−α}` implies `σ_n ≤ 2^{5α+1}γ^{−2}C₀n^{−α}`), used in Proposition 11.49(b) | arXiv:1204.2290v1 | **read in full by the reviewer** (12 pages); quoted correctly; the printed proof covers indices `≥ 4` only, which does not matter here; journal version (Constr. Approx. 37, 455–466) not read |
| greedy choice of evaluation points for worst-case recovery, analysed through Kolmogorov widths with that theorem | the `P`-greedy algorithm of kernel interpolation: Santin & Haasdonk, arXiv:1612.02672 (2017) | machine summary of the full text; this is the direct precedent of workstream P's Theorem 8 and was not cited by it |
| width of a box in `ℓ¹`: `d_m(B_∞^n, ℓ_1^n) = n − m` (Lemma 11(c) of workstream P, listed there as apparently new) | Pietsch (1974), Stesin (1975) | search summaries (later papers stating the theorem with this attribution) |
| the consistent set and the width of its bracket at a point | version space and its width; eluder dimension (Russo & Van Roy 2013) | from memory and a search summary; context only |
| Podryabinkin–Shapeev: `C = b(x*)A^{−1}`, grade `max_k |C_k|` | arXiv:1611.09346 | machine summary of the full text; the description in §11.17 is accurate |

Not read by anyone in this project, attributions from memory: Smolyak (1965), Micchelli–Rivlin
(1977), Traub–Woźniakowski (1980), Bakhvalov, Gal–Micchelli, Soyster (1973), Henderson (1974),
Figalli–Gigli (2010), Tobi et al. (2000), Birman–Solomyak (1967).
