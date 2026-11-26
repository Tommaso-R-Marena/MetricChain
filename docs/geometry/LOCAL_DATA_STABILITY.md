# Sequence-local distance data: the stability constant grows like the square of the length, and no faster

**Geometric Inference division — cycle 2, first note** (lower bounds: fifth checkpoint;
upper bound, Theorem L: eighth checkpoint).  Labels as in `ENSEMBLE_RIGIDITY.md`.
Unrefereed.  Single conformations, no ensembles.

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
proof).  **And it is never worse than `n²`** (Theorem L): for a chain whose consecutive
four-point simplices are uniformly non-degenerate, *every* point configuration whose
squared distances of sequence separation at most 4 are pointwise close to those of the
chain is within `6.9 (b/τ²) n(n + 1)` times the `ℓ²` error of it, up to a rigid motion —
globally, with a smallness threshold that does not depend on `n`.  The published
perturbation bound for this situation — sequential lateration in which each point is
attached to its `d + 1` predecessors — is exponential in `n` (§5).  So for rod-like chains
the stability constant of sequence-local distance data is `Θ(n²)`, with explicit constants
on both sides.  Consequences: a length-independent stability constant needs measured pairs
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

## 3. A matching global upper bound

For a configuration `X` of `n ≥ 5` points in `ℝ³` let
`P_i = [x_{i+1} − x_i, x_{i+2} − x_i, x_{i+3} − x_i]` (`1 ≤ i ≤ n − 3`) be the edge matrices of its
windows of four consecutive points, and

    τ = min_i σ_min(P_i)   (thickness),     D = max_i σ_max(P_i),     b = max_i |x_{i+1} − x_i| .

`τ > 0` iff no four consecutive points are coplanar.  For a second configuration `Y` write
`η_jk = |y_j − y_k|² − |x_j − x_k|²`.

**Theorem L (global quantitative rigidity from sequence-local distances) [P].**  Let `τ > 0`
and let `Y` be **any** configuration of `n` points in `ℝ³` such that

    (S)    |η_jk| ≤ τ⁴/(73 D²)    for all pairs with |j − k| ≤ 4.

Then there is an isometry `g` of `ℝ³` (possibly improper) with

    ‖Y − gX‖_F ≤ 6.9 · (b/τ²) · n(n + 1) · ‖η‖₂ ,       ‖η‖₂² = Σ_{|j−k| ≤ 3} η_jk² .

The distances of separation 4 enter through (S) only, and (S) cannot be dropped: reflecting
the points beyond a window in the plane of three consecutive points changes no distance of
separation at most 3.

**Corollary L.1 (noisy data; any estimator that fits as well as the truth) [P].**  Let
`q_jk = |x_j − x_k|² + ε_jk` for `|j − k| ≤ 4`, with `‖ε‖₂ ≤ τ⁴/(146 D²)`, and let `Ŷ` be any
configuration with `Σ(|ŷ_j − ŷ_k|² − q_jk)² ≤ Σ ε_jk²` — for instance a global minimiser of
this stress.  Then `min_g ‖Ŷ − gX‖_F ≤ 13.8 (b/τ²) n(n + 1) ‖ε‖₂`.

**Corollary L.2 (the exponent is sharp; `Θ(n²)` on helices) [P].**  For ideal helices of
fixed geometry (`τ`, `D`, `b`, `ρ`, `h` independent of `n`) and distances of separation at
most `K`, `4 ≤ K` fixed: the infinitesimal constant is at least `h²n²/(139 ρ b K^{3/2})`
(Theorem K(c)), and for all `Y` with distance errors `|δ_jk| ≤ τ⁴/(160 D³)` on these pairs
`d_P(X, Y) ≤ 13.9 (bD/τ²) n(n + 1) ‖δ‖₂`.

*Proof of Theorem L.*  *Step 1 (one window).*  Let `Q_i` be the edge matrix of the `i`-th
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

*Proof of L.1.*  `η(Ŷ) = (|ŷ_j − ŷ_k|² − q_jk) + ε_jk`, so `‖η‖₂ ≤ 2‖ε‖₂` over the pairs of
separation at most 4, which gives (S) and the bound.  *Proof of L.2.*
`η_jk = δ_jk(2|x_j − x_k| + δ_jk)`, `|x_j − x_k| ≤ D` for `|j − k| ≤ 3` and `≤ 2D` for separation
4; for `|δ| ≤ τ⁴/(160D³)` this gives (S) and `‖η‖₂ ≤ 2.01 D‖δ‖₂`.  ∎

