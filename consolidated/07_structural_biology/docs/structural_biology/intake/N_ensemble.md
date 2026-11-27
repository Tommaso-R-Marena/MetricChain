# STRUCTBIO intake N — Ensemble Identifiability and Certified Inference Division

Reviewer: STRUCTBIO research intake (workstream C, conformational ensemble inference). Read-only review.
Source: branch `research/ensemble-identifiability`, head **`8d42f609b8bd16a308275cf68856f3cf0460a6e1`** ("[ENS] Certified modulus on the torus (E20''), the permanent certificate for K states (E21), Gaussian control; audit passed"). Earlier report versions: v1 `a570520`, v2 `1a067b5`. Paths below are relative to the worktree root. I did not run `lake build`. I could not re-run any Python either, because `scipy` is not installed in this container. Every number I quote comes from the recorded outputs `experiments/ensemble/output.txt` and `output_threshold.txt`.

Labels are the repository's own: **[V]** Lean-checked (the declaration is named), **[P]** paper proof, **[K]** known/cited, **[N]** numerical, **[C]** conjecture. "Internal review" means review by an AI subagent of the same division; it is not peer review. Text marked **(my inference)** or **(STRUCTBIO addition)** is mine.

---

## 0. Bottom line

* The division has a coherent **exact, finite-dimensional, linear-information theory** of ensemble identifiability. Its one-sentence thesis is: on a finite configuration space, an ensemble is determined by the means of observables **iff** its support is the *whole* zero set of a non-negative function in their span **and** the features are affinely independent on that support (E1). It also gives stability constants, partial-identification intervals with a near-minimax estimator (E17), and capacity thresholds (how many conformers pair or k-body data can resolve).
* **What is machine-checked:** only the finite-X sufficiency/stability inequalities and combinatorial cores, namely 24 headline theorems plus 7 non-vacuity witnesses in 5 Lean modules. Every passage to continuous spaces, tori and real observables is a paper proof.
* **Review:** Parts I–III (E1–E12) passed one internal AI review (ER1): no numbered statement was false, but 5 major and 13 minor defects in the surrounding prose, all applied. Parts IV–V, E2.2, E7′ and §4.4 are under a second internal review that has not reported. **Part VI (E18–E21, the torus and torsion-angle results most relevant to STRUCTBIO) has been read by nobody but its author.** There has been no external review.
* **Bridge to experiment: essentially absent, and the division says so explicitly.** The report itself says: "What is *not* in this report: anything about real instruments; algorithms with complexity guarantees" (`ENSEMBLE_REPORT.md` §0).
* **No requests to engineering.** `docs/collaboration/requests/ensemble/` is empty, and ENSEMBLE-MSG-0002 says "To Engineering (E-E1). No request now." The division has stated no wish for software or benchmarks.
* **Prior-art gap relevant to us:** the division did not search maximum-entropy, BME or EROS ensemble refinement, nor Kruskal-type tensor identifiability. `PRIOR_ART.md` §6 lists as not yet searched: "the literature on maximum-occurrence and ensemble refinement in structural biology for a uniqueness theorem of the form E7".

---

## A. The model

**What an ensemble is** (`ENSEMBLE_REPORT.md` §1; `docs/ensemble/README.md` "Mandate"):
* An ensemble is a Borel probability measure `μ` on a compact metric configuration space `X`. `X` is "often finite".
* A *conformer* is an atom of a finitely supported ensemble; a *conformation* is a single point mass `δ_x`.
* Concrete instances of `X`:
  * finite abstract sets (Parts I and V; all of the Lean code);
  * the hypercube `{±1}ⁿ` modulo a global flip, used as a binary stand-in for rotamer or Ising states (Parts III, IV, VI);
  * frameworks `(ℝ^d)^N` modulo congruence (Part II);
  * relative poses in `SE(d)` of **two rigid bodies** (E7′);
  * the **torsion torus `𝕋^r`** (E20–E21);
  * Riemannian manifolds (E2.2).
* At finite temperature (Part IV) the prior is a "first-order (envelope) class" `𝒫(π,d) = {μ : μ(y)π(x) ≤ e^{d(x,y)} μ(x)π(y)}`, which is a polytope in the weights.

**What the observations are:**
* Means of observables: `y_i = ∫ φ_i dμ + ε_i`, `Φ: X → ℝ^m` continuous; the data are `Aμ = ∫Φ dμ`.
* Laws (whole distributions) of scalar features. These are still linear in `μ`; Part II uses them for distance distributions.
* Specific families:
  * pair correlations `E[x_i x_j]` on the cube;
  * correlations of even order `≤ 2d`;
  * per-edge squared-distance moments `E ℓ_e^{2j}`, `j ≤ 2K`;
  * multilinear trigonometric moments on `𝕋^r`: `∫ e^{i a·φ} dμ`, `a ∈ {−1,0,1}^r`, i.e. means of products of `1, cos φ_k, sin φ_k`.
* **Noise models:**
  * Part I: a deterministic tolerance `‖Aν − Aμ‖ ≤ τ`.
  * Part V: Gaussian noise `y = Aμ + σξ`.
  * Remark E2.3: forward-model error `sup_x‖Φ̃ − Φ‖ ≤ η` simply adds to `τ`.
  * "Parts II and III are about exact data… there is no noise model for laws" (§8).

**How the division relates these to experiment** (quoted):
* §8: "**What a law of a distance is, physically** (the science division, SCI-RES-0026 §3…): each measured distance distribution is the solution of an ill-posed deconvolution and comes with a band, not as a law; the distance is between labels on flexible linkers; different pairs are measured on different samples; scattering gives one pooled distribution and averaged couplings give moments. Theorems E7, E7′, E8 are statements about exact laws of exact distances and reach no datum before a stability modulus under a band exists (Problem O4)."
* §8: "**Point conformers.** Finite ensembles are an idealisation… **Genericity.** … Conformers that share rigid parts — the typical case in applications — … are not generic."
* Remark E2.3: "the error of the forward model enters through its supremum over the configuration space, not through its typical size".
* §4c.4 (via SCI-RES-0029): "mean squared distances of a chain are a linear image of the Fourier coefficients with indices in `{−1,0,1}` of the torsion distribution — is what makes the torus the right model". The research log adds: "mean squared distances are measured by scattering with labels".
* E1.3: mean squared distances on unconstrained `(ℝ^d)^N` identify **no** ensemble. The geometry division showed that statewise bond constraints restore identifiability.
* There is no mention anywhere of NMR NOEs, RDCs, J-couplings, SAXS, DEER, FRET, cryo-EM or B-factors by name.

