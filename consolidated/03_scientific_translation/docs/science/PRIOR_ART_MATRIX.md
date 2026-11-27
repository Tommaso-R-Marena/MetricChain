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
| addendum A17 — certification cost against a sampleable model as a function of the a-priori divergence bound (floor = `D_∞`; Rényi order `p`; Kullback–Leibler; moments of the energy insufficient); product and chain references; the Bennett bracket | **classified at checkpoint 39 (workstream A3).**  The cost table without a hint: **(1) in print** — Block–Shetty, arXiv:2602.23535 (Feb 2026), Theorems 5, 8, Propositions 1, 2; the Rényi rows earlier (Kunsch–Novak–Rudolf 2019; Bubeck–Cesa-Bianchi–Lugosi; Devroye et al.).  With a hint (A17.2): **(2) direct corollary** (their Theorem 6 re-read).  A17.5(ii) (no polynomial moment of the remainder suffices): **(3)**, not found stated.  A17.6 (product reference): **(2)**, and sharpened by A3 to `D_p ≤ Σ[(p−1)c_i²/8 + L(c_i)] ≤ pK/8` (Cesar–Rogers, arXiv:2004.07223, Lemma 3.2; Bun–Steinke, arXiv:1605.02065, Lemma 2.2).  A17.7 (Bennett bracket): the inequality and its extremal law **(1)** — Hoeffding 1963, Theorem 3, (2.8)–(2.10); its use as a certified second-order bound for free-energy perturbation **(4) not found**, with Decoster (J. Phys. A 37 (2004) 9051) unread.  A17.8 (chain reference): **(1)** — Chazottes–Collet–Külske–Redig, arXiv:math/0503483, proof of Theorem 1; Kontorovich–Ramanan 2008, Theorem 1.2.  The theory division's box-class statements (a)–(e): (a) **(1)** Hoeffding 1963 / Specht's ratio; (b) **(2)** K\* stopping criterion (Georgiev–Lilien–Donald 2008, Proposition 3); hinted cost **(2)**, and **(4)** as a theorem on hinted query complexity; unhinted bracket **(1)** (Liu–Fisher–Ihler 2015, Corollary 3.2) | the instance-wise two-sided statement with a hint in the query model (theirs); the reading of the table as a verification cost; the measurements on force-field instances (ours) | `A3_REPORT.md` (47 sources read in the relevant passages; 20 passages re-read by the coordinator); SCI-RES-0009  *Added 2026-11-26:* Block and Shetty is published — "Partition Function Estimation under Bounded f-Divergence", Proceedings of the 39th Conference on Learning Theory, PMLR 336:760–790, 2026 [search result and proceedings page title; the published version not opened; our reading was of arXiv:2602.23535v1] |
| workstreams P3, P5, P6 — a *certified* sandwich of banded pairwise models for a generalized-Born solvent term in rotamer variables; the lower bound for bounds that ignore the signs of the charges (P5) | measurements and paper proofs; **no novelty claimed** (the searches of P2, P3 and P5 are at abstract and snippet level) | **in print:** pairwise decomposition of MM/GBSA energies for protein design, with the decomposition error assessed *numerically* — Gaillard & Simonson, *J. Comput. Chem.* 35 (2014) 1371–1387, doi:10.1002/jcc.23637; Gaillard & Simonson, *J. Chem. Theory Comput.* 13 (2017) 4932–4943, doi:10.1021/acs.jctc.7b00202 (the GB term "is affected by pairwise decomposition errors when all positions are designed together"); an "exact decomposition of the GB term" for a GB variant with a fluctuating dielectric boundary — Gaillard, *J. Phys. Chem. B* 129 (2025) 10699–10710, doi:10.1021/acs.jpcb.5c03662 **[abstracts read by the coordinator through PubMed, 2026-11-26]**; Archontis–Simonson 2005 (row above).  At snippet level only, from workstream P5's search and not verified by the coordinator: charge-group truncation of electrostatics; the cut norm and Grothendieck's inequality (Alon–Naor) for maxima of quadratic forms over sign vectors.  **Not found at this level:** rigorous bounds on the decomposition error of a GB term; the sign-blind formulation | `workstreams/P5_REPORT.md` §5 and coordinator's note item 6; `P3_REPORT.md`; SCI-MSG-0024 |

