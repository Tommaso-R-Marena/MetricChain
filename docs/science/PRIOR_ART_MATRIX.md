# Prior-art matrix and originality classification

*Science division.  Version 1 (2026-11-25).  One table for everything the three branches
claim, with the class our searches support and where the evidence is.  **This file is an
index.**  Reading levels — full text, abstract, search snippet, from memory — are
recorded source by source in the reports named in the last column and are not repeated
here; nothing in this file should be cited without going to them.  "Not found" means not
found in the searches logged there; it is never a claim of novelty.*

Classes (as in `workstreams/A1_REPORT.md`): **(1)** established prior art · **(2)**
reformulation of known results · **(3)** known special case exists · **(4)** plausibly
original generalisation · **(5)** new combination of known elements · **(6)** plausibly
original theorem · **(7)** plausibly original capability · **(9)** unresolved.

## A. The theory division's query-complexity results

| claim (theory report row) | class | closest prior statements | evidence |
|---|---|---|---|
| G20/G21 — the adaptive exponent without a hint equals the hinted one, with a matching algorithm that needs neither log-concavity nor a sampler | **(6)** | concept precedents: Mathé–Novak 2007 (adaption helps on a non-symmetric class); explore-then-verify in pure exploration (Karnin 2016; Garivier–Kaufmann 2016); and, as a *principle*, the confirmation phase of sequential design and feedback coding (Chernoff 1959; Burnashev 1976; Yamamoto–Itoh 1979; stated for noisy search by Kaspi–Shayevitz–Javidi 2016) — with a different law | `A1_REPORT.md` §4.1, §9.2(d); SCI-REV-0004; SCI-RES-0003 |
| G18 — Monte Carlo is exponent-optimal among non-adaptive algorithms; `θ_na`, `a` | **(3)** | the formulas at the cone are the published freezing/bias formulas of the Jarzynski estimator in the random energy model (Suárez–Silbey–Oppenheim 2012) and the Chatterjee–Diaconis threshold (2018); method of the lower bound: Mathé–Novak.  Not found: minimaxity over the class | `A1_REPORT.md` §2.2, §4.2 |
| G11 — the threshold `n ln cosh(βc/2)` | **(5)** | the number is in print at the cone; its role as a sharp threshold was not found | `A1_REPORT.md` §4.8 |
| G22 — a field: flat histogram, hardest additive instance | **(4)** | capacity-achieving output law / universal mixture; isoperimetry of Ahlswede–Zhang and Yu by their method | `A1_REPORT.md` §4.3 |
| G23 — shear law; game-function pair | **(2)** | exponential change of measure; Neyman–Pearson identity; Forney's `E_2 = E_1 + T` | `A1_REPORT.md` §4.4, §9.2(b); `R5_REPORT.md` §7 |
| G25 — known parts that are functions of the type | **(2)** / **(9)** | invariance principle of design theory (Kiefer) with Bakhvalov averaging; shells unresolved | `A1_REPORT.md` §4.5 |
| G26 — two rounds lie strictly between a fixed sample and full adaptivity | **(6)**, conditional on G20/G21 | round hierarchies and the coupling device are standard (property testing; parallel optimisation; parallel log-concave sampling 2024–2026); none treats the exponent of a normalising constant by value queries; the separating mechanism (dilution) is distinctive | `A1_REPORT.md` §4.6; `R4_REPORT.md` §10 |
| G27 — Lemma 11.89 (odds ratio and mutual information) | **(1)** | Hasenclever–Scholz, arXiv:1302.6161, Proposition 8(a) | `A1_REPORT.md` §2.1; `R1_REPORT.md` §10; adopted by the theory division at `40c5bd7` |
| Theorem 11.99 — the channel-coding dictionary | **(2)** | identities: Csiszár; van Erven–Harremoës; Nakiboğlu (Definition 13 verbatim).  Mechanism: glassy phase of the random code ensemble (Merhav 2009); Jarzynski bias; Hoeffding's trade-off against product alternatives (Tomamichel–Hayashi 2018) | `A1_REPORT.md` §9; SCI-RES-0003 |
| Proposition 11.103(e) — "about `e^{u/2}` states" | **(5)** | cutoff-rate design of modulation alphabets is classical; the optimum `k = e^{u/2} + 1` and the reflection identity were not found | `A1_REPORT.md` §9.4 |
| Theorem 11.105 (theory report §11.28 at `dcdfea6`) — the robust range of a ratio of two macrostate weights is a transport problem with gains from `B` to `A`; closed pairs | **(4)** for the theorem, **(2)** for the dual | for a *separable* envelope the cone is the density-ratio class and the value is the classical range of a posterior odds (DeRobertis–Hartigan 1981; Geweke–Petrella 1995 for posterior odds); flows with gains (Jewell 1962); the same cone in metric differential privacy (Chatzikokolakis et al. 2013).  Not found: metric envelopes, the reduction to `B → A`, closed pairs.  Unresolved leads: credal sets from comparative probabilities with ratio bounds; log-Lipschitz cones of the Birkhoff method (from memory) | SCI-RES-0005 §2 (six searches, summaries only, no full text) |