**STRUCTBIO addition: how real data types map onto the model.**

| data type | how it fits the model | what that implies |
|---|---|---|
| NOE (`⟨r⁻⁶⟩`), PRE, FRET efficiency `⟨E(r)⟩`, RDC (`⟨P₂(cosθ)⟩`-type orientational means) | Means of known nonlinear functions of the geometry. This is exactly the Part I / Part V model on a finite conformer library. | E1, E1.1, E13, E17 apply once `X` is a discrete library and `Φ` is a forward-model matrix. E8's polynomial moment certificate and E20's multilinear structure do **not** apply directly to `r⁻⁶` or `r⁻³`. |
| ³J couplings (Karplus) | Linear in `cos φ` and `cos 2φ` of **one** torsion. `cos 2φ` lies outside the `{−1,0,1}` index set, and no cross-angle products appear. | By the logic of E20′ (`|D|=1`) and E21, J-couplings alone give no cross-torsion information. Separating states that differ in two torsions needs products over pairs of angles **(my inference)**. |
| DEER/PELDOR, smFRET histograms | Closest to Part II's "law of one edge length", but laws come with deconvolution bands, between spin or dye labels on linkers, measured on different samples. | E7/E8 need exact laws on a globally rigid graph of label sites. With a handful of label pairs, the graph is far from globally rigid on ≥ d+2 vertices **(my inference)**. |
| SAXS / WAXS | One pooled pair-distance distribution. Per-edge laws are lost (§8 says so). | Outside Part II. Under Part I it is a set of linear means. |
| Crystallographic multi-conformer occupancies (qFit-style), alternate locations, cryo-EM 3D-class populations | Directly "finite ensembles with weights". | A natural evaluation target for weight recovery (E20″(c), E17). B-factors are second moments, so E1.3 says they carry nothing beyond the mean Gram structure **(my inference)**. |

---

## B. Register of main results

Fields shared by every row:
* (1) Originating division: Ensemble, except E2.2 (a), which the report attributes to the science division (SCI-RES-0026 §2(c), SCI-RES-0028 §2(b)).
* (2) Source commit: `8d42f609` for the current statements. E1–E12 were first stated at `a570520`; E13–E17, E7′ and E2.2 at `1a067b5`.
* (7) Review status is abbreviated as follows. **ER1** means internal AI review ER1 (`docs/ensemble/reviews/ER1_internal_review.md`), verdict "correct". **ER2-pending** means a second internal review was commissioned and has not reported. **none** means read by the author only. The science division's review SCI-REV-0020 of E5, E7, E8, E1.3 and §5 was accepted as workstream R21 but has not been published.

All Lean names are in namespace `MetricChain.Ensemble`; witnesses are in `MetricChain.NonVacuity` (`proofs/AxiomAudit.lean`). The source location is `ENSEMBLE_REPORT.md` §x unless stated otherwise.

**E1 / E1.1 — identified = exposed simplex; mass and TV stability (§2.1)**
* (4) Lean: `eq_of_exposing_certificate` (the "if" direction of (a); allows `supp μ ⊆ S`); `mass_off_support_le` (in the form `γ·ν(X∖S) ≤ Σ|λ_i||Δdata_i|`). Witness: `ensemble_exposing_certificate_witness`.
* (5) Assumptions: (a) finite `X`; (b) compact `X`, minimal face of the moment body `conv Φ(X)`.
* (6) Status: P; "if" V; mass bound V, TV bound P.
* (7) Review: ER1, correct (F1, F7 wording fixed).
* (8) Numerics: T1, 1 500 instances; two independent LP tests agree 1500/1500.
* (9) Counterexamples and limits: the slogan "identified ⇔ exposed" is false in both directions (ED12). Example E1.2 is identified but only Hölder-½ stable on a continuum.
* (10) Physical reading: a support is identified iff it is exactly the ground-state set of an energy in the span of the observables.
* (11) Prerequisites: an explicit list of `X` and the feature matrix.
* (12) Software use: an identifiability test plus certificate; a stability bound with constants `(λ, γ, σ, R)`.
* (13) Competing methods: Donoho–Tanner non-negative sparse-recovery face criterion; dual certificates in super-resolution.
* (14) Becomes useless when the library `X` is not exhaustive, when `|X|` is exponential, or when the gap `γ` is not certifiable.
* (15) Ready: **yes** for finite libraries.

**E2 / E2.2 / E2.3 — one conformation: exact modulus and the bridge to robust optimality (§2.2)**
* (4) Lean: `transport_le_of_sharp`, `identification_of_robust_certificate`, `robust_certificate_of_sharp`, `residual_advantage_le`. These rely on theory's `robust_certified_iff` (imported from `proofs/Frontiers/EnvelopeDuality`).
* (5) Assumptions: compact `X`, continuous `ρ`; the Lean statements cover finite `X` and the `Σ|λ_i||Δ_i|` pairing (absolute norms) only.
* (6) Status: (a), (b) P; (c) V for finite `X`. E2.2 is P and the science division's. E2.3 is P.
* (7) Review: E2 ER1 (F10 hypotheses added); E2.2 and E2.3 ER2-pending.
* (8) Numerics: T2, 400 instances, duality gap `3.22·10⁻¹⁵`.
* (9) Limits: on a manifold with C¹ observables `κ = ∞`, whatever the observables. Only `W₂ ≤ √(κ₂τ)` survives.
* (10) Physical reading: a sharp minimum of a data-span energy certifies that averaged data pin the ensemble to one structure. On continuous coordinates, stability is a square root and the certificate is a curvature.
* (11) Prerequisites: an LP over `X`.
* (12) Software use: a "single-structure consistency" certificate; a forward-model-error budget via E2.3.
* (13) Competing methods: DRO/Wasserstein duality (Blanchet–Murthy, Gao–Kleywegt).
* (14) Becomes useless on continuous coordinates without a quadratic-growth constant, and when `η` (sup forward-model error) is at least the data accuracy.
* (15) Ready: **partially** (finite libraries only).