**Remarks.**
1. *Global, with a threshold independent of `n`.*  Nothing is assumed about `Y` except the
   pointwise condition (S) on its local distances: no closeness to `X`, no chain structure.
   If (S) fails, some squared distance of separation at most 4 is off by more than
   `τ⁴/(73D²)`; for two chains with bonds at most `b` the trivial bound `d_P ≤ 2b n^{3/2}` then
   gives `d_P ≤ max(6.9 (b/τ²) n(n+1), 146 b D² n^{3/2}/τ⁴)·‖η‖₂` (norm over separations at
   most 4) for **all** pairs of chains with `X` thick: a global constant of order `n²`.
2. *Why not exponential.*  Position errors of a sequential reconstruction multiply; errors
   of orthogonal frames add.  The proof never reconstructs positions step by step.
3. *The constants are crude.*  On the instances of §4 the left side is at most `0.0022`
   times the right side; along the softest modes of helices the ratio `d_P/‖η‖₂` is between
   `0.1 n²` and `0.4 n²` where the bound is `72 n²`.  The exponent, not the constant, is the
   content.  The dependence `τ^{-2}` is that of a single window and is attained there.
4. *Other dimensions.*  The proof works verbatim in `ℝ^d` with windows of `d + 1` points and
   distances of separation at most `d + 1` (constants depending on `d`).

## 4. Checks

`experiments/geometry/local_data_bounds.py`: (a) on 60 random instances (random point clouds
and chains, random sub-patterns of range `K ≤ 7`) the ratio `s_7/bound` is at most `0.06`;
(b) on 200 random torsion moves (`δ ∈ [0.05, π]`) the ratio of `‖Δd‖₂` to the bound is at most
`0.67`, and the largest `d_P/‖Δd‖₂` seen is 219; (c) the helix exponent.
`local_data_stability.py`: the table of `s_7` against `n` and the three upper bounds.
`local_data_upper.py`: Theorem L on 360 pairs `(X, Y)` (thick random chains and helices with
10 to 90 points; `Y` a random displacement, a softest mode, a smooth bending field or a
change of torsions, scaled to satisfy (S)): the left side is at most `0.0022` times the
right side; reflecting the tail of a chain in the plane of three consecutive atoms leaves
the separation-3 data unchanged to `10⁻¹⁴`, changes separation-4 data by `3.35` (violating
(S)) and moves the chain by `d_P = 16.2`; the tube bound of Theorem K(c) on helices
(`s_7 n²`: 63 against 825; 8.8 against 278; 81 against 1365).
Tests in `run_checks.py`: `local_data_bound_a`, `local_data_bound_b`, `helix_beam_law`,
`tube_bound_helix`, `local_procrustes_lemma` (Step 1 of the proof on thin and thick windows,
with adversarial perturbations), `theorem_L_instances`; each has a planted error in
`mutation_checks.py`.

## 5. Prior art, and what is claimed

**Theorem K.**  (a) is the statement that the `d`-dimensional algebraic connectivity of a
graph is at most its ordinary algebraic connectivity (Jordán–Tanigawa; Lew–Nevo–Peled–Raz)
together with the elementary bound `O(K³/n²)` for graphs of bandwidth `K`; the accumulation
of errors in sequential (trilateration) localisation is classical in the sensor-network
literature (Cramér–Rao analyses).  **No novelty is claimed for (a).**  [From memory of the
literature; no full text read.]  The beam scaling in (c) is that of the lowest bending mode
of a truss (`DEAD_ENDS.md` DG-4); the proof is the standard test field of rod theory.  What
we did not find stated is (b): the per-torsion superposition constant as a lower bound for
the stability of local distance data — elementary, and the point is the link, not the
difficulty.