## D. What would survive a hostile referee (our judgment, with its limits)

1. **G20/G21 with G18** — the pair of exact exponents; its non-trivial half is the adaptive
   upper bound, whose cost proof **has now been re-derived outside the theory division
   (workstream R6, SCI-REV-0007: it stands; eight minor points; a certified finite-`n`
   separation from non-adaptive algorithms from `n = 1400` on at `u = 1`)**.  It must be
   positioned against the confirmation phase.
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

## E. Addendum, 26 November 2026: statements of the three new divisions that this division checked (index only)

*Version 1 above covers three branches and is otherwise unchanged; a full second version is owed.  The rows
below point to the reviews; reading levels are there.*

| statement (division) | class our search supports | closest prior art | where |
|---|---|---|---|
| Theorem L — global stability of order `n²` from distances of sequence separation at most 4 (Geometry, `288b2de`) | **(3)/(5)**: known in a different setting, the transfer not found in print; not a new mechanism | geometric rigidity in thin rods (Mora–Müller 2003; Blanchard–Griso); lattice lemmas (Alicandro–Lazzaroni–Palombaro; Schmidt–Zeman); the one published *global* bound for this graph is exponential (Arias-Castro–Vishwanath); first-order polynomial bounds in print (Daitch–Spielman; Kyng et al.; Lew et al.) | SCI-REV-0023; `workstreams/A4_REPORT.md` |
| Theorem L in its threshold-free form — a global bound for every second configuration, from five-point windows with complete distances (Geometry, `9f164f9`) | **not found in print in a short search** (ten addresses, seven works, five queries; the review databases and a citation chase of the one-window lemma not reached) — a statement about the search | the one-window ingredient without a threshold is in print: Tu–Boczar–Simchowitz–Soltanolkotabi–Recht 2016, Lemma 5.4 (read in the passage; verified by the coordinator); the published global bound for this graph has a threshold and an exponential worst-case constant (Arias-Castro–Vishwanath, Theorems 2.1 and 3.1, read in the passages); clique-based facial reduction with a local, non-explicit robustness statement (Drusvyatskiy–Krislock–Voronin–Wolkowicz, Theorem C.5) | SCI-REV-0028; `workstreams/R27_REPORT.md` §5 |
| Theorem K(a) — every configuration has a first-order constant of order at least `n/K^{3/2}` (Geometry) | **(1)**: a corollary of printed statements (no novelty claimed by them) | Lew–Nevo–Peled–Raz 2023, Theorem 1.6 and Proposition 7.7; Presenza et al. 2022; Jordán–Tanigawa for the plane | the same |
| other statements of the new divisions reviewed for correctness, with prior-art findings inside the reviews | see the reviews | — | SCI-REV-0019 (Complexity: the hardness note), SCI-REV-0021 (Geometry: Theorems B, B′, G — one of them known in dimension one, as they record), SCI-REV-0020 (Ensemble), SCI-MSG-0033 (a threshold rule of ours and theirs is in print) |

## F. Addendum, 26 November 2026 (checkpoint 68): rotamer discretisation, exact side-chain optima, certified optimisation — what this division verified today, and its search log