**E3 — first-order constant `κ_μ` for finite ensembles (§2.3)**
* (4) Lean: none. (6) Status: P. (7) Review: ER1 (novelty lowered to "formulation": a Hoffman constant). (8) Numerics: T3, 60 instances.
* (10) Physical reading: to first order, stability depends on where the conformers are, not on their populations.
* (11, 14) Computing `κ_μ` needs vertex enumeration, so the result is useless at moderate `|X|`.
* (15) Ready: **no**, except via the LP `κ(g)` for a given test function `g`.

**E4 — Rényi–Heppes for arbitrary features (§3.1)**
* (4) Lean: `renyi_heppes` (finite `X`; `ν ≥ 0` arbitrary, `μ` supported on at most `K` points). Witness: `ensemble_renyi_heppes_grid`.
* (5) Assumptions: features are `r`-determining (two distinct points agree on fewer than `r` features), and `m ≥ K(r−1)+1`.
* (6) Status: V on finite `X`, P in general; sharp.
* (7) Review: ER1 (neighbour: the frameproof-code lemma of Boneh–Shaw).
* (8) Numerics: Lean witness; ER1 found 0 counterexamples in 729 searches.
* (9) Limits: useless for frameworks, because edge lengths are never `r`-determining.
* (10) Physical reading: enough per-feature histograms determine any `K`-conformer mixture among all ensembles.
* (11) Prerequisites: an `O(N²m)` agreement count.
* (12) Software use: a "how many histograms suffice" check for discrete state spaces.
* (13) Competing methods: discrete tomography.
* (14) Becomes useless when the feature values collide (`r` large).
* (15) Ready: **yes** (trivial).

**E5 / E6 / E7 / E8 — splices, distributional ensemble rigidity, `2K` moments (§3.2–3.3)**
* (4) Lean: none.
* (5) Assumptions: polynomial or rational feature map; **generic** conformers (coordinates algebraically independent over ℚ); `G` generically globally rigid with `N ≥ d+2`; exact laws.
* (6) Status: P, given two cited K theorems (Gortler–Healy–Thurston; Garamvölgyi–Gortler–Jordán 2022, Thm 3.5).
* (7) Review: ER1, correct. The science division's review is in progress (SCI-REV-0020 not yet published).
* (8) Numerics: R1–R8.
* (9) Counterexamples and dead ends:
  * the converse "identified ⇒ no chimera" is false (R7);
  * a non-generic twin exists on the line (R8);
  * the triangle (`N < d+2`) fails;
  * mean squared distances alone identify nothing (E1.3).
* (10) Physical reading: per-pair distance *distributions* on a globally rigid label graph determine a generic finite mixture of any size. The explicit certificate is `f(p)=Σ_e Π_i(ℓ_e²−ℓ_e(x_i)²)²`.
* (11) Prerequisites: rigidity-matroid rank (randomised numerics) and exact laws.
* (12) Software use: a design diagnostic for label-pair graphs.
* (13) Competing methods: generic global rigidity tests (stress matrices); unlabeled PCA.
* (14) Becomes useless with shared rigid domains (non-generic; O3), with banded or noisy laws (no modulus; O4), and with few labels.
* (15) Ready: **no** as inference; **partially** as a design diagnostic.

**E7′ — two rigid bodies, `m` legs (§3.3)**
* (4) Lean: none. (6) Status: P, given K (general position of generic lines). (8) Numerics: `platform_checks.py` P1–P3.
* (5) Assumptions: generic attachment points and poses; `d ∈ {2,3}`; exact laws.
* (7) Review: ER2-pending. ER1 found two errors in passing (`m = 1`; quantifier order), both corrected (ED14).
* (9) Limits: fails on an open set for `2 ≤ m ≤ dim SE(d)`.
* (10) Physical reading: seven inter-domain distance distributions in space (four in the plane) determine generic finite ensembles of relative domain poses.
* (12, 13) Software use: a two-domain DEER/FRET design rule. Competing method: Stewart–Gough forward kinematics.
* (14) Becomes useless with noisy laws or flexible linkers.
* (15) Ready: **no**.

**E8.1 / C1 — continuous obstruction (§3.4, §9)**
* (4) Lean: none. (5) Assumptions: `D ⊂ ℝⁿ` with `n ≥ 2`; C¹ observables. (8) Numerics: none.
* (6) Status: E8.1 is K plus a corollary (Vitushkin–Henkin, read via secondary sources); C1 is C. (7) Review: ER1, "correct, given V–H as quoted".
* (10) Physical reading: **a negative result**. No finite set of smooth observables' *laws* determines every ensemble on a ≥ 2-D space, so identification needs a class.
* (12) Software use: documentation and justification for priors.
* (15) Ready: not applicable.

**E9 / E10 / E11 — pair data on the cube: worst case and capacity `Θ(n)` (§4.1–4.2)**
* (4) Lean: none.
* (5) Assumptions: uniform random sign-vector conformers; exact pair correlations.
* (6) Status:
  * E9 is P (and K: 3-neighbourliness of the cut polytope);
  * E10 (a), (b) are P; E10 (c) is K plus two lines (Odlyzko via Irmatov);
  * E11 is P given K (Cover; Bai–Yin; Sheppard).
