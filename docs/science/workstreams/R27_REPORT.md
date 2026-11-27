# R27 — Adversarial review, with replication, of the Geometry division's Theorem L in its threshold-free form (Lemmas P, Q; Theorem L; Corollaries L.1–L.3; Theorem L⁺)

*Science division, workstream R27.  Work started 2026-11-26 22:46:24Z; this header last edited at 23:58:02Z (both read from the clock; the times in
`experiments/science/ws_R27/NOTES.md` likewise).
**This is an internal review by an AI agent, not external peer review.**  Object: `LOCAL_DATA_STABILITY.md` of the Geometric Inference division at its
commit `9f164f9` (read-only copy; §0, §1, §3, §4, §5, §6 read in full, all 562 lines), `GEOMETRY-RES-0007.md` (read in full); `PRIOR_ART.md` read only at
its row for Theorem L.  Their branch was not read by git and none of their scripts was available or used.  Pure geometry of point configurations;
nothing here concerns the design of sequences.*

**Four kinds of checking, kept apart.**  *Review* = I re-derived the statement and its proof by hand, line by line.  *Replication* = I recomputed with
code of my own, written from the statements (`experiments/science/ws_R27/`).  *Re-run* (their code) = **not done for anything** (not available).
*Read only* = neither.  Labels as in `COMMON.md`: [P] proved on paper, [K] known and cited, [N] numerical evidence only, [C] conjecture.

## 0. Verdict

| statement | verdict | checking done |
|---|---|---|
| **Lemma P** (Procrustes–Gram) | **proved as stated**; attribution correct; the constant is attained | review; replication (22 000 pairs + an equality family); source opened |
| **Lemma Q** (one window) | **proved as stated**; the constant is within 3 % of optimal; the sentence on sharpness that follows it is imprecise (minor) | review; replication (12 000 windows + search) |
| **Theorem L, local form** | **proved as stated**; hypothesis stronger than needed at the two ends; one free sharpening (both minor) | review of Steps 1–3; replication of every intermediate inequality; adversarial search |
| **Theorem L, uniform form** | **proved as stated** (arithmetic of Step 4 redone: 1.176 ≤ 1.18) | review; replication; adversarial search over both configurations |
| **Corollary L.1** | **proved as stated** | review; replication (330 estimates) |
| **Corollary L.2** | **proved as stated**; three conditions implicit in its wording must be explicit — one of them (`Ŷ ∈ ℝ³`) is essential: false in `ℝ⁴` | review; replication (864 + 10 933 pairs); counterexample outside the hypotheses |
| **Corollary L.3** | (a) **proved as stated** given Theorem K(c), which I re-derived; (b) **proved as stated** | review; replication (helices `n` = 20…320, 200 random chains) |
| **Theorem L⁺** | **proved as stated**; `Λ < 11.04` confirmed (supremum of the symbol 11.039116); attained in the limit | review; replication (1322 pairs inside the range, computed without cancellation) |

**No statement is false as stated and no proof has a gap.**  No violation in 23 360 pairs of the battery, in the searches, or inside the range of L⁺.
Largest ratio of distance to bound reached by adversarial search: **0.84** (local form, per point), **0.43** (local form, Frobenius; 0.25 at `n` = 16),
**0.018** (uniform form, `n` = 16).  Findings: **0 critical, 1 major** (it concerns what the first-order numbers let a reader conclude, and adds
information on their open problem O-16; no theorem is affected), **11 minor**.  Prior art (short search): the threshold-free form was not found in
the places looked at; that is a statement about this search.

## 1. The statements as I understand them, with the implicit hypotheses

**Setting.**  `X = (x_1,…,x_n)`, `Y = (y_1,…,y_n)`, points of `ℝ³`, `n ≥ 5`; an isometry is `x ↦ xR + t`, `R ∈ O(3)` (**improper allowed**);
`d_P(X,Y) = min_g ‖Y − gX‖_F`.  `η_jk = |y_j − y_k|² − |x_j − x_k|²` for the `4n − 10` pairs with `|j − k| ≤ 4` (**squared** distances).  For a
set `S` of consecutive indices, `σ₃(S)` = third (smallest) singular value of the centred `|S| × 3` matrix.  `W_i = {i..i+3}`, `τ_i = σ₃(W_i)`
(`1 ≤ i ≤ n−3`); `F_i = {i..i+4}`, `s_i = σ₃(F_i)` (`1 ≤ i ≤ n−4`); `τ_* = min τ_i`, `s_* = min s_i`, `b = max |x_{i+1} − x_i|`; `e_i` = `ℓ²` norm of
`η` on the ten pairs of `F_i`; `κ = 1/(2√(√2−1)) = 0.776887`; `δ_i = κ e_i/s_i`.

* **Lemma P.**  `U, X ∈ ℝ^{m×r}`: `min_{R∈O(r)} ‖U − XR‖_F² ≤ ‖UUᵀ − XXᵀ‖_F² / (2(√2−1)σ_r(X)²)`.  *Implicit:* nothing about `U`; "X of rank r" only makes
  the right side finite.
* **Lemma Q.**  `|S| ≥ 4`, `s = σ₃(S) > 0`, `Y` arbitrary **in ℝ³**: some `R ∈ O(3)`, `t` with `‖Y_S − X_S R − 1tᵀ‖_F ≤ κe/s`.  *Implicit:* all
  `|S|(|S|−1)/2` squared distances of the window enter `e`; `R` may be improper (it must be allowed to be).
* **Theorem L.**  `τ_* > 0`.  For every `Y ∈ (ℝ³)ⁿ` there is an isometry `g` — in the proof, the frame `(R_1, t_1)` of the first window — with
  (local) `|y_k − g(x_k)| ≤ δ_{i(k)} + Σ_{j<i(k)} (δ_j + δ_{j+1})(|x_k − c_{j+1}|/τ_{j+1} + ½)`, `i(k) = min(k, n−4)`, `c_{j+1}` the centroid of `W_{j+1}`;
  (uniform) `‖Y − gX‖_F ≤ 1.2 (b/(s_*τ_*)) (n+2)² ‖η‖₂`.  *Implicit:* `n ≥ 5`; `τ_{j+1}` is `σ₃` of the centred **four**-point window `{j+1,…,j+4}`
  shared by `F_j` and `F_{j+1}`; only `τ_2,…,τ_{n−4}` and `s_1,…,s_{n−4}` are used (finding F4); the uniform form uses `τ_* ≤ √(5/3) b` and `n ≥ 5`.
* **Corollary L.1.**  Data `q_jk = |x_j − x_k|² + ε_jk` on all pairs of separation ≤ 4; any `Ŷ ∈ (ℝ³)ⁿ` whose stress is at most `Σε²` has
  `d_P(Ŷ, X) ≤ 2.4 (b/(s_*τ_*))(n+2)²‖ε‖₂`, **constants of the true `X`**.
* **Corollary L.2.**  Any `Ŷ ∈ (ℝ³)ⁿ` with `τ_*(Ŷ) > 0`; data as above with `‖ε‖₂ ≤ ν`: `d_P(X, Ŷ) ≤ C(Ŷ)(‖r‖₂ + ν)`, `C(Ŷ)` the uniform constant of
  `Ŷ`.  *Implicit:* `Ŷ` three-dimensional; all `4n − 10` pairs measured; `ν` bounds the errors of the **squared** distances; an `X ∈ (ℝ³)ⁿ` exists.
