# Sequence-local distance data: the stability constant grows like the square of the length, and no faster

**Geometric Inference division — cycle 2, first note** (lower bounds: fifth checkpoint;
upper bound, Theorem L: eighth checkpoint).  Labels as in `ENSEMBLE_RIGIDITY.md`.
§3 reviewed by the Science division (SCI-REV-0028); §1, §2, §3.5 not.  Single conformations, no ensembles.

> **Read this first (tenth checkpoint, 2026-11-26).**  The Science division reviewed the
> originality of this note at our request (SCI-REV-0023; our proofs were not reviewed).
> Its findings are adopted in §5 and §6: Theorem L was not found in print, but **its
> mechanism and its exponent are those of the geometric rigidity estimate in a thin rod**,
> and its ingredients are printed for lattices; polynomial first-order bounds for chains of
> simplices are in print; Theorem K(a) is in print with a better constant.  Its question
> about the threshold led to the present form of Theorem L, **which has no threshold**, and
> to Theorem L⁺.  Its assessment of relevance stands and is sharpened in §6: **these are
> theorems about the exponent and the first-order constant; for data of realistic accuracy
> their guarantees are empty.**  §3 was rewritten at the tenth checkpoint.
>
> **And this (thirteenth checkpoint, 2026-11-27).**  §3 has now been **reviewed with
> replication by the Science division** (SCI-REV-0028, an internal review by another
> session, not external peer review): Lemmas P, Q, Theorem L in both forms, Corollaries
> L.1–L.3 and Theorem L⁺ are proved as stated; Lemma P was verified at its source.  One
> finding changes what a reader may conclude, and it is theirs: **the first-order constant
> is not a global constant, and the first-order regime is short** — local distances fitted
> to three tenths of an ångström admit configurations farther away than the radius of
> gyration; the factor `1/τ` of Theorem L is necessary.  We replicated it independently
> (`experiments/geometry/distant_fits.py`).  All twelve findings are applied below, each
> marked "SCI-REV-0028"; the wordings in §6 (i), (ii) follow the review's proposals.

## 0. Summary

Let a chain of `n` points be observed through distances between points whose sequence
separation is at most `K` (bond lengths and angles are the cases `K = 1, 2`; a
"trilateration" pattern needs `K ≥ 4`).  Such data determine a generic chain as soon as
`K ≥ 4`.  This note quantifies how well.  The stability constant

    C = sup  (superposition distance of two conformations) / (ℓ² difference of their measured distances)

is at least of order `n/K^{3/2}` for **every** configuration and every pattern of range `K`
(Theorem K(a); known in substance), at least the *per-torsion superposition constant* of the
theory report divided by `b·K²/(4√3)` (Theorem K(b): a duality between the lever-arm law
and the instability of local data; global, not infinitesimal), and at least of order
`n²/K^{3/2}` on helices and on every chain confined to a thin tube (Theorem K(c), now a
proof).  **And it is never worse than `n²`** (Theorem L): for a chain whose windows of four
consecutive points are non-degenerate, **every** point configuration — with no smallness
condition at all — is within `1.2 (b/(s_*τ_*)) (n + 2)²` times the `ℓ²` difference of the
squared distances of sequence separation at most 4, up to a rigid motion; the constant has
a local form in which a thin window costs only through its own thickness.  For small
errors the constant is the first-order one, `1/(2μ)`, in an explicit range (Theorem L⁺).
The published *global* perturbation bound for this situation in the localisation
literature (Arias-Castro–Vishwanath) is exponential in `n`; for the first-order problem
polynomial bounds are in print, and the continuum analogue — the geometric rigidity
estimate in a thin rod — has exactly this scaling (§5).  So for rod-like chains the
stability constant of sequence-local distance data is `Θ(n²)`, with explicit constants on
both sides (far apart: on the helix-like trace of §6 they are `2.3·10⁻⁴` and `28.8`, the
computed value `0.0104` — SCI-REV-0028 F9).  **What this does not give** (§6): the range in which the absence of distant
solutions is certified is far below any measurement accuracy, so for realistic data these
are statements about scaling, not guarantees.  Consequences: a length-independent stability constant needs measured pairs
of sequence separation at least of order `n^{2/3}` for any configuration, whatever the
number of local measurements; and on a rod-like chain **no** set of pairs has one in this
normalisation — even complete distance data have a constant of order `√n` at least, because
bending changes every distance only through the lever arm (radius over length).

## 1. Setting

`x_1, …, x_n ∈ ℝ³`; `F` a set of pairs with `|i − j| ≤ K`; `d_F(X) = (|x_i − x_j|)_{ij ∈ F}`;
`d_P(X, Y) = min_g ‖X − gY‖_F` over isometries `g` (`√n ·` RMSD after optimal superposition).
The **rigidity matrix** `R = R(F, X)` has a row `ê_ij ⊗ (e_i − e_j)` for every measured pair,
`ê_ij = (x_i − x_j)/|x_i − x_j|`: it is the derivative of `d_F`.  Its singular values in
increasing order are `s_1 ≤ s_2 ≤ …` (with `3n − |F|` zeros added if `|F| < 3n`); if the
configuration spans space the six infinitesimal isometries give `s_1 = … = s_6 = 0`, and the
framework is infinitesimally rigid iff `s_7 > 0`.  Then for infinitesimal displacements `V`
orthogonal to the isometries, `‖V‖ ≤ s_7^{-1} ‖R V‖`, and `1/s_7` is the best constant: the
**infinitesimal stability constant** `C_inf = 1/s_7`.  The **global stability constant** is
`C_glob = sup_{X ≠ Y} d_P(X, Y)/‖d_F(X) − d_F(Y)‖₂`, the supremum over pairs of chains with the
same statewise data; `C_glob ≥ C_inf` at every conformation.

## 2. Results

**Theorem K.**
(a) *Every configuration, every pattern of range `K`* **[P; known in substance — §4]**.

    s_7(R)² ≤ (5π²/3) · K(K+1)(2K+1) / n²,       hence      C_inf ≥ n / (π√10 · K^{3/2}) ≥ n/(10 K^{3/2}).

(b) *Torsion–distance duality (global)* **[P]**.  Let `X` be a chain with bonds of length at
most `b` and `Y` its image under a rotation of the atoms beyond bond `(p, p+1)` about that
bond by an angle `δ` (a torsion move: bond lengths and bond angles are unchanged).  Then

    ‖d_F(X) − d_F(Y)‖₂ ≤ 2 sin(δ/2) · b · √T_K,     T_K = Σ_{s=3}^{K} Σ_{t=1}^{s−2} min(t, s−1−t)² ≤ K⁴/48,

(`T_K = 1, 3, 9, 19, 38, 66` for `K = 3, …, 8`), and therefore

    C_glob ≥ κ_p(δ) / (b √T_K),        κ_p(δ) := d_P(X, Y) / (2 sin(δ/2)).