* (7) Review: ER1 (F3, F4, F5 corrections).
* (8) Numerics: C1–C5; L5 (all 4 960 triples at `n = 6`).
* (9) Limits: the projector certificate needs `K < n`; verifying its gap is a dense Ising minimisation.
* (10) Physical reading:
  * any ≤ 3 binary conformers are identified from pair correlations; 4 may not be;
  * typical `K ≤ n − 10n/ln n` are identified with certificate `‖P^⊥x‖²`;
  * `K ≥ (2+ε)n` are never identified, with any weights. This is a **capacity theorem**.
* (11) Prerequisites: projector algebra `O(nK²)`; the gap check is exponential in general.
* (12) Software use: a rule of thumb for "how many binary states can covariance data support", plus explicit twin generation (E11(b): signs of a Gaussian).
* (13) Competing methods: Kueng–Tropp binary component decomposition (`K = O(√n)`); associative-memory capacity (Cover, Gardner).
* (14) Becomes useless when conformers are correlated rather than random, which is the real case **(my inference)**.
* (15) Ready: **partially**.

**E12 — fixed vs adaptive pair designs (§4.3)**
* (4) Lean: none (E12(a) is listed as a machine-check candidate, OB7).
* (5) Assumptions: (b) none on the ensemble.
* (6) Status: (a), (b) P; (c) P given K (Cover). Part (b) is known (pivoted Cholesky).
* (7) Review: ER1, correct, including exact rational arithmetic.
* (8) Numerics: C6 (at `n = 60`, exactly `rn − r(r+1)/2` reads; reconstruction to `10⁻¹⁵`).
* (10) Physical reading: a fixed design needs all `n(n−1)/2` pairs; an adaptive design needs `rn − r(r+1)/2`; every certificate needs `Ω(Kn/ln(en/K))`.
* (12) Software use: an adaptive measurement-selection algorithm with a data-driven stopping rule.
* (13) Competing methods: randomly pivoted Cholesky (Chen–Epperly–Tropp–Webber).
* (14) Becomes useless under noise (O6 is open) and when pair correlations are not individually measurable.
* (15) Ready: **yes** (exact, simple).

**E13 — identification inside a first-order class; flow certificate (§4a.1)**
* (4) Lean: none.
* (5) Assumptions: finite `X`, finite envelope.
* (6) Status: P (LP duality).
* (7) Review: ER2-pending (ER1 remark on (a) applied).
* (8) Numerics: F3 (special case).
* (10) Physical reading: inside a Lipschitz-residual Gibbs class, the identified members are the exposed ones.
* (11) Prerequisites: an LP with `N²` flow variables.
* (12) Software use: exact bounds on a mean or population over a class.
* (13) Competing methods: density-ratio robust Bayes (DeRobertis–Hartigan).
* (14) Becomes useless when the envelope constants are unknown (they are "measured, not certified": MSG-0003 E-S3).
* (15) Ready: **partially**.

**E15 / E15T — thermal union bound (§4a.2)**
* (4) Lean: `thermal_union_bound`, `thermal_union_bound_density`, `thermal_union_bound_sharp` (plus `prodE_mono`, `deficit_cons`). Witness: `ensemble_thermal_union_bound_witness`. The Lean statement is `E|r−Er| ≤ 2Σ_i Cov(r,1_i)` for monotone `r` under an iterated product expectation; the translation to TV is P (OB13).
* (5) Assumptions: product reference with a site-additive symmetric envelope (E15); binary sites with a reference log-supermodular in disagreement variables, i.e. no bond frustrated at the centre (E15T).
* (6) Status: E15 P with core V; E15T(a) P given K (FKG, Karlin–Rinott); E15T(b) N.
* (7) Review: ER2-pending.
* (8) Numerics: F1, F2, F6 (exact on 3-site polytopes; maximum excess `≤ 3·10⁻¹⁵`); the violated-bond excess is `+0.23` to `+0.47`.
* (9) Dead ends: ED10 (a "violation" that was solver tolerance); ED11.
* (10) Physical reading: one-body populations certify TV-closeness to the most polarised member, with constant 1 and independent of dimension; frustration breaks it.
* (11) Prerequisites: `O(n)` arithmetic.
* (12) Software use: a falsification test ("either within `Στ` or the class is wrong").
* (14) Becomes useless when the class (`b_i`) is unknown, at a frustrated centre, or for non-binary sites with interactions (O7).
* (15) Ready: **yes** mechanically; physical validity is unclear.

**E16 — double cone (§4a.3)**
* (4) Lean: none. (6) Status: P. (7) Review: ER2-pending. (8) Numerics: F4.
* (10) Physical reading: a bimodal ensemble is identified inside the class by one pair observable `E[M_a²]` (even `n`). Bimodality is not itself an obstruction.
* (15) Ready: **no** (a specific extremal case).

**E17 — noise: modulus = dual certificate = estimator (§4b)**
* (4) Lean: none.
* (5) Assumptions: convex compact class; Gaussian noise `σ`; linear target `E_μψ`.
* (6) Status: P (elementary); K (Donoho 1994: factor 1.25).
* (7) Review: ER2-pending (ER1 "read once, saw no error; that is not a review").
* (8) Numerics: F5 (duality gap `5·10⁻¹⁵`, `ℓ^∞` version).
* (10) Physical reading: the minimax RMS error is between `0.199·ω(2σ)` and `0.5·ω(2σ)`; the dual `λ` is simultaneously the identified-interval certificate and a near-minimax affine estimator.
* (11) Prerequisites: an LP or SOCP over `X` or the class.
* (12) Software use: **property-level partial identification with error bars** (e.g. the population of state A) even when `μ` is not identified.
* (13) Competing methods: maximum entropy, BME, EROS and Bayesian reweighting, which give point estimates and not minimax intervals **(STRUCTBIO addition)**.
* (14) Becomes useless when the library is incomplete, when `σ` is non-Gaussian or correlated, or when `ω(2σ)` is close to the range of `ψ`.
* (15) Ready: **yes** for finite `X`.