* **Corollary L.3.**  (a) points of a circular helix with equally spaced axial coordinates (the hypothesis of Theorem K(c): within `ρ` of a line,
  `z_i = (i−½)h`), separations ≤ `K`, `K ≥ 4`: `h²n²/(139ρbK^{3/2}) ≤ 1/s_7(R) ≤ 9.6 (b²/(s_*τ_*))(n+2)²` (`R` the rigidity matrix of the distances);
  (b) `μ ≥ s_*τ_*/(2.4b(n+2)²)`.
* **Theorem L⁺.**  `A` = half-Jacobian of the squared distances, `μ` its `(3n−6)`-th singular value, `Λ` the largest Laplacian eigenvalue of the band
  graph, `C_L` any constant with `d_P ≤ C_L‖η‖₂` for all `Y`.  If `‖η‖₂ ≤ μ/(ΛC_L)` then `d_P ≤ ‖η‖₂/μ`, and `d_P ≤ ‖η‖₂/(μ + √(μ² − Λ‖η‖₂))` when
  `‖η‖₂ ≤ μ²/Λ`.  *Implicit:* a `C_L` exists (e.g. `τ_* > 0`), and then `μ > 0` is a consequence (L.3 (b)), not a hypothesis; `Y ∈ (ℝ³)ⁿ`.

## 2. Review, question by question, and findings

### 2.1 What the brief asked, answered (review [P]; replication in §3)

* **Lemma P — constant, arbitrary `U`, hypotheses.**  Re-derived (l.176–184): after `X ← XR` with `R` optimal, `XᵀU ⪰ 0`; the nine terms of
  `tr(XΔᵀ + ΔXᵀ + ΔΔᵀ)²` are `2tr(XᵀXA) + trA² + 4tr(AB) + 2trB²` (uses `B = Bᵀ`); `tr(A + √2B)² ≥ 0` and `tr(A·XᵀU) ≥ 0` give
  `≥ (2√2−2)tr(XᵀXA) ≥ 2(√2−1)σ_r²‖Δ‖²`.  Correct for arbitrary `U`; no closeness; full column rank is not even needed (right side `+∞`).
  **The constant cannot be improved** [P, mine; N: 1200 instances to 5·10⁻¹³]: for `m > r`, with `p` the weakest right singular vector of `X` and
  `w ⟂ range(X)`, `|w|² = (√2−1)σ_r²`, the matrix `U = X − Xppᵀ + wpᵀ` gives equality (collapse the weakest direction and replace it by an
  orthogonal one).  For `m = r` the supremum of the ratio is `2(√2−1)` [N].
* **Lemma P — source.**  Opened (reading levels in §5): Tu, Boczar, Simchowitz, Soltanolkotabi, Recht, "Low-rank Solutions of Linear Matrix
  Equations via Procrustes Flow", arXiv 1507.03566v2 (5 Feb 2016), **Lemma 5.4**, p. 9: "For any `U, X ∈ ℝ^{n×r}`, we have
  `dist²(U, X) ≤ 1/(2(√2−1)σ_r²(X)) · ‖UUᵀ − XXᵀ‖_F²`", `dist` defined in its (3.1) as the minimum over `R` with `RᵀR = I_r`; proof in its
  Appendix A — the same completion of a square as in the note.  The ICML 2016 proceedings version (JMLR W&CP 48) has the same Lemma 5.4 with the
  same number and statement.  **Attribution, number and statement match.**  (A slip in the *source's* Appendix A, not in the note: it writes
  "(A.1) holds with `η = 1/(2(√2−1)σ_r²(X))`", whereas (A.1) and its last line need `η = 2(√2−1)σ_r²(X)`; the lemma is unaffected.)
* **Lemma Q — centring, constant, improper rotations.**  `‖E‖_F = √2·e` (each pair twice), `‖−½JEJ‖_F ≤ e/√2`, Lemma P on the centred windows,
  `t = c_Y − c_X R`: `κ = 0.776887 < 0.777` ✓.  Improper `R` is necessary: with proper rotations only the lemma is false (mirror image: `e = 0`).
  The supremum of `‖ε‖s/(κe)` over all pairs of five-point windows is ≥ 0.971 [N]: the constant is within 3 % of optimal (it cannot be exactly
  attained through the equality case of Lemma P: `‖JEJ‖ = ‖E‖` needs `diag G_Y = diag G_X`, incompatible with it).
* **Lemma Q — the reflection example (Item 1 (iii)).**  Verified on every case: exactly one squared distance changes, by `4h⁻h⁺`.  But "sharp there"
  holds only up to a factor that depends on the shape of the window — finding F3.
* **Step 2 — the crux.**  On the four shared rows the two representations of `Y_W` are *equal*; centring gives
  `(X_W − 1c_W)(R_j − R_{j+1}) = J(ε_{j+1} − ε_j)|_W` exactly, and `‖MN‖_F ≥ σ_min(M)‖N‖_F` for `M` of full column rank.  **`τ_{j+1}` is the third
  singular value of the centred 4×3 matrix of the points `j+1,…,j+4`** (the window shared by `F_j` and `F_{j+1}`) — not of a five-point window.  The
  inequality `‖R_j − R_{j+1}‖_F ≤ (δ_j + δ_{j+1})/τ_{j+1}` is correct for every `τ_{j+1} > 0` and **whatever the determinants**: it is linear algebra, and
  when the determinants differ (`‖R_j − R_{j+1}‖_F ≥ 2`) it simply says that the two windows carry errors `δ_j + δ_{j+1} ≥ 2τ_{j+1}`.  When the shared
  window is nearly coplanar the bound degenerates like `1/τ` — and that is not an artefact: the intermediate line
  `‖R_j − R_{j+1}‖_F τ_{j+1} ≤ ‖ε_j|_W‖ + ‖ε_{j+1}|_W‖` is **attained exactly** (ratio 1.000000 by search, at a pair with opposite determinants and
  `‖R_1 − R_2‖_F = 2`), and a chain with one thin interior window has distant solutions at data distance `∝ τ` (F1).  `|m_j| ≤ (δ_j+δ_{j+1})/2` ✓.
* **Step 3.**  The telescoping identity holds (numerically to 3·10⁻¹⁵); `k ∈ F_{i(k)}` ✓.
* **Step 4.**  `|x_k − c_{j+1}| ≤ b(k−j+½)` ✓ (equality only possible at `k = j+1`); a pair of separation `s` lies in `5 − s ≤ 4` windows ✓;
  `Σ(δ_j+δ_{j+1})² ≤ (4κ‖η‖₂/s_*)²` ✓; `Σ_{u<k}(u+½)² ≤ (k+½)³/3` ✓; `Σ_k(k+½)³ ≤ (n+3/2)⁴/4` ✓; `(2√k+1)² ≤ 9k` ✓; `τ_* ≤ √(5/3)b` ✓;
  Minkowski: `κ[2/√3 + (3/√2)·√(5/3)·(n+½)/(n+3/2)²] ≤ 0.7769·(1.1547 + 0.3566) = 1.174` at `n = 5`, decreasing in `n` ✓ `≤ 1.18`; `1.18(n+3/2)² ≤ 1.2(n+2)²` ✓.
* **Corollaries.**  L.1: `η(Ŷ) = r + ε` ✓.  L.2: Theorem L with the roles exchanged, `d_P` symmetric ✓; **not circular** — the right side needs
  from the unknown `X` only that it exists in `ℝ³` and a bound `ν` on the noise (F2).  L.3 (b): for `V` orthogonal to the trivial motions,
  `d_P(X, X+tV) = t‖V‖` for small `t` and `‖η‖ = 2t‖AV‖ + O(t²)` ⇒ `‖V‖ ≤ 2C_L‖AV‖` ✓.  L.3 (a): 9.6 = 1.2·8 ✓; the lower bound is Theorem K(c),
  whose proof I re-derived (the bent-rod field, an 8-dimensional test space, Courant–Fischer; `14π² = 138.2 ≤ 139`).  "The exponent is sharp" ✓.