`κ_p(δ)` is the *exact* per-torsion superposition constant — the quantity that theory report
Theorem 4.6 bounds from above by `√(min(I_A, I_B))` and that at the worst conformation is at
least `0.61·b·m^{3/2}/(2 sin 60°)` for arms of `m = 8` atoms (GEOMETRY-RES-0002).  So **the
lever-arm law has a mirror image in inference: local distance data are unstable by at
least the per-torsion constant divided by `b√T_K ≤ bK²/(4√3)`**, i.e. `C_glob ≳ m^{3/2}/K²`.
(c) *Chains in a tube* **[P]**.  Let the points lie within distance `ρ` of a line, with
equally spaced axial coordinates `z_i = (i − ½)h` (an ideal helix; `L = nh`), `n ≥ 4`.  Then
for every set `F` of pairs

    s_7(R)² ≤ 196 π⁴ ρ² Σ_{jk ∈ F} |x_j − x_k|² / (n L⁴),

so for all pairs of separation at most `K` and bonds of length at most `b`:
`s_7 ≤ 14π² ρ b K^{3/2}/(h² n²)` and `C_inf ≥ h² n²/(139 ρ b K^{3/2})`.
*Numerically* **[N]**, for helical chains (constant torsion 60° or 150°, bond angle 111°)
and `K ∈ {4, 6}`: `s_7 = c/n²` with fitted exponents `−1.98 … −2.00` (`n = 40 … 160`); e.g.
`s_7 n² = 63` for the 60° helix with `K = 4`, where the bound gives `825`.  The softest mode is
a torsional (bending) motion: the smallest generalised singular value on the space of
torsional velocity fields is within 5 % of `s_7`.

*Proof of (a).*  By the Courant–Fischer principle `s_7² ≤ s_9² ≤ max_{v ∈ S} ‖Rv‖²/‖v‖²` for
any 9-dimensional space `S` of displacement fields.  Take `S = {v_i = Σ_{m=0}^{2} f_m(i) a_m :
a_m ∈ ℝ³}`, `f_m(i) = cos(mπ(i − ½)/n)` (orthogonal on `{1..n}`, `Σ f_0² = n`, `Σ f_m² = n/2`).
Then `‖v‖² ≥ (n/2)(|a_1|² + |a_2|²)`, and since `|ê·(v_i − v_j)| ≤ |v_i − v_j|` and
`|f_m(i) − f_m(j)| ≤ mπ|i − j|/n`,
`‖Rv‖² ≤ (|a_1|² + |a_2|²)(1 + 4)(π²/n²) Σ_{ij∈F}(i − j)²`, with
`Σ_F (i − j)² ≤ n Σ_{s=1}^{K} s² = nK(K+1)(2K+1)/6`.  ∎

*Proof of (b).*  Atoms `1, …, p+1` do not move and atoms `p, p+1` are on the axis, so a
measured distance changes only for a pair `i ≤ p − 1`, `j ≥ p + 2`.  For such a pair
`|d_ij(X) − d_ij(Y)| ≤ |y_j − x_j| = 2 sin(δ/2)·dist(x_j, axis) ≤ 2 sin(δ/2)(j − p − 1)b`, and,
moving the other side instead, `≤ 2 sin(δ/2)(p − i)b`.  With `s = j − i ≤ K` and `t = p − i`
there are `s − 2` pairs for each `s`, with `min(t, s − 1 − t)` as the smaller lever.  With
`u = s − 1` the inner sum is `u³/12 + u/6` (`u` even) or `(u³ − u)/12` (`u` odd), and summing
over `2 ≤ u ≤ K − 1` gives at most `K⁴/48 − K³/24 + 5K²/48 − K/12 − ¼ ≤ K⁴/48` for `K ≥ 3`.  ∎

*Proof of (c).*  Take the line as the `z`-axis.  For functions `W_1, W_2` of `z` let
`V(x, y, z) = (W_1(z), W_2(z), −xW_1′(z) − yW_2′(z))` (the displacement field of a bent rod).
The symmetric part of `∇V` has the single non-zero entry `−(xW_1″ + yW_2″)` at `(z, z)`, so
for two points with difference `Δ`,
`(V(P) − V(P′))·Δ = −Δ_z² ∫_0^1 (xW_1″ + yW_2″)(P′ + tΔ) dt`, of absolute value at most
`|Δ|² ρ max|W″|` inside the tube (`|W″|` the Euclidean norm of `(W_1″, W_2″)`).  Let `S` be the
space of the fields `v_i = V(x_i)` with `W_c = Σ_{m=0}^{3} α_{c,m} cos(mπz/L)`: by the discrete
orthogonality of the cosines at the points `z_i`, `‖v‖² ≥ (n/2)A²` with
`A² = Σ_c Σ_{m ≥ 1} α_{c,m}²` and `dim S = 8`; and `|W″| ≤ (π/L)² √98 · A`.  Hence
`‖Rv‖² ≤ 98 (π/L)⁴ ρ² A² Σ_F |x_j − x_k|²` and the Rayleigh quotient on `S` is at most the
right-hand side of (c); `s_7² ≤ max_S` by Courant–Fischer.  ∎

**Corollary K.1 (long-range data are necessary) [P from (a), (b), (c)].**  If a
measurement pattern of range `K` has `C_inf ≤ c₀`, then `K ≥ (n/(10c₀))^{2/3}`; if `C_glob ≤ c₀`
on a domain containing a conformation with per-torsion constant `κ`, then
`K² ≥ 4√3 κ/(b c₀)` — for `κ ∝ n^{3/2}` (extended arms): `K ≳ n^{3/4}`.  On an ideal helix (c)
gives `C_inf ≥ h²n²/(139 ρ b K^{3/2}) ≥ h²√n/(139 ρ b)` for every `K ≤ n`: no set of pairs,
not even the complete one, has a length-independent constant there.  (In root-mean-square
terms: superposition error per point over distance error per pair is at least of the order
of the aspect ratio `L/ρ`.)  The number of local measurements does not enter.
(An earlier version said "`K ≳ n^{4/5}` on helices", from a scaling `n²/K^{5/2}` that was a
heuristic and is not what the computations show — `s_7n² = 63` and `81` for `K = 4` and `6`;
the proved statement is the one above.  `DEAD_ENDS.md` DG-19.)

**Remark (why `n²`).**  A torsion move concentrates the strain on the pairs that straddle
one bond; a coherent bending spreads it over all bonds, and its strain is the curvature
`∼ A/L²` times the distance from the axis, which is the proof of (c).  In the rod model the
displacement of a coherent bending is the free–free beam form of GEOMETRY-RES-0002.

## 3. A matching global upper bound — without a threshold

*Revised at the tenth checkpoint.*  The form of the eighth checkpoint (Proposition L₀, §3.5)
had a smallness condition (S).  The Science division asked how small it has to be
(SCI-REV-0023 §5, question 1).  It is not needed.  The distances of separation at most 4
are **all** the distances inside every window of five consecutive points, and a point set
with complete distance data is controlled by an inequality between Gram matrices that has
no smallness assumption; consecutive five-point windows share a tetrahedron, not a
triangle, so their frames can be compared without a separate argument about reflections.

**Notation.**  For a set `S` of consecutive indices let `X_S` be the matrix whose rows are
the points `x_i`, `i ∈ S`, `c_S` their centroid, and `σ₃(S)` the third singular value of the
centred matrix `X_S − 1c_Sᵀ` — the *thickness* of the window,
`σ₃(S)² = min_{|u| = 1} Σ_{i∈S} ((x_i − c_S)·u)²`, which is non-decreasing in `S`.  For `n ≥ 5`:

    W_i = {i, …, i+3},   τ_i = σ₃(W_i)   (1 ≤ i ≤ n−3);        F_i = {i, …, i+4},   s_i = σ₃(F_i) ≥ max(τ_i, τ_{i+1})   (1 ≤ i ≤ n−4);
    τ_* = min_i τ_i ,     s_* = min_i s_i ,     b = max_i |x_{i+1} − x_i| .

