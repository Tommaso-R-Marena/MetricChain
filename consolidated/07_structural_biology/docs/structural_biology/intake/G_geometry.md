# STRUCTBIO intake — Geometric Inference, Rigidity and Inverse Problems division ("Geometry")

Reviewer: STRUCTBIO research-intake (workstream D). Source: read-only worktree `research/geometric-inference`, head **`288b2def39ae1bba0afabad0151e275b3a5cdbbc`** (2026-11-26 20:10 UTC, "Eighth checkpoint: Theorem L…"); `origin/research/geometric-inference` has the same head. Also read, through read-only `git show` on the remote refs: Science `SCI-REV-0023` (at `71bc661`, 21:49 UTC, after the Geometry head), Science `SCI-RES-0029`, and the Engineering benchmark registry (at `96c4fd2`). Nothing was built. The one script run was `demix.py` (1.1 s, with `-B`). The tree is clean afterwards.

Conventions in this report. Repository labels are copied exactly: **V** machine-checked, **P** paper proof, **P-exact** paper proof plus an exact computation, **K** known, **N** numerical, **C** conjecture. "REV-0001" is the division's *internal* adversarial review: a subagent of the same division, reviewing commit `e8e2582`. It is not independent. "SCI-REV-0021" is the Science division's review of commit `d84a43b`. Science calls it "an internal review by an AI session", not external peer review. **[mine]** marks my own inference or addition.

---

## A. The model

**Model, as stated in the repository.** The setting is fixed in `docs/geometry/ENSEMBLE_RIGIDITY.md` §1.
- There are `n` points ("atoms") in ℝ^d, with d = 3 for chains. "Statewise constraints" form a connected graph E₀ with fixed lengths.
- **Chains:** E₀ = {i,i+1} ∪ {i,i+2}. Bond lengths and 1–3 distances (so bond angles) are fixed. The `n−3` torsions are free. The freely jointed variant has bonds only.
- In most exact results there is **one bond angle at all positions**, with unit bonds: cos −5/13 (112.6°) or −1/3 (tetrahedral). The floating-point default is 111°. Heterogeneous angles are open (O-10).
- An **ensemble** is a Borel probability measure on conformation space. Competitors range over *all* ensembles, not just K-state ones.
- **Hinges** (`HINGE_ENSEMBLES.md`): states share rigid segments and differ in `s` torsions. Competing conformations may mirror a segment at a hinge, which gives the group O(2)^s.
- Scope sentence: "Scope: mathematics of abstract articulated systems. 'Chain' means a sequence of points with prescribed consecutive distances; no sequence, no target, no experiment." `HANDOFF.md`: "Scope: mathematics and synthetic systems only."

**Data types.**
1. **Ensemble-averaged squared distances**, M_ij = ⟨|x_i − x_j|²⟩:
   - all pairs (Theorems A, B, G, I);
   - a pair set F (Theorems E, F);
   - sequence-local bands 3 ≤ |i−j| ≤ w (Theorems H, F′);
   - linear functionals ⟨C_a, M⟩ ("block sums", Theorem F″).
2. **Laws** (one-dimensional distributions) of d_{i,i+3} and d_{i,i+4} (Theorem J).
3. **Single-conformation sequence-local distances**, |i−j| ≤ K (`LOCAL_DATA_STABILITY.md`, Theorems K and L).
4. Second and third moments of randomly rotated labelled coordinates (Corollary 9.1, Proposition 9.2).

**Exact vs noisy.** Identifiability results assume exact data. Quantitative results:
- Theorem G: W₂² ≤ C‖ΔM‖, but its constant κ is not computed.
- Theorem L, Corollary L.1: bounded deterministic noise with explicit constants.
- "No statistics": random-noise or Cramér–Rao bounds are not derived.
- §12: "**The mechanism needs the statewise constraints to hold exactly and identically in all states.** Nothing is proved for bond data known to finite accuracy or varying between states."

**Generic vs instance-specific.**
- Generic: Theorems C, H, I, J and genericity of F′, D(b). "Generic statements exclude a proper analytic subset that we do not describe completely" (O-11). Known excluded sets: planar conformations; **ideal helices** ("(CC), DEMIX and Theorem G never apply to mixtures of ideal helices"); **states that share rigid segments**, "the commonest two-state motions".
- Instance-checkable hypotheses: (CC) as a rank, a stress Ω, τ/D/b for Theorem L, the Jacobian rank of Theorem H.

**Relation to real measurements — the division's own words.** There are only two places.
- §12: "Averaged *squared* distances are one specific linear observable. Nothing here applies to averages of other functions of distance (inverse sixth powers, contact frequencies, scattering curves beyond their low-angle limit); for those the stacked configuration is not a Euclidean framework. Where the observable is measured (low-angle scattering with pairs of labels) the datum is usually a block sum ⟨C, M⟩, not single entries (Science division, SCI-RES-0029 §2)."
- `PRIOR_ART.md` links Example 3.3 to the "virtual structures" of ensemble- and time-averaged NMR restraints (Jardetzky 1980; Torda–Scheek–van Gunsteren 1989, "from memory").

The division asked whether this observable is measured at all (GEOMETRY-REQ-0003: "is there any measurable quantity … an ensemble average of squared distances between labelled sites … or is this observable a mathematical convenience?"). Science answered in SCI-RES-0029 §2, and these are Science's words, not Geometry's:
- the low-angle limit of a two-label interference experiment is "exactly your M_ij";
- the common biomolecular restraints average *other* functions: NOE/PRE ~r⁻⁶, FRET, ³J couplings; "pulsed dipolar spectroscopy returns a whole distance distribution per pair"; RDCs average second-rank tensors of bond directions.