* **Theorem L⁺.**  `η = 2A_{X′}V + Q(V)` exactly; `‖Q‖₂ ≤ ‖Q‖₁ = Vᵀ(L⊗I)V ≤ Λ‖V‖²`; `φ(v) = 2μv − Λv²` is increasing on `[0, μ/Λ]` with `φ ≥ μv`;
  Theorem L puts `v` there ✓.  `Λ < 11.04`: the symbol `8 − 2Σ_{s≤4}cos sθ` has maximum **11.039116** at `θ = 57.45°`; `Λ_n` increases to it
  (`Λ_5 = 5`, `Λ_12 = 9.643`, `Λ_20 = 10.505`, `Λ_1000 = 11.038914`) ✓.  The clause "if `‖η‖₂ ≤ μ²/Λ`" is needed (a valid `C_L` may lie in `[1/(2μ), 1/μ)`).
  Attained in the limit ✓ (ratio `1 − 5·10⁻⁸` along the softest mode).

### 2.2 Findings

**F1 — major (what a reader may conclude; no theorem affected).  The first-order constant is not the global one, and the first-order regime is
short.**  *Lines:* note l.531–534 (§6, reading (i)), l.541–543 ("The gap between `C_L` and `1/(2μ)` … is the open problem"), l.279–280;
GEOMETRY-RES-0007 l.95–99 ("to first order the local data of a 20-point helix-like trace are not badly conditioned (an rms distance error `σ` moves
the reconstruction by at most `9σ`)").  *Evidence* [N; explicit configurations, re-evaluated with a second code path]:
(i) on the idealised helix-like trace of 20 points a configuration at **RMSD 6.97 Å fits all 70 local distances to rms 0.237 Å** (largest error
1.39 Å; first order predicts 2.1 Å), one at RMSD 9.0 Å (the radius of gyration is 8.95 Å) fits them to 0.271 Å; for 12 points: 4.28 Å at 0.320 Å,
5.76 Å (> `R_g` = 5.66 Å) at 0.367 Å; strand-like (160°, 20 points): 4 Å at 0.026 Å, 10 Å at 0.068 Å, 18.6 Å at 0.2 Å (`R_g` = 19.05 Å)
(`item4_worstcase_run1.log`, `item4_worstcase_verify_run3.log`; control: at small amplitude the search returns the first-order value, 0.0556 against
0.0558).  The first-order factor `9σ` is recovered only up to `σ ≈ 0.2 Å`.  (ii) `sup_Y d_P/‖η‖₂ ≥ 1.92` on that trace against `1/(2μ) = 0.447`
(`item2_adv_fixedX_run2.log`).  (iii) [P for the mechanism, N for the numbers] a chain with **one nearly coplanar interior four-point window** (one
end point at height `h` over the plane of the three points before it) stays infinitesimally rigid with `1/(2μ)` bounded (→ 2.42 as `h → 0`: two
rigid pieces sharing four coplanar, non-collinear points have no relative infinitesimal motion), while its reflected tail has
`d_P/‖η‖₂ = d_P/(4|h⁻h⁺|)` = 2.3, 24, 242, 2420 for `h` = 0.1, 0.01, 0.001, 0.0001 (`item3_Lplus_v2_run1.log`, part 3).  So `C_glob(X) =
sup_Y d_P/‖η‖₂` is **unbounded relative to `1/(2μ)`**; every global constant must contain the factor `1/τ` of Theorem L (there `d_P/(C_L‖η‖₂)`
stays at 1.6·10⁻⁴ as `h → 0`: the order in `τ` is right); and in Theorem L⁺ the hypothesis `‖η‖₂ ≤ μ/(ΛC_L)` cannot be replaced by
`‖η‖₂ ≤ μ²/Λ` (for `h ≤ 10⁻³` the reflected configuration satisfies the latter and violates both conclusions).
*Replacement for l.531–534:* "(i) *First order:* on a helix-like trace of 20 points, distance errors of root-mean-square size `σ` move the
reconstruction by at most `9σ` (RMSD) **in the limit `σ → 0`**; the factor grows like `n²` and is one to two orders of magnitude larger on
strand-like traces.  **This is not a bound at finite `σ`, and the regime is short: by search (Science division, R27; explicit configurations) the
local distances of that trace are fitted to rms 0.24 Å (largest error 1.4 Å) by a configuration at RMSD 7.0 Å, and to 0.27 Å by one at RMSD 9.0 Å,
its radius of gyration; on the strand-like trace, to 0.07 Å by one at RMSD 10 Å.  In the worst case, sequence-local distances with errors of a few
tenths of an ångström do not determine the fold of these traces, whatever the algorithm.**"
*Replacement for the sentence at l.541–543:* "The gap between `C_L` and `1/(2μ)` is only partly an artefact: the best global constant
`C_glob = sup_Y d_P/‖η‖₂` is not `1/(2μ)`.  On the 20-point helix-like trace it is at least 1.92 (against 0.447), and for chains with one nearly
coplanar interior window `1/(2μ)` stays bounded while the reflected tail gives `d_P/‖η‖₂ ∝ 1/τ` (R27).  Hence the factor `1/τ` of Theorem L is
necessary and the range of Theorem L⁺ cannot be enlarged to `‖η‖₂ ≤ μ²/Λ`.  What remains open (`PROOF_OBLIGATIONS.md` O-16) is the size of
`C_glob` between these lower bounds and `C_L`: a factor 240 on the helix-like trace, and 55 on the worst pair found by search."

**F2 — minor (but it decides whether the software reader may apply Corollary L.2).**  *Lines:* l.250–259, l.543–544; GEOMETRY-RES-0007
l.102–106 ("an error bar … valid for any algorithm's output").  The corollary is right; its wording hides three conditions.  (a) **`Ŷ` must be a
configuration in `ℝ³`** — essential: for `Ŷ ∈ ℝ⁴` (an unprojected semidefinite or multidimensional-scaling solution) the statement is false: five
points of the helix-like trace, `y_i = (x_i, εw_i)` with `w` the affine dependency of the window: `‖η‖₂ = 2.04ε²`, `d_P = ε`, ratio `0.489/ε`
(`item4_examples_run2.log` (C)); only a Hölder-½ bound survives.  (b) all `4n − 10` pairs must be measured.  (c) `ν` bounds the errors of the
*squared* distances (`ε = δ(2d + δ)` for distance errors `δ`).  And "This is possible only because the theorem has no smallness condition" (l.258)
is too strong: with a threshold the same bar would exist whenever residual and noise are below it.
*Replacement for l.250–252:* "Let `Ŷ` be *any* configuration **of `n` points in `ℝ³`** with `τ_*(Ŷ) > 0` — the output of any algorithm **that
returns three-dimensional coordinates** — and let the data be `q_jk = |x_j − x_k|² + ε_jk` **for all `4n − 10` pairs of separation at most 4**, for an
unknown configuration `X` **in `ℝ³`**, with `‖ε‖₂ ≤ ν` **(errors of the squared distances)**."  *Add after l.259:* "**The statement is false for `Ŷ`
in `ℝ⁴`** (`y_i = (x_i, εw_i)`, `w` the affine dependency of a five-point window: `‖η‖₂ = O(ε²)`, `d_P ≍ ε`).  The absence of a smallness condition
makes the bar unconditional; with a threshold it would exist only below the threshold."