`τ_* > 0` iff no four consecutive points are coplanar; `τ_*` lies between half of the `τ` of
§3.5 and that `τ`.  For a second configuration `Y`: `η_jk = |y_j − y_k|² − |x_j − x_k|²`; `‖η‖₂` is
its norm over **all pairs of separation at most 4**; `e_i` its norm over the ten pairs
inside `F_i`.

**Lemma P (Procrustes–Gram inequality) [K].**  For `U, X ∈ ℝ^{m×r}` with `X` of rank `r`,

    min_{R ∈ O(r)} ‖U − XR‖_F²  ≤  ‖UUᵀ − XXᵀ‖_F² / ( 2(√2 − 1) σ_r(X)² ) .

(Tu, Boczar, Simchowitz, Soltanolkotabi and Recht, *Low-rank Solutions of Linear Matrix
Equations via Procrustes Flow*, Proc. 33rd ICML, 2016, Lemma 5.4; arXiv 1507.03566v2,
Lemma 5.4 — we cited it from memory; **the statement and the number were checked at the
source by the Science division** (SCI-REV-0028 F5), which also notes that the constant is
attained for every `X` when `m > r`.  The proof here is self-contained.)

*Proof.*  Replace `X` by `XR` for an optimal `R`; then `XᵀU` is symmetric positive
semidefinite (`R` is the orthogonal polar factor of `XᵀU`).  Put `Δ = U − X`, `A = ΔᵀΔ ⪰ 0` and
`B = XᵀΔ = XᵀU − XᵀX`, a symmetric matrix with `B ⪰ −XᵀX`.  From
`UUᵀ − XXᵀ = ΔXᵀ + XΔᵀ + ΔΔᵀ`, expanding the square of the Frobenius norm,

    ‖UUᵀ − XXᵀ‖_F² = 2 tr(XᵀX·A) + [ tr A² + 4 tr(AB) + 2 tr B² ] .

Since `tr (A + √2 B)² ≥ 0`, the bracket is at least `(4 − 2√2) tr(AB) ≥ −(4 − 2√2) tr(A·XᵀX)`.
Hence `‖UUᵀ − XXᵀ‖_F² ≥ (2√2 − 2) tr(XᵀX·A) ≥ 2(√2 − 1) σ_r(X)² ‖Δ‖_F²`.  ∎

**Lemma Q (a window with complete distance data) [P].**  Let `S` be a set of at least four
indices with `s = σ₃(S) > 0`, let `Y` be **any** configuration and `e` the `ℓ²` norm of `η` over
the pairs in `S`.  Then there are `R ∈ O(3)` and `t ∈ ℝ³` with

    ‖Y_S − X_S R − 1tᵀ‖_F ≤ κ e / s ,        κ = 1/(2√(√2 − 1)) < 0.777 .

*Proof.*  The Gram matrix of a centred configuration is `−½ J D J` (`D` the matrix of squared
distances, `J` the centring projection).  So the Gram matrices of the two centred windows
differ by `−½ J E J`, `E = (η_jk)_{j,k∈S}`, of Frobenius norm at most `½‖E‖_F = e/√2`.  Apply
Lemma P to the centred windows.  ∎

*The constant is essentially optimal, and the dependence on `s` is attained on every
window* [N; the Science division's review SCI-REV-0028, F3, whose wording this is — our
earlier sentence claimed sharpness from an inequality in the wrong direction].  The
supremum of `‖Y_S − X_SR − 1tᵀ‖_F·s/(κe)` over pairs of five-point windows is at least `0.97`
(numerically), and on a fixed window collapsing its thin direction gives at least `0.73` on
the windows tried.  The reflection of SCI-REV-0023 §5 (a) — mirror one end point of `F_i` in
the plane of its three middle points: exactly one squared distance changes, by `4h⁻h⁺`, and
the window moves by at most `2 min(|h⁻|, |h⁺|)` — attains the bound `3.11|h⁻h⁺|/s` only up to a
factor that depends on the shape of the window: `0.55` on a helix-like window, `0.21`–`0.24`
on strand-like ones, arbitrarily small when the three middle points are nearly collinear.

**Theorem L (global quantitative rigidity from sequence-local distances; no threshold)
[P].**  Let `s_i > 0` for all `i` and `τ_i > 0` for `2 ≤ i ≤ n − 4` (for `n ≥ 6` the second
condition implies the first); in this theorem `τ_*` may be read as `min_{2 ≤ i ≤ n−4} τ_i` —
**the end windows `W_1`, `W_{n−3}` may be flat**; for `n = 5` the theorem is Lemma Q.  For
**every** configuration `Y` of `n` points in `ℝ³` there is an isometry `g` (possibly improper)
such that for every `k`, with `i(k)` any index such that `k ∈ F_{i(k)}` — the smallest,
`i(k) = max(1, k − 4)`, gives the best bound; our scripts use the largest —
`δ_j = κ e_j/s_j` and `c_{j+1}` the centroid of `W_{j+1}`,

    (local)      |y_k − g(x_k)|  ≤  δ_{i(k)} + Σ_{j < i(k)} (δ_j + δ_{j+1}) · ( |x_k − c_{j+1}| / τ_{j+1} + ½ ) ,

and consequently

    (uniform)    ‖Y − gX‖_F  ≤  1.2 · (b / (s_* τ_*)) · (n + 2)² · ‖η‖₂ .

Nothing is assumed about `Y`: no closeness to `X`, no bound on the errors, no chain
structure — except that `Y` is a configuration **in `ℝ³`** (essential: SCI-REV-0028 F2).
[The hypothesis on interior windows only and the free choice of `i(k)` are the Science
division's observations (SCI-REV-0028 F4, F7): Step 2 uses `τ_{j+1}` for `1 ≤ j ≤ n − 5` only,
and Step 3 holds for every window that contains `k`.  We re-read the proof with them and
agree.  An interior window may not be flat: then `η = 0` with `d_P > 0` occurs.]

*Proof.*  Points are row vectors; an isometry is `x ↦ xR + t`.
*Step 1 (windows).*  Lemma Q for each `F_i` gives `R_i ∈ O(3)`, `t_i` and a residual
`ε_i = Y_{F_i} − X_{F_i}R_i − 1t_i` with `‖ε_i‖_F ≤ δ_i`.
*Step 2 (consecutive frames).*  `F_j` and `F_{j+1}` share the four points of `W = W_{j+1}`, and on
these rows `X_W R_j + 1t_j + ε_j = X_W R_{j+1} + 1t_{j+1} + ε_{j+1}`.  Centring the rows:
`(X_W − 1c_W)(R_j − R_{j+1})` is the centred difference of two residuals, of norm at most
`δ_j + δ_{j+1}`; the matrix `X_W − 1c_W` has full column rank and smallest singular value
`τ_{j+1}`; so `‖R_j − R_{j+1}‖_F ≤ (δ_j + δ_{j+1})/τ_{j+1}`.  Averaging the rows instead:
`t_{j+1} − t_j = c_W(R_j − R_{j+1}) + m_j`, where `m_j` is the difference of the means of the
two residuals over `W`, `|m_j| ≤ (δ_j + δ_{j+1})/2` (a mean of four vectors has norm at most
half the Frobenius norm).  No statement about determinants is needed: if two consecutive
frames had opposite orientation, `‖R_j − R_{j+1}‖_F ≥ 2` would simply be a large term.
*Step 3 (telescoping).*  Let `g(x) = xR_1 + t_1` and `i = i(k)`, so that `k ∈ F_i`.  Then

    y_k − g(x_k) = ε_i(k) + Σ_{j<i} [ x_k(R_{j+1} − R_j) + t_{j+1} − t_j ] = ε_i(k) + Σ_{j<i} [ (x_k − c_{j+1})(R_{j+1} − R_j) + m_j ] ,

