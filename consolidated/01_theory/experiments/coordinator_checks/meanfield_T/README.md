# Coordinator's checks of workstream T (known parts that are functions of the type; theory report §11.23)

Own code, written without looking at the workstream's solvers.  Run from this directory with `python3 <script>`.

| script | what it checks | output | run time |
|---|---|---|---|
| `tv_lib.py` | library: rate function `I`, its largest `u`-Lipschitz minorant `v`; **two inner solvers that share no approximation**: `r_fast` (clippings, `v` in the constraint, bisection in the upper threshold for every lower threshold, golden-section refinement) and `r_slow` (for every exit type a generic convex programme by SLSQP with `I` in the constraint — no clipping lemma, no table of `v`) | — | — |
| `tv_check1.py` | the two solvers agree on random profiles with 2–4 blocks (a numerical test of Lemma 11.77) | `out_tv_check1.txt` | 20 s |
| `tv_check2.py` | two phases (`βJ = 1.5`, `B = 0`, `u = 1`): the binary barrier shell at five accuracies; Nelder–Mead over all binary centres from four starts; the three-block profiles with a free block at `e = 0.002, 0.01, 0.02, 0.05` (own maximisation); re-evaluation with the slow solver | `out_tv_check2.txt` | 12 min |
| `tv_check3.py` | the junction with the uniform cube (`βJ* = 1.12498`; six couplings); a one-phase model with a field; the pair identity `n_μ(e + R) = R` two ways; shell-cone against point-cone; ferromagnets against the uniform cube on 180 random profiles | `out_tv_check3.txt` | 5 min |
| `tv_check4.py` | the late statements of the report: the threshold `u_top = 0.28153` (largest slope of a chord from the top of the barrier); at `u = 0.30` the binary barrier shell (`x = 0.4409`, `0.0022646`), `n_μ(S(0)) = 0` at that shell and `0.001839` at the best shell (`x = 0.4514`): the pair identity fails for cones around profile classes; the free block at `e = 0.02` as a function of the coupling (none at `βJ = 1.12`; `0.0192108`, `0.0181202` at `1.2`, `1.3`) | `out_tv_check4.txt` | 3 min |
| `slice_check.py` | the uniform measure on one slice as known part: the slice of type `½` has the uniform cube's exponent (to grid accuracy), other slices less.  **Its numbers for the slices `0.4`, `0.3`, `0.2` (`0.028092`, `0.024689`, `0.018902`) are biased upward by `10⁻⁴`** (inner minimum on a grid of exits); the correct values `0.028005`, `0.024588`, `0.018842` and the theorem behind them are in `../slices/` (theory report §11.25) | `out_slice_check.txt` | 2 min |
| `e_threshold.py` | the threshold `E` of the field case is the largest chord gap of `ln 2cosh(x/2)` over the window of fields: `0.212295` at `p = 0.1`, `u = 2` (the value `0.21227` used in two earlier documents is `F*(t)/t` at `t = 10⁻⁴`) | `out_e_threshold.txt` | 1 s |

All numbers of the workstream that were re-computed agree to the digits printed.

**Two errors of the coordinator's own first versions of `r_fast`, both found because an outer maximiser climbed onto them**
(recorded in `docs/DEAD_ENDS.md` D49): (1) the local minima of the scan were ranked by value, a plateau of equal values
(no clipping from below) filled all the slots and the other exit was never refined — a spurious `0.0251100` at an asymmetric
centre instead of `0.0251012`; (2) the repair compared neighbours with a tolerance of `10⁻¹⁵`, which dropped the zero region
(values of `5·10⁻¹⁷` next to exact zeros) — a spurious `0.0521` at a profile whose value is `0`.  The version here groups runs
of candidates without a tolerance and always includes the global minimum of the scan.