**E18 / E18′ — lifted certificates; a prior on the number of atoms (§4c.1–4c.2)**
* (4) Lean: none directly (for finite `X` the last step is `eq_of_exposing_certificate`). (6) Status: P (elementary). (7) Review: **none**. (8) Numerics: L2–L5.
* (5) Assumptions: a lift `v` with `vv*` in the data span; E18′ adds finite `X`, flat isolation and weights outside a null set.
* (10) Physical reading: knowing `K` buys a factor of order `n` in capacity (`n²/2` vs `2n`, E19(c)).
* (12, 14) Software use: the certificate `‖P^⊥v(x)‖²`. It becomes useless when the gap cannot be certified.
* (15) Ready: **partially**.

**E19 — even-order `≤ 2d` data on the cube (§4c.3)**
* (4) Lean: none. (7) Review: **none**. (15) Ready: **no** (research capacity results).
* (6) Status: (a) is K (Baldi–Vershynin 2019, **rediscovered** by the division, ED15; proof not read, OB15); (b)–(d) P given K; (e), (f) N; C3 is C.
* (8) Numerics: `kbody_capacity.py`. Four-body face thresholds are about 76, 152 and 233 at `n = 8, 10, 12`, against lift dimensions 29, 46 and 67; the Gaussian control gives 78, 142 and 214.
* (10) Physical reading: identification extends far beyond what a sum-of-squares certificate can certify (§4c.5).

**E20 — generic conformers on a variety; torus corollary (§4c.4)**
* (4) Lean: none.
* (5) Assumptions: irreducible variety; generic atoms; `K ≤ c` (codimension of the lifted variety); on `𝕋^r`, `K ≤ 2^r − r − 1` with all multilinear trigonometric data.
* (6) Status: P given K (Chiantini–Coppens Cor. 1.3, "statement read through a fetch").
* (7) Review: **none**.
* (8) Numerics: L4 (`r = 3`: 4 and 6 zeros; `r = 4`: 11 zeros; zeros found by multistart BFGS, which does not certify them).
* (10) Physical reading: up to 4, 11 or 26 generic torsion states (r = 3, 4, 5) are determined among all torus measures by multilinear moments.
* (14) Becomes useless with non-generic states, with data that lack all `2^r` multilinear moments, and with noise (no modulus for K > 2).
* (15) Ready: **no**.

**E20′ / E20″ — two states on a torus: certificate and certified modulus (§4c.4)**
* (4) Lean: `twoStateCert_eq_zero_iff`, `twoStateCert_nonneg`, `twoStateCert_unique_eq_zero`, `all_left_or_all_right`, `twoStateCert_comm`, `twoStateCert_growth_three`, `twoStateCert_fin_two`, `twoStateCert_growth_two`. Witnesses: `ensemble_two_state_certificate_witness`, `ensemble_two_state_growth_two_witness`, `ensemble_two_state_growth_three_witness`. The Lean statements are about abstract non-negative `a_k, b_k, θ_k`; the trigonometry, the shared angles and parts (b), (c) are on paper (OB19).
* (5) Assumptions: states `p, q` differ in angle set `D` with `|D| ≥ 2`; data are the means of `cos/sin φ_k` and of pairwise products over `D`.
* (6) Status: P; the zero set and the growth inequality are V.
* (7) Review: **none** (ED17: the kernel rejected a θ ≥ 0 draft).
* (8) Numerics: L6, 46 random pairs; worst ratio `f/(c*·min(d_p²,d_q²)) = 1.25`; on a grid LP the actual worst case is 0.15–0.30 of the bound.
* (9) Limits:
  * `|D| = 1` means never identified by multilinear data of any order;
  * the transfer to chains is conditional on two unchecked statements from other divisions (OB18): competitors keep shared segments rigid, and mean squared distances span the pairwise products (rank 9/9 for two torsions; not reported for three).
* (10) Physical reading: `f ≥ c*·min(d_p², d_q²)` with `c* = min(1, β_min/4)` (|D| ≥ 3) or `min(1, β_kβ_l/(4(β_k+β_l)))` (|D| = 2); `∫min(d_p²,d_q²)dν ≤ Λτ/c*`; the weights are recovered within `(4√ε+ε+2√2τ)/β_max`. **All constants are explicit.**
* (11) Prerequisites: closed-form arithmetic.
* (12) Software use: a certified two-state torsion deconvolution with error bars.
* (13) Competing methods: two-state fitting by least squares; none of them certified.
* (14) Becomes useless when `β_k` is small (nearly equal angles give a small `c*`), when `τ` is not small relative to `c*/Λ` (the weight bound goes as `√τ`), when the cross-angle products are not measured, or when there are more than two states.
* (15) Ready: **yes as a mathematical module**, conditional on data that contain the required moments.

