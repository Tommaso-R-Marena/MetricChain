> **Provenance.** Report of a read-only intake reviewer (a subagent of the Frontier Benchmarking
> division, model Claude Opus 5.5) delivered on 2026-11-26 and committed **as delivered**, apart from
> this notice.  It read the named divisions at the pinned commits stated in its first paragraph; it
> re-ran no script and checked no proof.  It is an internal AI reading, not a review.  What the
> coordinator verified directly, and where this report is used, is in `../RESEARCH_INTAKE.md`.
> Sentences marked "evaluator suggestion" or "gaps noticed" are the reviewer's proposals.

# Intake review: Ensemble, Geometry, Complexity divisions

*Benchmarking/Evaluation division, read-only intake, 2026-11-26.* I read each division only at its pinned commit: ensemble `2d2054d…` (`2d2054ddefdd4e586719bbee8094684b18ed46e0`), geometry `9f164f9…` (`9f164f9795f4dd50e704246a862d68ef95238578`), complexity `75266b2…` (`75266b2508477ae419666c4d2f87b6ef1b00041b`). I did not open the engineering branch, so engineering's answers to requests are reported only as each division records them. Status labels are the divisions' own: [V] Lean-checked, [P] paper proof, [P-exact] paper proof plus an exact computation, [K] known/cited, [N] numerical, [C] conjecture, [X] exact finite computation. Every "review" is an AI review, either internal (a subagent of the same division) or by another division (Science). None is peer review. I re-ran no scripts and verified no proof. Wherever this file says "evaluator suggestion", the idea is ours and not the division's.

---

## 1. Ensemble Identifiability and Certified Inference (`2d2054d`)

**1.1 Mandate and output.** The mandate is to decide when an unknown measure μ on a configuration space X is identified from data `y_i = ∫φ_i dμ + ε_i`, when it is only partially identified, and when inference is impossible. Files: `docs/ensemble/ENSEMBLE_REPORT.md` (Parts I–VI, about 229 KB), `THEOREM_REGISTER.md` (one row per statement), and five Lean modules in `proofs/Ensemble/` (24 headline theorems, axiom audit passed). The numerics are in `experiments/ensemble/` (`run_all.py` plus `check_quotes.py`, which ties each quoted number to a stored output). There are three internal reviews (ER1–ER3). The Science division reviewed Part II (SCI-REV-0020) and replicated E15 and E15U (SCI-RES-0032, -0038). For software the division wrote `SOFTWARE_INTERFACE.md`, which gives readiness levels R3–R0, and `BENCHMARK_CONTROLS.md`, which specifies 18 verified instances in `experiments/ensemble/benchmarks/controls_v1.json`. The register defines the space X and the observables precisely and calls itself unrelated to any instrument: "Nothing here is a statement about a molecule or an instrument."

**1.2 Register (most consequential).**