**F3 — minor.  The sharpness sentence after Lemma Q.**  *Lines:* l.197–201.  "the window moves by `2 min(h⁻, h⁺)` up to a rigid motion" is an
upper bound (the Procrustes distance of the window is 0.26 to 0.89 of it); and `s ≤ √2 max(h⁻,h⁺)` shows only that the bound is not *below*
`2.2 min(h)` — sharpness needs the reverse inequality, which fails for windows whose three middle points are nearly collinear.  Computed
(`item1_lemmas_run1.log` Q3): `d_P/bound` = 0.55 (helix-like window), 0.21–0.24 (strand-like, 150°–179°), 0.50 (two regular tetrahedra), 0.02–0.63
on 2000 random five-point chains (median 0.22), and 0.034, 0.0034, 0.0003 when the middle triangle has width 0.1, 0.01, 0.001.  The lemma is
nevertheless sharp up to a constant on every window, through another example (collapse of the thin direction: ≥ 0.73 on each window tried).
*Replacement:* "*The constant is essentially optimal, and the dependence on `s` is attained on every window.*  The supremum of
`‖Y_S − X_SR − 1tᵀ‖_F·s/(κe)` over pairs of five-point windows is at least 0.97 (numerically), and on a fixed window collapsing its thin direction
gives at least 0.73 on the windows tried.  The reflection of SCI-REV-0023 §5 (a) — mirror one end point of `F_i` in the plane of its three middle
points: exactly one squared distance changes, by `4h⁻h⁺`, and the window moves by at most `2 min(|h⁻|,|h⁺|)` — attains the bound
`3.11|h⁻h⁺|/s` up to a factor that depends on the shape of the window: 0.55 on a helix-like window, 0.21–0.24 on strand-like ones, arbitrarily
small when the three middle points are nearly collinear."

**F4 — minor.  The hypothesis `τ_* > 0` is stronger than the proof needs.**  *Line:* l.204 (and l.161–164).  Steps 2–4 use `τ_{j+1}` only for
`1 ≤ j ≤ n−5`: the end windows `W_1`, `W_{n−3}` never enter.  Checked: 3600 pairs with both end windows exactly coplanar (`τ_1 = τ_{n−3} = 0`),
no violation of (local) or of the uniform bound with `τ_*` taken over the interior windows; control (an interior window flattened as well):
`η = 0`, `d_P > 0` in 48 of 48 cases (`item4_examples_run2.log` (A2)).  *Replacement for "Let `τ_* > 0`":* "Let `s_i > 0` for all `i` and `τ_i > 0`
for `2 ≤ i ≤ n − 4` (for `n ≥ 6` the second condition implies the first), and let `τ_* := min_{2≤i≤n−4} τ_i`; the end windows `W_1`, `W_{n−3}` may
be flat.  For `n = 5` the theorem is Lemma Q."

**F5 — minor.  The citation of Lemma P can be made definite.**  *Line:* l.173–174 ("cited from memory").  *Replacement:* "(Tu, Boczar,
Simchowitz, Soltanolkotabi and Recht, *Low-rank Solutions of Linear Matrix Equations via Procrustes Flow*, Proc. 33rd ICML (JMLR W&CP 48), 2016,
Lemma 5.4; arXiv 1507.03566v2, Lemma 5.4, proof in its Appendix A — statement checked at the source by the Science division (R27).  The constant
is attained for every `X` when `m > r`: `U = X − Xppᵀ + wpᵀ`, `p` the weakest right singular vector, `w ⟂ range X`, `|w|² = (√2−1)σ_r(X)²`.  The
proof here is self-contained.)"

**F6 — minor.  Remark 5 understates how close the local form is.**  *Line:* l.314–315 ("at most 0.064 times the local bound and 0.002 times the
uniform one").  Those are values on their instances.  *Replacement:* "5. *The constants.*  On the instances of §4 the left side is at most 0.064
times the local bound and 0.002 times the uniform one; these are not worst cases.  An adversarial search over both configurations (Science
division, R27) reaches 0.84 of the local bound point-wise, 0.43 of it in Frobenius form (`n = 5`; 0.25 at `n = 16`) and 0.018 of the uniform bound
(`n = 16`: two straight arms joined by a short thin hinge, the error on two windows).  The local form cannot be improved by more than a small
factor in general; the uniform constant is at least 55 times too large on every pair tried."

**F7 — minor (a free sharpening).**  *Line:* l.205–208.  Step 3 works with *any* window containing `k`; the earliest, `i(k) = max(1, k−4)`, has
four fewer terms in the sum.  Checked: 71 688 point-wise inequalities, no violation, largest ratio 0.53; control (one more term dropped) violated
1742 times (`item4_extras_run1.log`).  *Replacement:* "… for every `k`, with `i(k)` any index such that `k ∈ F_{i(k)}` — the smallest,
`i(k) = max(1, k − 4)`, gives the best bound — …".

**F8 — minor.  Theorem L⁺: three wordings.**  (a) l.279–280, "at finite amplitude `1/(2μ)` alone is not a bound": true generically, not for every
chain — if `⟨AV, Q(V)⟩ ≠ 0` for the softest mode `V` then `d_P > ‖η‖₂/(2μ)` for `Y = X ± tV`, small `t` of one sign; on the 20-point helix-like
trace this number vanishes (3·10⁻¹⁶) and no violation was found among 211 configurations in the range (52 violations on the other five chains).
*Replacement:* "…; at finite amplitude `1/(2μ)` alone is in general not a bound (it fails along the softest mode `V` whenever `⟨AV, Q(V)⟩ ≠ 0`)."
(b) l.270–275: state the implicit hypothesis — *add:* "Let `X` be as in Theorem L (so that a constant `C_L` exists; then `μ > 0` by Corollary L.3
(b))."  (c) l.274, "`C_L` any constant for which Theorem L holds": *add* "— for instance `2‖M‖₂`, `M` the matrix of the local form (`local = Me`,
`‖e‖₂ ≤ 2‖η‖₂`), which is 5 times smaller than the uniform constant on the 20-point helix-like trace (88.7 against 456)."

**F9 — minor.**  *Line:* l.41–43 ("`Θ(n²)`, with explicit constants on both sides").  True; the two explicit constants are far apart.
Helix-like trace, `K = 4` (`item2_cor_L3_run1.log`): `2.3·10⁻⁴ n² ≤ 1/s_7 ≤ 28.8 (n+2)²`, the computed value being `0.0104 n²` (fitted exponent
1.98); `μ` exceeds the bound of L.3 (b) by a factor 1000–1050 there, 550–600 and 1500–1800 on the strand-like traces, ≥ 351 on 200 random chains.
*Add:* "(on the helix-like trace of §6 the two constants are `2.3·10⁻⁴` and `28.8`, the computed value `0.0104`)".

**F10 — minor.**  *Line:* l.245–248 (Corollary L.1).  *Add:* "(The hypothesis cannot be checked from the data, `Σε²` being unknown: it holds for a
global minimiser of the stress, not for the output of a local optimiser.)"