**E21 — the permanent certificate for K states (§4c.4)**
* (4) Lean: `permCert_nonneg`, `permCert_eq_zero_iff`, `permCert_eq_zero_iff_of_hall`, `permCert_zero_set` (product space with one coordinate type; Mathlib's Hall theorem). Witness: `ensemble_perm_certificate_witness`. Membership in the data span and the step to identification are P.
* (5) Assumptions: Hall condition: every set `I` of at least 2 states has at least `|I|` coordinates where its states do not all coincide. Sufficient for this certificate, not necessary for identification.
* (6) Status: P; (a), (b) V.
* (7) Review: **none**.
* (8) Numerics: L7 (torus, 15 families; cube `n = 6`, all 41 664 triples).
* (9) Dead end: ED18 (the converse fails on binary sites).
* (10) Physical reading: `K` torsion states that pairwise differ in at least `K` angles are identified from multilinear data of order `K`.
* (11) Prerequisites: a `K×r` permanent (fine for small `K`); Hall check by enumerating `2^K` subsets.
* (12) Software use: a certificate and identifiability check for small `K`.
* (14) Becomes useless when there is no stability modulus (none is given for `K > 2`) or when order-`K` cross-torsion moments are not available.
* (15) Ready: **partially**.

**Conjectures (status C):**
* C1: positive densities are never identified from finitely many smooth laws.
* C2: sharp pair-data threshold `α* ∈ (1,2)`, numerically 1.1–1.2. Evidence: exact LPs up to `n = 20`, with an `n = 22` row in `output_threshold.txt` but not in the text.
* C3: the capacity of `2d`-body data is `Θ(n^{2d−1})`.

---

## C. Algorithms and checkable certificates

| result | algorithm / certificate | input → output | complexity | arithmetic |
|---|---|---|---|---|
| E1 | LP for `(c, λ)` with `f = 0` on `S` and `f ≥ 1` off `S`, plus a rank test; or the fibre LP (`2|X|` LPs) | feature matrix `Φ` (m×N), support `S` → identified yes/no plus certificate | poly(N, m); **N = \|X\| must be enumerated** | float (HiGHS); rational exact is feasible |
| E1.1 | stability constants `‖λ‖_*/γ`, `σ`, `R` | certificate → mass/TV bound | verifying `γ = min_{X∖S} f` is a minimisation over `X` (the theory division's `(min,+)` kernel for pairwise `Φ` on product spaces) | the inequality is Lean-checked |
| E2/E3 | primal/dual LP for `ω(τ)` and `κ`; `κ_μ` by vertex enumeration | `Φ`, `ρ`, `x⋆`, `τ` → modulus | LP; `κ_μ` exponential | float |
| E4 | count pairwise feature agreements | features → minimal `m` | `O(N²m)` | exact |
| E5–E7 | matroid rank via Jacobian at a random point; connectivity by brute force over subsets | graph, `d` → connected? | as coded, exponential in `\|E\|` (a polynomial rank-oracle method exists: **my inference**) | float, randomised |
| E8 | explicit polynomial certificate `Σ_e Π_i(...)²` | conformers → certificate | closed form; *finding* conformers from moments is not analysed | — |
| E10/E18/E19 | projector `‖P^⊥v(x)‖²` | lifted conformers → energy | `O(NK²)` to build; the gap check is NP-hard-type in general (§8: "a hard minimisation") | float |
| E12(b) | pivoted Cholesky stopping at zero residual diagonal | entry oracle → full `C` | `rn − r(r+1)/2` queries | **exact** (ER1: exact rationals) |
| E13(c) | flow LP | class `(π, d)`, target `f` → certified bound | LP in `N²` variables | float |
| E15/E15T | closed-form `Σ_i[μ*_{a,i}(a_i) − μ(x_i=a_i)]` | one-body populations and class → TV bound | `O(n)` | exact |
| E17 | modulus program, then the affine estimator `T̂ = λ·y + c` | `Φ`, `ψ`, class, `σ` → estimate plus minimax interval | LP/SOCP over `X` | float |
| E20″ | closed-form `c*`, `Λ`, weight bound | `p`, `q`, `τ` → certified bounds | `O(r²)` | exact |
| E21 | permanent; Hall check | `K` states → certificate | `K×r` permanent (`O(2^K r)` by Ryser-type methods for small `K`: **my inference**); Hall check over `2^K` subsets | exact |
| §4.4, E19(e) | cutting-plane face decision | random conformers → face? | full enumeration of `2^{n−1}` states per solve | float |

**Existence-only statements, with no constructive procedure given:**
* E1(b) (compact case);
* E5, E6, E7 (generic exceptional sets are not computed);
* E7′;
* E8.1 and C1;
* E10(c) and E11(a) (probabilistic);
* E19(a)–(d);
* E20 for `K > 2` (generic; zeros are found only by uncertified multistart);
* E13(b) (a criterion only).

The division's own limitation (§8): "**No algorithm with a complexity guarantee.** Certificates are exhibited; finding them … is not analysed."

---

## D. Existing code

**Python** (`experiments/ensemble/`):
* Dependencies: numpy and scipy only (`linprog(method="highs")`, `least_squares`, `minimize`, `nnls`, `scipy.spatial.transform.Rotation`); stdlib `fractions` is used for C1's exact arithmetic. The handoff says to install numpy, scipy, mpmath, sympy and networkx.
* Structure: scripts with fixed seeds, no package, no API, no tests framework; each ends by printing PASS.
* `run_all.py` runs six scripts. It claims "about fifteen minutes"; the recorded times sum to about 453 s: exposedness 41 s, rigidity 106 s, pair_capacity 22 s, finite_temperature 16 s, platform 97 s, lifted 171 s.

Reusable functions:

| script | reusable functions | what they compute |
|---|---|---|
| `exposedness_checks.py` | `identifiable_by_fiber(Phi, mu)`, `certificate_exists(Phi, S)`, `omega_primal/omega_dual`, `kappa_frozen`, `vertices_T1`, `kappa_g` | **E1 and E2 LPs; the most directly reusable code** |
| `rigidity_checks.py` | `rigidity_matrix`, `rank_fn`, `matroid_connected` (brute force), `cayley_menger`, `realise` (multistart least squares) | E5–E8 checks |
| `pair_capacity_checks.py` | `spurious_count`, `fibre_is_point`, `is_face`, `adaptive_cholesky(oracle, n, tol)` | E9–E12 |
| `finite_temperature_checks.py` | `class_constraints_cube`, `ising_reference_case` | E13–E17 on the cube class |
| `platform_checks.py` | `feats`, `jac`, `connected` | E7′ |
| `lifted_checks.py` | `torus_lift`, `projector_certificate`, `zeros_on_torus`, `two_state_f`, `permanent_rect` | E18–E21 |
| `capacity_threshold.py`, `capacity_cutting_plane.py`, `kbody_capacity.py`, `symmetric_stability.py` | face decisions | research threshold tools. Cutting plane: about 20 s per decision at `n = 20`, 1 GB of memory at `n = 22`. Results were appended by hand to `output_threshold.txt`. |

The review's own scripts are in `docs/ensemble/reviews/ER1_scripts/` (independent LPs). They are not part of `run_all`, and the division has not re-run them.

**Lean** (`proofs/Ensemble/`, about 950 lines): five modules, 24 headline theorems and 7 witnesses, all imported and audited in `proofs/AxiomAudit.lean`. `Exposedness.lean` imports `proofs.Frontiers.EnvelopeDuality` from the theory division. Every statement concerns finite types, abstract real-valued functions, or the iterated `prodE` expectation. None of it is a computable checker that could be called from software. Their value to STRUCTBIO is as **specifications** of inequalities that a software certificate checker must satisfy.

Status-document inconsistencies:
* The "Resume here" section of `RESEARCH_LOG.md` says the Lean code is "three modules, twelve headline theorems" and lists running the audit as a next step. `status/ensemble.md` says five modules, 24 theorems, and audit passed.
* Treat the status file as current **(my inference)**.

---

## E. Dead ends, obligations, limitations, inter-division traffic

**Dead ends** (`DEAD_ENDS.md`, ED1–ED18). The ones that matter most here:
* **ED7:** the pair-data threshold is not `n`; a Wendel-type count is wrong.
* **ED12:** three summary slogans were false.
* **ED15:** Baldi–Vershynin rediscovered.
* ED17: a missing positivity hypothesis caught by Lean.

The rest are mathematical corrections and edge cases (ED1–ED6, ED8, ED9, ED11, ED14) or numerical-verification pitfalls (ED10, ED13, ED16, ED18). ED16 includes: "a grid LP on the torus proves non-identification when it finds a twin and proves nothing when it does not". For STRUCTBIO testing, the pitfalls in ED10, ED13, ED16 and ED18 are the useful catalogue: solver tolerance mistaken for a counterexample, checks asserting `or True`, numpy boolean bookkeeping, and checks asserting more than the proposition.

**Open obligations** (`OPEN_OBLIGATIONS.md`). Rated high:
* OB1: review of Parts IV and V.
* OB4: read Garamvölgyi–Gortler–Jordán §§4–5.
* OB10: prior art for Parts IV, V and E7′.
* OB12: apply SCI-REV-0020.
* OB17: review Part VI.

Rated medium or low:
* OB2, OB5, OB6, OB8, OB15: cited sources not read in the original.
* OB13: Lean for E15(c) on class members.
* OB16: prior art for the torus results.
* OB18: the chain-transfer premises of E20′ (unchecked).
* OB19: Lean on the circle.

**Open problems** (§9): O1–O10. Those most relevant to software:
* **O4:** a quantitative modulus for ensemble rigidity under banded laws, which is exactly what DEER/FRET use would need.
* **O6:** adaptivity under noise.
* **O8:** compute the noise modulus for the report's classes.
* **O3:** shared rigid parts.
* **O10:** the torus beyond sums of squares.

**Stated limitations** (§8): exact data for laws; point conformers; genericity; no complexity guarantees; asymptotics; sources not fully read.

**Messages and requests:**
* Messages sent: ENSEMBLE-MSG-0001 to 0004.
* Responses sent: ENSEMBLE-RES-0001 (geometry), RES-0002 (theory, science), RES-0003 (geometry, science).
* **Requests sent: none** (the directory is empty).
* Questions open with other divisions (`ENSEMBLE_TO_ALL.md`): E-S2, E-S3, E-S4, E-T1, E-T2, E-T3, E-T4, E-G2′, E-G4, E-G5, E-C1, E-C2.
* Engineering: "E-E1 … No request now … we will do that locally first and send a precise request only if larger sizes are worth it" (MSG-0002). OB14: larger threshold runs "would need the owner's authorisation".
* Resource use: "No shared Modal computation requested or used" (`status/ensemble.md`).
* There is no stated wish for software or benchmarks. The nearest is RES-0002's checker proposal: verifying dual feasibility for marginal-law ranges "is a `(max,+)` convolution", exact in polynomial time on a lattice.

---

## F. Prior art and novelty verdicts (`PRIOR_ART.md`)

| topic | sources the division names (reading level) | verdict |
|---|---|---|
| Moment problems, representing measures | Karlin–Studden, Krein–Nudelman, Choquet (memory); Kemperman, Lasserre (memory); Curto–Fialkow flat extensions (memory) | E1 "known in substance; formulation" |
| Carathéodory / Tchakaloff | Rogosinski, Richter, Tchakaloff, Winkler: extreme points of moment sets have ≤ m+1 atoms (memory) | — |
| Sparse non-negative recovery / super-resolution | Donoho–Tanner 2005 and Bruckstein–Elad–Zibulevsky 2008 (summary, via the science division); de Castro–Gamboa, Candès–Fernandez-Granda, Schiebinger–Robeva–Recht, Eftekhari et al. (memory) | E1(a) is their finite face criterion |
| DRO / transport duality | Blanchet–Murthy, Gao–Kleywegt, Mohajerin Esfahani–Kuhn (memory) | E2: "formulation" |
| Conic gain / Hoffman | Chandrasekaran–Recht–Parrilo–Willsky 2012 (memory) | E3: "formulation" |
| Tomography / projections | Rényi 1952, Heppes 1956 (summary); Fraiman–Moreno–Ransford; frameproof codes (Boneh–Shaw) | E4: "generalisation of a known theorem; formalisation" |
| Rigidity | Garamvölgyi–Gortler–Jordán 2022 (partial); Gortler–Healy–Thurston (memory); Jackson–Jordán; unlabeled PCA (Yao–Peng–Tsakiris) | E5(a), E6, E7, E8 "new (not found)"; E5(b) a transfer |
| Cut polytope / associative memory | Odlyzko 1988 (summary); Kueng–Tropp 2021 (partial); Cover 1965; Gardner 1988; Personnaz–Guyon–Dreyfus; Slawski–Hein–Lutsik; binary source separation | E9 known; E10 and E11(a) "synthesis"; E12(b) known |
| Higher-order capacity | **Baldi–Vershynin 2019 (statements verbatim; rediscovered)**; Abbe–Shpilka–Wigderson | E19(a) is K; (b)–(d) synthesis |
| Secant varieties / tensor identifiability | Chiantini–Coppens Cor. 1.3 (fetched); Chiantini–Ciliberto, Chiantini–Ottaviani–Vannieuwenhoven (**memory, "not searched"**) | E20 "synthesis"; E20′ "elementary; not searched" |
| Minimax estimation | Donoho 1994 (summary) | E17 "known theory, formulation" |
| Robust Bayes / FKG | DeRobertis–Hartigan; Holley/FKG; Talagrand and Bobkov–Götze L¹ Poincaré inequalities (memory) | E15, E15T "new (not found)"; elementary tools |

**Absent from the register (STRUCTBIO observation):**
* Kruskal's theorem and the Jennrich/simultaneous-diagonalisation identifiability of mixtures;
* Teicher-type identifiability of finite mixtures;
* maximum-entropy, BME (Bottaro–Bengtsen–Lindorff-Larsen), EROS (Różycki–Kim–Hummer), Metainference, sparse ensemble selection (SES, ENSEMBLE, ASTEROIDS), and Bayesian/Occam weighting.

The only maximum-entropy content is via the science division's `INFERENCE_LIMITS.md` ("maximum-entropy refinement is stable (`TV ≤ tanh(βω/4)`)", RESEARCH_LOG cycle 0). The novelty claims "new (not found)" for E5–E8, E15, E16 and E7′ have therefore **not** been tested against the structural-biology ensemble literature.

---

## G. STRUCTBIO assessment (my own)

**1. A finite-library identifiability and partial-identification certifier.** Built on E1, E1.1, E2.3, E13(c) and E17; this is the highest value.
* Inputs: a candidate conformer library `X`, from MD clustering, rotamer enumeration or multi-model PDB entries; a forward-model matrix `Φ` (predicted NOE `r⁻⁶` averages, J via Karplus, RDCs, SAXS intensities, one row per observable); data; `σ`; a forward-model error bound `η`.
* Outputs:
  * (a) for a fitted ensemble: identified or not, with an exposing certificate `(c, λ)`, the gap `γ` and the stability constant;
  * (b) when not identified, an explicit **twin ensemble** (a negative result is itself an output);
  * (c) for a target property `E_μψ` (population of state A, mean radius of gyration): the identified interval and the E17 near-minimax estimator with RMS bounds `[0.199, 0.5]·ω(2σ)`.
* Implementation: LP or SOCP over `|X|` up to about 10⁴–10⁶ with HiGHS. Exact-rational re-verification of the dual is possible.
* Existing code: `exposedness_checks.py` functions, plus Lean `mass_off_support_le` and `eq_of_exposing_certificate` as specifications.
* Validation ladder:
  * L0: T1–T3 and F5, plus ER1's independent LPs.
  * L1: random instances.
  * L2: alanine dipeptide / short peptide with a discretised φ–ψ library and synthetic J/NOE data.
  * L3: PDB multi-conformer (qFit) or NMR-bundle deposits as ground-truth libraries.
  * L4: held-out observables (cross-validated RDC Q-factors) on public NMR ensembles.
  * L5: retrospective comparison of intervals against published BME/maximum-entropy reweighting studies.
* What would make it useless:
  * The truth is not in `X`. Every theorem holds only "among all ensembles **on X**".
  * `η` (a supremum over `X`, E2.3) exceeds the data accuracy.
  * `|X|` is exponential, so the certificate gap cannot be verified.
  * The intervals are routinely the trivial `[min ψ, max ψ]`. A likely real-data outcome, but that is still a reportable negative.

**2. A certified two-state (and small-K) torsion deconvolution.** Built on E20′, E20″ and E21.
* Inputs: two (or K) candidate torsion states and the multilinear trigonometric moments of the differing angles.
* Outputs: a closed-form certificate check; the certified bound `∫min(d_p²,d_q²)dν ≤ Λτ/c*`; weight error bars; and an explicit non-identifiability verdict for `|D| = 1`.
* The arithmetic is exact and the Lean cores exist, which makes this the most "formally backed" module. It is, however, **unreviewed** (Part VI).
* Validation ladder:
  * L0: the L6 and L7 scripts and the Lean witnesses.
  * L1: random tori.
  * L2: MD of a two-state peptide or side chain, with moments computed from trajectories.
  * L3: PDB alternate-location pairs.
* What would make it useless:
  * No experiment measures cross-torsion products directly. The route via mean squared distances (SCI-RES-0029: rank 9/9 for two torsions) is unchecked by this division (OB18) and needs rigid shared segments.
  * `β` small or `τ` large make the bounds vacuous.
  * There is no modulus for `K > 2`.

**3. Measurement-design and negative-identifiability diagnostics.** Built on E1.3, E4, E7/E7′, E11, E12(b) and E20′ `|D| = 1`.
* Tools:
  * given a label-pair graph, report whether per-pair distance distributions could *in principle* identify generic mixtures (generic global rigidity and matroid connectivity);
  * an E7′ rule for two-domain systems (seven legs in space);
  * adaptive pair selection by pivoted Cholesky (exact);
  * capacity rules of thumb (pair data: at most about `2n` binary states);
  * standard twin constructions (Hadamard, sign-of-Gaussian, rescaling for mean squared distances, one-torsion circles).
* Validation: L0–L2 are straightforward. L3/L4 would mean, for example, comparing DEER label-pair sets in public studies with what E7 requires.
* What would make it useless: every positive statement here assumes exact laws and generic conformers. In practice domains share rigid parts (O3) and laws carry bands (O4), so only the **negative** diagnostics transfer robustly. This module should be scoped as "impossibility witnesses", not as an inference engine.

**Not recommended now:**
* Thermal union bound (E15/E15T) and E13: they need first-order class constants that are not physically certified.
* Capacity-threshold tools (§4.4, E19): research only, exponential cost.

**Key risks for STRUCTBIO:**
1. Part VI and Parts IV–V are unreviewed; schedule an independent check before any shipped claim.
2. Novelty versus the ensemble-refinement literature is unsearched; claim "rigorous formulation", not "new method".
3. The Lean results are inequality cores on finite types. Software must not advertise "machine-checked inference" beyond those exact declarations.