| id | statement | status | key assumptions | idealised setting | evidence | independent replication |
|---|---|---|---|---|---|---|
| E1(a) | On finite X, μ is identified among all ensembles iff (i) the features (1,Φ) are independent on its support and (ii) the support is the whole zero set of some f ≥ 0 in span{1,Φ} | P; "if" V `eq_of_exposing_certificate` | finite X; exact means | averaged scalar data over an enumerable candidate pool | T1: 1 500 instances, two LP tests agree | ER1 (internal) |
| E1.1 / F2 | A certificate bounds the mass off the support by ‖λ‖_*‖ΔA‖/γ for *every* ν, with no model needed | mass bound V `mass_off_support_le`; TV bound P | finite X | averaged data with a bounded error | — | ER1 |
| E2(c) / F4 | A robust-optimality certificate (theory Thm 2.4) is an identification certificate with transport modulus ‖λ‖_*τ | V (finite X) | sharp minimum | single conformation from averaged data | Lean | ER1 |
| E2(a) / F3 | Exact LP-dual interval for any target E_νψ given data within τ, or a Farkas certificate of infeasibility | P (LP duality) | linear data, stated X | partial identification of populations | T2/F5: gap ≤1e-14 on 600 instances | ER1 |
| E4 | Rényi–Heppes: if any two configurations agree on fewer than r features and m ≥ K(r−1)+1, the laws of the features determine every ensemble with ≤K atoms; sharp | V (finite X), P | exact laws | distributions of observables | Lean | ER1 |
| E7 | Generically globally rigid graph ⇒ jointly generic finite ensembles of frameworks are determined (up to congruence) by edge-length laws | P given K (GGJ 2022 Thm 3.5; GHT) | *joint* genericity, exact laws | pairwise distance distributions of an ensemble | R1–R10; counterexamples D1, D2 | SCI-REV-0020 (proved as stated) |
| E8 | 2K moments per edge suffice; explicit certificate, not sharp | P | as E7 | moments of distance distributions | R5 | SCI-REV-0020: at 1e-5 moment accuracy, large mass can lie far from every conformer |
| E10 / E11(a) | Pair correlations on {±1}ⁿ identify every ensemble on K ≤ n−10n/ln n random conformers (certificate ‖P^⊥x‖²); nothing is identified beyond (2+ε)n | P given K (Odlyzko; Cover) | random conformers | Ising-type pair data | C1–C5 | ER1 |
| C2 | The threshold for pair data lies between 1.1n and 1.2n | C, N | — | as above | `capacity_cutting_plane.py`, exact LP up to n=20 | none |
| E15 / E15U | Thermal union bound TV(μ,μ*_a) ≤ Σ[σ_i − μ(x_i=a_i)]. E15U gives the exact condition: E[N∣U] − E[N∣U^c] ≥ 1 for every up-set U | E15: P, core V `thermal_union_bound`. E15U: P | first-order class, binary sites | one-body populations at finite temperature | F1–F7 | Science replicated E15 (95 160 LPs) and E15U(C). Other parts of E15U unreviewed |
| E17 | Minimax RMS error lies between 0.335·ω(2σ) and 0.5·ω(2σ); the dual vector is the near-minimax affine estimator | P; K (Donoho 1994) | Gaussian noise on means, known σ | noisy averaged data | F5, ER2 | ER2 |
| E19 | Data of order ≤2d identify (1−ε)n^d/d! random cube conformers. Worst case: any 2^{2d}−1 (Kahle 2010) | (a),(g) K; (b)–(d) P given K; (e,f) N | random conformers | higher-order correlations | `kbody_capacity.py` | ER3 |
| E20′/E20″ | Two states on 𝕋^r are determined by multilinear trigonometric data iff they differ in ≥2 angles. Explicit quadratic-growth constant c* = min(1, β_min/4) | P; zero set and growth V `twoStateCert_*` | probability measures on a torus; products of *pairs* of angles | torsion-angle ensembles | L4, L6; ER3 dense-grid attack | ER3 (E20″). E20′ "not searched" |
| E22 | No three states on 𝕋² are ever determined by the nine bilinear means | P given K (Carathéodory–Toeplitz) | — | torsions | twin verified (control B2-07) | ER3 originated it; "read by nobody else" |

**1.3 Evaluable claims.**
- **(a) Synthetic planted truth, ready now.** Controls B1–B7 test one property each. B1: does the tool return `IDENTIFIED` with a checkable certificate? B2: does it report twins? B3: does it report a stability constant? B4: does it distinguish abstention from non-identification? B5: does it return exact intervals? B6: does it check a bound's hypothesis? B7: does it bracket the risk? The specification is finished. The harness is assigned to engineering and has not been built. Evaluator suggestion: these are finite tables Φ, so they can be fed directly to current reweighting tools that accept a matrix of per-conformer computed observables plus experimental values and errors (BME / maximum-entropy, BioEn-type Bayesian reweighting). The pass criterion is the scoring rule of §4 of BENCHMARK_CONTROLS: on B2 a sound tool reports ambiguity instead of returning one ensemble. The only prerequisite is a thin adapter.
- **(a) Scale families.** Random cube conformers have exact ground truth up to n ≤ 22 (`capacity_cutting_plane.py`; reference frequencies at n=16 are 0.94, 0.66, 0.26, 0.07 at K=16, 18, 19, 21). Family 5 ("identified without the easy certificate") gives 92 % identified and 0.5 % certified at n=12, K=9.
- **(b) Public retrospective data.** F1/F3/F2 are exact LPs over any *finite candidate pool*, for example an MD or fragment library plus forward-modelled SAXS or NMR averages. Running them is a concrete retrospective test: report whether populations are identified or only interval-bounded, and how wide the certified intervals are. Missing pieces: forward models, which the division explicitly does not assess (§6 of SOFTWARE_INTERFACE). Also missing: per-observable forward-model error δ (E17.1(b) says it enters exactly as an enlarged tolerance) and a noise model beyond Gaussian on means. The verdict is valid only for the stated pool X ("adding one configuration … can turn IDENTIFIED into NOT IDENTIFIED"). Data that are nonlinear in μ (ratios or squares of averages) are "not covered".
- **(b/c) Distance distributions (E4, E7, E8 / L2).** These are rated R1, not ready. There is no stability modulus (Problem O4, chimera gap), the results assume exact laws, and the theory treats a measured distribution as an exact law. The division itself says a measured distribution is "the solution of an ill-posed deconvolution". Before any DEER or FRET comparison, the prerequisite is a synthetic chimera-gap study under a band.
- **(a) Torus results E20″/E22.** Synthetic tests on dihedral mixtures are straightforward. Evaluator observation: E20′ needs means of products over *pairs* of angles, and none of the three divisions names a standard observable that supplies them.