**[mine]** The repository says nothing about cross-linking, cryo-EM maps, SAXS P(r) or CYANA/Xplor restraint sets.
- **NOE upper bounds** are inequalities on ⟨r⁻⁶⟩^{−1/6}. They are not covered by any theorem here, for either the ensemble or the single-structure results.
- **DEER** gives per-pair distributions. Only Theorem J (laws) is of that shape, and it needs *all* separation-3 and separation-4 pairs along the chain. That is not a realistic spin-label design.
- **Single-structure Theorems K and L** are about exact or bounded-error *distances* between point sites. They are the nearest to a "known backbone + distance restraints" use case.

---

## B. Register of main results

Two fields are the same for every row and are not repeated: **(1)** originating division = Geometry, except where noted; **(2)** source commit = `288b2de…`. "Review" quotes the register's review column. Register ids are from `docs/geometry/THEOREM_REGISTER.md`. All Lean names are in namespace `MetricChain.Geometry`, file `proofs/Geometry/EnsembleRigidity.lean`. The status file reports zero `sorry`, a 5110-declaration axiom audit, and "lake build succeeds"; I did not rebuild.

**B1. Theorem A — one conformation, conic criterion** (G1.4; `ENSEMBLE_RIGIDITY.md` §4.1)
- (4) Lean: `sqdist_midpoint_of_conic` covers (iii)⇒(ii) only.
- (5) X spans ℝ^d. The claim: δ_X is identifiable from averaged squared distances ⇔ 𝒩(X) = 0 (constrained edge directions lie on no conic at infinity) ⇔ X is not a midpoint of two non-congruent conformations.
- (6) P. (7) REV-0001: "proved". (8) Tests `affine_flex_midpoint`, `four_atom_mixture`.
- (9) Every 4-atom chain fails (cis/trans, Example 3.3). Planar conformations fail.
- (10) Under ensemble averaging a single conformation can be impersonated by a mixture of affine flexes.
- (11) A 6-column linear system on 2n−3 edge vectors.
- (12) A "can averaged restraints fake this structure?" check. (13) Classical affine-flex/conic-at-infinity theory (Connelly); (ii)⇔(iii) known.
- (14) Useless if the constraints are not exact or the observable is not ⟨r²⟩.
- (15) **Partially**: trivial to code; physical applicability is limited.

**B2. Theorems B / B′ — mixture identifiable among all ensembles** (G1.5, G1.6, G1.7)
- (4) Lean: `mixture_identifiable_stacked`, the coordinates form "against finite competing mixtures". The conclusion is only that each competing state has the distance matrix (`SameShape`) of some X_k. Weights are not treated, and (CC) and spanning are *hypotheses*. Also `finite_mixture_identifiable`, `mixture_state_of_conic`, `block_rigidity`, `state_is_linear_image`, `exists_linearMap_of_gram_eq`, `stacked_sqdist`. Non-vacuity: `line_mixture_example`, a 1-D two-state instance (`line_conic`, `line_span`, `line_states_differ`).
- (5) K-state mixture with stacked configuration z ∈ (ℝ^{3K})^n. **(CC)**: dim 𝒩(z) = K−1, i.e. only trivial quadrics. B′ is an exact barycentric-uniqueness criterion on 𝒫(z).
- (6) P. Finite competitors V as above. Arbitrary (L²) competitors, weights and B′ are paper only.
- (7) REV-0001 proved it, after 14,640 falsification starts. SCI-REV-0021 "proved as stated; replicated for K ≤ 3"; F1 says (CC) is "sufficient, not necessary".
- (8) `trivial_quadrics_only`, `demix_recovers`.
- (9) (CC) fails for helices, planar states and shared-segment pairs with ≤ 3 differing torsions. Any ensemble with a continuous part is "never identifiable" (Cor 4.2 complement (c)).
- (10) Discrete-state ensembles are uniquely determined by mean-square distances when bond geometry is exactly fixed.
- (11) Rank of a (2n−3) × (9K²+3K)/2 linear system.
- (12) Uniqueness certificate for a mixture model. (13) Novelty: d = 1 is **known** (Laurent–Poljak 1996 via Tropp 2018, found by SCI-REV-0021 F3). The rank-d extension is "not found".
- (14) Useless for continuous ensembles, inexact geometry, or observables other than ⟨r²⟩.
- (15) **Partially**: the certificate is implementable, but physical validity of the inputs is unproven.

**B3. Theorem C — sharp (CC) thresholds** (G1.8–G1.11)
- (4) None.
- (5) Generic K-tuples. (a) Freely jointed chains: n−1 ≥ (9K²+K+2)/2. (b) Bond lengths and angles: n ≥ ⌈(9K²+K+8)/4⌉ = 5, 12, 23, 39, … (c) Concavity of the generic rank r_N, which gives (CC) for n ≥ (9K²−5K+6)/2 for every K and every bond angle. (d) The sharp threshold for all K.
- (6) (a) P. (b) **P-exact**, for K ≤ 20 at cos −5/13 and K ≤ 12 tetrahedral. (c) P. (d) **C**.
- (7) (a), (b) REV-0001 proved, replicated exactly K ≤ 12. (c), present form: "**not reviewed**". (d) "could not falsify".
- (8) `exact_conic_rank.py` (48 witnesses for K ≤ 12 plus 8 for K = 13–20); `conic_threshold_float`.
- (9) O-1 reduces (d) to "the last increment is 2".
- (10) Minimum chain length for which linear-algebra demixing is possible: 12 atoms for 2 states, 23 for 3.
- (11) Modular rank. (12) Design rule for experiments or benchmarks. (13) None found.
- (14) Generic only, so says nothing about a given instance (use the B2 rank instead). Homogeneous geometry only.
- (15) **No** (as a tool); yes as benchmark parameters.

