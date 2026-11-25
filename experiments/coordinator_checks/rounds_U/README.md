# Coordinator's checks of workstream U (rounds of adaptivity; theory report §11.24)

Own code, written from the statements of the report.  Run from this directory.

| script | what it checks | output | run time |
|---|---|---|---|
| `u_check1.py` | the two-round upper bound `T^{(2)}(0) = min_{φ,ξ} max{φa + (1−φ)θ_na(ξ), min(φa, (1−φ)ξ) + (1−φ)a}` by direct minimisation: `0.6181a, 0.6197a, 0.6243a, 0.6413a, 0.6646a` at `u = 0.05, 0.5, 1, 2, 3` (the golden ratio in the small-slope limit) | `out_u_check1.txt` | 10 s |
| `u_check2.py` | Theorem 11.86.  (A) the asymptotic lower bound: `Ξ(θ, φ₁)`, `θ₂*(u)` at five slopes (`0.346a … 0.440a`), `Ξ(h, φ₁) > 0`.  (B) **the twins at finite `n` from the statement of the theorem** (own implementation on type grids; the code asserts the Lipschitz property, the coincidence on `V₂`, `W₁ ⊂ V₂` and the value `g₁` on `W₁`): the largest budget at which the twins differ by more than 1 in `ln A`, and the exponent `−ln(p₁ + p₂)/n`, against the lower bound for all algorithms at the same accuracy (`u = 1`: `n = 400 … 3200`; `u = 2`: `n = 200 … 1600`) | `out_u_check2.txt` | 4 min |
| `u_check3.py` | the round-limited recursion: `T^{(2)}(g)` on a grid of accuracies (below `θ_na`, nonincreasing, above the hinted exponent), and three rounds at bounded accuracy through the ladders `(1,1,1)`, `(2,1)`, `(1,2)`: `T^{(3)}(0) ≤ 0.5406a` at `u = 1` | `out_u_check3.txt` | 10 s |

The workstream's numbers are reproduced (its exact finite-`n` table uses a slightly
different second set and other splits; the values differ in the third digit and the
conclusion — the two-round *lower bound* exceeds the lower bound for all algorithms from
`n ≈ 800` on at `u = 1`, from `n ≈ 200` at `u = 2` — is the same; these are two lower bounds,
and no separation from adaptive algorithms is shown at such sizes: Scientific Discovery
Division, SCI-REV-0003, m5).  Theorem 11.84 was first checked only by reading its two
claims against `docs/workstreams/K_REPORT.md` §2.4 (steps 2, 6, 7), on the good event — and
that reading missed that Claim B fails off it (SCI-REV-0003, M1).

**Added with the fourteenth checkpoint (review SCI-REV-0003 of the Scientific Discovery
Division).**  Written by the assistant who checked the review for the coordinator, from
the statements of the report; re-run by the coordinator with identical output.

| script | what it checks | output | run time |
|---|---|---|---|
| `m1_stopping_rule.py` | finding M1: the candidate set of stage 2 computed point by point from the display of Theorem 11.84 (reduced constants) and in closed form with the unreduced constants of the theorem, at the flat instance: with honest brackets of ratio `e^{x_1}` at most a few thousand candidates; with trivial brackets from rung 1 the candidate set is all `M_max` outer points (`2.2·10¹²` against `N_2 = 4.4·10⁹` at `u = 1`, outer dimension 60 of `n = 80`), so the bound of Claim B does not hold "in every run" without the stopping rule | `out_m1_stopping_rule.txt` | 1 s |
| `t3_witness.py` | the reviewer's witness for three rounds: the ladder `(1,1,1)` at `φ = 0.512`, `ξ_1 = 0.631a`, `ξ_2 = 0.107a` gives `0.54026a` (`0.54020a` after a local polish) | `out_t3_witness.txt` | 3 s |
| `r42_finite.py` | Corollary R4.2 at finite `n`: `E′ = −n⁻¹ ln max(p₁, p₂) ≥ E = −n⁻¹ ln(p₁ + p₂)` on the rows of the table of Theorem 11.86, with `E′ − E ≤ 6.3·10⁻⁵`; the hypotheses `p₁ ≤ (n₁+1)(n₂+1)e^{−T}`, `p₂ ≤ (n₂+1)e^{−T}` | `out_r42_finite.txt` | 1 s |

The deterministic statement behind the repair — for stored brackets of ratio at most `e^x`
the candidate set has at most `N` members, whatever the brackets — is tested against
adversarial arrays in harness XX.5, and the withdrawn claim is the documented refutation
DEAD.27.