**Theorem L.**  Searched on 2026-11-26 (two web searches; one paper read through a fetch of
its arXiv HTML version).
* *The closest published result:* E. Arias-Castro and S. Vishwanath, "Stability of
  Sequential Lateration and of Stress Minimization in the Presence of Noise" (arXiv
  2310.10900, 2023–24).  Setting: noisy squared distances on a lateration graph (an ordering
  in which every point is adjacent to at least `p + 1` earlier ones), configuration in
  general position.  Their Theorem 2.1: if `Σε² ≤ σ²` then sequential lateration returns
  points with `min_g Σ|y_i − g(x_i)|² ≤ A Σε²`; Theorem 3.1: the same for stress minimisers;
  Proposition 3.2: a lower bound linear in `Σε²` with a constant that does not depend on
  `n`.  Their constant (their equations (2.30), (2.33), as read from the HTML version by our
  fetch) is `A_n ≤ (1 + C_2α)^{n−p−1}·(…)`, `α` the largest squared aspect ratio of a
  landmark set — **exponential in `n`** — in exactly the case of Theorem L, each point
  attached to its `p + 1` predecessors, which they call the worst case; the admissible noise
  level shrinks exponentially as well.  They state that the bound is unlikely to be tight
  and give no polynomial one.  **[K; from one automated reading of the paper — statement
  numbers and formulas should be confirmed by a second reader.]**
* *What Theorem L adds for this graph:* a constant polynomial in `n` — `n²` for the error,
  `n⁴` for the squared error — under a *uniform* non-degeneracy of the windows (their
  general-position hypothesis is not uniform, ours is quantitative: `τ`, `D`); a smallness
  threshold independent of `n` and pointwise; a statement about every configuration
  consistent with the data rather than about the output of one algorithm (Corollary L.1
  covers stress minimisers); and the matching lower bound `n²` on rod-like chains, which
  shows that polynomial growth is real.  It does not cover general lateration graphs.
* *Related theory:* geometric rigidity estimates in nonlinear elasticity (Friesecke, James,
  Müller 2002: the deformation gradient is close to one rotation, with a constant that
  degenerates for thin domains; rod theories built on it; a recent proof with explicit
  constants by Conti and Zwicknagl) **[K, from search summaries and memory]**.  Theorem L is
  a discrete analogue for a chain of simplices observed through its local distances, with
  the rod scaling `L²` and an elementary proof; "errors of frames add" is the discrete form
  of the argument that passes from local rotations to a global one.  The gross errors
  ("flips") of one trilateration step studied in the sensor-network literature (Moore et
  al. 2004) are what condition (S) excludes.
* **Novelty assessment.**  The polynomial bound for band lateration graphs was not found;
  the one published bound we found for this case is exponential.  Two searches and one paper
  are a thin basis: the statement is elementary enough to be folklore in rod theory or in
  the literature on discretizable distance geometry.  An independent search is requested
  (GEOMETRY-MSG-0007).

Sources: [arXiv 2310.10900](https://arxiv.org/abs/2310.10900),
[Moore et al., SenSys 2004](https://people.csail.mit.edu/teller/pubs/MooreEtAlSensys2004.pdf),
[arXiv 2006.08840](https://arxiv.org/pdf/2006.08840),
[arXiv 2608.00863](https://arxiv.org/pdf/2608.00863).

## 6. Limitations and open ends

* Theorem L is for `ℝ³`, exact windows of four consecutive points and distances of
  separation at most 4; its constants are loose by two to three orders of magnitude on the
  instances computed; (S) is pointwise and small (`τ⁴/(73D²)` is `6·10⁻⁶` for a typical
  random chain with unit bonds and about `10⁻⁵` to `2·10⁻⁵` for the helices of §4).  A sharp
  constant, and the right dependence on `τ` for chains with a few thin windows, are open.
* For compact (globular) chains the true constant is smaller than `n²`: Theorem K(a) gives
  `n/K^{3/2}` and (c) gives `L²/(ρ…)` with `L ∼ n^{1/3}`; where between `n` and `n²` typical
  compact chains lie is not studied (one sample per size gave exponents between `−1.7` and
  `−2.1` for `s_7` of random coils).
* (b) uses bonds of length at most `b` and nothing else; with fixed bond angles the levers
  are shorter by the factor `sin(θ/2)` on extended arms.
* Nothing here uses long-range pairs; the complementary question — how few long-range
  pairs improve the constant, and by how much — is a measurement-selection problem (an
  E-optimal design; known approximation results apply to the infinitesimal constant).  By
  Corollary K.1 they cannot make it length-independent on a rod.
* No statistics: the noise is deterministic and bounded; a Cramér–Rao or minimax statement
  for random noise is not derived.