and taking norms gives (local).
*Step 4 (uniform constants).*  `|x_k − c_{j+1}| ≤ b(k − j + ½)` for `j < i(k)`.  A pair lies in
at most four of the windows `F_i`, so `Σ_j e_j² ≤ 4‖η‖₂²` and
`Σ_j (δ_j + δ_{j+1})² ≤ (4κ‖η‖₂/s_*)²`.  By the Cauchy–Schwarz inequality and
`Σ_{u<k}(u + ½)² ≤ (k + ½)³/3`:

    |y_k − g(x_k)| ≤ (κ‖η‖₂/s_*) · [ 4b(k + ½)^{3/2}/(√3 τ_*) + 2√k + 1 ] .

Summing the squares over `k` (`Σ_k (k + ½)³ ≤ (n + 3/2)⁴/4`, `(2√k + 1)² ≤ 9k`), using
`τ_* ≤ 1.3 b` (the centred tetrahedron has `Σ|x_p − c|² = ¼Σ_{p<q}|x_p − x_q|² ≤ 5b²`) and `n ≥ 5`:
`‖Y − gX‖_F ≤ 1.18 (b/(s_*τ_*)) (n + 3/2)² ‖η‖₂`.  ∎

**Corollary L.1 (any estimator that fits as well as the truth; any noise level) [P].**  Let
`q_jk = |x_j − x_k|² + ε_jk` for `|j − k| ≤ 4` and let `Ŷ` be any configuration with
`Σ(|ŷ_j − ŷ_k|² − q_jk)² ≤ Σ ε_jk²` — for instance a global minimiser of this stress.  Then
`min_g ‖Ŷ − gX‖_F ≤ 2.4 (b/(s_*τ_*)) (n + 2)² ‖ε‖₂`.  (`‖η(Ŷ)‖₂ ≤ 2‖ε‖₂`.)  (The hypothesis cannot be
checked from the data, `Σε²` being unknown: it holds for a global minimiser of the stress,
not for the output of a local optimiser — SCI-REV-0028 F10.)

**Corollary L.2 (an error bar computed from the estimate alone) [P].**  Let `Ŷ` be *any*
configuration **of `n` points in `ℝ³`** with `τ_*(Ŷ) > 0` — the output of any algorithm **that
returns three-dimensional coordinates** — and let the data be `q_jk = |x_j − x_k|² + ε_jk` **for
all `4n − 10` pairs of separation at most 4**, for an unknown configuration `X` **in `ℝ³`**, with
`‖ε‖₂ ≤ ν` **(errors of the squared distances)**.  Then

    min_g ‖X − gŶ‖_F ≤ C(Ŷ) · ( ‖r‖₂ + ν ),     r_jk = |ŷ_j − ŷ_k|² − q_jk ,     C(Ŷ) = 1.2 b(Ŷ)(n + 2)² / (s_*(Ŷ) τ_*(Ŷ)) .

Every quantity on the right is computed from the estimate, the data and the noise bound;
nothing is assumed about `X`.  (Theorem L with `Ŷ` as the reference configuration and `X` as
the arbitrary one.)  The absence of a smallness condition makes the bar unconditional;
with a threshold it would exist only below the threshold.  **The statement is false for
an estimate in `ℝ⁴`** — an unprojected semidefinite or scaling solution: `y_i = (x_i, εw_i)`,
`w` the affine dependency of a five-point window, has `‖η‖₂ = O(ε²)` and `d_P ≍ ε`.  [The three
conditions in bold and this counterexample are the Science division's (SCI-REV-0028 F2);
the corollary was right, its wording hid them.]

**Corollary L.3 (the exponent is sharp; `Θ(n²)` on helices; infinitesimal rigidity with a
constant) [P].**  (a) For ideal helices of fixed geometry and distances of separation at
most `K`, `4 ≤ K` fixed, the first-order constant for *distance* errors is at least
`h²n²/(139 ρ b K^{3/2})` (Theorem K(c)) and at most `9.6 (b²/(s_*τ_*)) (n + 2)²` (Theorem L:
for distance errors `δ`, `η_jk = δ_jk(2|x_j − x_k| + δ_jk)` and `|x_j − x_k| ≤ 4b`; more measured
pairs can only lower the constant).  (b) For every chain with `τ_* > 0` the
smallest non-zero singular value `μ` of the matrix `A` of Theorem L⁺ satisfies
`μ ≥ s_*τ_*/(2.4 b (n + 2)²)`: apply the theorem to `Y = X + tV` and let `t → 0`.

**Theorem L⁺ (the sharp constant, in a certified range) [P].**  Let `A` be the matrix with one
row per pair of separation at most 4 — `(x_j − x_k)ᵀ` in the block of `j`, its negative in the
block of `k`: half the Jacobian of the squared distances — and `μ > 0` its smallest non-zero
singular value (the `(3n − 6)`-th).  Let `Λ` be the largest Laplacian eigenvalue of the graph
of measured pairs (`Λ < 11.04`) and `C_L` any constant for which Theorem L holds for `X` — the
uniform one, or `2‖M‖₂` with `M` the matrix of the local form, which is 5 times smaller on
the 20-point helix-like trace (88.7 against 456; SCI-REV-0028 F8).  Let `X` be as in
Theorem L (then `μ > 0` by Corollary L.3 (b)).  For every `Y` **in `ℝ³`** with `‖η‖₂ ≤ μ/(ΛC_L)`:

    d_P(X, Y) ≤ ‖η‖₂ / ( μ + √(μ² − Λ‖η‖₂) )    if ‖η‖₂ ≤ μ²/Λ ,        and    d_P(X, Y) ≤ ‖η‖₂/μ    in any case.

As `‖η‖₂ → 0` the constant tends to `1/(2μ)`, the first-order constant, which is attained
along the softest mode; at finite amplitude `1/(2μ)` alone is in general not a bound (it
fails along the softest mode `V` whenever `⟨AV, Q(V)⟩ ≠ 0`; on the 20-point helix-like trace
this number vanishes — SCI-REV-0028 F8).  **The range cannot be enlarged to `‖η‖₂ ≤ μ²/Λ`,
and `1/(2μ)` is not a global constant** (§6, reading (ii)).

