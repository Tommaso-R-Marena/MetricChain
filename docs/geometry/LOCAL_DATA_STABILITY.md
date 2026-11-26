# Sequence-local distance data cannot determine global shape stably

**Geometric Inference division — cycle 2, first note.**  Labels as in
`ENSEMBLE_RIGIDITY.md`.  Unrefereed.  Single conformations, no ensembles.

## 0. Summary

Let a chain of `n` points be observed through distances between points whose sequence
separation is at most `K` (bond lengths and angles are the cases `K = 1, 2`; a
"trilateration" pattern needs `K ≥ 4`).  Such data determine a generic chain as soon as
`K ≥ 4`.  This note quantifies how badly: the stability constant

    C = sup  (superposition distance of two conformations) / (ℓ² difference of their measured distances)

is at least of order `n/K^{3/2}` for **every** configuration and every pattern of range `K`
(Theorem K(a); known in substance), at least the *per-torsion superposition constant* of the
theory report divided by `b·K²/(4√3)` (Theorem K(b): a duality between the lever-arm law
and the instability of local data; global, not infinitesimal), and of order `n²/K^{5/2}` on
helices (numerical, with the mechanism).  Consequence: a length-independent stability
constant needs measured pairs of sequence separation at least of order `n^{2/3}` for any
configuration, and `n^{4/5}` on extended chains — whatever the number of local measurements.

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
(c) *Helices* **[N]**.  For helical chains (constant torsion 60° or 150°, bond angle 111°)
and all pairs of separation at most `K ∈ {4, 6}`: `s_7 = c/n²` with fitted exponents
`−1.98 … −2.00` (`n = 40 … 160`); e.g. `s_7 n² = 63` for the 60° helix with `K = 4`.  The
softest mode is a torsional (bending) motion: the smallest generalised singular value on
the space of torsional velocity fields is within 5 % of `s_7`.

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

**Corollary K.1 (long-range data are necessary) [P from (a), (b); the last clause N].**  If a
measurement pattern of range `K` has `C_inf ≤ c₀`, then `K ≥ (n/(10c₀))^{2/3}`; if `C_glob ≤ c₀`
on a domain containing a conformation with per-torsion constant `κ`, then
`K² ≥ 4√3 κ/(b c₀)` — for `κ ∝ n^{3/2}` (extended arms): `K ≳ n^{3/4}`; on helices
(c) gives `K ≳ n^{4/5}`.  The number of local measurements does not enter.

**Remark (why `n²`).**  A torsion move concentrates the strain on the `O(K²)` pairs that
straddle one bond; spreading a total bend over all bonds divides the strain per pair by
`n/K` at the same displacement, which turns `n^{3/2}/K²` into `n²/K^{5/2}`.  In the rod model
the displacement of a coherent bending is the free–free beam form of GEOMETRY-RES-0002.

## 3. Checks

`experiments/geometry/local_data_bounds.py`: (a) on 60 random instances (random point clouds
and chains, random sub-patterns of range `K ≤ 7`) the ratio `s_7/bound` is at most `0.06`;
(b) on 200 random torsion moves (`δ ∈ [0.05, π]`) the ratio of `‖Δd‖₂` to the bound is at most
`0.67`, and the largest `d_P/‖Δd‖₂` seen is 219; (c) the helix exponent.
`local_data_stability.py`: the table of `s_7` against `n` and the three upper bounds.
Tests `local_data_bound_a`, `local_data_bound_b`, `helix_beam_law` in `run_checks.py`.

## 4. Prior art, and what is claimed

(a) is the statement that the `d`-dimensional algebraic connectivity of a graph is at most
its ordinary algebraic connectivity (Jordán–Tanigawa; Lew–Nevo–Peled–Raz) together with
the elementary bound `O(K³/n²)` for graphs of bandwidth `K`; the accumulation of errors in
sequential (trilateration) localisation is classical in the sensor-network literature
(Cramér–Rao analyses).  **No novelty is claimed for (a).**  [From memory of the literature;
no full text read.]  The beam scaling in (c) is that of the lowest bending mode of a truss
(`DEAD_ENDS.md` DG-4).  What we did not find stated is (b): the per-torsion superposition
constant as a lower bound for the stability of local distance data — elementary, and the
point is the link, not the difficulty.

## 5. Limitations and open ends

* Lower bounds only.  A matching upper bound `C_inf ≤ c n²` for trilateration patterns on
  chains with a quantitative non-degeneracy (thickness) condition is not proved (a
  discrete Korn inequality); the global constant is not bounded above at all.
* (b) uses bonds of length at most `b` and nothing else; with fixed bond angles the levers
  are shorter by the factor `sin(θ/2)` on extended arms.
* Random coils: one sample per size gives exponents between `−1.7` and `−2.1` for `s_7`;
  not studied.
* Nothing here uses long-range pairs; the complementary question — how few long-range
  pairs give a length-independent constant — is the measurement-selection problem
  (an E-optimal design; known approximation results apply to the infinitesimal constant).
