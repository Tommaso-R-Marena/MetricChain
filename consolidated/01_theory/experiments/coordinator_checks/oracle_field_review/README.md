# Checks made when SCI-RES-0006 (a one-body marginal oracle with a field) was applied

Fifteenth checkpoint of cycle 10.  The Scientific Discovery Division's workstream F
(SCI-RES-0006; its report `docs/science/workstreams/SF_REPORT.md` on the branch
`research/scientific-translation`) proved conjecture (f) of the first version of theory
report Proposition 11.109 by a *compensation lemma*, and corrected two numbers of its
conjecture (e).  Before the section was rewritten (now Proposition 11.109, Theorem 11.109a,
Proposition 11.109b) the coordinator re-derived the proofs and replicated the finite
statements and the numbers with the code in this directory.  **Nothing here is imported
from that division.**  Run from this directory; numpy and scipy; each script under two
minutes.  The harness test XXIII.7 is a reduced version with ten mutations.

| script | what it checks | output |
|---|---|---|
| `r0_check.py` | the hinted exponent of the zero residual at `p = ¼`, `u = 1`, `e = 0.02` from the closed form of Theorem 11.59(c) and from the game form: `0.013669` (the first version of the section quoted `0.0134` from a coarse grid) | `out_r0_check.txt` |
| `comp_check.py` | the compensation lemma and its ingredients by exact enumeration on `Q_n`, `6 ≤ n ≤ 10`, 24 random cases: mass and mean type of the excess of the cyclic average of cone dips (Theorem 11.109a(b)); membership of the compensated null and alternative in the class; **all one-body marginals of both equal the excess type (to `2·10⁻¹⁵`)**; the gain `ln(1 + E/(1+b))`; the uncompensated control `Φ/(1+Φ)(c_Δ − p_γ)`; the counting bound (trivial at these sizes: the supports fill type classes) | `out_comp_check.txt` |
| `thmA_sums.py` | Theorem 11.109a(c) at the saddle of `R^max`, `(p, u) = (0.3, 1)`, `e = 0.3E`, by exact sums over joint types for `n = 100 … 3200`: the exponent of the lower bound `1/(n·H_{k,r})` rises to `0.01044` at `n = 3200` against `R^max = 0.012210` | `out_thmA_sums.txt` |
| `e_numbers.py` | Proposition 11.109b at the test point: the tilt upper bound `0.012941`; the supremum over two-block profiles of mean type `p` (equal to it; its maximiser has a block law outside the window); the same with block laws in the window, `0.012635`; dips of the forced centre type (annular `0.00845`, balls `0.00570`); the decrease `5.3 %`–`7.6 %` | `out_e_numbers.txt` |
| `e_numbers2.py` | cross-check of the window-restricted supremum by a one-dimensional scan and of the inner minimisation by brute force | `out_e_numbers2.txt` |

What was **not** re-computed: the division's tables for other parameters, its two-body
construction, its tolerance statement.  The theory report quotes those as the division's.
