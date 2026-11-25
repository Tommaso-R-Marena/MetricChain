# Coordinator's checks of workstream W (several site types, larger alphabets; theory report §11.26)

An own implementation, written from the statements of the report and not from its code
(`wv_lib.py`: vertices of the Lipschitz polytope of a site by enumeration of bases; the matrix game
by linear programming; the Rényi form of the site function with its dual bound; thresholds and
Shannon capacities; chains of several site types).  Run from this directory; numpy and scipy only.

| script → output | what it checks | run time |
|---|---|---|
| `w_check1.py` → `out_w_check1.txt` | numbers of vertices of the four example sites; Theorem 11.99 — the Rényi form against the game at the Rényi centre, its dual bound, and a blind search over additive instances (12 cases); the table of the worked example for six chains (`E`, `a`, `h`, `R̂(0.3E)`, `θ_na(0.3E)`; largest deviation from the report `5·10⁻⁷`); non-additivity at three accuracies; the pair identity (`10⁻¹³`) | 4 min |
| `w_check2.py` → `out_w_check2.txt` | the negative results: three letters, Hamming, `u = 1`: `E = 0.119499` (uniform) against `0.120196` for `(0.05, 0.5, 0.45)`; the convex kink of `F*` of the triangle site at `t = 0.378` and the jump of the maximiser of `R̂`; **the small-slope regime** — for `u = 0.3, 0.5, 0.6` a law near `(½, ½, 0)` has a larger `h` than the uniform law, for `u = 0.8, 1` a smaller one (crossing `ln 2`); the same for `a` (crossing `0.5194`) | 5 min |
| `w_check3.py` → `out_w_check3.txt` | uniform sites with three and four letters, all box vertices: `h`, `a`, `E` against single dips on `k` equally weighted groups of letters (`k | q`) at `u = 0.5, 1, 2, 3` | 2 min |
| `w_check4.py` → `out_w_check4.txt` | the comparison columns of the worked example at `e = 0` (zero residual; binary coarse-graining and deletion); the uniform four-letter site at `u = 1`: `F*(t) = max(F*_2(t), F*_4(t))` on a grid of 97 slopes (`5·10⁻¹⁶`), crossing and convex kink at `t = 0.65` | 90 s |

Not re-run here: the workstream's exact sums over joint types, its brute-force runs and its
isoperimetric families (`experiments/workstreams/W/`).  A run for six letters (62 vertices) was
abandoned as too slow for this implementation.
