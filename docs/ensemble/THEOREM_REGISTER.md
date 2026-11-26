# Theorem register — Ensemble division

One row per statement.  Labels as in `README.md`.  "Checked" lists everything beyond the
written proof.  "Novelty" is the class after the search recorded in `PRIOR_ART.md`; "new"
means "not found in a documented search", never "proved to be new".  All Lean declarations
are in the namespace `MetricChain.Ensemble` (witnesses: `MetricChain.NonVacuity`).  Scripts
are in `experiments/ensemble/`.  Internal review: see `RESEARCH_LOG.md` for what has been
reviewed and by whom; nothing here has been reviewed outside this division.

| # | statement (short) | label | where | checked | novelty |
|---|---|---|---|---|---|
| E1(a) | finite `X`: identified ⇔ features independent on the support and the support is the zero set of a non-negative function in the span | P; "if" V | report §2.1 | Lean `eq_of_exposing_certificate`, witness `ensemble_exposing_certificate_witness`; script T1 (1 500 instances, two independent LP tests agree) | known in substance; formulation |
| E1(b) | compact `X`: identified ⇔ finitely many configurations over the minimal face, independent features | P | §2.1 | — | known in substance |
| E1.1 | a certificate `(λ, γ, σ)` gives `ν(X∖S) ≤ ‖λ‖_*‖ΔA‖/γ` and a total-variation bound | V (mass bound), P (TV bound) | §2.1 | Lean `mass_off_support_le` | elementary |
| E1.2 | an identified conformation with modulus `√τ` (non-exposed extreme point) | P | §2.1 | by hand | example |
| E1.3 | second moments identify only conformations; mean squared distances identify no ensemble of frameworks | P | §2.1 | by hand | elementary |
| E2(a) | duality formula for the identification modulus of a conformation | P | §2.2 | script T2 (400 instances, gap `3·10⁻¹⁵`) | formulation (LP duality) |
| E2(b) | best linear constant `κ` = least dual norm of a `ρ`-sharp energy in the span | P | §2.2 | script T2 | formulation |
| E2(c) | bridge: robust-optimality certificate ⇒ identification with modulus `‖λ‖_*τ`; reading on the residual | V | §2.2 | Lean `transport_le_of_sharp`, `identification_of_robust_certificate`, `robust_certificate_of_sharp`, `residual_advantage_le` | new as a statement (not found); two lines given Theorem 2.4 |
| E3 | first-order constant `κ_μ` = sup–min over interpolating majorants; exact linearity for small `τ`; independence of the weights | P | §2.3 | script T3 (60 instances) | new (not found); elementary |
| E4 | Rényi–Heppes for `r`-determining features: `m ≥ K(r−1)+1` laws determine `K` conformers among all ensembles; sharp | V (finite `X`), P | §3.1 | Lean `renyi_heppes`, witness `ensemble_renyi_heppes_grid` | generalisation of a known theorem; formalisation |
| E5(a) | connected algebraic matroid ⇒ generic tuples have no splice on the variety | P | §3.2 | script R2, R3, R6 | new (not found) |
| E5(b) | a separator gives product structure and realisable chimeras on an open set | P | §3.2 | script R4 | transfer of a published lemma + local argument |
| E6 | identification of generic finite ensembles from coordinate laws (feature-space version) | P | §3.2 | — | new (not found) |
| E7 | ensemble rigidity ⇔ generic global rigidity (`N ≥ d + 2`) | P given two K | §3.3 | scripts R1–R4 | new (not found) |
| E8 | `2K` moments per edge suffice; explicit certificate | P | §3.3 | script R5 | new (not found) |
| E8.1 | two different ensembles with the same laws of finitely many `C¹` observables (`n ≥ 2`) | K + corollary | §3.4 | — | corollary of Vitushkin–Henkin |
| E9 | pair data: three conformers always identified; four not always | K; example P, N | §4.1 | script C4 | known |
| E10(a,b) | random supports with `K < 0.2933n` are identified with any weights; certificate `‖P^⊥x‖²` | P | §4.2 | scripts C1, C2, C3 | synthesis |
| E10(c) | the same up to `K ≤ n − 10n/ln n` | P given K (Odlyzko) | §4.2 | script C2 (leading term) | synthesis |
| E11 | `K/n → α > 6.338`, equal weights: not identified (full-support twin) | P given K (Bai–Yin, Sheppard) | §4.2 | script C5 | new (not found); elementary |
| E12(a) | a fixed design that identifies all two-conformer ensembles is complete | P | §4.3 | script C6 | formulation |
| E12(b) | adaptive: `rn − r(r+1)/2` pair correlations determine `C` for every ensemble of correlation rank `r` | P | §4.3 | script C6 | known (pivoted Cholesky) in a new role |
| E12(c) | every certificate of a typical `K`-support needs `Ω(Kn/ln(en/K))` pairs | P given K (Cover) | §4.3 | — | formulation |
| C1 | conjecture: every positive continuous density is unidentified from finitely many smooth observables' laws | C | §9 | — | — |