## B. Kernels, certification geometry, chains

| claim (row) | class | closest prior statements | evidence |
|---|---|---|---|
| E1 — pairwise kernel with dead-end elimination, machine-checked | **(7)**, narrow | every rule is known; no proof logging for cost-function networks / MAP found; verified pseudo-Boolean proof checking (CakePB; Koops et al. 2025) now within a factor 20 of solving, importable into Lean 4 (PBLean 2026) | `A2_REPORT.md`; SCI-REV-0006 |
| E1 — residual kernel, valid for a whole envelope class | **(7)** | no proof-logging system found certifies a statement about a *class* of instances | SCI-REV-0006 |
| D3 — partition-function kernel | **(5)** | verified model counters exist beyond exact counting | SCI-REV-0006 (W1) |
| D4 — voxel-integral enclosures | **(7)**, elementary | "provable" in the protein-design literature is a paper proof relative to the model | SCI-REV-0006 |
| G1 — certificates are coverings | **(2)** | certified Lipschitz optimisation | SCI-REV-0006 |
| G4 — dichotomy and rate–distortion exponent | **(6)** (an application of type covering) | none from 2022–2026 found | SCI-REV-0006 |
| G7 — finite-temperature exponent | **(3)** | Merhav 2011, an example | SCI-REV-0006 (W7) |
| G13 — normal form | **(2)** | weightable quasi-metrics / partial metrics | SCI-REV-0006 |
| G16 — lever-arm law | **(3)** | reduced moments of inertia; a published certificate in robot motion planning (Schwarzer–Saha–Latombe 2005) | SCI-REV-0006 (W6) |
| G19 — linear classes; profile envelope | **(1)**; **(2)** | optimal recovery; the second lower bound of the Gromov–Wasserstein distance, whose zero set is homometry | SCI-REV-0006 (W3) |
| G24 — "Fekete for sets"; limit shape of lattice bridges | **(3)/(2)**; **(4)** | Newton–Okounkov bodies of graded semigroups; the lattice application not found | SCI-REV-0006 (W8); SCI-REV-0002 |
| C4 — torsion → RMSD closed form | **(6)**, elementary | planar weighted Procrustes residual | SCI-REV-0006 |

## C. The science division's own results

