# Theorem register — Ensemble division

One row per statement.  Labels as in `README.md`.  "Checked" lists everything beyond the
written proof.  "Novelty" is the class after the search recorded in `PRIOR_ART.md`; "new"
means "not found in a documented search", never "proved to be new".  All Lean declarations
are in the namespace `MetricChain.Ensemble` (witnesses: `MetricChain.NonVacuity`).  Scripts
are in `experiments/ensemble/`.  Review: rows E1–E12 were examined by the internal
adversarial review ER1 (`reviews/ER1_internal_review.md`; an AI review by a subagent of this
division, not peer review) — verdict "correct" for every numbered statement, with the
corrections of wording, hypotheses and novelty class recorded below and in the report §7.
Rows E2.2, E7′, E13–E17 have not been reviewed by anyone but their author (three remarks
of ER1 on them are applied).  Nothing here has been reviewed outside the programme.

| # | statement (short) | label | where | checked | novelty |
|---|---|---|---|---|---|
| E1(a) | finite `X`: identified ⇔ features independent on the support and the support is the zero set of a non-negative function in the span | P; "if" V | report §2.1 | Lean `eq_of_exposing_certificate`, witness `ensemble_exposing_certificate_witness`; script T1 (1 500 instances, two independent LP tests agree) | known in substance; formulation |
| E1(b) | compact `X`: identified ⇔ the preimage of the minimal face is finite with affinely independent features | P | §2.1 | ER1: proof checked | known in substance |
| E1.1 | a certificate `(λ, γ, σ)` gives `ν(X∖S) ≤ ‖λ‖_*‖ΔA‖/γ` and a total-variation bound | V (mass bound), P (TV bound) | §2.1 | Lean `mass_off_support_le` | elementary |
| E1.2 | an identified conformation with modulus of exact order `√τ` (non-exposed extreme point): `2√(2τ)(1+o(1)) ≤ ω(τ) ≤ τ + π√τ` | P | §2.1 | by hand; upper bound added after ER1 F9 | example |
| E1.3 | second moments identify only conformations; mean squared distances identify no ensemble of frameworks (except the one with all edge lengths zero) | P | §2.1 | by hand | elementary |
| E2(a) | duality formula for the identification modulus of a conformation | P | §2.2 | script T2 (400 instances, gap `3·10⁻¹⁵`) | formulation (LP duality) |
| E2(b) | best linear constant `κ` = least dual norm of a `ρ`-sharp energy in the span | P | §2.2 | script T2 | formulation |
| E2(c) | bridge: robust-optimality certificate ⇒ identification with modulus `‖λ‖_*τ`; reading on the residual | V for finite `X` and the pairing `Σ_i|λ_i||Δ_i|` (every absolute norm); P for compact `X` (with `d(x⋆,·)` continuous) and general norms | §2.2 | Lean `transport_le_of_sharp`, `identification_of_robust_certificate`, `robust_certificate_of_sharp`, `residual_advantage_le` | formulation (the dictionary was not found in print; two lines given Theorem 2.4) |
| E2.2 | continuous spaces: `κ = ∞` for `ρ = d` with `C¹` observables; `W₂² ≤ κ₂τ` under quadratic growth; modulus `√τ` | P | §2.2 | — | **the science division's** (SCI-RES-0026 §2(c), SCI-RES-0028 §2(b)); part (b) is our E2 with `ρ = d²` |
| E3 | first-order constant `κ_μ` = sup–min over interpolating majorants; exact linearity for small `τ`; independence of the weights | P | §2.3 | script T3 (60 instances) | formulation (`1/κ_μ` is a minimum conic gain / Hoffman constant; ER1 F11) |
| E4 | Rényi–Heppes for `r`-determining features: `m ≥ K(r−1)+1` laws determine `K` conformers among all ensembles; sharp | V (finite `X`), P | §3.1 | Lean `renyi_heppes`, witness `ensemble_renyi_heppes_grid` | generalisation of a known theorem; formalisation.  The support step is the frameproof-code lemma (Boneh–Shaw 1998); the statement for weights and arbitrary measures was not found there |
| E5(a) | connected algebraic matroid ⇒ generic tuples have no splice on the variety | P | §3.2 | script R2, R3, R6 | new (not found) |
| E5(b) | a separator gives product structure and realisable chimeras on an open set | P | §3.2 | script R4 | transfer of a published lemma + local argument |
| E5/E6, converse | "identified ⇒ no chimera" is **false**: exact criterion is uniqueness of the non-negative table on realisable colourings; counterexample on an open set of frameworks | P (counterexamples by ER1) | §3.2 | script R7 (21 pairs, LP) | found by the internal review |
| E6 | identification of generic finite ensembles from coordinate laws (feature-space version) | P | §3.2 | — | new (not found) |
| E7 | distributional ensemble rigidity ⇔ generic global rigidity (`N ≥ d + 2`) | P given two K | §3.3 | scripts R1–R4; R8 (genericity is needed: a non-generic twin on the line, found by ER1) | new (not found) |
| E8 | `2K` moments per edge suffice; explicit certificate | P | §3.3 | script R5 (203 zeros from 400 starts, all at a conformer) | new (not found) |
| E7′ | two rigid bodies with `m` generic legs: leg-length laws determine generic finite ensembles of poses if `m ≥ dim SE(d) + 1`; fail on an open set if `2 ≤ m ≤ dim SE(d)` | P given K (general position of generic line vectors) | §3.3 | script `platform_checks.py` P1–P3; statement and proof corrected after ER1 §7 (`m = 1`; quantifier order) | new (not found) |
| E8.1 | two different ensembles with the same laws of finitely many `C¹` observables (`n ≥ 2`) | K + corollary | §3.4 | — | corollary of Vitushkin–Henkin |
| E9 | pair data: three conformers always identified; four not always | P (explicit certificate, §4c.1 Remark 1; also K: 3-neighbourliness); example P, N | §4.1, §4c.1 | scripts C4, L5 (all 4 960 triples at `n = 6`) | known; the certificate proof (no citation needed) is ours |
| E10(a,b) | random supports with `K < 0.2933n` are identified with any weights; certificate `‖P^⊥x‖²` | P | §4.2 | scripts C1, C2, C3 | synthesis |
| E10(c) | the same up to `K ≤ n − 10n/ln n`; `P(𝓔^c) = 4C(K,3)(¾)ⁿ(1+o(1))` for `K ≥ 3` | K (Odlyzko, as restated by Irmatov) + two lines P (linear dependence) | §4.2 | script C2 (leading term; agreement within sampling error where the term is below 0.1) | synthesis; the energy is that of the projection rule of associative memories |
| E11(a) | `K ≥ (2+ε)n` random conformers: w.h.p. no ensemble supported on all of them is identified (any weights) | P given K (Cover) | §4.2 | consistent with the exact threshold computations of §4.4; ER1: proof checked | synthesis (the classical capacity bound `α ≤ 2` read through E1) |
| E11(b) | `K/n → α > 6.338`: every positively weighted ensemble on the conformers has a full-support twin (explicit for equal weights: signs of a Gaussian vector) | P given K (Bai–Yin, Sheppard) | §4.2 | script C5 | not found; elementary |
| E12(a) | a fixed design that identifies all two-conformer ensembles is complete | P | §4.3 | script C6 | formulation |
| E12(b) | adaptive: `rn − r(r+1)/2` pair correlations determine `C` for every ensemble of correlation rank `r` | P | §4.3 | script C6 | known (pivoted Cholesky) in a new role |
| E12(c) | every certificate of a typical `K`-support needs `Ω(Kn/ln(en/K))` pairs | P given K (Cover) | §4.3 | — | formulation |
| E13(a) | finite envelope: a member of a first-order class is extreme iff its tight graph is connected | P | §4a.1 | — | elementary |
| E13(b) | identified inside the class ⇔ an exposed face through it carries injective data | P | §4a.1 | script F3 (special case) | formulation |
| E13(c) | exact flow certificate for a bound on a mean over the class | P (LP duality) | §4a.1 | — | the format is the science division's (`INFERENCE_LIMITS.md` §8); exactness is LP duality |
| E15(a,b) | product reference, symmetric site-additive envelope, any alphabets: `TV(μ, μ*_a) ≤ Σ_i [1 − μ(x_i=a_i)/μ*_{a,i}(a_i)]` | P | §4a.2 | script F2 (96 cases) | new (not found) |
| E15(c) | binary sites: `TV(μ, μ*_a) ≤ Σ_i [μ*_{a,i}(a_i) − μ(x_i=a_i)]`, with equality cases | P; core inequality V | §4a.2 | Lean `thermal_union_bound`, `thermal_union_bound_density`, `thermal_union_bound_sharp`, witness `ensemble_thermal_union_bound_witness` (the Lean statement is the inequality `E|r − Er| ≤ 2Σ_i Cov(r, 1_i)` for a monotone `r` under an iterated product expectation; the translation to total variation and one-body deficits is on paper); script F1 (exact maximisation over the class polytope for `n = 3`; 360 sampled cases) | new (not found) |
| E15T(a) | any reference that is log-supermodular in the disagreement variables (Ising-type known part on any graph, every bond satisfied by the centre; binary sites): population bound and `TV(μ, μ*_a) ≤ Σ_i [E_μ h_i(x_{<i}) − μ(x_i=a_i)] ≤ Σ_i [μ*_a(x_i=a_i) − μ(x_i=a_i)]` | P given K (FKG; Karlin–Rinott) | §4a.2 | script F6 (exact maximisation on three sites; complete graphs on 4–7 sites sampled) | new (not found) |
| E15T(b) | with a violated bond both bounds fail | N (exact LP counterexamples on chains) | §4a.2 | script F6 | — |
| E15(d) | cube: identified by one-body data inside the class ⇔ at most one unsaturated marginal | P | §4a.2 | script F3 (60 members) | new (not found); elementary |
| E16 | double cone: unique maximiser of `E[M²]` (even `n`); a segment for odd `n` | P | §4a.3 | script F4 (LP over the class polytope, `n = 4, 5, 6`) | new (not found); elementary |
| E17(a) | modulus duality `ω(ε) = min_λ{ε‖λ‖₂ + R_𝒫(ψ − λ·Φ)}` | P | §4b | script F5 (`ℓ^∞` version, 200 instances) | formulation (known technique) |
| E17(b,c) | minimax RMS error between `0.199·ω(2σ)` and `0.5·ω(2σ)` | P (elementary two-point bound and affine estimator) | §4b | — | known theory (Donoho 1994, sharper: 1.25) in the programme's terms |
| E18 | lifted certificates: `‖P^⊥v(x)‖²` for a lift `v` with `vv^*` in the span of the data; identification when the zero set is finite with independent rank-one matrices (also when it is larger than the support) | P | §4c.1 | scripts L2, L4, L5 | elementary; formulation (instances: E10, flat extensions, the geometry division's certificate) |
| E18′ | finite `X`, a prior on the number of atoms: flat-isolated supports are determined among ensembles with at most `K` atoms for all weights outside a finite union of proper affine subspaces | P | §4c.2 | script L3 (exhaustive at `n = 5`) | elementary (not found as stated) |
| E19(a) | cube, degree-`d` lift: `K ≤ (1−ε)C(n−1,≤d)` random conformers are lift-isolated w.h.p. | **K** (Baldi–Vershynin 2019, Thms 4.1, 4.2; statement read verbatim, proof not read) | §4c.3 | script L1 | known; **rediscovered** here before the search found it (`DEAD_ENDS.md` ED15) |
| E19(b) | data of even order `≤ 2d`: every ensemble on such conformers is determined among all ensembles; explicit energy `‖P^⊥ξ_d‖²` | P given K | §4c.3 | script L2 (38 supports, fibre LP) | synthesis |
| E19(c) | pair data with at most `K` conformers assumed: determined for `K ≤ (1−ε)n²/2` and generic weights; not determined among all beyond `2n` | P given K | §4c.3 | script L3 (small `n`) | synthesis (the contrast `n²/2` against `2n` was not found stated) |
| E19(d) | no identification beyond `(2+ε)D_odd ~ 2n^{2d−1}/(2d−1)!` conformers | P given K (Cover) | §4c.3 | consistent with (e) | synthesis (capacity of higher-order associative memories) |
| E19(e,f) | four-body data: face threshold about 76, 152, 233 for `n = 8, 10, 12` (lift dimensions 29, 46, 67); a Gaussian cloud of the same size and dimension: 78, 142; for pair data the cube exceeds the Gaussian threshold | N | §4c.3 | `kbody_capacity.py` (with its Gaussian control), `output_threshold.txt` | — |
| E20 | generic `K ≤ c` conformers on a variety whose lift has projective codimension `c` are determined among all ensembles; torus `𝕋^r` with multilinear data: `K ≤ 2^r − r − 1` | P given K (Chiantini–Coppens, Cor. 1.3; statement read through a fetch) | §4c.4 | script L4 (`r = 3`: 4 and 6 zeros; `r = 4`: 11 zeros) | synthesis (for moments: classical) |
| E20′ | two states on a torus are determined by multilinear data iff they differ in at least two angles; explicit product certificate on pairs of angles | P; the zero set of the certificate V | §4c.4 | Lean `twoStateCert_eq_zero_iff`, `twoStateCert_nonneg`, `twoStateCert_unique_eq_zero`, `all_left_or_all_right`, witness `ensemble_two_state_certificate_witness` (the Lean statement is about abstract non-negative functions `a_k`, `b_k`; the trigonometric identification and the passage to identification are on paper); script L4 (zeros; grid LP) | elementary; not searched |
| C3 | conjecture: the capacity of data of even order `≤ 2d` on the cube is of order `n^{2d−1}` for `d ≥ 2` | C; evidence N | §4c.3 | `kbody_capacity.py` | — |
| C2 | conjecture/problem O1: there is a sharp threshold `α*` for random simplicial faces of the cut polytope, strictly between 1 and 2; numerically between 1.1 and 1.2 (exact LP decisions up to `n = 20`) | C; evidence N | §4.4, §9 | scripts `capacity_threshold.py`, `capacity_cutting_plane.py`, `symmetric_stability.py`; `output_threshold.txt` | — |
| C1 | conjecture: every positive continuous density is unidentified from finitely many smooth observables' laws | C | §9 | — | — |