**F11 — minor.**  *Lines:* l.7–16, l.543–544 ("valid and useless").  One part of the note is *not* empty as a guarantee and deserves a
sentence: Lemma Q for a single window.  For one helix-like five-point window with all ten distances known to within 0.1 Å it gives RMSD ≤ 0.32 Å
(worst case found: 0.15 Å); 0.99 Å at 0.3 Å (found 0.48 Å); for strand-like windows 2.1 Å (160°) and 8.0 Å (175°) at 0.1 Å
(`item4_extras_run1.log`).  *Add to §6:* "Lemma Q alone is a usable bound for one window with complete distances (helix-like window: RMSD ≤
0.32 Å for distance errors ≤ 0.1 Å, within a factor 2.2 of the worst case found); it is the chaining that makes the constants useless."

**F12 — minor (confirmations worth recording; no change needed).**  l.164 ("`τ_*` lies between half of the `τ` of §3.5 and that `τ`"): ratio of the
two in [1.0000, 1.9997] on 20 000 windows ✓.  l.159 (thickness non-decreasing in `S`) ✓.  The table of §6 (l.521–529) is reproduced to the digits
given: `C_L` 184.5 / 455.7 / 9795 / 1784 / 4406 / 94 710 / 65 130; `1/(2μ)` 0.2313 / 0.4471 / 9.502 / 3.246 / 7.311 / 167.9 / 41.61; first-order
factor 4.208 / 8.96 / 206.8 / 57.82 / 140.1 / 3463 / 753; the "certified range" column agrees when `Λ_n` (not 11.04) is used and the conversion to
a distance error divides by `2 d_rms √N` — worth saying in the caption.  Remarks 4 and 6 (separations `K ≥ 5`; other dimensions): (local) with
`1/√K` holds on 1000 arbitrary pairs for each of `(d, K)` = (2,3), (3,4), (3,5), (3,6), (3,7), (4,5).

## 3. Tests, each with its control; the largest ratios

All code is mine, written from the statements; double precision; an inequality counts as violated if `LHS > RHS(1 + 10⁻⁹) + 10⁻⁹·scale`; a ratio is
formed only when its right side exceeds `10⁻⁷·scale` (below that both sides are rounding noise).  Every control is an inequality that is **not**
claimed and that the same code must find violated.

| # | check | size | violations | largest LHS/RHS | control → pairs violating it | log |
|---|---|---|---|---|---|---|
| 1 | Lemma P, `m×r` from 1×1 to 10×5, `U` Gaussian / `X` ± noise / 0 / rank one / columns reflected / collapsed / rotated, `X` also ill-conditioned | 22 000 | 0 | 1.000000 | factor `√2−1` dropped → 4472 | `item1_lemmas_run1.log` |
| 2 | Lemma P, equality family | 1200 | — | `|ratio − 1| ≤ 5.1·10⁻¹³` | — | same |
| 3 | Lemma P, supremum over `U` (L-BFGS) | 120 starts | 0 | 1.000000 (`m > r`), 0.828427 (`m = r`) | — | same |
| 4 | Lemma Q, windows of 4, 5, 6, 8 points (Gaussian, chains, helix, strands, thin), nine kinds of `Y` | 12 000 | 0 | 0.933 | `κ → ½` → 635; proper rotations only → 1332; `σ₂` for `σ₃` → 987 | same |
| 5 | Lemma Q, supremum over both windows | 250 starts | 0 | 0.808 (4 points), 0.971 (5), 0.971 (6) | `κ → ½` violated by the maximiser | same |
| 6 | reflection example: one distance changes by `4h⁻h⁺`; `d_P ≤ 2min|h|`; `s ≤ √2 max|h|`; `d_P ≤` bound | 12 named + 2000 random windows | 0 (asserted) | 0.0003 … 0.63 | — | same |
| 7 | **Theorem L**: every inequality of Steps 1–4, both bounds; 85 chains `X` (`n` = 5…40: random unit-bond, angle-constrained, helix-like, strand-like 160°/170°/175°/179°, one thin interior window of height 0.1/0.01/10⁻⁴, point clouds, double tetrahedron) × `Y` of 20 kinds (noise 10⁻⁶…10, tails and heads reflected at every position, unrelated chains, clouds, mirror images, pieces rotated about a bond / about an axis through two points / about a random axis, one point moved by up to 10⁴ diameters at every position, all points equal, collinear, planar projections, softest modes ±, scalings incl. 0 and −1, order reversed, two points swapped) | 12 427 pairs | **0** | Lemma Q 0.736; Step 2 0.540; `|m_j|` 0.236; lever arm 0.950; pair count 0.926; (local) per point 0.535; `d_P/‖local‖₂` 0.279; `d_P`/uniform 0.0055; identities of Steps 2–3 to 3·10⁻¹⁵ | separation-4 errors left out of `η` → 2004 (all reflections); uniform constant /1000 → 468, /10⁴ → 2466 (/10 and /100 → 0 on this battery; /100 is violated in row 11, /10 by nothing found); `κ → ½` → 5; proper rotations only → 2954; `s_j` in place of `τ_{j+1}` in Step 2 → 240; "a pair lies in three windows" → 81; (local) without the lever arm → 2092; (local)/10 → 1704 | `item2_battery_run2.log` (`_run1` agrees) |
| 8 | the same with the roles exchanged (situation of Corollary L.2) | 10 933 pairs | 0 | uniform 0.0055 | — | same |
| 9 | adversarial, `X` fixed (19 chains, `n` = 5…20), `Y` optimised by L-BFGS with analytic gradients from 66–84 starts per chain and objective | — | 0 | uniform 0.0074; local Frobenius 0.355; per point 0.647 | gradient check 6·10⁻⁸ (a gradient scaled by 1.3 → 0.13); uniform /1000 violated | `item2_adv_fixedX_run2.log` |
| 10 | adversarial over both configurations, numerical gradients + Nelder–Mead, `n` = 5…8 | — | 0 | uniform 0.0092; local Frobenius 0.434 (`n`=5), 0.310, 0.295, 0.256; per point 0.841 (`n`=5), 0.836 (`n`=6) | per-point bound with `κ → ½` violated | `item2_adv_joint_run2.log` |
| 11 | adversarial over both configurations, **uniform bound**, analytic gradients on a smooth lower bound of the ratio, `n` = 5…40, three seeds | — | 0 | 0.0077 (5), 0.0085 (6), 0.0103 (7), 0.0113 (8), 0.0120 (9), 0.0145 (10), 0.0141 (11), 0.0167 (12), 0.0174 (14), **0.0180 (16)**, 0.0155 (18), 0.0158 (20), 0.0129 (24), 0.0141 (28), 0.0126 (32), 0.0098 (40) | uniform /100 violated | `item2_adv_jointU_run1_seed27116.log`, `…27117.log`, `item2_adv_jointU_run2_large_seed27121.log` |
| 12 | Step 2 alone, six points, both configurations, starts with a thin shared window and opposite determinants | 120 starts | 0 | `‖R₁−R₂‖τ/(δ₁+δ₂)`: 0.830; `‖R₁−R₂‖τ/(‖ε₁|_W‖+‖ε₂|_W‖)`: **1.000000** (opposite determinants) | `s₁` in place of `τ` → violated | `item2_adv_step2_run1.log` |
| 13 | Corollary L.1 (stress minimisers, noise 10⁻⁶…10 × mean squared distance) | 330 | 0 | 1.2·10⁻³ | constant /1000 → 1 | `item2_corollaries_run1.log` |
| 14 | Corollary L.2, bound computed from the estimate, the data and `ν` only | 864 | 0 | 1.6·10⁻³ | `ν` left out (data fitted exactly by another configuration) → 30 of 30 | same |
| 15 | Corollary L.3 (a), (b): helix-like and two strand-like traces, `n` = 20…320, `K` = 4, 6; 200 random chains | 230 | 0 | — | lower bound ×100 → 20; upper bound /10⁴ → 25; (b) ×10³ → 64 | `item2_cor_L3_run1.log` |
| 16 | **Theorem L⁺** inside `‖η‖₂ ≤ μ/(Λ_nC_L)`: six chains, amplitudes 1…10⁻⁴ of the range; softest mode ±, random and mixed directions, constrained maximisation of `d_P` | 1322 | 0 (tolerance 10⁻¹⁰) | 0.99999995 | `d_P ≤ ‖η‖/(2μ)` → 52; `1.01μ` for `μ` → 187; outside the hypotheses (thin window, reflected tail, `‖η‖₂ ≤ μ²/Λ`): both conclusions fail, as they should | `item3_Lplus_v2_run1.log` |
| 17 | end windows coplanar (F4) | 3600 | 0 | 0.286 | interior window flattened → 48 of 48 | `item4_examples_run2.log` |
| 18 | analogues `(d, K)` (Remarks 4, 6), local form | 6 × 1000 | 0 | 0.447 | lever arm dropped → 4…60 per case | same |
| 19 | (local) with the earliest window (F7) | 71 688 points | 0 | 0.527 | one more term dropped → 1742 | `item4_extras_run1.log` |