| claim | class | closest prior statements | evidence |
|---|---|---|---|
| identified sets from averaged data (model-free; divergence ball) | **(1)** | generalised moment problem; maximum occurrence, maxOR/minOR in NMR (2005–2014); Christensen–Connault 2023; optimal uncertainty quantification | `SM_REPORT.md`; SCI-MSG-0002 |
| identified sets over an envelope class intersected with data; flow-with-gains certificates | **(5)** | density-ratio classes of robust Bayes; no treatment with moment constraints found | `SM_REPORT.md` K6 |
| Theorem 8 — data certify a lower bound on model error | **(1)** for the quantity (extent of falsification); certified numbers for molecular models not found | Masten–Poirier; Christensen–Connault | SCI-MSG-0003 |
| Lemma 1, Theorem 2(a,b), Theorem 3 | **(1)** / textbook | orthogonal arrays; `k`-wise independence; Rao's bound; maximal mass functions; Albanna et al. 2017 for the unrestricted class | `SM_REPORT.md`; `R3_REPORT.md` §6 |
| Theorem 2 inside a Gibbs class with bounded energy differences; entropy price `⌊k/2⌋ ln n` | **(5)** | not found | `SM_REPORT.md`; `R3_REPORT.md` R2 |
| Theorems 4, 4′, 4‴, 4-τ, Proposition 5b — what averaged and thermodynamic data are worth to a query algorithm ("oracle invariance") | **(6)**, short | value-of-information theorems of this kind not found; the code mechanism is textbook; statistical-query literature only spot-checked | `SM_REPORT.md`; `R3_REPORT.md` §6; addendum A12 |
| Theorem 7 — stability of maximum-entropy refinement | **(3)** | mechanism: Barron–Sheu 1991; the cancellation of the feature part and the sharp constant `tanh(βω/4)` not found | SCI-MSG-0003; `R3_REPORT.md` R1 |
| addenda A11, A13 — the stochastic sandwich for robust macrostate ratios | **(5)**, probably folklore in statistical mechanics | Holley 1974; monotonicity in a field; the sandwich for arbitrary bounded-difference perturbations and its use for robust ranges not found in one search | addendum A11, remark (4) |
| addendum A16 — with a mean-energy datum: entropy bracket `n·h(σ_u) ≤ S ≤ n ln 2`; free accuracy `KL(σ_u‖½)` against `KL(½‖σ_u)`; plateau twin | **(5)**, not searched | ingredients are textbook (`ln Z = S − βU`; chain rule; the perturbation bracket of free-energy calculations); as a statement about the value of a datum to a query algorithm: **no search made** | addendum A16; author only |
| homometric lattice chains; Debye intensities in the profile class | **(5)**, simple | Patterson homometry; Boutin–Kemper (generic point sets, does not apply to chains) | `A2_REPORT.md` |
| certified kinetics: cut certificates; robust barrier interval; covering characterisation | **(2)** for the principles (Edmonds–Fulkerson; Aldous–Fill; Dirichlet/Thomson); **(5)** for the composition and K3, K5–K7, K14; PSPACE obstruction = Wrochna's theorem read as a barrier statement | no certified or machine-checked barrier or rate bound found in twenty searches (several at snippet level) | `SK_REPORT.md` §4 |
| polytope against ellipsoid: certificate iff power function below gap; two-sided design bound; no free hedging; LP-funnel slope | **(2)**/**(5)**: nearly every ingredient known (hypercircle; fractional-factorial posteriors; finite-order weights; kernelised optimism) | the two-sided sup-norm design bound on `𝔽₂ⁿ`, `h((1−ρ)/2)`, the `ln Z` interval, the LP-funnel slope not found — abstracts and snippets only | `SX_REPORT.md` §4 |
| class constants of a solvation term per torsion; sup/RMS gap | measurement, not a claim of novelty | known: GB is not pairwise and an expansion in Born radii repairs most of it (Archontis–Simonson 2005); tuple expansions in rotamer variables (LUTE) | `SP_REPORT.md` §4 (six abstract searches) |
| Proposition A1.1 / A1.2 — a product sampler attains the capacity at bounded accuracy for every `n` | **(5)** | chain rule, convexity, Azuma; the `e^{KL}` rule of importance sampling | `A1_REPORT.md` §2.5, §9.3 |

## D. What would survive a hostile referee (our judgment, with its limits)

1. **G20/G21 with G18** — the pair of exact exponents; its non-trivial half is the adaptive
   upper bound, whose cost proof nobody outside the theory division has re-derived
   (workstream R6 is doing so).  It must be positioned against the confirmation phase.
2. **G26** — the two-round separation, reviewed by us (SCI-REV-0003): stands, conditional
   on item 1 for its reading.
3. **The residual kernel** as a capability (class-wide certificates), if its advantage over
   pseudo-Boolean proof logging is measured.
4. Of ours: the oracle-invariance statement (as a companion of item 1) and the measured
   class constants (as the empirical keystone of any applied claim).

*Limits of the whole matrix:* searches were made by language-model agents with web
search and page fetching; publishers' full texts were often not accessible; several
classical sources (Novak 1988–1996; Harper 1966; Kiefer 1959; Chernoff 1959; Burnashev
1976; Betrò–Guglielmi) were cited through papers that describe them.  The lists of what
was *not accessed* are in `A1_REPORT.md` §4.10 and §9.5, `SM_REPORT.md`, `A2_REPORT.md`.