*Proof.*  Let `g` be optimal, `X′ = gX`, `V = Y − X′`, `v = ‖V‖_F = d_P(X, Y)`.  Optimality gives
`Σ v_k = 0` and `Σ x′_k × v_k = 0`, i.e. `V` is orthogonal to the infinitesimal isometries of
`X′`, which are the kernel of `A_{X′}` (rank `3n − 6`).  Squared distances are quadratic in
the configuration, so exactly `η = 2A_{X′}V + Q(V)` with `Q(V)_jk = |v_j − v_k|²`.  Now
`‖A_{X′}V‖₂ ≥ μ v` (`A_{gX}` and `A_X` have the same singular values) and
`‖Q(V)‖₂ ≤ Σ|v_j − v_k|² ≤ Λ v²`.  Hence `2μv − Λv² ≤ ‖η‖₂`.  By Theorem L,
`v ≤ C_L‖η‖₂ ≤ μ/Λ`, and on `[0, μ/Λ]` the function `v ↦ 2μv − Λv²` is increasing with
`2μv − Λv² ≥ μv`: `v` is at most the smaller root, and at most `‖η‖₂/μ`.
`Λ < 11.04`: the Laplacian of the finite band graph is dominated by the compression of
the infinite one, whose symbol `8 − 2Σ_{s≤4} cos sθ` is at most `11.04`.  ∎

The local half of this argument — a radius of validity from the smallest singular value of
the rigidity matrix and a bound on the second-order term — is standard (for instance
Holmes-Cerfon, Theran and Gortler, arXiv 1908.03802, as described in SCI-REV-0023's report;
not opened by us).  What Theorem L adds is that the statement holds for **every** `Y` whose
data are within the range, not for `Y` in a neighbourhood of `X`: there is no distant
configuration with nearly the same local distances.  The range is small (§6).

**Remarks.**
1. *Where the threshold of the earlier form came from.*  Windows of four points share
   triangles, a triangle does not see on which side the next point lies, and the earlier
   proof excluded the mirror image by a separate estimate that needed the errors to be
   small against `τ⁴/D²`.  Five-point windows share tetrahedra and the question does not
   arise.  The data are the same.
2. *Why not exponential.*  Position errors of a sequential reconstruction multiply; errors
   of orthogonal frames add.  The proof never reconstructs positions step by step.
3. *Local constants (question 2 of SCI-REV-0023 §5).*  In (local) a thin window `j` costs
   `1/(s_jτ_{j+1})` times the lever arm of the points beyond it, not `1/τ_*²` everywhere.
4. *Larger separations (question 3 there).*  With distances of separation at most `K ≥ 4`
   use windows of `K` and `K + 1` consecutive points: (local) holds verbatim with `½`
   replaced by `1/√K`, and the thicknesses can only grow with the window (checked on
   instances for `K = 5, 6, 7`; the uniform constant was written out for `K = 4` only).
5. *The constants.*  On the instances of §4 the left side is at most `0.064` times the local
   bound and `0.002` times the uniform one; these are not worst cases.  An adversarial
   search over both configurations (Science division, SCI-REV-0028 F6) reaches `0.84` of
   the local bound point-wise, `0.43` of it in Frobenius form (`n = 5`; `0.25` at `n = 16`) and
   `0.018` of the uniform bound (`n = 16`: two straight arms joined by a short thin hinge).
   So the local form cannot be improved by more than a small factor in general; the
   uniform constant is at least 55 times too large on every pair tried.
6. *Other dimensions.*  In `ℝ^d`: windows of `d + 1` and `d + 2` points, distances of
   separation at most `d + 1`.

### 3.5 The earlier form (eighth checkpoint): errors of separation at most 3 on the right

Kept because its right-hand side involves the errors of separation at most 3 only (those
of separation 4 enter through a threshold), which Theorem L does not give.  Notation of
this subsection: `P_i = [x_{i+1} − x_i, x_{i+2} − x_i, x_{i+3} − x_i]`, `τ = min_i σ_min(P_i)`,
`D = max_i σ_max(P_i)`.

**Proposition L₀ [P].**  Let `τ > 0` and let `Y` be any configuration of `n` points in `ℝ³` such
that

    (S)    |η_jk| ≤ τ⁴/(73 D²)    for all pairs with |j − k| ≤ 4.

Then there is an isometry `g` with `‖Y − gX‖_F ≤ 6.9 (b/τ²) n(n + 1) ‖η‖_{2, ≤3}`, the norm over the
pairs of separation at most 3.  For this form some condition on the separation-4 data is
necessary: reflecting the points beyond a window in the plane of three consecutive points
changes no distance of separation at most 3.  The size of (S) is far from necessary: the
reflection changes one squared distance of separation 4 by `4h⁻h⁺ ≥ 4τ²/√3`, a factor of at
least `169 (D/τ)²` above (S) (Science division, SCI-REV-0023 §5 (a)).

*Proof.*  *Step 1 (one window).*  Let `Q_i` be the edge matrix of the `i`-th
window of `Y`, `M_i = Q_iP_i^{-1}` (the linear map taking differences of points of the
window of `X` to those of `Y`), and `Δ_i = Q_iᵀQ_i − P_iᵀP_i`.  The entries of `Δ_i` are
`η_{i,i+a}` on the diagonal and `½(η_{i,i+a} + η_{i,i+b} − η_{i+a,i+b})` off it, so
`‖Δ_i‖_F² ≤ 4Σ_a η_{i,i+a}² + (3/2)Σ_{a<b} η_{i+a,i+b}² ≤ 4e_i²`, `e_i` the `ℓ²` norm of `η` on the six
pairs of the window.  `M_iᵀM_i = I + P_i^{-ᵀ}Δ_iP_i^{-1}`, hence
`‖M_iᵀM_i − I‖ ≤ ξ_i := 2e_i/τ²`.  With the polar decomposition `M_i = R_iS_i`, `R_i ∈ O(3)`,
`S_i = (M_iᵀM_i)^{1/2}`: `‖M_i − R_i‖ = ‖S_i − I‖ ≤ ‖S_i² − I‖ ≤ ξ_i` (`|s − 1| ≤ |s² − 1|` for
`s ≥ 0`).  Under (S), `e_i ≤ √6·τ⁴/(73D²)` and `ξ_i ≤ 0.068`.
*Step 2 (consecutive windows have nearly the same rotation).*  The windows `i` and `i + 1`
share three points, so `M_i` and `M_{i+1}` agree on the plane `Π` spanned by
`x_{i+2} − x_{i+1}`, `x_{i+3} − x_{i+1}`.  With `T = R_{i+1}ᵀR_i` and `ξ = ξ_i + ξ_{i+1}`:
`|Tv − v| ≤ ξ|v|` on `Π`; for the unit normal `ν` of `Π`, `Tν = det(T)·(Tu_1 × Tu_2)` gives
`|Tν − det(T)ν| ≤ 2ξ`.  So `‖T − I‖ ≤ √6 ξ` if `det T = 1`, and `‖T − σ_Π‖ ≤ √6 ξ` if
`det T = −1` (`σ_Π` the reflection in `Π`).  The second case is excluded by the distance
between `x_i` and `x_{i+4}`: with `p = x_i − x_{i+1}`, `q = x_{i+4} − x_{i+1}` (both of length at
most `D`), `y_{i+4} − y_i = M_{i+1}q − M_ip`, so `|y_{i+4} − y_i|` differs from `|q − Tp|` by at
most `ξD`, and in the second case from `r := |q − σ_Πp|` by at most `(1 + √6)ξD`.  But
`r² = |q − p|² + 4(p·ν)(q·ν)`, and `|p·ν| ≥ τ/√3`, `|q·ν| ≥ τ` (heights of the two apexes over
the common face: `min_{Σλ=1}|P_iλ| ≥ τ/√3`; the distance of a column of `P_{i+1}` from the
span of the others is at least `τ`).  So `|η_{i,i+4} − 4(p·ν)(q·ν)| ≤ (1+√6)ξD(4D + (1+√6)ξD) ≤ 17ξD²`
would give `4τ²/√3 ≤ |η_{i,i+4}| + 17ξD²`, which (S) forbids
(`|η_{i,i+4}| + 17·4√6·τ²/73 < 2.3τ²`).  Hence `‖R_{i+1} − R_i‖ ≤ √6(ξ_i + ξ_{i+1})` for all `i`.
*Step 3 (errors of rotations add).*  `‖R_i − R_1‖ ≤ 2√6 Σ_{l ≤ i} ξ_l`, because orthogonal
matrices preserve norms — the differences telescope without amplification.  Every bond
vector lies in a window: `y_{j+1} − y_j = M_{ω(j)}(x_{j+1} − x_j)`, `ω(j) = min(j, n − 3)`.  So
`y_i − y_1 − R_1(x_i − x_1) = Σ_{j<i}(M_{ω(j)} − R_1)(x_{j+1} − x_j)` has norm at most
`b Σ_{j<i}(1 + 2√6) Σ_{l ≤ j} ξ_l ≤ 5.9 b ‖ξ‖₂ Σ_{j<i}√j ≤ 3.94 b ‖ξ‖₂ i^{3/2}`.  With
`g(x) = y_1 + R_1(x − x_1)`: `‖Y − gX‖_F² ≤ 15.5 b²‖ξ‖₂² Σ_i i³`, i.e.
`‖Y − gX‖_F ≤ 1.97 b n(n + 1)‖ξ‖₂`.  Finally a pair of separation `s ≤ 3` lies in `4 − s ≤ 3`
windows, so `‖ξ‖₂ ≤ (2√3/τ²)‖η‖₂`.  ∎

