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