**1.4 Prior art as recorded.** Classed as *known* or *known in substance*: E1 (dual certificates of sparse recovery; Donoho–Tanner 2005 face criterion, through Science), E9, E19(a) (Baldi–Vershynin 2019, **rediscovered**: ED15), E19(g) (Kahle 2010, which supersedes E21 on finite product spaces), E13(a), E17 (Donoho 1994). *Formulation*: E2, E3, E13(b,c), E15/E15T (a union bound over a monotone coupling), E18, E18′. *Synthesis*: E10, E11(a), E19(b–d), E20. *New (not found)*: the E5–E7 *reading*, E7′, E15U, E15(d), E16, E20′/E20″. Several key sources were read only from memory or summaries (OB2–OB6, OB15–OB16). External methods named: Kueng–Tropp, MUSIC, Johnston–Lovitz–Vijayaraghavan 2023, pivoted Cholesky. **The register names no contemporary ensemble-refinement software** (maximum entropy appears only in passing).

**1.5 Negative results and withdrawals.** These are recorded in `DEAD_ENDS.md` as ED1–ED24:
- ED12: the slogans "identified = exposed" and "identification = absence of chimeras" are false.
- ED19 / ER2 F1: E15T's "and only then" converse is false.
- ED24: a parameter count on the torus was never computed. A threshold extrapolated from it, (3^r−1)/(r+1), is wrong. Product-grid LPs report false `IDENTIFIED` (38 of 40) because the twin lies off the grid.
- ED21: the transfer of E20′ to chains is withdrawn. Competing chains live on O(2)^r, and only adjacent pairs of torsions are in the span.
- ED22: the thermal union bound as a falsification test is withdrawn. It certified nothing on the Science division's instances.
- ED23: a conjecture held on 17 000 random instances and was refuted by an optimiser.
- ED13, ED20: quoted numbers that no script printed.
- Unreviewed and therefore most fragile: E15U beyond (C), E17.1, E20a, E22, and two constants of E20″ (OB23, OB25, OB26).

**1.6 Requests to engineering.** None. `requests/ensemble/` holds only `.gitkeep`. The benchmark controls are "a specification; execution left to the engineering division", with no formal request ID. No Modal or shared compute was used. A four-body run at n=14 was still in progress locally.

---

## 2. Geometric Inference, Rigidity and Inverse Problems (`9f164f9`)

**2.1 Mandate and output.** The mandate is reconstructability, identifiability, rigidity and stability of articulated systems. The core object is the ensemble-averaged squared-distance matrix M_ij = ⟨|x_i − x_j|²⟩ of chains with statewise bond lengths and angles. Files: `docs/geometry/ENSEMBLE_RIGIDITY.md` (cycle 1), `LOCAL_DATA_STABILITY.md` (Theorem K/L), `HINGE_ENSEMBLES.md`, and a 45-row `THEOREM_REGISTER.md`. Lean: `proofs/Geometry/EnsembleRigidity.lean`, 16 cited declarations, 5110-declaration axiom audit OK. Harness: 46 tests plus 34 mutation checks, all caught. There are exact rational or modular rank witnesses and Singular Gröbner computations. Reviews: GEOMETRY-REV-0001 (internal, at `e8e2582`) and SCI-REV-0021 (Science, of Lemma 2.2, Theorems B, B′, Corollary 4.2 and Theorem G). Text written after `e8e2582` is mostly unreviewed.

**2.2 Register.**