## 4. Checks

`experiments/geometry/local_data_bounds.py`: (a) on 60 random instances (random point clouds
and chains, random sub-patterns of range `K ≤ 7`) the ratio `s_7/bound` is at most `0.06`;
(b) on 200 random torsion moves (`δ ∈ [0.05, π]`) the ratio of `‖Δd‖₂` to the bound is at most
`0.67`, and the largest `d_P/‖Δd‖₂` seen is 219; (c) the helix exponent.
`local_data_stability.py`: the table of `s_7` against `n` and the three upper bounds.
`local_data_upper.py`:
* Lemma P on 20 000 pairs of matrices (arbitrary, including collapsed and reflected ones):
  the ratio of the two sides is at most `0.76`;
* **Theorem L on 420 pairs `(X, Y)` with `Y` arbitrary** — noise of any size, softest modes
  of any amplitude, tails reflected in the plane of three consecutive points, unrelated
  chains, random point sets, mirror images, heads rotated about an axis through two
  points: no step of the proof and no bound is violated; the Procrustes distance is at
  most `0.064` times the local bound and `0.002` times the uniform one; the local form
  also for separations at most 5, 6, 7 (105 pairs each);
* Theorem L⁺ on 360 pairs inside its range: `d_P` is at most `0.99` times the bound, and
  along the softest mode of `A` (harness test) within `6·10⁻⁵` of it;
* Proposition L₀ on 360 pairs satisfying (S): the left side is at most `0.0003` times the
  right side (earlier versions of this note said `0.0022`: that number was inflated by
  round-off in the Procrustes distance, `DEAD_ENDS.md` DG-25);
* a reflected tail: separation-3 data unchanged to `10⁻¹⁴`, one separation-4 distance
  changed by `2.99`, `d_P = 5.06`, local bound 265;
* the tube bound of Theorem K(c) on helices (`s_7 n²`: 63 against 825; 8.8 against 278; 81
  against 1365).
`local_data_guarantees.py`: the table of §6.
Tests in `run_checks.py`: `local_data_bound_a`, `local_data_bound_b`, `helix_beam_law`,
`tube_bound_helix`, `procrustes_gram_lemma`, `theorem_L_any_Y`, `theorem_L_sharp_constant`,
`local_procrustes_lemma` and `theorem_L0_instances` (the earlier form); each has a planted
error in `mutation_checks.py` (among them: the factor `√2 − 1` of Lemma P dropped; the
separation-4 errors left out of `‖η‖`; the first-order constant used as a bound).

## 5. Prior art, and what is claimed

The originality of this note was reviewed at our request by the Science division
(SCI-REV-0023, workstream A4: 123 logged queries and addresses, 33 texts opened, one in
full; an internal review by an AI session, not peer review; our proofs were not reviewed).
Where an attribution below carries "[A4]" the source was read by that review, at the level
its report states, and not by us.

**Theorem K.**  (a) is the inequality `a_d(G) ≤ a(G)` between the `d`-dimensional and the
ordinary algebraic connectivity — Jordán and Tanigawa (SIAM J. Discrete Math. 36 (2022),
Theorem 4.2, for `d = 2`, as cited); for all `d`, Lew, Nevo, Peled and Raz, "Rigidity expander
graphs", arXiv 2304.01306, Theorem 1.6, and independently Presenza, Mas, Giribet and
Alvarez-Hamelin, arXiv 2209.14893 — together with the spectral gap of a band graph, which
the first of these computes for the "generalized path graph" (proof of Proposition 7.7):
`s_7² ≤ 2π²K(K+1)(2K+1)/(3n²)`, **a better constant than ours** [A4].  That proposition also
shows that the order `n` of (a) is attained over all configurations (at prisms wider than
long), which does not decide our open end on compact chains of fixed window geometry.
**No novelty is claimed for (a).**  The beam scaling in (c) is that of the lowest bending
mode of a truss (`DEAD_ENDS.md` DG-4); the proof is the standard test field of rod theory.
What we did not find stated is (b): the per-torsion superposition constant as a lower bound
for the stability of local distance data — elementary; the point is the link.

**Theorem L.**  Searched by us (two web searches, one paper) and then by the Science
division [A4].  **The statement was not found; it is not new in mechanism or in scaling.**

