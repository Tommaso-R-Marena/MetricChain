# Workstream A2 — running notes (prior art and originality: kernels, certification geometry, chains)

Started 2026-11-25 17:40 UTC.  Rule: this file is updated after every step.

Reading-level tags used throughout: `[full text]`, `[abstract]`, `[search snippet]`,
`[from memory — unverified]`.  Epistemic labels: [V] [P] [K] [N] [C] [H].

## Step 0 — orientation (17:40)

* Read `docs/science/workstreams/COMMON.md` [full] and `A2_brief.md` [full].
* Created `experiments/science/ws_A2/`.
* Claims to test: (1) E1/D3/D4 kernels; (2) G1, G4, G7; (3) G13; (4) G16; (5) G19; (6) G24; (7) C4.
* Next: README, THEORY_REPORT §0.2, §6.4, §10 rows, §11.14/§11.17/§11.22, §13; prior_art L1…L8.

## Step 1 — reading the repository statements (17:45–18:05)

Read [full]: README.md; THEORY_REPORT §0.2 (rows A1…E2), §3.4, §4.4 (Thm 4.6, Cor 4.7 + prior-art
paragraph), §6.1–6.4, §10 table (G1–G27 + "honest reading"), §11.1–11.6, §11.11, §11.14, §11.17.

Exact claims under test (as worded in the repository):
* E1 (§0.2): "no *native* verified checker for cost-function-network / MAP / DEE certificates found; such runs can
  in principle be encoded as pseudo-Boolean proofs and checked with existing verified checkers" ; §6.4: "Neither
  OSPREY nor toulbar2 emits checkable proofs, and no verified checker for cost-function-network / MAP lower
  bounds, DEE steps or approximate partition-function bounds was found".   <-- TEST AGAINST 2023-2026 CFN proof logging.
* D3: "verified checkers exist for exact model counting only; this rule set: no match found".
* D4: "rigorous voxel-integral bounds inside a provable design algorithm: no match found".
* D1: thermal DEE as a certificate rule for partition functions: no match found.
* G1: "reformulation of a known notion ...; the slack form with a known part and an asymmetric envelope was not found".
* G4: "no match found; an application of the type covering lemma".
* G7: "exponent formula is a corollary of Merhav's (2011) theorem...; the identification ... no match found".
* G13: "elementary (Johnson reweighting, min-plus adjointness); the packaging for certification apparently new".
* G16: "lever-arm effects are folklore in molecular modelling, the quantitative consequences for certification were
  not found (no literature search was possible in the review)".
* G19: "the linear theory is known ...; its reading as the exact envelope of a residual class next to a known part,
  and the consequences for certificates, were not found; none of it is deep".
* G24: "limits of supermultiplicative models and the cluster method for lattice-gas ground states are known; ...
  the limit shape for this model, the stability lemma and the numbers were not found".
* C4: "small-angle content classical (Pitzer–Gwinn; Eckart); finite-angle closed form and chained bound: no match found".

## Step 2 — reading the existing prior-art checks (18:05–18:25)