*Written with SCI-REV-0026 (our review of the Structural Biology division's first checkpoint).  Reading level
of every row: **abstract, through the PubMed record**, unless stated; no paper was opened.  The search was
bounded and is logged below; a limited search that finds nothing certifies nothing.*

| statement | source (reading level) | what it bears on |
|---|---|---|
| the minimum over rigid rotamers and the minimum over energy-minimised conformations "are likely to be different" | Georgiev, Lilien, Donald, *J. Comput. Chem.* 29 (2008) 1527, doi:10.1002/jcc.20909 | our addendum A17 (26), item 100 — **established before us**; line 2 of every budget of a rigid-rotamer result |
| in 69 core redesigns a continuous-rotamer model finds, in nearly all, a different and lower-energy answer than rigid rotamers; more rigid rotamers were never better; a dead-end elimination with a guarantee for continuous rotamers | Gainza, Roberts, Donald, *PLoS Comput. Biol.* 8 (2012) e1002335, doi:10.1371/journal.pcbi.1002335 (a design study; cited for the discretisation only) | the same; the incumbent for a provable minimum that is not a table artefact |
| energetics of off-rotamer conformations; discrepancies between predicted and observed fractions largest for leucine | Petrella, Karplus, *J. Mol. Biol.* 312 (2001) 1161, doi:10.1006/jmbi.2001.4965 | strain of library rotamers |
| the global optimum of a standard energy function improves side-chain accuracy by less than 0.1 % over simulated annealing; learned weights 72 % → 78 %; an extended library with learned weights 82.6 %; the global optimum found for about 85 % of a benchmark set by a relaxation | Yanover, Schueler-Furman, Weiss, *J. Comput. Biol.* 15 (2008) 899, doi:10.1089/cmb.2007.0158 | whether a certified optimum changes a conclusion (it changes none about accuracy); found first by the Frontier Benchmarking division at snippet level |
| side-chain conformational entropy of whole proteins on fixed backbones by Monte Carlo | Zhang, Liu, *PLoS Comput. Biol.* 2 (2006) e168, doi:10.1371/journal.pcbi.0020168; DuBay, Geissler, *J. Mol. Biol.* 391 (2009) 484, doi:10.1016/j.jmb.2009.05.068 | uncertified precedents for free energies of side-chain ensembles |
| learned side-chain packers reported better than SCWRL4, FASPR and the Rosetta packer | Misiura et al., *Proteins* 90 (2022) 1278, doi:10.1002/prot.26311; McPartlon, Xu, *PNAS* 120 (2023) e2216438120, doi:10.1073/pnas.2216438120 | the context of any side-chain placement comparison |
| no proof logging for cost-function-network solvers | **not found** in: the developers' four-page description of toulbar2 for the 2025 pseudo-Boolean competition (full text searched for "proof", "certif", "VeriPB": no occurrence); M. J. McIlree, *Pseudo-Boolean proof logging for constraint propagation algorithms*, PhD thesis, Glasgow 2026 (258 pages; extracted text searched for "cost function", "weighted CSP", "WCSP", "soft arc", "toulbar", "weighted constraint", "soft constraint": no occurrence; the thesis was not read); two web queries | agrees with the bounded searches of the Structural Biology, Theory and Frontier Benchmarking divisions; **four bounded searches are not an absence** |
| necessary optimality under interval data: a solution is optimal in every scenario iff it is optimal when its own elements are at their upper ends and all others at their lower ends | **from memory** (interval-data combinatorial optimisation); nothing opened | the construction of SCI-REV-0026 §4; no novelty claimed; tested by brute force (`experiments/science/software_evaluation/necessary_optimality_check.py`) |
| weighted model counting of factor graphs with one variable per table entry | **from memory** (Chavira and Darwiche, *Artif. Intell.* 172 (2008)); not opened | "checkable enclosures of Boltzmann-weighted sums" are reachable by composing published tools |

**Search log (2026-11-26, about 23:15–23:30 UTC).**  PubMed queries (author and title words): "Gainza Donald
continuous rotamers"; "Georgiev Donald minimized dead-end elimination"; "Petrella Karplus off-rotamer"; "DuBay
Geissler side-chain torsional entropy"; "side-chain conformational entropy of proteins, Liu JS"; "McPartlon
Xu side-chain packing"; "DLPacker"; "Yanover Weiss minimizing and learning energy functions side-chain
prediction" — eight queries, eight records read.  Web queries: "proof logging cost function networks weighted
CSP soft arc consistency certified optimality VeriPB"; "toulbar2 proof logging certificate of optimality
branch and bound cost function network 2026".  Two documents downloaded and searched by term (above).
**Not reached:** the papers themselves; the OSPREY literature after 2012; any search for the construction of
addendum item 101 (b) (cell free energies with a certified upper end); any search for certified robustness of
side-chain optima.
