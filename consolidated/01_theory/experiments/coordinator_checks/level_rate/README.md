# The rate of the level recursion — coordinator's exploration (2026-11-26)

What these scripts are for, and what they are not.  The mathematics is in
`docs/workstreams/R_brief.md` §2 (two short lemmas proved there; everything else heuristic).
**Nothing here is a certified bound**: `iterate_exact.py` interpolates on a grid, and
`lines_lb.py` evaluates a proved lower bound in floating point.

The recursion: `T_1 = θ_na`, `T_{k+1} = min(T_k, R[T_k])`, `τ_k = sup T_k` (theory report, Theorem 11.52,
(11.18.2)).  Conjecture: `k²(τ_k − h) → 2π²·h²·θ_hint″(0)`.

| script | what it computes | output |
|---|---|---|
| `pairs.py` | the two pairs `(θ_na, θ_hint)`: Gaussian small-slope limit, cube at slope `u` | — |
| `iterate_exact.py pair levels [ratio] [ne]` | the recursion on a geometric grid (`10^{-11}` … `ε*`), linear interpolation, the infimum over `(φ, β)` on a grid of outer rates `e` and tolerance fractions; prints `τ_k`, `k²(τ_k − h)`, its ratio to the conjectured constant, and the scaled defect profile `k²(T_k − θ_hint)(ζh/k)/(h²θ_hint″(0))` at `ζ = ¼, ½, 1, 2, 3, 5` | `out_iterate_gauss_160.txt`, `out_iterate_cube1_120.txt` |
| `lines_lb.py` | the lower bound `τ_k^{LB}` from minorant lines (Lemma L): tangent lines of `θ_na` iterated by the slope map `Σ_B` until they leave the regular range `s < 1 − B/a`; bisection over the intercept `B` | `out_lines_lb.txt` |
| `ode_f0.py` | the similarity profile: `ζf′²/2 + ζf′ + (ζ−2)f = 0` through its folded saddle `(3, 3/2)`; `f(0) = 19.7392088 = 2π²` | `out_ode_f0.txt` |
| `dual_ub_gauss.py` | the upper-bound dynamics in dual variables for the Gaussian pair (`R_brief.md` §2.5 made concrete: a convex majorant is described by `S(B)`, the least slope of a line with intercept `B` below it; one level sends `S` to the lower convex envelope of `min(1, Σ_B(S(B)))` on `[0, τ′]`, `τ′` the root of `S(B) = 1 − B/a`) — on a grid, **not one-sided** | `out_dual_ub_gauss.txt` |
| `dual_ub_cube.py [u]` | the same dual upper-bound dynamics for the cube (slope map through `J`; start `hull(θ_na) = max(θ_na(x), a − x)`) — a grid approximation, **not one-sided** | `out_dual_ub_cube_u1.txt` |
| `ub_subsolution.py pair [s_t − L_h] [κ₀]` | a candidate **convex sub-solution** of the dual upper-bound dynamics: `W_k` = the orbit of the flat line after `k − κ₀` steps up to the point where it reaches the slope level `s_t`, continued by its tangent line.  Checks on grids: convexity below `s_t`; (S1) `W_{k+1} ≤ min(1, Σ_B(W_k))` on the regular range; the top condition (the tangent line of `W_{k+1}` reaches slope `1` no earlier than `W_k` reaches the dropping slope); and `S_k ≥ W_k` for the grid dynamics.  By the comparison lemma (in the docstring) these give `τ_{k+1} ≤ E(W_k)`, the point where `W_k` reaches the dropping slope | `out_ub_subsolution_gauss.txt`, `out_ub_subsolution_cube1.txt` |
| `lines_lb_general.py` | the lower bound from lines for a pair given by its dual function `J` alone (`h = max J`, `a = lim J(t)/(1−t)`, slope map `t′ = Q^{−1}(B/(1−σ))`, `σ′ = t′(1−σ)/(1−t′)` with `Q = J/(1−t)`; the tangent line of `θ_na` with intercept `B` is the image of the flat line): Gaussian pair, cube, and four **biased cubes** (`J` = the game function `F*` of §11.20) | `out_lines_lb_general.txt` |
| `epochs.py` | single-line epochs with optimised outer rates (the calculus of Theorem 11.58a with the rate of every slope step chosen freely): `k²(B_k − h)` grows linearly in `k` — this schedule has the rate `C/k` only | `out_epochs.txt` |

Readings (2026-11-26):