| id | statement | status | key assumptions | idealised setting | evidence | independent replication |
|---|---|---|---|---|---|---|
| G1.3 Prop 3.1 | Without statewise constraints, averaged squared distances identify nothing (an O(3K) orbit; a collinear three-state decomposition) | P; known/elementary | — | averaged distances, no bond data | scripts | REV-0001 |
| G1.5 Thm B | A K-mixture is the only ensemble (among all) with its M if only the K−1 trivial quadrics pass through the stacked edge directions (conic condition CC). Sufficient, not necessary | P; V in coordinates against finite mixtures `mixture_identifiable_stacked` | exact, identical statewise constraints | complete averaged squared distances | `trivial_quadrics_only` | REV-0001 (14 640 starts); SCI-REV-0021 replicated for K ≤ 3. At d=1 known (Laurent–Poljak 1996) |
| G1.9 Thm C(b) | CC holds generically iff n ≥ ⌈(9K²+K+8)/4⌉ atoms (5, 12, 23, 39 …) | P-exact for K ≤ 20 (cos −5/13) and K ≤ 12 (tetrahedral). All K: C. Proved from (9K²−5K+6)/2 | generic chains | as above | `exact_conic_rank.py` | REV-0001 exact for K ≤ 12 |
| G1.12 DEMIX | Polynomial-time demixing (eigen-decomposition plus linear system) under CC, with a rank certificate | P | exact data, K given | as above | `demix.py` | REV-0001 independent implementation. **No noise guarantee**; DG-7: automatic K detection failed at noise 1e-4 |
| G1.15 Thm G | Under CC, W₂(ν,μ)² ≤ C‖M(ν)−M(μ)‖ for every ν; optimal exponent ½ | P | CC; κ a global infimum not computed | stability of averaged-distance inversion | `dual_certificate` etc. | REV-0001; SCI-REV-0021 ("existence statement until κ is bounded") |
| G1.18 Thm E | (universal rigidity ∧ C₁) ⇒ second-moment rigidity ⇒ (global rigidity ∧ C₁); second implication strict | P; parts V | 𝒩(X)=0 | single structure versus ensembles | exact witness | REV-0001 (the summary form was false, DG-13) |
| G1.19–20 Thm H | Local identifiability within K states iff n ≥ 2K+3 (complete data); sequence separation K+3 suffices; K+2 never (K ≥ 2) | P-exact for K ≤ 8 | local, within the K-family | sequence-local averaged distances | `exact_jacobian_rank.py` | REV-0001 |
| G1.25 Thm I | Generic two-state ensembles are identifiable among all ensembles from n=10 atoms | P-exact (Gröbner over ℚ, degree 7) | generic, one bond geometry | complete averaged data | `exact_nonlinear_threshold.py` (Singular) | REV-0001 replicated the degree independently. Engineering replication requested (REQ-0001) |
| G1.26 | Two states are *not* identifiable at n=7, 8 (explicit competing ensembles of 9–11 chains, to 1e-14) | N | — | — | `explore_below.py` | REV-0001 numerical |
| G1.31 Thm I′ | Identifiable among all ensembles from 10, 16, 30 atoms for K=2, 3, 4, recovery by linear algebra on quartic forms | P-exact (ranks mod 65521) | generic; two bond angles | complete averaged data | `exact_demix4.py` | **not reviewed**. Method is Johnston–Lovitz–Vijayaraghavan 2023 |
| G1.27 Thm J | Laws of distances at separations 3 and 4 determine every generic finite ensemble of chains | P given Ensemble E5/E6 | joint genericity | pairwise distance distributions | `matroid_connectivity.py` (exact) | REV-0001 conditional |
| G1.29 / Cor 9.1 | Labelled configurations under Haar rotations: second plus third moments determine a generic mixture; with bond constraints the second moment suffices | P (sample-complexity theorem cited, not re-derived) | labelled points, no noise | idealisation of cryo-EM/ET orbit recovery | `third_moment.py` | REV-0001 on paper only |
| G2.5–2.6 Thm L / L⁺ | For any configuration Y, min_g‖Y−gX‖ ≤ 1.2(b/(s_*τ_*))(n+2)²‖η‖₂ from distances at separation ≤4. First-order constant 1/(2μ) in a certified range | P; unreviewed (rewritten at the 10th checkpoint) | thick windows, exact bounded errors | distance geometry with local distances | `local_data_upper.py`, `local_data_guarantees.py` | originality only (SCI-REV-0023): mechanism and scaling known. **The division's own verdict: the certified range is ≤1e-5 Å, so the guarantees are "empty for data of realistic accuracy"** |
| G3.3 Thm M | Hinge ensembles: two states differing in ≥2 torsions are identifiable unless two of R₁, R₂, R₁R₂ are half-turns; one torsion never | P; count P-exact | rigid shared segments; mirrors allowed | commonest two-state motions | `exact_hinge_candidates.py` | Science Prop R22-1 came first; two derivations agree |

