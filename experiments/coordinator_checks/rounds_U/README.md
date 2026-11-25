# Coordinator's checks of workstream U (rounds of adaptivity; theory report §11.24)

Own code, written from the statements of the report.  Run from this directory.

| script | what it checks | output | run time |
|---|---|---|---|
| `u_check1.py` | the two-round upper bound `T^{(2)}(0) = min_{φ,ξ} max{φa + (1−φ)θ_na(ξ), min(φa, (1−φ)ξ) + (1−φ)a}` by direct minimisation: `0.6181a, 0.6197a, 0.6243a, 0.6413a, 0.6646a` at `u = 0.05, 0.5, 1, 2, 3` (the golden ratio in the small-slope limit) | `out_u_check1.txt` | 10 s |
| `u_check2.py` | Theorem 11.86.  (A) the asymptotic lower bound: `Ξ(θ, φ₁)`, `θ₂*(u)` at five slopes (`0.346a … 0.440a`), `Ξ(h, φ₁) > 0`.  (B) **the twins at finite `n` from the statement of the theorem** (own implementation on type grids; the code asserts the Lipschitz property, the coincidence on `V₂`, `W₁ ⊂ V₂` and the value `g₁` on `W₁`): the largest budget at which the twins differ by more than 1 in `ln A`, and the exponent `−ln(p₁ + p₂)/n`, against the lower bound for all algorithms at the same accuracy (`u = 1`: `n = 400 … 3200`; `u = 2`: `n = 200 … 1600`) | `out_u_check2.txt` | 4 min |
| `u_check3.py` | the round-limited recursion: `T^{(2)}(g)` on a grid of accuracies (below `θ_na`, nonincreasing, above the hinted exponent), and three rounds at bounded accuracy through the ladders `(1,1,1)`, `(2,1)`, `(1,2)`: `T^{(3)}(0) ≤ 0.5406a` at `u = 1` | `out_u_check3.txt` | 10 s |

The workstream's numbers are reproduced (its exact finite-`n` table uses a slightly
different second set and other splits; the values differ in the third digit and the
conclusion — two rounds need more than the bound for all algorithms from `n ≈ 800` on at
`u = 1`, from `n ≈ 200` at `u = 2` — is the same).  Theorem 11.84 was checked by reading its
two claims against `docs/workstreams/K_REPORT.md` §2.4 (steps 2, 6, 7); no script.