* Gaussian pair, constant `π²/16 = 0.616850`: grid recursion `k²(τ_k − h)/const = 0.9960, 0.9982` at
  `k = 100, 160`; lower bound from lines `0.9902, 0.9938, 0.9969` at `k = 100, 160, 320`; the lower bound
  is below the grid value at every `k` (difference `1.0·10⁻⁷` at `k = 160`).
* Cube `u = 1`, constant `0.0711473 = 0.64129·a` (the "`0.65/k²`" of the theory report, §11.19 remark
  (1)): grid recursion ratio `0.990` at `k = 55`, `0.994` at `k = 85`; lower bound `0.9824` at `k = 55`,
  `0.9918` at `k = 120`.
* The scaled defect profiles of the two pairs agree (e.g. at `ζ = 2`: `2.933` and `2.91` against
  `f(2) = 2.931` of the ODE).
* The dual upper-bound dynamics (`dual_ub_gauss.py`; uncertified): `τ_2 = ½`, `τ_3 = 5/14 = 0.35714`
  (grid recursion `0.35593`), and `lower bound ≤ grid recursion ≤ dual upper bound` at every `k`
  computed; `k²(τ_k^{UB} − h)/const = 1.00016, 1.00006, 1.00001` at `k = 100, 160, 320`.  For large `k` the
  three sequences behave like `const/(k + c)²` with `c = ½` (lower bound: the root of
  `(k−1)θ(B) + φ₀(B) = π`), `c ≈ 0.15`–`0.2` (grid recursion) and `c ≈ 0` (dual upper bound: the root
  of `kθ(B) = π` up to `O(k⁻⁴)` — the naive line formula, which is wrong at small `k`, becomes
  right to higher order).
* Cube, `u = 1`, dual upper-bound dynamics (`dual_ub_cube.py`; uncertified): `τ_2 = 0.0555175` (the exact value;
  the interpolating grid recursion has `0.0555255`), then `grid recursion ≤ dual upper bound` at every `k`;
  ratio to the constant `0.99873, 0.99903` at `k = 120, 160` — like `const/(k + 0.08)²`, where the lower
  bound is like `const/(k + ½)²` and the grid recursion like `const/(k + ¼)²`.  The top of the dynamics is
  controlled with a margin on the cube: `2θ_hint″(0)h²/(a(1 − L_h − h/a)²) = 1 + u²/16 + O(u⁴) > 1`
  (`1.062` at `u = 1`), with equality in the Gaussian limit.
* A proof route for the upper half of the conjecture (`ub_subsolution.py`; grid numerics, not certified).
  With a delay of two levels and the tangent at the slope level `L_h + 0.1`, the candidate satisfies all
  four conditions at every level `4 ≤ k ≤ 120` for the Gaussian pair and the cube at `u = 1, 2` (with a
  delay of one or none the comparison `S_k ≥ W_k` fails), and the resulting bound is
  `k²(E(W_{k−1}) − h)/const = 1.34, 1.18, 1.09, 1.06` at `k = 20, 40, 80, 120` — like `const/(k − 3.6)²`.  What a
  proof still needs: (S1) on the tangent part (it follows from the monotonicity of the partial
  derivatives of the slope map and the convexity of the orbit curve), convexity of the orbit curve and
  the top condition for all `k` (asymptotically self-similar in the top band; checked to `k = 120`), and
  the base case at `k = 4`.
* Universality (lower-bound side, `lines_lb_general.py`): for the biased cubes `(p, u) = (0.3, 1), (0.1, 1),
  (0.1, 2), (0.02, 2)` the ratio `k²(τ_k^{LB} − h)/(2π²h²θ_hint″(0))` is `0.992, 0.998, 0.993, 0.993` at `k = 160` and
  increasing in `k`, as for the cube (`0.994`) and the Gaussian pair (`0.994`): the law depends on the pair
  through `h` and the curvature of its dual at the maximum only.
* An error made on the way and kept as a warning: propagating the lines of a convex
  *majorant* by the same slope map and reading off `sup min(B, (1−s)a)` is **not** an upper
  bound once a line's slope jumps beyond `1` (it gave `τ₃ ≤ ⅓` for the Gaussian pair, where
  `τ₃ = 0.3573`); the monotone hull has to be taken (`R_brief.md` §2.5).

Commands: `python3 iterate_exact.py gauss 160 1.01 500`, `python3 iterate_exact.py cube:1 120 1.01 500`
(about 18 and 11 minutes), `python3 lines_lb.py`, `python3 ode_f0.py`, `python3 epochs.py`.