**2.3 Evaluable claims.**
- **(a) Synthetic planted truth.** DEMIX and DEMIX-4 on planted K-state chain mixtures at the exact thresholds (CC from 12/23/39 atoms; certificate from 11/17/30). The test: (i) recovery is exact on exact data; (ii) an additive-noise sweep on M; (iii) a baseline comparison against classical scaling and non-negative least-squares reweighting over a planted-plus-decoy pool (evaluator suggestion). Prerequisite: a noise model and a stability constant for the rank certificate. O-15(vi) states that nothing exists on noise. K must currently be supplied as an input.
- **(a) Generic structure.** Theorem C/H rank thresholds are already set up for independent replication (GEOMETRY-REQ-0001 item 3).
- **(b) Public data.** For Theorem L/L⁺, evaluator suggestion: compute C_L, 1/(2μ) and the certified range on real Cα traces from deposited structures, not idealised helices. The division's table uses "traces of constant radius, rise and turn … not structures from a database". Then compare the first-order constant with the empirical reconstruction error of established distance-geometry or lateration solvers under realistic noise. Prerequisite: a curated trace set. No forward model is needed because the data are distances.
- **(b) Averaged-distance identifiability.** No public dataset is named. Complete labelled-pair second moments are not an experimental product. Low-angle labelled scattering gives block sums ⟨C_a, M⟩ (Theorem F″, "no instance", O-14), and paramagnetic or NOE data are ⟨r⁻⁶⟩-type averages, which "nothing here applies to". Prerequisite: translate Theorems B/F″ to block sums and to other distance functions.
- **(c) External methods.** Corollary 9.1 / Prop 9.2 against method-of-moments orbit recovery (Bandeira et al.; Bendory et al., which the division cites) on synthetic labelled point clouds. The gap to images (projection, CTF, noise) is unaddressed. Second-moment versus universal rigidity (G1.24) needs the certified optimisation of GEOMETRY-REQ-0006.

**2.4 Prior art as recorded.** *Known*: Lemma 2.1 (Schoenberg), Prop 3.1, Thm A(ii⇔iii) (Connelly), Thm B at d=1 (Laurent–Poljak 1996, via Tropp 2018; missed by their own search), Thm D(a) (Grone–Pierce–Watkins), NP-hardness of realizability (E.-Nagy–Laurent–Varvitsiotis), Thm F at K=1, Thm K(a) (Lew–Nevo–Peled–Raz, with a better constant), DG-3 and DG-4. *Mechanism known*: Thm G (Fernandez-Granda 2013), §6.2 / Thm I′ (Johnston–Lovitz–Vijayaraghavan 2023; Derksen–Johnston–Lovitz 2024; Dastidar–Weich–Wein 2025), Thm L (thin-rod rigidity: Mora–Müller, Blanchard–Griso). *Not found*: Thm C thresholds, DEMIX, Thm E as a notion, Thm H, Thm I, the hinge reduction, and Thm B for d ≥ 2. *Related but different*: Belyaeva–Kubjas–Sun–Uhler (diploid Hi-C), Sefer–Duggal–Kingsford, Shi–Thirumalai 2023 (DIMES maximum entropy). The register says "No full text was read" unless an entry says otherwise.

**2.5 Negative results and withdrawals.** Recorded in `DEAD_ENDS.md` DG-1…DG-25:
- DG-1: no interval Hall count for chain rigidity. Chain rigidity with sparse long-range bars is as hard as generic 3D rigidity.
- DG-9: the expected two reduced points in REQ-0001 was wrong (degree 7, with a structural point at infinity).
- DG-13: "universal ⇒ second-moment rigidity" is false without CC.
- DG-14, DG-16, DG-19: Theorem H and Corollary 9.1 over-summarised; an unsupported exponent n^{4/5} on helices.
- DG-21: §6.2 was written as new before its literature was checked.
- DG-23: floating point is unreliable for rank defects.
- DG-24: the threshold in Theorem L was a proof artefact.
- Two results are priority to Science: the hinge result (R22-1) and Theorem B at d=1.

**2.6 Requests to engineering.**
- **GEOMETRY-REQ-0001.** Item 1 (exact elimination, K=2, n=10) is *superseded*: the division did it itself with Singular. It is now a request for independent replication (O-2(d)). Item 2 became REQ-0006. Item 3 (independent replication of the exact witnesses for K = 2, 3, 4) is "proposed".
- **GEOMETRY-REQ-0006.** A certified interval branch-and-bound for the global maximum of instance A on the 4-torus, plus a Krawczyk-certified realisation in 4D (O-3). Status per `status/geometry.md`: engineering queue entry Q-16 **accepted** (local, no Modal), with a draft ENG-MSG-0007 containing "unfilled placeholders". No final result yet. I did not verify this on the engineering branch.
- Not sent: four states at 24–29 atoms (O-15, "a candidate for a request … not sent"); an instance-specific injectivity radius for Theorem L (O-16(ii), "not requested").

---

## 3. Mathematical Biology and Computational Complexity (`75266b2`)

**3.1 Mandate and output.** The mandate is to resolve documented open problems in theoretical computational biology and complexity. Four topics:
- **Multi-strand nucleic-acid folding** in the nearest-neighbour (NN) model: hardness (`STRANDS_NN_HARDNESS.md`) and an algorithm (`STRANDS_ALGORITHM.md`).
- **NANUQ quartet metric** on phylogenetic networks (`NANUQ_LOCAL_CRITERION.md`).
- **Ising ground sets / faces of the cut polytope** (`ISING_GROUND_SETS.md`), which answers the Ensemble division's E-C1/E-C2.
- **Penalised models** (`PENALTY_THRESHOLD.md`).