* *The published global bound for this graph.*  E. Arias-Castro and S. Vishwanath,
  "Stability of Sequential Lateration and of Stress Minimization in the Presence of Noise",
  arXiv 2310.10900v3; SIAM J. Math. Data Sci. 7(3) (2025) 1077–1097 [arXiv version read in
  full by A4 and once, through a fetch, by us; the journal version by nobody].  Noisy
  squared distances on a lateration graph, configuration in general position.  Theorem 2.1:
  if `Σε² ≤ σ²`, sequential lateration returns points with `min_g Σ|y_i − g(x_i)|² ≤ AΣε²`;
  Theorem 3.1: the same for every stress minimiser; Proposition 3.2: a lower bound of the
  same form with constant `1/(8δ)`, `δ` the maximum degree (realised by a dilation, and blind
  to bending [A4]).  The explicit constant (their (2.6); (2.30) in the arXiv HTML rendering,
  which is what our earlier text quoted) is
  `A_n ≤ (1 + C_2α)^{n−p−1}/((p+1)ω²)·max{C_1α, C_2/(1 + C_2α)}`, with `α` the largest squared
  aspect ratio and `ω` the smallest width of a landmark set — quantities of the same kind as
  our thicknesses — and the admissible noise ((2.7)) decreases like `(1 + C_2α)^{−(n−p−2)}`.
  They write that the bound "takes into account the worst case scenario where … each node
  `v_k` is connected to precisely the preceding `p + 1` nodes" — the graph of Theorem L — that
  the constant "is unlikely to be tight in more friendly (and less contrived) settings", and
  that their analysis "can only be accurate, if at all, in the very worst case"; they
  neither claim nor deny that the exponential growth is real there.  No polynomial bound.
  The paper that introduced lateration graphs (Aspnes et al. 2006) states, for the graphs
  of its hardness construction, the "suspicion … that edge-length errors accumulate at most
  polynomially across the graph", without proof [A4].
* *The mechanism is that of thin-rod theory.*  Theorem L is a discrete version, for a chain
  of points observed through its distances, of the geometric rigidity estimate of nonlinear
  elasticity in a thin rod: Friesecke, James and Müller (2002) [not opened by anyone here];
  in a thin plate the constant "degenerates like h⁻²" (Friesecke–James–Müller 2006,
  Theorem 10) [A4]; for rods, Mora and Müller (Calc. Var. PDE 18 (2003), proof of Theorem
  2.1) take one rotation per cell of the size of the thickness, compare overlapping cells
  and obtain `∫|R(x_1+ξ) − R(x_1)|² ≤ C(|ξ|/h + 1)² ∫dist²(∇_h y, SO(3))` [A4] — our Steps 1–3
  in the continuum; Blanchard and Griso (Anal. Appl. 7 (2009), as restated in arXiv
  1010.3614, Theorem 3.2) give a rotation field with `‖dR/ds‖_{L²} ≤ (C/δ²)‖dist(∇v, SO(3))‖_{L²}`,
  `C` independent of thickness and length [A4].  With cell size of the order of the bond and
  of the thickness these give our `(b/τ²)n²` up to constants.
* *The discrete ingredients are in print too.*  Lemma P: Tu et al. 2016 (above; from our
  memory).  The Gram matrix of one window controls the window up to an orthogonal map,
  with constant `1/σ_min`: Arias-Castro, Javanmard and Pelletier (J. Mach. Learn. Res. 21
  (2020), Theorem 1); for lattice simplices Alicandro, Lazzaroni and Palombaro (arXiv
  1601.05968, Lemma 1.2) and Lazzaroni, Palombaro and Schlömerkemper (arXiv 1501.07505,
  Lemma 3.2) [A4].  Two neighbouring simplices of opposite orientation violate the bond
  between the two vertices opposite to their common facet — the role of the separation-4
  distances, and the "flips" of Moore et al. (2004): Alicandro–Lazzaroni–Palombaro, Lemma
  1.3 [A4].  Rotations of overlapping cells compared and accumulated on lattices: Schmidt
  and Zeman (arXiv 2208.04199, Theorem 2.4) [A4]; that errors of orthogonal alignments
  add, by "norm preservation by orthogonal matrices", is stated for sequential stitching in
  arXiv 2604.21094 (proof of Lemma 18) [A4].
* *Polynomial bounds for the first-order problem exist.*  Daitch and Spielman (arXiv
  cs/0703119, Lemma 3.2: a path of `k` well-shaped triangles, `O(k³)`); Kyng, Peng,
  Schwieterman and Zhang (arXiv 1805.09442, Lemma 3.3: `λ_min = Ω(n⁻¹Δ⁻⁴)` for tetrahedral
  trusses), who remark that their three-dimensional analogue of the path lemma loses a
  factor exponential in the hop distance "due to the accumulation of rotational operators"
  and that they "are not sure whether this exponential increase is simply due to an
  algebraic artifact"; Lew et al. (Proposition 7.7: `Θ_d(1/n²)` for the best rigidity
  eigenvalue of the band graph over all configurations) [A4].  Corollary L.3 (b) is a
  statement of this kind, `μ ≳ s_*τ_*/(b n²)`, for chains with uniformly thick windows; for
  such chains the comparison of frames answers the question of Kyng et al.: the loss is
  polynomial.
* *Other global or finite-perturbation results, not for this graph:* Javanmard and
  Montanari (Found. Comput. Math. 13 (2013), Theorem 1.1; the lower bound by a bending
  map); Chaudhury, Khoo and Singer (SIAM J. Optim. 25 (2015), Theorem 13); Holmes-Cerfon,
  Theran and Gortler (arXiv 1908.03802: explicit but local radii from the smallest singular
  value of the rigidity matrix — the local half of Theorem L⁺); Alestalo, Trotsenko and
  Väisälä (complete distance data; constant governed by diameter over thickness) [A4].
* **What is claimed.**  A global stability inequality — for *every* configuration, with no
  smallness condition, with a constant of order `n²` that is explicit and local — for the
  distances of sequence separation at most 4 of a chain with non-degenerate windows; the
  matching order `n²` on rod-like chains; and the first-order constant `1/(2μ)` for all
  configurations whose data lie in an explicit range.  We did not find these stated.  They
  are a transfer of a known argument to distance data, assembled from known lemmas — not a
  new mechanism, and not the first polynomial bound of any kind for chains of simplices.
  With respect to the published global bound for band lateration graphs the constant
  improves from exponential to `n⁴` (squared error) and the admissible noise from
  exponentially small to unrestricted.  **The search has gaps** [A4]: not read are
  B. Schrader, "Propagation of errors in schematic chains of triangles in space with
  measured distances", Bull. Géodésique 86 (1967) and the classical geodesy of
  trilateration chains; Luo and Wu, J. Optim. Theory Appl. 149 (2011); Anderson, Shames, Mao
  and Fidan, SIAM J. Discrete Math. 24 (2010); the journal version of Arias-Castro–
  Vishwanath; Friesecke–James–Müller 2002 itself; no search in zbMATH or MathSciNet.  The
  threshold-free form and Theorem L⁺ were written after that search and were not searched
  for separately.

