# Coordinator's checks for theory report §11.25 (slices)

Independent numerical checks of Lemma 11.89 (odds ratio), Theorem 11.90 (a slice is never harder than
the cube) and of the numbers quoted in the section.  Nothing here is used by the proofs; the code shares
nothing with the harness (`experiments/falsify_conjectures.py`, block XXI) except the definitions.

| file | what it checks | run time |
|---|---|---|
| `odds_ratio_proof_check.py` → `out_odds_ratio_proof_check.txt` | every step of the proof of Lemma 11.89: the information density of an Ising pair, the gradient of the mutual information (central differences), `T(h) < 0`, the kernel inequality and the identity that reduces step (4) to it, monotonicity of the capacity in the field of the channel and the position of the optimal input, and the statement itself on 2·10⁵ tables | 15 s |
| `slice_lib.py` | library: block profiles inside one type class; the inner problem for any number of blocks by clipping (Lemma 11.77(a); no duality); closed forms for binary centres | — |
| `slice_check1.py` → `out_slice_check1.txt` | (a) the Legendre pair and the closed form of Theorem 11.90(b) against direct evaluation and against the multi-block solver; (b) 300 random profiles with 3–5 blocks against the best binary centre; (c) Nelder–Mead over three-block profiles (5 cases, 6 starts each): the optimum is the binary one to `2.5·10⁻¹⁶`; (d) domination by the cube pointwise in `t`, and for the non-adaptive function; (e) a first table | 90 s |
| `slice_table.py` → `out_slice_table.txt` | the table of Theorem 11.90: `R^κ(0)`, the best centre type, `a^κ = N^κ(0⁺)`, at `u = 1, 2` | 20 s |
| `potts_check.py` → `out_potts_check.txt` | the remark on more than two letters: the mutual information of a Potts pair maximised over both marginals (`q = 3, 4`; the maximiser is uniform on 2, 3 or 4 letters depending on the coupling); uniform `k`-ary cubes (`R₂ > R₃` for `u < ln 2`); the game function as an integral of the mutual information along the tilting path | 40 s |

Run from this directory (`python3 slice_check1.py`); numpy and scipy only; fixed seeds.

**Correction of an earlier computation.**  `../meanfield_T/slice_check.py` gave `0.028092`, `0.024689`,
`0.018902` for the slices of density `0.4`, `0.3`, `0.2` at `u = 1` (quoted as `0.0281`, `0.0247`, `0.0189` in
`DEAD_ENDS.md` D49, item 5, before this checkpoint).  That script takes the inner minimum over a grid of
exits, which is biased upward, and the outer maximum then selects the bias.  The closed form, the
multi-block solver and a direct evaluation on a grid of shells agree on `0.028005`, `0.024588`, `0.018842`.
The qualitative statement (every slice other than `½` is strictly below the cube) is unaffected and is now
a theorem.

**Added with the fourteenth checkpoint (review SCI-REV-0001 of the Scientific Discovery Division).**
The review found (its m12) that the scripts above test profiles with more than two blocks for the
hinted function `r` at accuracies `e ≥ 0` only — not at `e < 0`, where the first proof of Theorem 11.90(a)
had a gap, and not for the non-adaptive function `n` — and that item (e) of `slice_check1.py` evaluates
`N^κ` at `X = 10⁻⁹`, where the square-root cusp at zero costs two units in the fifth digit (`0.110924`
for `0.110944`).  The three scripts below were written, from the statements of the report, by the
assistant who checked the review for the coordinator; the coordinator re-ran them with identical
output (timing lines apart).

| file | what it checks | run time |
|---|---|---|
| `m2_check.py` (`m2_check.py 1`, `m2_check.py 2`) → `out_m2_check_part1.txt`, `out_m2_check_part2.txt` | Theorem 11.90(a) at negative accuracies, three independent computations: (A) the two-block supremum; (B) **all** laws on a grid of 1201 block densities, any number of blocks — for fixed multipliers the dual function is linear in the law, so the supremum over feasible laws is a linear programme with three constraints; (C) explicit profiles with three to five blocks, random and by Nelder–Mead.  Nine `(κ, u, e < 0)` and a control at `e = 0`: no excess over two blocks; the optimum is a two-atom law, or a three-atom law with zero budget and the value `−e` | 2 × 2 min |
| `m2_check_margin.py` → `out_m2_check_margin.txt` | the same linear programme with the feasibility tolerance tightened: the largest excess is `−1.4·10⁻¹¹` | 2 min |
| `minor_checks.py` → `out_minor_checks.txt` | the reviewer's four-line proof (thermodynamic integration on the fibre, `S ≥ 16cosh²(ω/4)` on 20 000 random tables, the curvature form `Ψ″ = 4/S`), and the minor findings m1–m6, m11, m12: the optimal input of an asymmetric channel (field against the channel, distribution towards the more reliable symbol), the closed form over shells `ℓ ≥ 0` only, the game form at negative accuracies, the two forms of the cube's function, the centre types for `N^κ(0⁺)` and the cusp, the non-adaptive function for profiles with any number of blocks | 70 s |

In the harness the negative accuracies are covered by XXI.6.

**Added with the nineteenth checkpoint (the Computational Research Division's ENG-RES-0012).**
That division computed the smallest sensitive balls on type classes exactly up to `n = 10 000` and
asked whether the best centre types it finds (`0.455` at `κ = 0.4`, `0.405` at `κ = 0.3`) agree with the
closed form.  `centre_type.py` → `out_centre_type.txt` (a few seconds): the limiting centre types are
`0.45404` and `0.40803` (and `0.36190` at `κ = 0.2`); the maximum is flat — centre types within `±0.008` of
the best one lose `10⁻⁵` in the exponent — which is why the finite-`n` maximiser wanders; with the centre
restricted to the class the limits are `0.027592` and `0.023021`, which that division's restricted
values (`0.027940`, `0.023398` at `n = 10 000`) approach from above.  Answered in THY-RES-0012 §4.1.
