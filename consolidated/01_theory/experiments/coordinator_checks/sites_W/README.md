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

**Added with the fourteenth checkpoint (review SCI-REV-0005 of the Scientific Discovery Division, and §5
of its review SCI-REV-0001).**  `review_R5/`: the scripts with which the findings of the review were
checked before they were written into theory report §11.26 — by the assistant who checked the review
for the coordinator, from the statements of the report, with own code (`dlib.py`) and with the harness
helpers `st_*` imported as a library; re-run by the coordinator from that directory.

| script → output (in `review_R5/`) | what it checks |
|---|---|
| `c01_m1.py` → `out_c01_m1.txt` | finding M1 (Theorem 11.97(c)): the evaluation step — the least `I(X′;U|T)` under the cost constraint against `R̂(B′ − α(μ))` — on four chains and 48 random pairs; the window step |
| `c02_m2.py`, `c02b_m2.py` → `out_c02_m2.txt`, `out_c02b_m2.txt` | finding M2: `θ_na` is Lipschitz in the composition with constant `max_j a_j` (three chains with `st_theta_na`, `st_a`; 20 000 random pairs with own code: ratio at most `0.31`) |
| `c03_m8_kink.py` → `out_c03_m8_kink.txt` | m8: the slope jump of `F*` at the kink of the triangle site is `+0.0056` (branch slopes `0.054049`, `0.059631` at `t_c = 0.377987`, three routes); the printed `+0.0052` is a second difference on a grid of step `5·10⁻⁴` |
| `c04_additions.py` → `out_c04_additions.txt` | the ceiling `F*(t) ≤ t(1−t)u²/8` on 40 sites; the comparison with the cube for weight `½` on a set of letters (200 cases); the data points at `u = 0.5`; the numbers behind m1 and m4 |
| `c05_m12.py` → `out_c05_m12.txt` | m12: the "blind search" column of `out_w_check1.txt` exceeds the certified dual bound by `1.2 … 3.5·10⁻⁹` because `st_game` solves its linear programme with default tolerances; after a certified re-evaluation the excess is at most `−3.6·10⁻¹⁶` — no statement is affected (checks are at `2·10⁻⁷`) |
| `c06_grid_concavity.py` → `out_c06_grid_concavity.txt` | the grid of 171 three-letter laws at `u = 0.5` and `u = 1`; a local search for the largest `h` at `u = 0.5` (ends at `(0.04505, 0.45676, 0.49819)`, `h = 0.0076753`); 500 random two-letter sites with asymmetric envelopes: no positive second difference of `F*` |
| `c07_omega.py` → `out_c07_omega.txt` | arithmetic of the error term `ω_n` of Theorem 11.97(c) |

Known limitation of a harness helper found on the way: `st_a` (Blahut–Arimoto, 4000 steps, no
certificate) is not converged for site laws with a rare letter (`0.0302712` for `0.0303217` at
`(0.05, 0.5, 0.45)`, `u = 0.5`); it returns a lower bound, and no registered test depends on its last
digits.