Sources: [arXiv 2310.10900](https://arxiv.org/abs/2310.10900),
[Moore et al., SenSys 2004](https://people.csail.mit.edu/teller/pubs/MooreEtAlSensys2004.pdf);
all other references as given in the Science division's report
`docs/science/workstreams/A4_REPORT.md` on its branch.

## 6. What the theorems do and do not guarantee; limitations and open ends

**On idealised traces the certified range is empty in practice.**  The table
(`experiments/geometry/local_data_guarantees.py`; lengths in ångström; traces of constant
radius, rise and turn — the geometries of SCI-REV-0023 §5, not structures from a database)
gives, for squared distances of separation at most 4: the constant `C_L` of Theorem L; the
sharp first-order constant `1/(2μ)`; the range `‖η‖₂ ≤ μ/(ΛC_L)` in which Theorem L⁺ certifies
it, expressed as a root-mean-square error of the distances; and the worst-case first-order
RMSD per unit root-mean-square distance error.  (The range is computed with the largest
Laplacian eigenvalue of the finite graph, not with `11.04`, and converted to a distance
error by dividing by `2 d̄ √N`, `d̄` the mean measured distance and `N` the number of pairs.
The table was reproduced to the digits given by the Science division, SCI-REV-0028 F12.)

| trace | `n` | `C_L` | `1/(2μ)` | certified range (rms distance error) | first-order RMSD per unit rms distance error, worst case | the same, independent errors, on average |
|---|---|---|---|---|---|---|
| helix-like (radius 2.3, rise 1.5, 100° per point) | 12 | 185 | 0.23 | `2·10⁻⁵` | 4.2 | 1.6 |
| | 20 | 456 | 0.45 | `3·10⁻⁶` | 9.0 | 2.3 |
| | 100 | 9 800 | 9.5 | `2·10⁻⁹` | 207 | 16.5 |
| strand-like (radius 0.94, rise 3.3, 160° per point) | 12 | 1 780 | 3.3 | `9·10⁻⁸` | 58 | 12.3 |
| | 20 | 4 410 | 7.3 | `1·10⁻⁸` | 140 | 25 |
| | 100 | 94 700 | 168 | `9·10⁻¹²` | 3 460 | 271 |
| strand-like, 175° per point | 20 | 65 100 | 42 | `1·10⁻¹⁰` | 753 | 102 |

(Last column, added at the thirteenth checkpoint: for independent distance errors of equal
variance the least-squares reconstruction has, to first order, mean squared displacement
`σ² Σ_i s_i(R)⁻²` — the sum over the non-zero singular values of the rigidity matrix.  It is
a first-order expectation, **not a guarantee**: nothing certifies it outside the range of
the fifth column.)

Reading.  (i) *First order:* on a helix-like trace of 20 points, distance errors of
root-mean-square size `σ` move the reconstruction by at most `9σ` (RMSD) **in the limit
`σ → 0`**; the factor grows like `n²` and is one to two orders of magnitude larger on
strand-like traces.  **This is not a bound at finite `σ`, and the regime is short** [N; the
major finding of the Science division's review SCI-REV-0028 (F1), explicit configurations
found by search; replicated by us with independent code, `distant_fits.py`, to the digits]:
the local distances of that trace are fitted to rms `0.27` Å by a configuration at RMSD
`9.0` Å — its radius of gyration is `8.95` Å — and to `0.30` Å by one at `9.95` Å (to `0.24` Å
at `7.0` Å by the Science division's finer search); for 12 points, to `0.37` Å at `5.76` Å
(radius of gyration `5.66` Å); on the strand-like trace of 20 points, to `0.10` Å at `12` Å
and to `0.20` Å at `18.6` Å.  The first-order factor is recovered only up to `σ ≈ 0.2` Å on the
helix-like trace (at `σ = 0.11` Å the worst configuration found is at RMSD `1.0` Å).  **In the
worst case, sequence-local distances with errors of a few tenths of an ångström
(helix-like) or a few hundredths (strand-like) do not determine the fold of these
idealised traces, whatever the algorithm.**
(ii) *Globally:* the range in which we can **certify** that no distant configuration fits
the data is `10⁻⁵` ångström or less.  Above it Theorem L still holds, but its constant is a
thousand times the first-order one and its bound exceeds the size of the molecule.  So, as
the Science division's review says of the earlier form, **these are theorems about the
exponent and about the first-order constant; as a guarantee for data of realistic accuracy
they are empty**, and nothing in this note shows that sequence-local distances of
realistic accuracy determine a fold — by (i), in the worst case they do not.  **The gap
between `C_L` and `1/(2μ)` is only partly an artefact** [SCI-REV-0028 F1; the text of this
paragraph follows its proposal]: the best global constant `C_glob = sup_Y d_P/‖η‖₂` is not
`1/(2μ)`.  On the 20-point helix-like trace it is at least `1.92` (against `0.447`), and for
chains with one nearly coplanar interior window `1/(2μ)` stays bounded while the reflected
tail gives `d_P/‖η‖₂ ∝ 1/τ` (one squared distance changes, by `4h⁻h⁺`).  Hence **the factor
`1/τ` of Theorem L is necessary in every global constant**, and the range of Theorem L⁺
cannot be enlarged to `‖η‖₂ ≤ μ²/Λ`.  What remains open (`PROOF_OBLIGATIONS.md` O-16) is the
size of `C_glob` between these lower bounds and `C_L`: a factor 240 on the helix-like trace,
and 55 on the worst pair found by search.
(iii) Corollary L.2 gives an error bar from an estimate alone — for an estimate in `ℝ³`
with every pair measured; with the present constants it is valid and useless for the
same reason.  **One part is not empty** (SCI-REV-0028 F11): Lemma Q alone is a usable bound
for one window with complete distances — a helix-like five-point window whose ten
distances are known to within `0.1` Å is fixed to RMSD `≤ 0.32` Å up to an isometry, within
a factor `2.2` of the worst case found; it is the chaining that makes the constants
useless.
(iv) *On average* (the Frontier Benchmarking division's item G-2 asks for an average-case
statement): to first order, independent errors are four to thirteen times less harmful
than the worst case, because the worst case is one soft mode out of `3n − 6`; a 20-point
helix-like trace with distance errors of `0.1` Å would be reconstructed to `0.23` Å RMSD on
average.  By (i) this description can hold at most up to errors of about `0.2` Å on that
trace and a few hundredths on the strand-like one; below those levels it is supported by
search only, and certified only in the range of the fifth column.
(v) *A route that does not close the gap* [N; `DEAD_ENDS.md` DG-26]: a positive semidefinite
stress of maximal rank gives a bound that is global and linear in the error in Gram
space (for every configuration in every dimension), at the price of the factor
`1 + Λ‖ω‖/λ⁺(Ω)`.  With the best stress supported on the band, this factor is `2·10³`,
`2·10⁴`, `5·10⁵` for helix-like traces of 12, 20, 40 points and `3·10²`, `3·10³`, `7·10⁴` for
strand-like ones — it grows faster than `n⁴` (the five-point affine dependency acts like
a fourth difference) — against `C_L·2μ ≈ 10³` and `6·10²` for Theorem L, independent of `n`.
The relaxation loses because chains fold softly into a fourth dimension.

**Other limitations.**

* Theorems L, L⁺ are for `ℝ³`, exact windows and complete data of separation at most 4 (a
  missing pair inside a five-point window breaks Lemma Q for that window; the Proposition
  L₀ route needs fewer pairs but has a threshold).  Deterministic bounded errors only: no
  Cramér–Rao or minimax statement for random noise, where the typical error is far below
  the worst case.
* For compact (globular) chains the true constant is smaller than `n²`: Theorem K(a) gives
  `n/K^{3/2}` and (c) gives `L²/(ρ…)` with `L ∼ n^{1/3}`; where between `n` and `n²` typical
  compact chains lie is not studied (one sample per size gave exponents between `−1.7` and
  `−2.1` for `s_7` of random coils).
* Theorem K(b) uses bonds of length at most `b` and nothing else; with fixed bond angles the
  levers are shorter by the factor `sin(θ/2)` on extended arms.
* Nothing here uses long-range pairs; how few long-range pairs improve the constant, and by
  how much, is a measurement-selection problem (an E-optimal design; known approximation
  results apply to the first-order constant).  By Corollary K.1 they cannot make it
  length-independent on a rod.