**B4. DEMIX, Proposition 6.1** (G1.12) — see C1. (6) P. (7) REV-0001 proved; independent re-implementation; the soundness for every realizable input is the referee's (m10). (9) DG-7: automatic K-detection fails at noise 10⁻⁴. "No stability claim is made for the algorithm". (15) **Partially**.

**B5. Theorems F / F′ / F″ — stress certificates; sequence-local averaged data** (G1.13, G1.14, G3.6)
- (4) Core V: `stress_certificate`, `stress_energy_eq`, `mixture_energy_eq` (first half of the proof, finite mixtures).
- (5) F: (CC) holds, plus Ω ⪰ 0, Ω𝟙 = 0, support on F ∪ E₀, ker Ω = span(𝟙, z). F′: (CC) plus every 3K+1 consecutive stacked points affinely independent, which is generic; separation 3K+1 then suffices. F″ is for block sums.
- (6) P. (7) F: REV-0001 proved; instances are the referee's. F′: proved; the genericity proof is "not reviewed". F″: "not reviewed".
- (8) The referee's SDP `review1/k_stress.py` (cvxpy): stresses exist for bands ≤ 7 and ≤ 8 at n = 14, 16. None exist within separation 3K. F″ has no instance (O-14).
- (9) No stress supported within separation 3K, so on band data F never beats F′.
- (10) Certificate for scattered measured pairs. For K = 1 it is the classical universal-rigidity (super-stability) certificate.
- (11) SDP, then an exact rational LDLᵀ check (Theory's suggestion T1). (12) Checkable identifiability certificate for incomplete data. (13) K = 1 is Connelly's condition; K ≥ 2 "not found".
- (15) **Partially**: SDP code exists only in the referee folder; an exact checker is not written.

**B6. Theorems G / G′ — global W₂ stability** (G1.15, G1.15′)
- (4) None (O-7(e)).
- (5) (CC), or for G′ the hypotheses (H), (H′), (J). Smooth conformation space. Certificate φ(X) = ‖Π^⊥X‖².
- (6) P. G′ for two states P-exact via Theorems I and H.
- (7) REV-0001 proved (a)–(e), with one false constant corrected. SCI-REV-0021: "(c)–(d) are existence statements until κ is bounded (F2)". G′: REV-0001 read the statement only.
- (8) κ is **2–12× smaller than its local values**; the constant √(n−1−3K)/(2κ) is **47–570** in six instances.
- (9) Exponent ½ is sharp: state broadening by ε is invisible at order ε.
- (10) Converts mean-square distance error into ensemble transport error.
- (11) Global lower bound of φ/min_k d_P² over torsion space; not done (O-5).
- (12) Quantitative uncertainty for ensembles. (13) Mechanism known (Fernandez-Granda 2013 dual certificate).
- (14) The division says of κ: "a general theorem whose guarantee is computationally empty until κ is bounded".
- (15) **No**, until a certified κ exists.

**B7. Theorems D, E — realizability; second-moment rigidity hierarchy** (G1.16–18, G1.24)
- (4) `globallyRigid_of_secondMomentRigid`, `secondMomentRigid_of_universal`, `universal_not_secondMomentRigid` (the necessity of (C₁)).
- (5) D: 𝒦 = 𝒮 iff |E₀| ≤ 9 (n ≤ 6), strict from n = 7. E: (universal rigidity ∧ 𝒩(X)=0) ⇒ second-moment rigid ⇒ (global rigidity ∧ 𝒩(X)=0).
- (6) D(a) P from K; D(b) P-exact; E P with two V steps; E(d) strictness P-exact; G1.24 N (requested certification GEOMETRY-REQ-0006, not delivered).
- (7) REV-0001 proved. M1 found the summary slogan false without (C₁) (DG-13). M3: the referee filled a gap with an exact witness.
- (10) A rigidity notion for averaged restraints. (12) A classifier: for n ≤ 6 the SDP feasibility test is exact. (13) Universal/global rigidity literature.
- (14) Small n only for the exact equivalence.
- (15) **No** (conceptual), except the D(a) SDP test for tiny systems.

**B8. Theorem H — local identifiability within K-state ensembles** (G1.19, G1.20)
- (5) Unit bonds, cos −5/13 or −1/3. Complete data: full Jacobian rank iff n ≥ 2K+3. Bands F_w: w ≥ K+3 suffices for n ≥ (K²+3K+4)/2; for K ≥ 2, w ≤ K+2 never suffices.
- (6) P-exact, K ≤ 8. (7) REV-0001: proved given base cases; M2 overstatements corrected.
- (8) `exact_jacobian_rank.py 8` (about 3 s). (9) Local only. At n = 7, 8 (two states) the ensemble is locally unique among two-state ensembles, yet non-identifiable globally (DG-10).
- (10) Each extra state costs one unit of sequence range. (11) Jacobian rank (instance-checkable).
- (12) Local-identifiability test. (14) Useless as a global guarantee.
- (15) **Partially**: the per-instance Jacobian rank is implementable.

**B9. Theorem I — two states from 10 atoms** (G1.25, G1.26, G1.21)
- (5) Generic pairs, cos −5/13 or generic geometry, n ≥ 10. 𝒫(z) = {E₁/w₁, E₂/w₂}, even over ℂ.
- (6) P-exact: Singular Gröbner basis over ℚ, degree 7 = 1+1+5. G1.26 (failure at n = 7, 8) is N. G1.21 (⌊9K/2⌋+1) is N/C.
- (7) REV-0001 proved and replicated independently. Engineering's replication (REQ-0001, Q-12) was "in progress" at engineering `96c4fd2`.
- (11) Singular; not in the harness default.
- (14) Excludes shared-segment pairs and helices.
- (15) **No** (a generic theorem); its gap shows linear certificates are conservative.

**B10. Theorem J — laws of separations 3 and 4** (G1.27)
- (1) Geometry, applying the **Ensemble division's** E5/E6, which are unrefereed.
- (5) Generic finite ensembles, any K, laws of d_{i,i+3} and d_{i,i+4}. A single separation never suffices.
- (6) P, given E5/E6. (7) REV-0001: correct given E5/E6, which it did not read.
- (8) `matroid_connectivity.py` (exact, mod p). (10) The closest result to DEER-style data (distributions).
- (14) Needs every i,i+3 and i,i+4 law.
- (15) **Partially**: the matroid test is implementable as design guidance.

**B11. Theorem K — lower bounds for sequence-local single-structure data** (G2.1–G2.4)
- (5) (a) Any configuration: s₇² ≤ (5π²/3)K(K+1)(2K+1)/n², so C_inf ≥ n/(10K^{3/2}). (b) A torsion move changes range-K distances by ≤ 2 sin(δ/2) b √T_K. (c) Tube or ideal helix: C_inf ≥ h²n²/(139ρbK^{3/2}). Corollary K.1: a length-independent constant needs K ≳ n^{2/3}; on helices no pair set has one.
- (6) P; the exact helix scaling is N. (7) "not reviewed".
- SCI-REV-0023: (a) is "a direct corollary of a printed statement" (Lew–Nevo–Peled–Raz, with a 2.5× better constant).
- (8) `local_data_bounds.py`; tests `local_data_bound_a/b`, `helix_beam_law`, `tube_bound_helix`.
- (10) Backbone-local restraints cannot pin global shape on extended or helical segments.
- (11) SVD of the rigidity matrix. (12) Underdetermination detector (softest mode). (13) Algebraic connectivity, beam/truss theory.
- (15) **Yes** for the computed s₇ / C_inf. The bounds are explanatory.

**B12. Theorem L — global n² upper bound** (G2.5, G2.6; Corollaries L.1, L.2)
- (5) Any n ≥ 5 points in ℝ³ with τ = min_i σ_min(window edge matrix) > 0. Y is any configuration with |η_jk| ≤ τ⁴/(73D²) for |j−k| ≤ 4. Then min_g‖Y−gX‖_F ≤ 6.9(b/τ²)n(n+1)‖η‖₂ (η over separations ≤ 3). L.1: any estimator that fits as well as the truth is within 13.8(b/τ²)n(n+1)‖ε‖₂.
- (6) P. (7) Register: "not reviewed". **SCI-REV-0023** is a *prior-art and relevance* review only: "Nobody in this division reviewed the proof of Theorem L".
- (8) `local_data_upper.py`: 360 pairs; left/right ≤ 0.0022. Tests `local_procrustes_lemma`, `theorem_L_instances`.
- (9) (S) cannot be dropped (tail reflection).
- (10) Errors of overlapping frames add rather than multiply.
- (11) O(n) evaluation from coordinates.
- (12) An explicit per-instance a-priori bound. (13) Arias-Castro–Vishwanath (exponential); thin-rod geometric rigidity (Mora–Müller etc., per SCI-REV-0023).
- (14) **Vacuous at realistic geometries (SCI-REV-0023 §5).** On an α-helix Cα trace, (S) requires distance errors ≈ 1.3·10⁻⁴ Å. At the threshold the RMSD guarantee exceeds Rg from about 16 residues on (295 Å vs Rg 43 Å at n = 100). (S) sits 10⁴–10⁶ below the reflection limit G = min_i 4|h⁻h⁺|.
- (15) **Partially**: trivial to implement, but only useful as an exponent/scaling statement.

**B13. Hinge ensembles, Theorem M, Proposition M2** (G3.1–G3.5)
- (1) **Science division first** (Proposition R22-1, SCI-REV-0021; one hinge is Science's SCI-RES-0029). Geometry gave an independent second derivation and added: the reduction M2, the sharp half-turn criterion, all s ≥ 2, and the exact count.
- (5) Two states, conic-free segments (≥ 5 atoms, generic). One hinge: never identifiable. Two hinges: exactly 8 candidates (a cube of mirrored assemblies), identifiable iff at most one of R₁, R₂, R₁R₂ is a half-turn. s ≥ 2: identifiable.
- (6) P; the counts 8 and 2 are P-exact (Singular). (7) "two independent derivations agree". G3.4 and G3.5 are "not reviewed".
- (8) `hinge_pairs.py`, `exact_hinge_candidates.py`, `hinge_halfturns.py`, `hinge_multistate.py`.
- (9) Three states at two hinges can fail (one explicit instance, N). Segments of ≤ 4 atoms are not covered.
- (10) **The most biology-shaped result**: hinge/domain motions. Mirrored-domain "ghosts" are an analogue of the RDC ambiguity.
- (11) Closed-form candidates plus an LP.
- (12) Instance-level uniqueness check for two-state hinge models. (13) DMDGP reflection branching; Curto–Fialkow moment problems.
- (14) Needs exact rigid segments and the ⟨r²⟩ observable; there is no stability theorem (O-13).
- (15) **Partially**.

**B14. Smaller items.**
- G1.28 kink formula and "torsion sharpness" (GEOMETRY-RES-0002): P in the rod model plus N; not reviewed.
- G1.22 / G1.29 (Corollary 9.1, Proposition 9.2): moments of randomly rotated labelled data, an MRA/cryo-EM-style model. Cor 9.1 is P conditional on a cited sample-complexity theorem that was not re-derived (O-9). Prop 9.2 is P, checked on paper only.
- G1.23 (NP-hardness of realizability): K.
- None of these is implementation-ready.

---

## C. What software could implement today

| # | capability (source) | input → output | complexity | arithmetic | status |
|---|---|---|---|---|---|
| C1 | **DEMIX** (Prop 6.1; `demix.py`) | M (n×n), E₀ pairs + lengths, optional K → K, weights, states, certificate: nullity = K−1, s*, eigen-gap | one n×n eigendecomposition; SVD of (2n−3)×(3K(3K+1)/2); one 3K×3K eigenproblem | float. The rank certificate is sound only for exact realizable input; under noise it is "reported, not enforced" | runs (demo n ≤ 48, 1 s). At noise 10⁻⁴ the state RMSD reaches 0.71 (K=4, n=39), governed by s* ≈ 10⁻³–10⁻¹ |
| C2 | **Instance (CC) / conic-rank test** (Thms A, B; `exact_conic_rank.py`, `conic_matrix`) | conformation(s) or stacked z → dim 𝒩 | linear algebra | exact for rational coordinates via `Mod`/`rank_mod_p`. Full rank mod p proves full rank over ℚ; deficiency mod p proves nothing | code exists (generator tied to its own exact chain builder) |
| C3 | **Stress certificate** (Thm F; referee `k_stress.py`) | z, measured pairs → Ω ⪰ 0 with prescribed kernel, or none | SDP plus exact verification | SDP float (cvxpy); exact LDLᵀ check proposed, not written | partial |
| C4 | **Jacobian local-identifiability test** (Thm H; `exact_jacobian_rank.py`) | torsions, weights, pair set → full column rank? | (pairs)×(K(n−3)+K−1) | exact mod p at rational witnesses | exists for synthetic witnesses |
| C5 | **Rigidity-matrix stability** (Thm K; `local_data_bounds.rigidity_matrix`) | X, pair set → s₇, C_inf = 1/s₇, softest mode | SVD of |F|×3n | float | exists; standard (cf. normal-mode / FIRST-style analyses **[mine]**) |
| C6 | **Theorem L bound** (`local_data_upper.theorem_L_sides`) | X (and an optional Y or noise level) → τ, D, b, threshold (S), global bound | O(n) | float (could be exact) | exists; vacuous constants |
| C7 | **Hinge cube + LP** (Thm M; `hinge_pairs.cube_candidates`, `lp_unique`, `hinge_halfturns.py`) | two states, hinge indices, M → 8 candidates, weight ranges | constant per hinge pair plus a small LP | float (Singular for exact counts) | exists for two states |
| C8 | **Matroid connectivity of a measurement pattern** (Thm J; `matroid_connectivity.py`) | n, pattern → connected/free | modular rank | exact mod p | exists |
| C9 | **Certificate φ, local κ** (Thm G) | z → φ(X) = −½⟨Π^⊥, D(X)⟩; local κ as an eigenvalue | linear | float | computable, but **not a bound** (the global κ is 2–12× smaller) |

**Existence or generic statements only:** Theorem C thresholds, Theorem I and G1.21, Theorem D(b), Theorem E(d), G1.24, Theorem J genericity, Corollary 9.1, Theorems G(c)–(d) without a certified κ.

**[mine]** For real PDB data the key mismatch is that C1, C2, C3, C7 assume bond lengths and angles that are *identical across states and exactly known*. Deposited coordinates (3 decimals, refined against force-field restraints) satisfy this only approximately. The exact rank tests would then certify a slightly different, perturbed model, and no theorem here covers that perturbation. This is not proved anywhere; §12 says only that "nothing is proved".

---

## D. Code inventory

**`experiments/geometry/geomlib.py`** (193 lines; numpy and `fractions`). Read in full. Its API:
- `chain(n, tors, b=1.0, theta=111°)`: NeRF builder; homogeneous b and θ only.
- `edm(X)`; `stack(Xs, w)`, which gives z_i = (√w_k x_i^{(k)}).
- `sym_index(m)`, `quad_row(v, idx)`, `sym_from_vec(vec, m, idx)`: upper-triangle coordinates of quadrics.
- `edge_vectors(Z, angles=True)`: bonds plus 1–3 vectors. `conic_matrix(Z, angles)`: the conic system.
- `kabsch_rmsd(A, B, allow_reflection=True)`.
- Exact arithmetic: `rat_circle(t)` (rational cos/sin from half-angle tangents); `cross`; `chain_exact(n, tors_t, cth, sth)` over any field; `Mod` (𝔽_p, p = 2147483629); `rank_mod_p(rows, p)` (int64 Gaussian elimination); `tonelli(a, p)` (modular square root, used for ℚ(√2)).
- Torsion convention: torsion m is the dihedral of atoms m..m+3, 0-based.
- Not a package: no tests of its own, no type checks, no heterogeneous geometry, no I/O for PDB.

**Other scripts.** Runtimes are from `HANDOFF.md`. All are numpy/scipy or stdlib; three need **Singular**: `exact_nonlinear_threshold.py`, `exact_hinge_candidates.py`, and test `hinge_candidates_exact`.
- `run_checks.py`: 41 tests, about 50 s. `mutation_checks.py`: 29 planted errors.
- `experiments/geometry/README.md` is stale ("31 tests", "19 planted errors").
- Exact: `exact_conic_rank.py` (K ≤ 12: 35 s; K ≤ 20: 3 min), `exact_jacobian_rank.py` (3 s), `exact_4d_extreme.py`, `exact_hierarchy_witness.py` (Fractions), `exact_general_position.py`, `exact_nonlinear_threshold.py` (80 s over ℚ), `matroid_connectivity.py`.
- Float: `demix.py` (1 s, measured); `explore_below.py` (LP over sampled 𝒫(z)); `hierarchy_example.py`; `er_not_ur_instance.py` (3 min); `explore_er2/3.py`; `hinge_pairs.py` (2–3 min); `hinge_multistate.py` (2 min); `hinge_halfturns.py`; `hinge_fourier_rank.py`; `local_data_bounds.py`, `local_data_stability.py`, `local_data_upper.py`; `torsion_sharpness.py` (slow part (2)); `third_moment.py`; `explore_jacobian/spurious/misc.py`.

**`review1/`** holds the internal referee's own code (`mylib.py`; nothing imported from the division), preserved unmodified. It checked:
- the nullity formula, with 0 mismatches across 16 bond angles and heterogeneous bonds/angles;
- exact conic ranks for K ≤ 12 at four rational geometries;
- a falsification search on Theorem B (thousands of Levenberg–Marquardt starts at n = 12–14; every converged fit was the true ensemble);
- 𝒫(z) plus LP: alternatives at n = 7, 8 and at K = 3, n = 13 (saved as `alt_*.npz`);
- Theorem I via its own Macaulay matrices and Singular (degree 7);
- κ attacks (`d_certificate.py`), Theorem H at 60 digits, DEMIX re-implementation, the SDP stresses (`k_stress.py`, needs cvxpy), helices (`m_helix.py`), and a Lean copy compile.

Verdict: "No stated theorem was found to be false"; 4 major and 16 minor findings, all acted on. Not checked by the referee: anything after `e8e2582` (Theorems G′, K, L, M; the present form of C(c)), K = 4–8 base cases of Theorem H, and certified κ.

**Reuse potential [mine].**
- High: `conic_matrix` + `rank_mod_p` (exact instance certificates); `demix` (reference implementation); `rigidity_matrix` / `thickness` / `d_procrustes`; the `cube_candidates` + `lp_unique` hinge code.
- Needed: heterogeneous bond geometry, PDB ingestion, interval/rational certification, a noise-aware DEMIX (DG-7), and a written exact stress checker.

---

## E. Dead ends, obligations, limitations, inter-division traffic

**Dead ends** (`DEAD_ENDS.md` DG-1…DG-20). Most relevant to STRUCTBIO:
- DG-1: no window/Hall count characterises generic rigidity of chains with distance bars; it is "exactly as hard as generic rigidity in three dimensions".
- DG-3: the PSD-stress Hölder-½ bound is known (Sturm; Drusvyatskiy–Pataki–Wolkowicz).
- DG-4: n² beam scaling for trilateration is known in substance.
- DG-7: DEMIX auto-K fails under noise 10⁻⁴.
- DG-9, DG-10: heuristic counts mislead; local ≠ global identifiability.
- DG-13: the false slogan "universal ⇒ second-moment rigidity".
- DG-19: an unproved exponent was published.
- DG-20: priority loss to Science, and a returned paper (Tropp) not read before being called a "relative".

**Open obligations** (`PROOF_OBLIGATIONS.md`):
- O-1: sharp threshold for all K.
- O-2: K ≥ 3 below (CC); n = 9 for two states; a proof of non-identifiability at 7–8.
- O-3: certified "second-moment rigid, not universally rigid".
- O-4: optimal separation among all ensembles.
- **O-5: certified κ.**
- O-6: Theorem H for all K.
- O-7: Lean gaps (weights, L² ensembles, B′, G, and (CC) for 3-D chains).
- O-8: measure theory.
- O-9: the sample-complexity citation.
- O-10: heterogeneous angles.
- O-11: genericity sets.
- O-12 to O-14: more hinge states, a hinge dual certificate or stability theorem, an instance of F″.

**Limitations as stated.** §12 of `ENSEMBLE_RIGIDITY.md`, `LOCAL_DATA_STABILITY.md` §6 ("constants are loose by two to three orders of magnitude"; (S) "is 6·10⁻⁶ for a typical random chain"; "no statistics"; compact chains not studied), and `HINGE_ENSEMBLES.md` §6.

**Requests and messages.** Status column as of `288b2de` unless stated.

| id | to/from | subject | status |
|---|---|---|---|
| GEOMETRY-REQ-0001 | → Engineering | (1) exact elimination K=2, n=10, superseded by the division's own Theorem I: the expected "two reduced points" was wrong (degree 7, DG-9); (2) certified optimum; (3) replication of exact ranks | "proposed / item 1 superseded". At Engineering `96c4fd2` registered as **Q-12, "in progress (independent subagent)"**; reply drafted in `ENG-MSG-0007.draft.md` with a placeholder `<<GEOMETRY RESULT>>`, not delivered |
| GEOMETRY-REQ-0006 | → Engineering | interval branch-and-bound certification of instance A (second-moment rigid, not universally rigid) | proposed; **no Engineering response found** |
| GEOMETRY-REQ-0002 / RES-0001, RES-0005 | ↔ Ensemble | division of labour; Theorem J; body counts | completed in part |
| GEOMETRY-REQ-0003 → SCI-RES-0029, **SCI-REV-0021** | ↔ Science | review of B, B′, G; prior art; assumption audit | review done; F1–F10 applied (RES-0004); **R22-GEO-3 (short segments), -4 (certified κ), -5 (hinge stability) open** |
| GEOMETRY-REQ-0004 / COMPLEXITY-RES-0002 | ↔ Complexity | complexity of realizability; identifiability–certification gap | **planted model owed** by Geometry |
| GEOMETRY-REQ-0005 / THY-MSG-0018 | ↔ Theory | exact stress checking (answer T1: rational LDLᵀ) | acknowledged; follow-ups not started |
| GEOMETRY-MSG-0007 §1 → **SCI-REV-0023** | Science → Geometry (21:48 UTC, **after the Geometry head**) | independent prior-art check of Theorem L | **delivered, unanswered**. Six requests A4-GEO-1…6 open, plus question 1 (threshold of order 4\|h⁻h⁺\|) |

**SCI-REV-0023 verdict, verbatim headline:** "Theorem L was not found in print, but neither its mechanism nor its exponent is new: both are those of the geometric rigidity estimate in a thin rod, and each step of your proof idea is printed for lattices. Your sentence 'the published perturbation bound for this situation is exponential in n' needs an amendment — polynomial first-order bounds for chains of simplices are in print."
- Category: "known in a different setting, the transfer not in print".
- What may be claimed: "a discrete, distance-data version of the thin-rod geometric rigidity estimate, which we did not find stated; it replaces the exponential constant of the published global bound for band lateration graphs by n⁴ (squared error) under a uniform non-degeneracy assumption".
- Theorem K(a) is "a direct corollary of a printed statement".
- Four corrections to Geometry's reading of Arias-Castro–Vishwanath (equation numbers, the "not tight" quote, quantitativeness, a journal version).
- Unread items: Schrader 1967 and Luo–Wu 2011.
- The proofs of K and L were not reviewed by anyone outside Geometry.

**Engineering benchmark requests to Geometry:** none found. The Geometry status file says "Engineering: nothing addressed to this division at `c81166b`". The Engineering registry row "ensemble, geometry, complexity — branches not yet published at the last fetch" is stale.

---

## F. Prior art identified, and novelty verdicts

Verdicts below are the division's (`PRIOR_ART.md`) and Science's. Almost all prior-art statements are "summary level" or "from memory" unless marked as read.
- **Distance geometry / EDM:** the stacking lemma is Schoenberg/folklore (K). Classical scaling (Torgerson) is used in DEMIX.
- **Universal rigidity, stress matrices, conics at infinity:** Connelly 1982/2005, Alfakih, Gortler–Thurston 2014, Connelly–Gortler 2015. Theorem A (ii)⇔(iii) and Theorem F for K = 1 are known; the reading "(i)" is a reinterpretation.
- **Global rigidity:** Gortler–Healy–Thurston 2010, used in E(d).
- **Spectrahedra / elliptope:**
  - Barvinok 1995 and Pataki 1998 give D(a).
  - Grone–Pierce–Watkins and Li–Tam give the freely jointed case.
  - E.-Nagy–Laurent–Varvitsiotis: NP-hardness (K); "extreme Gram dimension" does not cover chain patterns (SCI-REV-0021 F9).
  - **Laurent–Poljak 1996 via Tropp 2018 is Theorem B at d = 1** (found by Science).
  - Saunderson–Chandrasekaran–Parrilo–Willsky on ellipsoid fitting (related).
- **Dual certificates:** Fernandez-Granda 2013, the mechanism of G(b)–(c).
- **Trilateration / lateration:** Zhu–So–Ye 2010 (F′ is an "application"); Arias-Castro–Vishwanath 2023/25 (exponential); Moore et al. 2004 (flips). Per SCI-REV-0023 also Daitch–Spielman, Kyng–Peng–Schwieterman–Zhang, Lew–Nevo–Peled–Raz, Aspnes et al. 2006, Mora–Müller 2003, Blanchard–Griso, Alicandro–Lazzaroni–Palombaro, Schmidt–Zeman.
- **DGP/DMDGP branch-and-prune:** mentioned only in passing ("reflection branching in discretizable distance geometry [K, from memory]"; Theorem L "may be folklore … in the literature on discretizable distance geometry"). No Lavor/Liberti/Mucherino work is cited or compared. **[mine]** DMDGP's 2^k reflection-symmetry results are the obvious comparator for Theorem L's (S) and for Theorem M's mirror candidates.
- **Body-bar / body-hinge, molecular conjecture:** only in GEOMETRY-RES-0005, which mentions Tay's body–bar matroid and Connelly–Jordán–Whiteley. The **molecular conjecture (Katoh–Tanigawa), FIRST, KINARI and pebble-game protein rigidity are never mentioned**. **[mine]** They are the established software competitors for "which parts of a protein are rigid/flexible".
- **NMR structure calculation** (CYANA, Xplor-NIH, ensemble/time-averaged refinement): only the "virtual structures" remark (Jardetzky, Torda–Scheek–van Gunsteren, from memory).
- **Other related work:** Hi-C/diploid genome identifiability (Belyaeva–Kubjas–Sun–Uhler; Cifuentes et al.), DIMES (Shi–Thirumalai), multi-reference alignment (Bandeira et al.; Bendory–Edidin), and RDC "ghost orientations".
- **"Not found":** rank-d B/B′ for general constraints, Theorem C, DEMIX, F (K ≥ 2), E as a notion, D for chains, H, I, M (but Science first), and L ("transfer not in print"). Every "not found" rests on 13 summary-level web searches. The division's own lesson (DG-20): "An absence in searches is not a proof of novelty."

---

## G. My assessment for STRUCTBIO (all **[mine]**)

**G-1. Local-distance observability and underdetermination analyser (from C5 + C6 + Theorem K + Theorem J's pattern test).**
- *Function:* given a PDB backbone (Cα or N-Cα-C) and a set of observed pairs with error bars, compute:
  - rigidity-matrix s₇ and its softest modes, i.e. directions the data cannot see;
  - the Theorem-L thickness τ_i per window and the mirror gaps 4|h⁻h⁺| (SCI-REV-0023 §5), which flag where handedness is resolvable at the stated error;
  - matroid connectivity of the pattern (Theorem J).
  This directly serves "detection of underdetermined structural information".
- *Validation:*
  - L0: harness tests.
  - L1: synthetic helices and coils (known n² law).
  - L2: perturbed ideal SS elements.
  - L3: CATH/PDB domains with Cα–Cα windows.
  - L4: predicted mobile regions vs B-factors, HDX or NMR order parameters on held-out sets.
  - L5: deposited NMR restraint sets (BMRB/PDB), asking whether restraint-poor regions are the soft modes.
- *Useless if:* the analysis is only infinitesimal (s₇ is local). The global Theorem-L bound is vacuous at sub-Å noise. NOE bounds are r⁻⁶-averaged *inequalities*, not distances. Competing tools (FIRST/KINARI, ENM normal modes, DMDGP feasibility) already give the same flexibility map.

**G-2. Exact instance certificate for discrete-state ensembles from mean-square distances (C1 + C2 + C3, with C7 for hinges).**
- *Function:* given candidate states and a pair set, decide exactly (rational/modular) whether (CC) or a stress certificate holds, i.e. whether no other ensemble of conformations with identical bond geometry can reproduce the averaged ⟨r²⟩. For hinge (domain) motions, enumerate the 8 mirror assemblies and solve the LP.
- *Validation:* L0–L2 are ready (the division's and the referee's scripts, including saved counter-ensembles `alt_*.npz`). L3: PDB apo/holo pairs as two-state hinge ensembles (exact model). L5 has essentially no matching data: ⟨r²⟩ is measured only by labelled low-angle scattering (Science), as block sums, which needs F″ (no instance yet).
- *Useless if:* the physical observable is r⁻⁶, FRET efficiency or DEER distributions; bond geometry varies between states (always true in deposited structures); the ensemble has any continuous spread ("never identifiable"); or the states are helical or share segments without satisfying M's hypotheses.
- *Value:* mainly as an **assumption-violation demonstrator and benchmark generator** (generic vs instance-specific, local vs global, the 7/10/12 thresholds), not as a production tool.

**G-3. Benchmark suite of hard negative and positive instances** (lowest cost, highest certainty).
- *Contents:*
  - exact witnesses: rank-4 extreme chain, hierarchy witness, Theorem I degree 7;
  - numerically explicit competing ensembles at n = 7, 8 and K = 3, n = 13;
  - the hinge half-turn competitors;
  - the tail-reflection counterexample to dropping separation-4 data;
  - helix families where (CC) fails.
- *Use:* these test any STRUCTBIO uniqueness/uncertainty claim for false positives. Validation is L0–L2 by construction.
- *Useless if:* someone expects them to transfer to deposited structures without the exact-geometry caveat.

**G-4 (conditional). Certified ensemble uncertainty via Theorem G / G′.** Not implementable until O-5 (certified κ) is done; observed constants of 47–570 suggest the bounds will be loose. Defer.

**Bottom line.** The division's work is rigorous and carefully labelled, with honest error records. But it is built on two idealisations that real data violate:
1. exact, state-independent bond geometry;
2. the observable ⟨r²⟩, or exact distances.

The single-structure local-data results (K, L) are the closest to protein use, and Science has shown that Theorem L's constants are vacuous at physical noise. The near-term STRUCTBIO yield is an observability/underdetermination analyser plus a certified benchmark corpus, not a deployable uniqueness certifier for experimental restraints.