Read [full]: L1 §0, §C3, §C4(i),(ii), §C5, §6–8; L2 §C8(a)–(e) + cross-cutting + limits; L3 §C13;
L4 §0, §1 (K1–K11), §C1, §C2, §C4, §C5, §C9, §10–12; L6 §T6–T8, §9–12; L8 (all); S_REPORT §3.3 remarks, §5.5, §10, §11.
Not re-read: L5, L7 (A1's territory), L4 C3/C6/C7/C8.

What the earlier checks already establish (so I do NOT repeat):
* L1 C4(ii): landscape VIPR / VeriPB / CakePB / PBLean / LeanVIPR / certified MaxSAT B&B (Vandesande–Coll–Bogaerts AAAI'26) /
  Bryant et al. Lean4 CPOG / MICE; toulbar2 user guide + PB25 description list no proof logging (checked to mid-2025);
  explicitly says "a 2026 preprint on the subject could still exist".  <-- my first target.
* L2 C8(b): K*/BBK*/MARK* bound a sum of *minimised* energies; MARK* main text read; supplement not read.
* L3 C13: Pitzer–Gwinn, Popov–Grudinin one-body formula, Kudin–Dymarsky, DiffDock Prop 1, Go–Scheraga, Noguti–Go, Wang–Chirikjian,
  TFD; "a rigorous lever-arm scaling theorem ... was not found".  Robotics dynamics (joint-space inertia matrix) NOT searched.
* L4/L6: Hansen–Jaumard–Lu (abstract only), Bachoc–Cesari–Gerchinovitz (full), Bouttier et al. (full), Baran–Demaine(-Katz) (full),
  de Montbrun–Gerchinovitz, priority k-centre, Csiszár dual, Kostina–Verdú Thm 8, Merhav 2025 Kraft, type covering (Csiszár 1998 read).
* L8: nothing read in the original by the coordinator; "Not searched by anyone: ... the statistical-mechanics literature on
  realisable pair-correlation functions".  No scattering/homometry/Boutin–Kemper/Mémoli search for G19.
* S_REPORT §10: 10 searches; Janse van Rensburg (abstract/ToC), Bennett-Wood et al. (4 pp. full), Kanamori via summaries.
  "I did not search the mathematical literature on limit shapes of ground states".

Terms absent from all repo docs (grep): weightable quasi-metric, partial metric, Randers, Newton–Okounkov, Khovanskii, Lanford,
Featherstone, Ziemian / rotation set (only in briefs), Latombe, CONAN, Debye, Torquato, unassigned distance geometry, reward shaping.
=> these are my candidate *new* prior-art relations to verify on the web.

Plan (priority order): P1 CFN/MAP/Z proof logging 2023–2026; P2 identifiability from distance profiles (Boutin–Kemper,
Mémoli–Needham, SAXS p(r), uDGP, Torquato degeneracy); P3 G24 named theorems (Okounkov bodies / Lanford / rotation sets /
Janse van Rensburg); P4 G16 lever arm (Featherstone JSIM, motion planning displacement bounds, CONAN); P5 G13 (weightable
quasi-metrics, Randers, potential shaping); P6 G1/G4/G7 follow-ups + Merhav 2011 full text + what "provable" means in OSPREY;
P7 C4.

## Step 3 — P1: proof logging / certificates for CFN, MAP, counting (18:25– )

Search log (tool: WebSearch standard unless stated; "->" = outcome)
S1. `proof logging cost function networks toulbar2 VeriPB certified WCSP soft arc consistency` -> nothing CFN-specific; surfaced
    LIPIcs.CP.2026.43, arXiv:2511.10273 (certified B&B MaxSAT, already in L1), Oertel thesis (Lund 2026), McIlree thesis (Glasgow 2026).
S2. `"cost function network" OR "weighted constraint satisfaction" certificate of optimality proof checker pseudo-Boolean proof 2025 OR 2026`
    -> nothing CFN-specific; Dold et al. ICAPS 2025 (in L1); Koops et al. CP 2025 (VeriPB+CakePB PBO toolchain, "within a factor 20
    of solving time" [search snippet]); ASE 2025 MaxSAT domain-specific certificate format [search snippet] (to read).
S3. `toulbar2 "proof logging" OR "certified" OR "VeriPB" cost function network de Givry Katsirelos 2026` -> nothing toulbar2-specific.

Read:
* McCreesh, Nordström, Oertel, Tan, "Proof Logging for Projected Enumeration (and Counting?) Problems in VeriPB", CP 2026,
  LIPIcs 379, 43:1–43:21, doi:10.4230/LIPIcs.CP.2026.43.  [full text of abstract, §1, §2 (start), §4 (start), §5, refs — PDF
  downloaded, pdftotext].  Content: VeriPB + formally verified CakePB extended to *enumeration* proofs (solution-excluding rule with
  projection onto a preserved set; strengthening/deletion kept); `output EQUIENUMERABLE` for count-preserving transformations;
  counting without enumeration is "future possibility" (hence the "?" in the title).  Quote (§4): "We remark that specialised
  certification methods are available for both exact [18] and approximate [55] model counting."  [55] = Tan, Yang, Soos, Myreen,
  Meel, "Formally certified approximate model counting", CAV 2024, LNCS 14681, 153–177, doi:10.1007/978-3-031-65627-9_8.
  ==> D3 wording "verified checkers exist for exact model counting only" is TOO STRONG as a description of the landscape:
      a formally verified checker for *approximate (PAC)* model counting exists (to be read), and since 2026 a verified checker
      for *enumeration* (unweighted) in a general-purpose proof system.  Neither is a deterministic two-sided bound on a *weighted*
      sum, so the "this rule set: no match" half may survive.  TO VERIFY by reading CAV 2024.

S4. `Tan Yang Soos Myreen Meel "Formally certified approximate model counting" CAV 2024 ...` -> arXiv:2406.11414.
    READ [abstract in full from the arXiv PDF v2; body not read]: "the first certification framework for approximate model counting
    with formally verified guarantees ... (i) a static, once-off, formal proof of the algorithm's PAC guarantee in the Isabelle/HOL
    proof assistant; and (ii) dynamic, per-run, verification of ApproxMC's calls to an external CNF-XOR solver using proof
    certificates ... certificate checker is able to fully certify 84.7% of instances".  Unweighted counting, probabilistic (ε,δ).
S5. `Py Cherif Habet "Proofs and certificates for Max-SAT" ...` -> JAIR 75 (2022) 1373–1400, doi:10.1613/jair.1.13811
    [search snippet only; JAIR page returned HTTP 502]: MS-Builder generates Max-SAT certificates "in the particular form of a
    sequence of equivalence-preserving transformations"; MS-Checker verifies them with Max-SAT inference rules.  (EPT sequences as
    native certificates — the Boolean special case of a CFN reparameterisation witness.  Not formally verified as far as the
    snippet says.)  TO READ via IJCAI 2023 extended abstract.
S6. `certified bounds weighted model counting proof checker "upper and lower bounds" certificate partition function ...` ->
    Cheng, Luo, Jiang, "Knowledge Compilation for Incremental and Checkable Stochastic Boolean Satisfiability", IJCAI 2024,
    pp. 1862–1872 (paper 206).  READ [abstract, §1, §3.3, §4 in full from the PDF; experiments skimmed]: cert-SSAT extends CPOG:
    "we relax the logical equivalence checking in CPOG into two logical implication checks to separately certify lower and upper
    bounds of SSAT satisfying probability"; pruned (unexplored) branches are replaced by ⊥ in G_l and by the explored branch in G_u;
    Theorem 5: Pr[Φ] = p if (G_l → ϕ) ∧ (ϕ → G_u) and both evaluate to p.  Checker = cpog-check (RUP); 80.5 % of solvable
    instances fully certified.  => a *two-sided* certificate scheme for a weighted count with *pruning* exists (2024), but it
    certifies exact values (bounds meet) or a lower bound; no temperature-dependent prune ratio, no ε-interval, checker for the
    implication variant not stated to be formally verified.
S7. `"proof logging" OR "certifying" "MAP inference" OR "Markov random field" ... verified checker Coq OR Lean OR Isabelle` ->
    nothing for MAP/MRF; surfaced LIPIcs.CP.2026.52 (VIPR certificates from any LP solver exposing duals/Farkas; search snippet).
S8. arXiv API: `all:"proof logging" AND (all:"cost function" OR all:WCSP OR all:"weighted constraint")` -> 0 hits;
    `all:toulbar2 AND (all:certif* OR all:proof)` -> 0; `all:"cost function network" AND all:certificate` -> 0;
    `all:"proof logging"` -> 20 hits (listed; none on CFN/MAP/partition functions; newest: 2609.20873 "The Refutation Gap"
    (Pandey, Sep 2026; DRAT-certified optimality of XOR circuits, abstract read via fetch tool), 2607.21199 "Towards a Certifying
    Grounder", 2511.16637, 2511.10273v2, 2504.18443, 2501.17493, 2404.17316, 2401.09277).  `abs:"cost function networks"` -> 4 hits, none on certificates.
S9. GitHub code search (gh api search/code): `veripb repo:toulbar2/toulbar2` -> 0; `"proof log" repo:toulbar2/toulbar2` -> 0;
    `certificate repo:toulbar2/toulbar2` -> 9 files (the `-x` "sol taken as a certificate" = a solution file).
S10. toulbar2 1.0.0 user guide (https://toulbar2.github.io/toulbar2/userdoc.html) READ [full page through fetch tool, two parts,
    2026-11-25]: only `-x` mentions "certificate" (an initial solution); no proof/VeriPB/checker option; `-logz`; `-epsilon=[float]`
    "approximation factor for computing the partition function"; `-dee` "restricted dead-end elimination".
S11. `"cost function networks" OR "WCSP" "certificate" OR "proof" lower bound "equivalence preserving transformations" ...` ->
    Dlask–Werner–de Givry (CP 2021 / Constraints 2023, super-reparametrizations; certificate of unsatisfiability of the
    active-tuple CSP from the solver's history) [search snippet]; Larrosa–Rollon arXiv:2003.02718 (MaxSAT proof systems; OSAC
    sound if weights positive at the end) [search snippet]; Montalbano et al. arXiv:2509.17706 (in L1).

INTERIM VERDICT P1 (E1): after 11 searches incl. the arXiv API and the toulbar2 code base, still NO proof-logging / verified checker
for cost-function networks, WCSP soft arc consistency, MAP/MRF LP bounds or DEE as of 2026-11-25.  The repo's E1 sentence stands.
Things to ADD to §6.4: (1) EPT-sequence certificates with an (unverified) checker exist for MaxSAT (Py–Cherif–Habet 2022);
(2) native (non-PB) MaxSAT proof logging (van Doren–Antonopoulos–Piskac, ASE 2025: "first MaxSAT-specific proof-logging framework
for core-guided OLL solvers", median verification overhead "under 2% of solve time" [abstract+intro read from the PDF]);
(3) CakePB-verified PBO within a factor 20 of solving time (Koops et al. CP 2025) — weakens "the 43× figure is the number to beat";
(4) verified approximate counting (Tan et al. 2024), verified enumeration (McCreesh et al. 2026), two-sided SSAT bounds (Cheng et al. 2024).

S12. fetched IJCAI 2023 extended abstract of Py–Cherif–Habet (https://www.ijcai.org/proceedings/2023/0787.pdf) READ [abstract in full,
    intro skimmed]: MS-Builder "generates certificates for the Max-SAT problem in the particular form of a sequence of
    equivalence-preserving transformations"; MS-Checker "able to verify the validity of any Max-SAT certificate using Max-SAT
    inference rules".  No proof assistant is mentioned (grep: no "verified"/"Coq").
S13. Hallen & Donald, "Protein design by provable algorithms", CACM 62(10) 2019, PMC6788629 READ [full text through the fetch tool;
    answers are the tool's extraction with short quotes]: guarantees are relative to the input model — "they ensure modeling error is
    the only error in protein design calculations"; voxel energy "generally the continuously minimized energy"; NO mention of
    floating-point arithmetic, rounding, interval arithmetic, proof assistants or independently checkable certificates;
    "continuous entropy" only in a footnote.  => "provable" there = a paper proof about the algorithm relative to the model,
    executed in floating point; not a per-run certificate and not machine-checked.
S14. `OSPREY ... "BigDecimal" OR "arbitrary precision" OR "floating point" ...` -> nothing on numerical precision [snippets].
S15. `interval arithmetic rigorous global optimization molecular conformation ...` -> Lin & Stadtherr, J. Comput. Chem. 2005
    (doi:10.1002/jcc.20285), "Deterministic global optimization of molecular structures using interval analysis": "a mathematical and
    computational guarantee that the molecular structure with the global minimum potential energy will be found" [search snippet];
    Lavor 2003 (interval B&B on a dihedral-angle model) [search snippet].  (Lin–Stadtherr appears in L2's query list.)

## Step 4 — P2: identifiability of a conformation from its distance profile (G19) (18:55– )

S16. `Mémoli Needham "Distance distributions and inverse problems for metric measure spaces" ...` -> arXiv:1810.09646v5
    (Studies in Applied Mathematics 2022).  READ [PDF: abstract, §2 "Global distance distributions" incl. definition of L_{H,p},
    Example 2.5, Prop. 2.7–2.8, opening of §3 with Theorem 4; rest not read].
    * H_X(r) := μ⊗μ{(x,x') : d(x,x') ≤ r}  (= normalised cumulative pair-count profile).
    * L_{H,p}(X,Y) := Wasserstein-p distance on ℝ between dH_X and dH_Y; explicit formula ∫_0^1 |H_X^{-1} − H_Y^{-1}|^p.
    * "these pseudometrics serve as lower bounds for Gromov-Wasserstein p-distances, as was shown in [70]" (Mémoli 2011);
      Prop 2.8: L_{H,p} ≤ L^K_{h,p} ≤ d_{GW,p}.
    * "It is well known that L_H does not distinguish elements of C_{N,k} for any (N,k) with N > 3" (N points in ℝ^k);
      Example: X={0,1,4,10,12,17}, Y={0,1,8,11,13,17} have equal distance distributions.
    * Theorem 4 (their restatement of Boutin–Kemper): L_H is locally injective on Euclidean point clouds.
    ==> d_P of Theorem 11.48(b) is L·(number of pairs)·L_{H,1} for the metric min(|x_p−x_q|², S_c) per pair type: the "second lower
        bound" of the Gromov–Wasserstein distance.  NOT named in the repo (grep: Mémoli only in L3 for another paper).
S17. `Boutin Kemper "On reconstructing n-point configurations ..."` -> arXiv:math/0304192 (Adv. Appl. Math. 32 (2004) 709–735).
    READ [PDF: abstract, introduction, Def. 1.1, Thm 1.6 statement, Remark 1.7, Lemma 1.8 with proof, Cor. 1.9, Prop. 1.10
    statement, Prop. 1.12, Prop. 1.13 statements, Cor. 1.15–1.16; proofs of 1.6/1.10 and all of Part 2 not read].
    * Def 1.1: reconstructible from distances = determined up to permutation and a Euclidean transformation in AO_m (reflections
      included) by the distribution (multiset) of the squared distances.
    * Thm 1.6: for n ≤ 3 or n ≥ m+2 there is a non-zero polynomial f such that every configuration with f ≠ 0 is reconstructible.
    * Lemma 1.8: "If the pairwise distances between the P_i's are not all distinct then f(P_1,…,P_n) = 0."  => the generic test
      says NOTHING for chains with equal bond lengths or for lattice chains (always repeated distances).  Prop 1.10 is a finer
      test for configurations with repeated distances (double cosets of the symmetry group of the distance pattern).
    * Prop 1.13: if the Gram matrix has the generic rank min(n−1,m), there is ε > 0 such that every configuration within ε with the
      same distribution of distances is congruent to it (local reconstructibility, no distinctness needed).
    * Remark 1.7: for 4 ≤ n ≤ m+1 generic configurations are (expected to be) not reconstructible.
    What this literature does NOT answer (my reading): a *cutoff* (profile truncated at S_c), *pair types*, constrained chain
    geometry (fixed bond lengths and angles), lattice chains, and any *quantitative* (stability) version.
S18. `small-angle scattering pair distance distribution function p(r) Debye formula uniqueness ambiguity ... AMBIMETER` -> snippets
    only: p(r) keeps no orientational information; mirror/point symmetry operations leave p(r) unchanged; inversion ill-conditioned.
    Fetched PMC4392415 = Tria et al. IUCrJ 2015 (EOM 2.0; not about ambiguity) and PMC4420545 = Konarev & Svergun, IUCrJ 2 (2015)
    352–360, doi:10.1107/S2052252515005163 [fetch-tool extraction]: "the number of meaningful Shannon channels that can be
    determined from a given data set" as "an estimate of the information content of the scattering data".
    Petoukhov–Svergun 2015 (AMBIMETER) NOT accessed -> cite only as [from memory — unverified].  (Workstream M owns this topic.)
S19. `Jiao Stillinger Torquato "Geometrical ambiguity of pair statistics" ...` -> arXiv:0908.1366 (Phys. Rev. E 81, 011105 (2010)).
    READ [PDF: abstract in full, introduction pp. 3–8 in part]: "it is known that the pair-distance information contained in g2 is in
    general insufficient to uniquely determine a point configuration"; kite/trapezoid: two non-congruent 4-point planar
    configurations with the same six distances ("two-fold degenerate"); mirror images are counted as identical; "in general
    degeneracy is rare"; "no functional of g2 ... can uniquely specify g3".  Part II (arXiv:1007.1374) for two-phase media [snippet].
S20. Huang & Dokmanić, "Reconstructing Point Sets from Distance Distributions", arXiv:1804.02465v4 (IEEE TSP 2021) READ [abstract]:
    turnpike (line) / beltway (loop) from unassigned noisy pairwise distances = unassigned distance geometry problem (uDGP).
S21. `Gortler Theran Thurston "Generic unlabeled global rigidity"` -> Forum Math. Sigma 7 (2019) e21, arXiv:1806.08688 [abstract via
    fetch tool]: for d ≥ 2 a generic configuration is determined by an unlabeled set of point-pair lengths (with d and n) iff it is
    determined by the labelled edge lengths (generic global rigidity of the underlying graph).  => closest result for a *subset* of
    pairs; needs genericity, so again silent on equal bond lengths / lattices; the profile's subset (pairs below the cutoff) is
    conformation-dependent, which that theory does not treat.
S22. `Duxbury ... "The unassigned distance geometry problem"` -> Discrete Appl. Math. 204 (2016), doi:10.1016/j.dam.2015.10.029
    [search snippet]: uDGP arises "when trying to find atomic structure from diffraction-type data"; conditions for unique
    realisation, build-up algorithms.
S23. `Wasserstein distance between radial distribution functions OR "pair distance distribution" structural similarity ...` -> a
    2021 phosphor-search paper (PMC8079038) using a bag of interatomic distances + Wasserstein distance [search snippet]; nothing
    for SAXS p(r) with W1.
M_brief check: workstream M item 7 covers "scattering-specific identifiability" too; I restrict myself to what bears on G19.

## Step 5 — P3: G24 limit shape: named theorems (19:25– )

S24. `Kaveh Khovanskii "Newton-Okounkov bodies, semigroups of integral points" ...` -> arXiv:0904.3350 (Ann. of Math. 176 (2012)).
    READ [PDF: intro "Theorem 1", §1.1 Defs 1.1–1.2, Prop 1.3, Thm 1.4 with proof, Cor 1.5, Thm 1.6 statement, Defs 1.9–1.10; rest not
    read].  For an additive semigroup S ⊂ ℤⁿ: Reg(S) = G(S) ∩ Con(S); Thm 1.6 (approximation theorem): for a closed strongly convex
    cone inside Con(S) meeting its boundary only at 0 there is N such that every point of the group G(S) in that cone at distance
    > N from the origin belongs to S.  Def 1.10: Newton–Okounkov convex set Δ(S,M) = Con(S) ∩ π_M^{-1}(m); compact iff strongly admissible.
    ==> If the concatenation property (C) of Thm 11.69 held with β = 0, {(q, M) : q ∈ Q_M} would be a graded semigroup and K^{br}
        its Newton–Okounkov body; "Fekete's lemma for sets" is the (approximate-semigroup) version of S_k/k → Δ(S).  Thm 1.6 is
        STRONGER than Hausdorff convergence for exact semigroups (interior lattice points are eventually all attained).
S25. `rotation set subshift of finite type Ziemian ...` -> Kucherenko & Wolf, "Geometry and entropy of generalized rotation sets",
    arXiv:1210.0135 (Israel J. Math. 2014).  READ [PDF: abstract, introduction, Prop. 3 statement].  Rot(Φ) = {∫Φ dμ : μ invariant}
    "is a compact and convex subset of ℝ^m" ("easy to see"); "Ziemian studied the case when [the system] is a transitive subshift of
    finite type and the potential Φ is constant on cylinders of length two" — then the rotation set is a polyhedron; Rot_Pt(Φ) =
    Rot(Φ) for mixing SFTs / systems with specification (ergodic measures dense).  Ziemian 1995 itself NOT read.
    ==> answer to the brief's question: for a locally constant vector potential on an SFT the limit set of finite-orbit averages IS the
        rotation set, and it is a POLYTOPE whose vertices are attained by periodic orbits (rate O(1/N)).  The chain profile is not
        of this kind: in sequence coordinates h is long-range and only superadditive; the N^{-1/3} law at the crystal vertex is
        incompatible with any SFT/locally-constant description.  In space coordinates (Lemma 11.67: a three-shell lattice gas) the
        object is the set of mean values of a local vector observable over (constrained) finite configurations — the classical
        "configuration polytope"/ground-state setting (Kanamori; Israel's convexity theory), with the chain constraint on top.
S26. `Lanford 1973 "Entropy and equilibrium states in classical statistical mechanics" ...` -> NOT accessible (Springer LNP 20);
    only secondary remarks [search snippets].  Cite as [from memory — unverified]: superadditivity ⇒ microcanonical entropy concave
    on a convex set of values of finite-range vector observables.
S27. `Janse van Rensburg supermultiplicative "density function" ...` -> arXiv:1603.08553v6 (J. Phys. A 54 (2021) 105003).
    READ [PDF: abstract, §1 start, list of statements (Lemma 2.1, Thms 2.2, 2.4, 2.5, 3.1, 3.2, 4.1)]: ONE energy variable;
    p_{n1}(m1)p_{n2}(m2) ≤ p_{n1+n2}(m1+m2) "together with mild assumptions" ⇒ density function limit exists on (ε_m, ε_M) and is
    concave; the support [ε_m, ε_M] comes from Fekete for the extreme energies (Lemma 2.1).  => Thm 11.69 = the several-variable
    version of the *support* statement, with a bounded error; consistent with the repo's own attribution.
S28. `maximum number of nearest-neighbour contacts ... "N^{2/3}" ...` -> Mainini–Piovano–Schmidt–Stefanelli "N^{3/4} law in the
    cubic lattice" (J. Stat. Phys. 2019) [snippet]; Strachan–Swanepoel "edge isoperimetry of lattices" (Ann. Comb. 2025) [snippet];
    and K. Bezdek, "Contact numbers for congruent sphere packings in Euclidean 3-space", arXiv:1102.1198v2 (Discrete Comput. Geom.
    48 (2012) 298–309).  READ [PDF: abstract, introduction, Theorem 1.1 and Corollary 1.2 statements; proofs not read]:
    Thm 1.1(ii): "Let Λ be any lattice of E³ with shortest non-zero lattice vector of length 2. Then C_Λ(n) < 6n − (3·(18π)^{1/3}/π)
    n^{2/3} = 6n − 3.665… n^{2/3} for all n ≥ 2"; (iii) 6n − 486^{1/3} n^{2/3} < C_fcc(n) for n = k(2k²+1)/3.
    ==> Prop. 11.73's bound e₈(S) ≤ 6N − 3N^{2/3} is IMPLIED WITH A BETTER CONSTANT: pairs at squared distance 8 in the diamond
        lattice are nearest-neighbour pairs inside each of its two fcc sublattices, so e₈(S) = C_fcc(S_A) + C_fcc(S_B) <
        6N − 3.665(N_A^{2/3} + N_B^{2/3}) ≤ 6N − 3.665 N^{2/3}  (subadditivity of t ↦ t^{2/3}).   [P, mine; one-line]
        Then ‖N^x‖₁ ≤ 35N − (9·2^{-2/3} + 4·3.665)N^{2/3} + O(1) = 35N − 20.3 N^{2/3} + O(1): the proved constant of the surface
        law improves from k ≥ 0.50 to k ≥ 0.58 (data: 1.71–1.86).  Novelty of the e₈ half of Prop 11.73 should be withdrawn.

My own remark (to state as [P], elementary, not checked numerically): for ANY family with (C), (E), (B) and any p in the interior of K,
dist(p, E_M) = O(M^{-1/2}) (choose d+1 points of E_m around p, mix k_i copies: error β/m + (β' + (d+2)R)m/M, optimise m ≈ √M).
So the N^{-1/3} law is a boundary effect.  For exact semigroups K–K Thm 1.6 gives O(1/M).

## Step 6 — P4: G16 lever arm (19:50– )

S29. `Featherstone "An Empirical Study of the Joint Space Inertia Matrix" ...` -> Int. J. Robotics Research 23(9) (2004) 859–871,
    doi:10.1177/0278364904044869.  READ [abstract only, via the ANU research-portal page; full text restricted until 2037]:
    "The joint-space inertia matrix of a robot mechanism can be highly ill-conditioned"; the condition number "grows anywhere from
    O(N) to O(N⁴) with the number of bodies in the system"; "not merely a numerical artifact; it is symptomatic of an underlying
    property of the mechanism itself".  (That the N⁴ case is the unbranched chain and that diagonal entries grow like m³ is
    [from memory — unverified]; the m³ itself is the same one-line computation as in Theorem 11.36.)
S30. `Schwarzer Saha Latombe "Adaptive dynamic collision checking" ...` -> IEEE Trans. Robotics 21(3) (2005) 338–353,
    doi:10.1109/TRO.2004.838012.  READ [PDF from typeset.io; text extraction loses the formulas; §"upper bound" and Lemma 2 read
    in words]: for a kinematic chain with revolute and prismatic joints and a linearly interpolated configuration path, "an upper
    bound on the lengths of the curves traced by the points of [a link]" is Σ_i R_i|Δq_i| where for a revolute joint R_i "is an upper
    bound on the distances between the points of [the link] and the axis of rotation of joint i".
    ==> the per-joint weighted-ℓ¹ displacement bound with lever-arm weights (the "naive lever-arm bound" of §4.4, the envelope
        format Σ c_i|δ_i| of §11.14) is standard in motion planning, where it is used exactly as a *certificate* (collision-free
        path segments).  Not there: superposition (RMSD after optimal alignment), reduced inertia, the m^{3/2} law, query complexity.
S31. `"lever arm" effect backbone dihedral angle error propagation chain length RMSD scaling ...` -> no quantitative law found;
    Bastolla & Dehouck (J. Chem. Inf. Model. 2019; torsion-space description of conformational change; "the impact of modifying one
    torsion angle strongly depends on all other angles") [search snippet].
S32. `systematic conformational search torsion angle resolution ... "CONAN" Smellie ...` -> NOT confirmed: I remembered a
    displacement-bounded torsion step in CONAN (Smellie et al. 2003); the search gave only a review-table entry.  Do not cite.
S33. Featherstone full text: ANU repository copy restricted (fetch).  NOT ACCESSED.

## Step 7 — P5: G13 normal form (20:05– )

S34. `"weightable quasi-metric" definition weight function ... Matthews 1994 Künzi Vajner` -> Deza, Deza, Vidali, "Cones of weighted
    and partial metrics", arXiv:1101.0517v3.  READ [PDF: abstract, §1 definitions, §2 maps P and Q]: "A quasi-semimetric f is
    weightable if there exist a (weight) function w : V_n → ℝ≥0 such that f_ij + w_i = f_ji + w_j for all i, j"; partial metrics
    "were introduced by Matthews in [Ma92]"; map Q: (q, w) = Q(d; w) with q_ij = (d_ij − w_i + w_j)/2, d_ij = q_ij + q_ji the
    symmetrisation; "down-weighted": d_ij ≥ w_i − w_j.  Künzi–Vajner 1994 [Warwick abstract page, search snippet only];
    Matthews 1992/1994 NOT read (attribution via Deza et al.).
    ==> G13(b)/(c): for symmetric d the reduced envelope σ(a,y) = d(a,y) + f^d(a) − f^d(y) is exactly a *weightable quasi-metric*
        with weight w = −2f^d (+const): σ = 2·Q(2d; w); "down-weighted" ⇔ f^d is 1-Lipschitz for d ⇔ σ ≥ 0.  Equivalently a
        *partial metric* p(a,y) = d(a,y) − f^d(a) − f^d(y) + const whose self-distance is (minus twice) the regularised known part.
        The correspondence itself is classical (Matthews); its use for certificates was not found.  Repo does not mention it.
S35. `Randers metric exact 1-form ...` -> [search snippets only]: adding an exact 1-form df (norm < 1) to a Randers/Riemannian
    metric leaves the pregeodesics unchanged and the symmetrised distance unchanged (arXiv:0903.3501, Caponio–Javaloyes–Sánchez).
    The formula d_F(x,y) = d_α(x,y) + f(y) − f(x) is my one-line computation (integral of df along any curve).  Continuous
    analogue of the normal form: "known part = exact 1-form of a Randers-type asymmetric distance".
(Reward shaping, Ng–Harada–Russell 1999, and A* with consistent heuristics as Dijkstra on reduced costs: [from memory — unverified].)

## Step 8 — P6/P7: G1/G4/G7 follow-ups, Merhav in full, C4 (20:20– )

S36. Merhav, "On optimum strategies for minimizing the exponential moments of a given cost function", arXiv:1103.2882v1.
    READ [PDF: abstract; Section 4 "asymptotic regime" pp. 15–17 in full; the BSS phase-transition example p. 22].  Exact form:
    conditions (a) [for every type class T_Q and every x ∈ T_Q, ℓ(x, s*) ≤ n(λ(Q) + o(1))] and (b) [every strategy has
    ℓ ≥ n(λ(Q) − o(1)) on a non-exponentially-small fraction of T_Q]; then "It is then a straightforward exercise to show, using the
    method of types, that s* is a universal asymptotically optimum strategy ... with E(s*, α, P) = max_Q [αλ(Q) − D(Q‖P)]" (eq. 37);
    first example: fixed-rate lossy coding of a memoryless finite-alphabet source with an additive distortion meets (a), (b) with
    λ(Q) = D_Q(R) "based on the type covering lemma".  => the repo's attribution for G7 is CORRECT in substance; it is an
    *example of a general observation* (not a numbered theorem), stated for memoryless sources, finite alphabets, additive
    single-letter distortion.  The repo's "[K, not verified in detail]" can be upgraded to [K, full text of the relevant section read].
S37. `certified Lipschitz optimization instance-dependent sample complexity lower bound 2023 2024 2025 follow-up ...` -> only the
    2021 paper itself (v5 revised March 2023).   S38. `query complexity global optimization Lipschitz function Hamming cube ...
    "rate-distortion" certificate` -> nothing combining rate–distortion with certificates.
S39. arXiv API: `all:"error certificates" AND all:Lipschitz` -> 2 hits (the 2021 paper; an unrelated 2026 PINN paper);
    `abs:certified AND abs:"Lipschitz optimization"` -> 0; `abs:"Piyavskii" AND (instance OR certificate OR regret)` -> 4 (Gokcesu &
    Gokcesu 2021–22 regret papers; Bachoc et al.); `abs:"rate-distortion" AND ("query complexity" OR "black-box optimization" OR
    "zeroth-order")` -> 1 unrelated.   => no 2022–2026 prior art found that changes the L4/L6 verdicts on G1, G4, G7.
S40. `RMSD after optimal superposition two rigid fragments rotated about hinge axis ... closed-form` -> no hinge/torsion formula;
    general Kabsch/quaternion material only.  C4 "no match found" stands (medium confidence).  My remark: C(φ) =
    2(S − |I_A + I_B e^{iφ}|) is the planar weighted Procrustes residual (weighted circular variance of the angles 0, φ).

## Step 9 — own numerics (20:30– ): scripts in this directory
N1. `homometry_saw.py` (own code): SAWs on Z² (N ≤ 16) and Z³ (N ≤ 9), up to the point group incl. reflections + translations.
    Columns: N, walks with fixed first step, W_N walk classes, S_N site sets, D_N distinct FULL squared-distance multisets,
    number of homometric groups, P_all / P_sep3 = truncated profiles at S_c = 5 (all pairs / chain separation ≥ 3).
    Z²:  6: 36 walks, 18 sets, 17 multisets (first homometric pair!);  8: 272/115/109;  10: 2034/781/744;  12: 15037/5541/5371;
         14: 110188/39592/39036 (536 groups);  15: 296806/106630/105971 (649 groups, 1308 sets);  16: see output file.
    Z³:  6: 92/47/43;  7: 402/184/171;  8: 1832/768/679;  9: 8453/3411/3047 (276 groups containing 640 site sets = 19 %).
    Smallest example (Z², 6 beads), checked by hand: A = {(0,0),(0,1),(0,2),(1,2),(1,3),(2,3)}, B = {(0,0),(0,1),(1,1),(1,2),(1,3),(2,3)}:
    both have squared distances 1⁵ 2³ 4¹ 5³ 8¹ 10¹ 13¹; A has its collinear triple at an end, B in the middle => not congruent.
    Sanity: W_4 = 5 (Z²), 6 (Z³) by Burnside; W_16(Z²) should be 802 075 (the referee's count in §11.17).
    Runtime: Z² to N=14: 70 s CPU; N=15,16: ~10 min; Z³ to N=9: 42 s.
N2. `torsion_checks.py` (own code, seed 20261125): C4 — 20 000 random two-body torsion moves: closed form = direct minimisation over ψ
    (rel. dev. 7e-6, grid) = 2(S − |I_A + I_B e^{iφ}|); Kabsch (proper) cost ≤ coaxial cost in all cases, max ratio 0.9983;
    4 I_red sin² ≤ C ≤ 4 min(I_A,I_B) sin² never violated.   G16 — all-trans chain: 2√min(I_A,I_B)/m^{3/2} = 0.625, 0.585,
    0.565, 0.554, 0.549, 0.547, 0.546 at m = 10…640 (fitted exponent 1.47 → 3/2); regular helices: sup of 2√(2I_red)/m^{3/2} at the
    central torsion 0.58–0.64 (τ = 90°); phantom random rotamer coils (N = 403): median 2√min I / m = 1.17 (i.e. ∝ m, not m^{3/2}).
N3. `lever_constant.py` (own code): all-trans arms joined to the central bond through scanned torsions (20° grid, 3 per side):
    sup 2√(2 I_red)/m^{3/2} = 1.013, 0.978, 0.961 at m = 20, 40, 80, attained with a gauche (±60°) torsion next to the central
    bond; sup I_arm/m³ → 2/9 = 0.2222 (zigzag of advance b·sin(θ/2) = 0.8165 b per bond, exactly perpendicular to the axis), so
    the limit is 2√(2/9) = 0.943.  => Theorem 11.36's "c_i ≥ 0.824 Λ b m^{3/2}" is confirmed in power and is not sharp in the
    constant for the central torsion: 0.943 is attained asymptotically (independent replication of the law, [N]).
    Runtime 80 s CPU.