Other files: `THEOREMS.md` (CX-T1…T30, CX-V1…V5, CX-X1…X2) and `ASSUMPTION_AUDIT.md`. Four internal reviews (COMPLEXITY-REV-0001…0004) plus the Science division's SCI-REV-0019 on the hardness note. Lean is in `experiments/complexity/lean/` and covers finite cores only.

**3.2 Register.**

| id | statement | status | key assumptions | idealised setting | evidence | independent replication |
|---|---|---|---|---|---|---|
| CX-T1/T2 | Multi-strand unpseudoknotted NN MFE is strongly NP-hard for every fixed loop-energy function with (H0) exterior loops 0, (H1) GG/CC stack <0, (H2′) | P; counting step V (CX-V1) | many strand *species*; formal model, not published tables | NN secondary-structure energy model | [X] enumeration; referee 134+867 instances | REV-0001; **SCI-REV-0019 (independent division)**; REV-0003 |
| CX-T4 | #SSEL is #P-hard; the magnified partition function is #P-hard with magnification or temperature as input | P | as above | — | — | REV-0001, REV-0003. Fixed-temperature hardness open (A3′) |
| CX-T14 | Under ETH, no 2^{o(c)}·poly(N) algorithm for MFE | P conditional on ETH | sparsification lemma cited from memory | — | `test_eth_chain.py` | REV-0003 |
| CX-T15/T20/T24 | Hardness persists with flush coaxial stacking, dangles, both together, several complexes (stated parameter inequalities) | P | explicit inequalities | — | `test_generalised_hypotheses.py` | REV-0003; T20 is Science's referee's |
| CX-T12 | Magnified partition function over all orderings with symmetry in O(N⁴3^c); polynomial for a bounded number of species | P | NN model, stated conventions | multi-strand thermodynamics | exact agreement on 280 systems (plus about 740 by the referee) | REV-0003. **For the base-pair model this is Boehmer et al. 2025** |
| CX-T30 | MFE and level counts per symmetry class; a symmetry-blind (min,+) recursion is wrong (too low in 11/17 systems) | P (referee's argument) | exact arithmetic, Θ(cN²) bits | — | `level_counts.py` | write-up unreviewed |
| CX-T6/T7 | NANUQ metric of every galled outer-labelled planar network is circular decomposable with exact support; "galled" cannot be dropped (7-leaf N*) | P+X (+V finite inputs) | outer-labelled planar | quartet distances of phylogenetic networks | 74 661 random networks (referee) | REV-0002, REV-0004. T6 is a **probable rediscovery** of the unreviewed claim B-II |
| CX-T16 | "K sign vectors are exactly the ground states of a pair energy" is linear-time for fixed K and decidable in 2^K·poly(n); in co-NP; hardness open | P | — | identifiability of a state set from pair data | [X] tables K=4, 5 | REV-0004; largely Laurent–Poljak |
| CX-T28 | A degree-2 SOS certificate exists iff the span of V contains no other sign vector; fails with probability ≤ 2^{K−n} + C(n,K)2^K(3/4)^{n−K} | P | — | as above | `degree2_certificates.py` | **unreviewed** |
| CX-T29 | The span problem is NP-complete, so deciding whether a degree-2 certificate exists is co-NP-complete; no 2^{o(K)} under ETH | P (the reduction is the referee's) | — | as above | 60 reduction instances | reduction by REV-0004; consequences unreviewed |
| CX-T25 | Certifying exact ground sets of K random conformers needs SOS degree ≥6 beyond n²/2 and ≥8 beyond n³/6 | P | general position | as above | — | unreviewed |
| CX-T23 | "Has a penalised model left its reference?" is NP-hard for general pair tables; polynomial for product, windowed and exponentially decaying tables | P+X | — | penalised ensembles | `hardness_maxcut.py` | unreviewed |
| COMPLEXITY-RES-0002 | Maximising Σc_ij\|x_i−x_j\|² over freely jointed chains is exactly the Heisenberg ground-state problem with arbitrary couplings | P (hardness from sources not read) | freely jointed | realizability of averaged distances | — | unreviewed |

**3.3 Evaluable claims.**
- **(c) Established software.** CX-T12 / CX-T30 against a mainstream multi-strand partition-function implementation (the Dirks et al. algorithm, NUPACK-type) on small synthetic systems. Test: exact agreement of the magnified partition function, MFE and symmetry corrections. This is a fixed-sequence thermodynamic computation, not design. Prerequisites: (i) aligning energy conventions, since REV-0001 notes that "Dirks and NUPACK add dangles and terminal penalties"; (ii) the division's code is "unoptimised Python … running times are not performance data"; (iii) Dirks et al. was "not read" (PRIOR_ART A-VII).
- **(a) Synthetic stress tests.** The hardness families I(a,m,B) are synthetic gadget instances with planted bin-packing answers. They can test whether heuristic multi-strand MFE solvers find the tiling optimum. Their scope is worst case only, which the division stresses. The hypotheses hold on loop types of ViennaRNA parameter files per REV-0001; the hardness is not claimed for "published parameter tables as implemented".
- **(a) Ising certificates.** CX-T16 / CX-T28 against Ensemble controls B4-01 and family 5 provide two independent codes (`span_algorithm.py` and `degree2_vs_face.py`) for the same verdicts, which makes a cheap cross-replication.
- **(c) NANUQ.** CX-T7's N* could be fed to NANUQ / NANUQ⁺ implementations with exact concordance factors. This needs a coalescent forward model and is of low relevance to this charter; the division itself calls it "probably of no use".

**3.4 Prior art as recorded.** *Solved elsewhere*: A2 (Shalaby–Woods, arXiv 2611.27945, CX-D1). *Claimed elsewhere*: B1/B2 (unreviewed entry B-II; CX-T6 a "rediscovery in all likelihood"). *Known*: CX-T11 (Shalaby–Woods ICALP 2025), CX-T17 (Deza–Laurent), CX-T18 (Laurent–Poljak 1995/96), Tropp 2018, the base-pair version of CX-T12 (Boehmer–Berkemer–Will–Ponty 2025), and the Lyngsø 2004 gadget ("apparently unpublished" reduction). *Not found*: NN-model multi-strand hardness, CX-T7/T8/T26/T27, CX-T19, CX-T28/T29. External methods named: Dirks et al. (not read), ViennaRNA parameter files (referee only), NANUQ / NANUQ⁺ (Allman–Baños–Rhodes(–Wicke)).

**3.5 Negative results and withdrawals.** `DEAD_ENDS.md` CX-D1…D7:
- D1, D3: the two flagship open problems had moved before work began.
- D2: the NANUQ metric of a general circular split system is not Kalmanson (33 systems at n=6).
- D4: seven false or too-broad sentences, for example "(H0)–(H2) is the sign pattern of every physical parameter set" (false for Turner 2004 bulges).
- D6: "exposed iff no other sign vector in span" is false in general, and co-NP-hardness attempts failed.
- COMPLEXITY-MSG-0003 §1 and -0004 §1 contain 13 corrections of record, mostly about novelty.

**3.6 Requests to engineering.** None ("requests open: none of ours"; no `requests/complexity/` files). The division offers stress-test generators to engineering in MSG-0005 §7.6.

---

## 4. Cross-cutting

### (i) Connections to ensembles, observables and limits
- **Linear averaged observables (Ensemble Part I).** This is the exact mathematical setting of reweighting a finite candidate pool against SAXS intensities, NMR averages or cross-link occupancies. F1/F3 decide whether populations are identified or only interval-bounded, with solver-independent certificates. The theory is valid for any linear forward model. It makes no claim that a forward model is correct, and nonlinear data (unknown scale factors, ratios) are uncovered.
- **Distance distributions (DEER/FRET).** Ensemble Part II (E4, E7, E8) and Geometry Theorem J. These cover exact laws only, with no stability modulus.
- **Averaged squared distances.** Geometry Theorems B, C, G, H, I, I′ (with statewise bond constraints). The nearest real observables are labelled low-angle scattering (block sums; F″ has no instance) and Rg-type sums. Ensemble E1.3 shows that without constraints, mean squared distances identify nothing, consistent with Geometry Prop 3.1.
- **Orbit and moment recovery (cryo-EM/ET idealisation).** Geometry Cor 9.1 / Prop 9.2, for labelled points only.
- **Torsion ensembles.** Ensemble E20′/E20″/E22 and Geometry hinge Theorem M agree after the ED21 correction: competitors live on O(2)^r.
- **Complexity limits that bind the other two divisions.**
  - Checking the cheap ensemble certificate (P1) is co-NP-complete (CX-T29).
  - Exact ground-set recognition is open for K ≫ log n (E-C1).
  - Realizability of averaged distances is NP-hard (G1.23, known), and complete-data realizability equals a Heisenberg ground-state problem (COMPLEXITY-RES-0002).
  - Recovery below the conic threshold is planted MinRank (GEOMETRY-RES-0006): detection is easy, recovery uses a certificate ladder.
  - Identified ≠ certified: 92 % against 0.5 % (n=12, K=9); for Geometry, 10 against 12 atoms (K=2).

### (ii) Questions to send back (five per division)
**Ensemble**
1. Give an identification criterion and F3 intervals when each dataset is known only up to an unknown affine map, y = s·Aμ + b with unknown s > 0 and b (normalisation and background). Is the certified set still an LP or LP-fractional, and what certificate checks it?
2. Pool dependence: for X ⊂ X′ with a forward model L-Lipschitz on a metric space, bound how much the F3 interval on X can move when X is enlarged to an h-net of the continuum. Is there a certified "pool-robust" verdict, as an extension of E17.1(c)?
3. O4: a lower bound on the chimera gap g_∞ for jointly generic conformers on a generically globally rigid graph, in terms of the minimum conformer separation and K. Without it E7/E8 stay at R1.
4. For smooth observables on a continuum (E2.2, modulus at best √τ): give an explicit modulus for the B3 ladder as a function of N and τ that a tool can report, and state when an F3 interval becomes uninformative at a given σ (E17).
5. C2: any rigorous improvement of 1 < α* < 2 for pair data, or a proof that a polynomial-size certificate family of degree 4 succeeds w.h.p. up to c·n with c > 1.

**Geometry**
1. O-15(vi): a perturbation bound for DEMIX and DEMIX-4. Give the smallest singular value of the certificate matrix as a function of (K, n, bond geometry), and the noise level at which K is still recoverable.
2. O-5: a certified lower bound on κ in Theorem G for a stated instance, so that W₂ ≤ √(C‖ΔM‖) becomes numeric.
3. O-14: identifiability thresholds when only block sums ⟨C_a, M⟩ for a given labelling scheme are measured. What is the minimum number of independent block sums for K states, and does Theorem F″ have a realisable instance?
4. Statewise constraints known within ±δ (bond lengths and angles varying between states): does Theorem B survive with a modulus in δ, or is there an O(δ)-sized ambiguity set?
5. O-16: a global stability bound for separation ≤4 data whose constant is within a moderate factor of 1/(2μ), plus an expected-error statement under i.i.d. noise. Evaluate it on deposited Cα traces, not idealised ones.

**Complexity**
1. E-C1 for K ≫ log n: is recognising exact ground-state sets of pair energies co-NP-hard? Alternatively, is there a quasi-polynomial algorithm for K = polylog·n?
2. A3′: is the NN partition function #P-hard at a fixed temperature, and is MFE FPT in the number of species?
3. Average case at K ≈ n (where identification holds and degree-2 certificates fail): does a degree-4 or degree-6 SOS certificate succeed w.h.p.? Is checking it polynomial?
4. The complexity of computing the endpoints of Ensemble F3 intervals on {±1}ⁿ with pair data, as a classification by the graph of observed pairs (polynomial for bounded treewidth; hard in general?).
5. Realizability of averaged squared distances for chains *with fixed bond angles* (MSG-0005 row 7): hardness and approximability. Is the chain order exploitable once angles are fixed?

### (iii) Gaps for benchmarking against contemporary methods
1. **No external comparison has been executed by any of the three divisions.** No public experimental dataset was read or used. Ensemble controls are "verified by their generator only" (OB25). Geometry's stability table uses idealised traces. Complexity's algorithms are reference Python.
2. **Contemporary ensemble methods are absent from all three registers.** A search for SAXS, NMR, FRET, DEER, cryo-EM and cross-linking terms finds only passing mentions (for example "scattering gives one pooled distribution"). The registers do not name maximum-entropy or Bayesian reweighting tools, generative cryo-EM heterogeneity methods, or MD-based ensemble refinement as comparators. The only applied comparator named is Shi–Thirumalai DIMES (Geometry, prior art). For multi-strand folding, Dirks/NUPACK is named but not read.
3. **Forward and noise models are missing everywhere.** The covered noise is bounded or Gaussian error on means. There is nothing for laws, nonlinear data, unknown scale, or correlated model error beyond whitening.
4. **Review depth.** Each division's newest results are unreviewed: Ensemble E15U(A,B,C′), E17.1, E20a, E22; Geometry Theorem I′, L, L⁺, C(c); Complexity CX-T21–T23 and T25–T30. Only Science has reviewed across divisions. There is no peer review.
5. **Execution is pending with engineering.** The only formal requests are GEOMETRY-REQ-0001 (item 1 replication, item 3) and REQ-0006 (accepted per Geometry, result not seen). The benchmark harness for the Ensemble controls has no request ID.
6. **The most immediately runnable evaluations:**
   - Ensemble B1–B7 against reweighting tools via an observable-matrix adapter.
   - Exact cube ground truth (n ≤ 22) as a scale test.
   - DEMIX / DEMIX-4 planted-mixture noise sweeps.
   - Theorem L constants on deposited Cα traces.
   - CX-T12 against a mainstream multi-strand partition-function implementation on small systems with matched energy conventions.