**Largest ratio of distance to bound reached:** local form per point **0.84** (`n` = 5, 6); local form in Frobenius norm **0.43** (`n` = 5, where it
is Lemma Q with a factor `√5`), 0.31, 0.30, 0.26 at `n` = 6, 7, 8, and 0.25 at the maximisers of the uniform ratio for `n` = 12, 16; **uniform form 0.0180** (`n` = 16).  The maximisers of the uniform ratio have a common
design (inspected for `n` = 12, 16): two nearly straight arms of long bonds joined by a hinge of short bonds (0.2–0.26 `b`); all thin windows
equally thin (`τ ≈ 0.063b`, `s ≈ 0.077b`); the error on the two central windows, on pairs of separation 1 and 2 (92 % of `‖η‖²`), one change of
determinant between consecutive frames.  Beyond `n ≈ 16` this design loses, as it must (its distance grows like `n^{3/2}`, the bound like `n²`).
These are local optimisers from finitely many starts: **no certificate that the suprema are attained**.

## 4. The classes of the assumptions, and what the theorem guarantees

| hypothesis | class | evidence |
|---|---|---|
| no four consecutive points coplanar, **interior** windows (`τ_i > 0`, `2 ≤ i ≤ n−4`) | **essential — removal makes it false**; quantitatively the factor `1/τ` is necessary | interior window exactly coplanar: the tail reflected in its plane has `‖η‖₂ = 0` (10⁻¹⁵) and `d_P` = 0.02…3.6 (nine instances, `item4_examples_run2.log` (A1)); thin window: `d_P/‖η‖₂ ∝ 1/h` (F1) |
| the same for the two **end** windows `W_1`, `W_{n−3}` | **not needed** (F4) | 3600 pairs, no violation |
| five-point windows not flat (`s_i > 0`) | implied by the interior condition for `n ≥ 6`; `1/s` necessary in Lemma Q | collapse example: ≥ 0.73 of the bound on every window tried |
| complete data of separation ≤ 4 — a pair of separation 4 missing | **removal makes it false** | reflection changes only that pair: measured `‖η‖₂` = 10⁻¹⁵, `d_P` = 0.96…3.5 ((B1), 7 instances) |
| — a pair at an end vertex missing (e.g. (1,2)) | **removal makes it false** | `x_1` reflected in the plane of `x_3, x_4, x_5` ((B2)) |
| — an interior pair of separation 1–3 missing | **needed by the proof** (Lemma Q needs all ten distances of a window); whether the conclusion survives with other constants is **not settled here** [C: it does] | first-order rigidity survives (`μ` goes from 0.302 to 0.281–0.302 at `n` = 8 and from 0.179 to 0.167–0.179 at `n` = 12; (B3)); no proof, no counterexample |
| "exact windows" — read as: the measured pairs form windows of *consecutive* points (a band) | **convenience**: the proof uses only a chain of complete windows whose consecutive members share ≥ 4 non-coplanar points | by the same proof [P, not replicated for irregular chains]; regular cases `K` = 5, 6, 7 replicated |
| — read as: the constants are those of the exact `X` | **replaceable**: they may be taken from an estimate (Corollary L.2) | 864 + 10 933 pairs |
| dimension 3 for `X` | **convenience; removal changes the constants** (`d+1`, `d+2` points; `½ → 1/√(d+1)`) | `d` = 2, 4 on 1000 pairs each |
| `Y` in the same dimension as `X` | **essential — removal makes it false** (only Hölder-½ survives) | `Y ∈ ℝ⁴`: `d_P/‖η‖₂ = 0.489/ε` (F2) |
| separation exactly 4 | `K ≥ 4`: convenience; `K ≤ 3`: **false in this form** (that is Proposition L₀'s territory) | control C1: 2004 reflections violate the bound without the separation-4 errors |
| chain structure of `X` (bonds ≤ `b`) | used only in the uniform form (Step 4); (local) holds for any `X` with non-flat windows | point clouds in the battery |
| deterministic errors | not a restriction of validity (the bound holds for every realisation of random errors) but of sharpness: **removal would change the constants**; for Gaussian errors the first-order root-mean-square error of the least-squares estimate is 0.26 (`n` = 20) to 0.08 (`n` = 100) of the worst case on the helix-like trace | `item4_tables_run1.log`, last column; no probabilistic theorem exists in the note |
| squared distances, `ℓ²` norm | convenience (`η = δ(2d + δ)`) | — |

**The paragraph a software author can act on** (idealised traces, lengths in ångström; `σ` = root-mean-square error of the `4n − 10` measured
distances of sequence separation ≤ 4, worst allocation of the errors; [N] throughout, logs `item4_tables_run1.log`, `item4_extras_run1.log`,
`item4_worstcase_verify_run3.log`).  *Do not use Theorem L or Corollary L.2 as an error bar.*  With the present constants the bound is smaller
than the object (radius of gyration) only if `σ < 3.8·10⁻³` Å for a helix-like trace (radius 2.3, rise 1.5, 100°) of 5 points, `8.5·10⁻⁴` Å for
20, `1.8·10⁻⁴` Å for 100; for a strand-like trace (radius 0.94, rise 3.3) at 160°: `2.8·10⁻⁴`, `8.7·10⁻⁵`, `1.9·10⁻⁵` Å; at 170°: `7.6·10⁻⁵`,
`2.3·10⁻⁵`, `5.1·10⁻⁶` Å; at 175°: `1.9·10⁻⁵`, `5.9·10⁻⁶`, `1.3·10⁻⁶` Å.  For `σ ≥ 0.01` Å it exceeds the size of the object at every length
`n ≥ 5` on all four traces; at `σ = 10⁻³` Å it is informative only for helix-like traces of at most 16 points.  The local form gains a factor 5 (helix-like) or 2.5 (strand-like)
at 20 points and changes nothing; taking the constant from an estimate makes it larger (in the median 1.1× to 5× for estimates within 0.05–0.5 Å of the truth),
and that corollary applies only to a three-dimensional estimate with all `4n − 10` pairs measured.  *What you can use:* (1) **one window**: five
consecutive points whose ten distances are known to within 0.1 Å are fixed, up to a rigid motion or a reflection, to RMSD ≤ 0.32 Å on a
helix-like window and ≤ 2.1 Å on a strand-like one (Lemma Q; no smallness condition; within a factor 2–3 of the worst case found); (2) the
**first-order sensitivity** `1/(2μ)`, one singular value decomposition of the `(4n−10) × 3n` Jacobian: worst-case RMSD ≈ `9σ` (helix-like, 20
points), `140σ` (strand-like, 20 points), growing like `n²`, typical random errors 4 to 12 times smaller — **but only as `σ → 0`**: the local
distances of the 20-point helix-like trace are fitted to rms 0.24 Å by a configuration 7.0 Å away and to 0.27 Å by one farther than the radius of
gyration; those of the strand-like trace to 0.07 Å by one 10 Å away.  So distances of separation ≤ 4 with errors of a few tenths of an ångström
(helix-like) or a few hundredths (strand-like) do not by themselves fix the fold in the worst case, with any algorithm: longer-range information
is needed, and near-planar stretches are where it is needed first (there the separation-4 distance separates a window from its mirror image by
`4h⁻h⁺` only: 34 Å² on the helix-like trace, 6.2, 1.7 and 0.43 Å² at 160°, 170°, 175°).  None of this is a statement about measured structures.

## 5. Prior art for the threshold-free form (Item 5; short), and the search log

**Result.**  A global bound without a smallness condition for reconstruction from the distances of a band (lateration) graph, obtained by
stitching windows with complete distances, **was not found** in the ten addresses (seven works) opened and the five queries below.  "Not found" is a statement about
this search (one agent, about fifteen minutes, no database of reviews).  What was found, by ingredient:

* *The published global bound for this graph has a threshold.*  Arias-Castro and Vishwanath, arXiv 2310.10900v3 [the passages: Theorems 2.1, 3.1,
  Proposition 3.2, (1.1), (1.2), (2.6), (2.7) and the remarks around them; proofs not read]: Theorem 2.1 — "there are `σ > 0` and `A > 0` … such
  that, if `Σε² ≤ σ²`, sequential lateration outputs an embedding … satisfying `min_g Σ‖y_i − g(x_i)‖² ≤ AΣε²`"; Theorem 3.1 the same for stress
  minimisers; `A_n` in (2.6) grows like `(1 + C₂α)^{n−p−1}` and the admissible noise (2.7) decays likewise, in "the worst case scenario where …
  each node `v_k` is connected to precisely the preceding `p + 1` nodes".  The note's description of this paper is accurate.
  arXiv 2207.07218 (Arias-Castro and Chau, patch stitching) [record only]: its page says "Theory was removed to spin off another paper", i.e. the
  paper above; no stitching bound there now.
* *The one-window ingredient without a threshold is in print* — Lemma P itself: Tu et al. 2016, Lemma 5.4 [the passage: statement, and its proof in
  Appendix A of arXiv v2; statement also in the ICML version].  Also, implicitly, Arias-Castro, Javanmard and Pelletier, arXiv 1810.09569v2,
  Theorem 1 [the passage: the statement]: its linear bound (5) needs `‖X‡‖ε ≤ 1/√2`, but its two branches together give, for all `Y`,
  `min_Q‖Y − XQ‖_p ≤ (1 + √2·d^{1/2p})‖X‡‖‖YYᵀ − XXᵀ‖_p` — my one-line combination (`ε ≤ √2‖X‡‖ε²` when `‖X‡‖ε ≥ 1/√2`), not a statement of
  theirs; for the Frobenius norm in dimension 3 the constant is 2.86 against 1.10 from Lemma P.
* *Clique-based reconstruction with a robustness statement* — Drusvyatskiy, Krislock, Voronin and Wolkowicz, arXiv 1410.6852v2 [the passages:
  abstract, introduction paragraph, Theorem C.5 with its proof]: faces of the semidefinite cone from cliques of measured distances; Theorem C.5:
  "there exist constants `ε > 0` and `κ > 0` so that `‖P∘K(Alg(d̂)) − d‖ ≤ κ‖d̂ − d‖` whenever `‖d̂ − d‖ < ε`" — local, constants not explicit, a
  statement about the data fit of the output.  Not the statement of Theorem L.
* *Errors of stitched orthogonal frames add* — Nguyen-Cong, Hy and Dinh, arXiv 2604.21094 [the passages: Lemmas 17, 18 and the paragraphs around
  them; proofs not read]: Lemma 18, "`‖X_u − Z_u‖_F ≤ O(depth(u)·E_align) + O(E_local)`" for sequentially stitched spectral patches; `O(·)`
  constants, patches of eigenvectors rather than distances, no lever arm.  (The note already cites this through the earlier review.)
* *Seen only in search summaries or as a record, not read:* Kohli, Mishne and Cloninger, arXiv 2303.11620 (rigid alignment of overlapping patches)
  [search summary]; Maystre et al., arXiv 2510.13406 [record only] (a Procrustes bound from approximately preserved dot products); Singer, PNAS 105
  (2008) [search summary].
* [from memory — unverified, not opened] The continuum estimate that the note names as its model, Friesecke–James–Müller's geometric rigidity
  (`‖∇v − R‖_{L²} ≤ C‖dist(∇v, SO(n))‖_{L²}` for every `v ∈ W^{1,2}`), is itself free of any smallness condition; if that recollection is right, the
  absence of a threshold is inherited from the model too, and what is specific to distance data is the treatment of mirror images (five-point
  windows sharing tetrahedra).

**What this search did not reach.**  zbMATH, MathSciNet; a citation chase of Tu et al.'s Lemma 5.4 into distance geometry and sensor-network
localisation — the most likely place for a threshold-free stitching bound if one exists; the journal versions of the papers above (SIAM J. Math.
Data Sci. for Arias-Castro–Vishwanath; JMLR for Arias-Castro–Javanmard–Pelletier; SIAM J. Optim. for the facial-reduction paper); Krislock and
Wolkowicz (2010); the items the earlier review already listed as unread (Schrader 1967; Luo and Wu 2011; Anderson, Shames, Mao and Fidan 2010;
Friesecke–James–Müller 2002); the geodesy of trilateration chains; nothing in languages other than English.

**Log** (every query and address; nothing of this project in any query).

| # | address or query | what it gave | reading level |
|---|---|---|---|
| W1 | `https://arxiv.org/abs/1507.03566` | record of Tu et al.: v1 13 Jul 2015, v2 5 Feb 2016 | record only |
| W2 | `https://arxiv.org/pdf/1507.03566v2` (23 pages; text extraction, and pages 9, 20, 21 rendered and read) | Lemma 5.4 (p. 9) and its proof (Appendix A, pp. 20–21) | the passage |
| W3 | `https://proceedings.mlr.press/v48/tu16.pdf` (10 pages) | ICML 2016 version: the same Lemma 5.4 | the passage (statement) |
| W4 | `https://arxiv.org/abs/2207.07218` | Arias-Castro & Chau; "Theory was removed to spin off another paper" | record only |
| W5 | `https://arxiv.org/abs/2310.10900` | record: v1 17 Oct 2023, v3 8 Dec 2024 | record only |
| W6 | `https://arxiv.org/pdf/2310.10900v3` | Theorems 2.1, 3.1, Proposition 3.2, (2.6), (2.7) | the passages |
| W7 | query: stability bound network localization lateration graph noise "polynomial" accumulation of error Procrustes stitching overlapping cliques global bound without small noise assumption | the arXiv 2310.10900 pages; Moore et al. 2004 | search summary |
| W8 | query: patch stitching embedding error bound Procrustes alignment overlapping patches error accumulation number of patches theorem rigid alignment noise | arXiv 2207.07218, 2303.11620, 2604.21094, 2510.13406 | search summary |
| W9 | query: noisy Euclidean distance matrix completion overlapping cliques facial reduction error bound chordal graph singularity degree Hölder error bound square root | arXiv 1410.6852, 1405.2037 | search summary |
| W10 | query: quantitative global rigidity estimate point configuration from distances "for all" configurations no smallness assumption chain of simplices sequence local distances stability constant length squared | qualitative global-rigidity papers; Singer 2008; Javanmard–Montanari | search summary |
| W11 | `https://arxiv.org/pdf/1410.6852` | Theorem C.5 | the passages |
| W12 | `https://arxiv.org/abs/2510.13406` | record of Maystre et al. | record only |
| W13 | query: "Procrustes" "Gram" inequality dist(U,X)^2 ≤ ||UU^T − XX^T||_F^2 / (2(√2−1)σ_r^2) lemma multidimensional scaling perturbation bound classical scaling global | Arias-Castro–Javanmard–Pelletier | search summary |
| W14 | `https://arxiv.org/pdf/2604.21094` | Lemmas 17, 18 | the passages |
| W15 | `https://arxiv.org/pdf/1810.09569` | Theorem 1 | the passage |

Downloaded files were kept outside the repository, in the session's scratch directory, and read as text.

## 6. What I did not check; my own errors; files

**Not checked.**  (1) Their code and their numbers as such (0.76, 0.064, 0.002, 0.99, 6·10⁻⁵, 5.06/265): no re-run; mine are on other instances.
(2) Theorem K(a), K(b), Proposition L₀ and §3.5: outside the brief (K(c) re-derived only because L.3 rests on it).  (3) Nothing was formalised.
(4) The searches are local optimisers in double precision: the suprema of §3 are lower bounds, with no certificate; joint searches up to `n` = 40
only, `X`-fixed searches up to `n` = 20.  (5) Remarks 4 and 6: only the local form on instances, not uniform constants; chains of windows of
unequal size: not replicated.  (6) Whether a global bound survives the loss of an interior pair of separation ≤ 3 (my conjecture, unproved).
(7) The proof of Lemma 5.4 in the ICML version (it is not in the ten pages), the journal versions of the papers of §5.  (8) The worst-case
configurations of F1 were found on four idealised traces; they are explicit and re-evaluated, but the thresholds quoted are upper bounds for the
true minima, and nothing was done on measured structures.

**My own errors** (all caught before they reached a result; none left in a cited log).  (a) The first adversarial script formed the per-point ratio
with no noise floor: for a reflected tail the points before the reflection have a bound that is exactly 0 and a distance of 10⁻¹⁵, which printed
"ratios" of 1.9, 23 and 2·10¹⁵ and "violations".  Both runs were stopped (`item2_adv_fixedX_run1.log`, `item2_adv_joint_run1.log`: incomplete, not
cited), diagnosed (`diag_ptratio_run1.log`), fixed and rerun.  (b) `item3_Lplus.py` formed `Y = X + V` in double precision inside a range where the
displacements are 10⁻⁹…10⁻⁴: six spurious "violations" by ≤ 5.5·10⁻⁶; replaced by `item3_Lplus_v2.py`, which computes `η` and `d_P` from `V`
without cancellation (cross-checked) — 0 violations at tolerance 10⁻¹⁰.  Part (2) of `item3_Lplus_run1.log` is not to be cited.  (c) An `assert`
of mine (an instance filter, not a theorem check) stopped `item4_examples_run1.log`; rerun as `_run2`.  (d) Two versions of the scan in
`item4_worstcase_verify.py` used SLSQP and returned "none" in most rows (and one printed a control from the wrong row); replaced by a penalty
formulation (`_run3`); Part 2 of `_run1`, `_run2` is not to be cited.  (e) My notes first said "26 reference chains" for the fixed-`X` search; it
is 19 (corrected in the notes).  (f) The last line of `item2_battery_run1.log` says "False" for "every control failed" because the uniform constant
divided by 10 or 100 is not violated by that battery; the wording was fixed for `_run2` (divided by 100 it is violated in the searches, row 11; divided by 10 by nothing I found).
(h) Small text-editing commands on my own files (string replacements) were run as `python3 -` without `-B` and without the memory cap; they
import nothing of mine and compute nothing, and left no cache directory.  (i) A 50-second trial of `item2_adv_jointU.py` went to the terminal, not
to a log; none of its numbers is cited.  (j) Never more than two computations of mine ran at once; while two were running I did run short
commands beside them (downloads, text extraction, `grep`, file edits) — negligible load, but more than two processes for moments.
(g) One run (`item2_adv_jointU_run2_large…`) took 596.9 s, within the ten-minute limit by three seconds.

**Tool actions declined:** one — a foreground `sleep 100` before reading two logs was blocked by the shell tool; it was not worked around (no
further sleeps; the logs were read when complete).  No write, network or other action was declined.

**Files** (`/home/user/MetricChain/experiments/science/ws_R27/`).  `NOTES.md` (log, the first-pass review by hand, both web tables).  Library:
`r27lib.py`, `thmL_steps.py`.  Scripts and the complete logs to cite: `item1_lemmas.py` → `item1_lemmas_run1.log`; `item2_battery.py` →
`item2_battery_run2.log` (and `_run1`, the version before the role exchange was added); `item2_adv_fixedX.py` → `_run2.log`;
`item2_adv_joint.py` → `_run2.log`; `item2_adv_jointU.py` → `item2_adv_jointU_run1_seed27116.log`, `…_seed27117.log`,
`item2_adv_jointU_run2_large_seed27121.log`; `item2_adv_step2.py` → `_run1.log`; `item2_cor_L3.py` → `_run1.log`; `item2_corollaries.py` →
`_run1.log`; `item3_Lplus_v2.py` → `item3_Lplus_v2_run1.log` (`item3_Lplus.py`/`_run1.log`: superseded, its part (3) only); `item4_tables.py` →
`_run1.log`; `item4_examples.py` → `_run2.log`; `item4_worstcase.py` → `_run1.log` and `item4_worstcase_found.npz`; `item4_worstcase_verify.py` →
`_run3.log`; `item4_extras.py` → `_run1.log`; `diag_ptratio.py` → `_run1.log`.  Each script caps its address space at 2 GB and prints its peak
memory in its last line (largest: 136 MB).  The `.npy` files hold the best pairs `(X, Y)` of the searches (`…_seed1.npy`: a 50-second trial printed
to the terminal).  The scripts on disk are the versions of the last run of each.  To re-run any of them:
`cd /home/user/MetricChain/experiments/science/ws_R27 && OMP_NUM_THREADS=1 python3 -B <script> > <new log>`.

---

## Coordinator's status (checkpoint 69) — a placeholder, not yet a coordinator's note

The agent handed back at about 23:59 UTC on 26 November 2026 (0.59 million tokens, 73 minutes, 115 tool uses).
**This report has not yet been read in full or checked by the coordinator, and nothing of it has been sent to
the Geometry division.**  It is committed at this checkpoint so that it cannot be lost; until a coordinator's
note replaces this paragraph and a SCI-REV message publishes the findings, nothing above is a finding of the
division.  By its hand-back: no statement of the Geometry division's note is false and no proof has a gap;
one major finding that affects no theorem (the first-order constant is not the global one, and the
first-order regime is short); eleven minor findings.  The agent reported one declined tool action — a
foreground wait for its own running jobs, blocked by the shell tool; not worked around, and nothing was asked
of the coordinator — and it lists ten web addresses and five generic search queries (its §5).
