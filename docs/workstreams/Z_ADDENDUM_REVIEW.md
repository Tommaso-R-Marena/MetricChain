# Independent referee report on `docs/workstreams/Z_ADDENDUM.md`

*Referee: independent AI referee (internal review, not external peer review), 2026-11-26.
Brief: `docs/workstreams/Z_ADDENDUM_review_brief.md`.  Scripts and outputs:
`experiments/workstreams/Z/review_addendum/`.  This file was written incrementally.*

> **Which version was reviewed.**  The addendum as it stood when the brief was written
> (315 lines; sections A0–A10).  While this review was in progress the author read this
> file, applied its findings in place and added two sections, A6a and A6b.  §§0–4 below
> refer to the version reviewed; §5 is a postscript on the changed version (the repairs
> as applied — two slips; A6a and A6b are outside the brief and are **not refereed** here).

## 0. Summary of verdicts

**No error of substance found.  Every numbered statement of the addendum is correct as
stated or correct after a repair of wording; three sentences of the surrounding text
are wrong or misleading as written, and two quoted numbers are slips.**  I tried to
break the statements on paper (every step re-derived) and with code of my own that
shares nothing with the author's (§1): none broke.

| statement | verdict |
|---|---|
| Lemma A1 (A1) | **correct**; repair of wording: the clause "Consequently …" needs `W₀ ≡ 0` (or a base of type `𝓗^∞(𝔏₀; E)`).  A top above `b⁺` and (S2) on `[0, b_{j+1}]` only are indeed enough |
| Lemma A2 (A1) | **correct as stated** |
| Lemma A3 (A2) | **correct as stated** (closed interval, end value, finite slope at zero, `f(0) = 0` all in order) |
| Corollary A4 | **correct as stated** |
| Proposition A5 | **correct as stated** (`b_j > h` is the one place that needs (H1)) |
| Proposition A6 | **correct as stated** (`Σ ≥ s + B/h − 1`; admissibility; both cases `G_∞ > 1`, `G_∞ = 1`; the bound afterwards) |
| Proposition A7 | **correct as stated**, given Lemma RC / Lemma T / Theorem R of `R_REPORT.md`; Corollary A4 is applied in the right direction |
| Proposition A8 | **correct as stated**; equality at `j = 2`, strict from `j = 3` (numerically) |
| Theorem Z′ | **correct as stated, conditionally** (as Theorem Z, base = Theorem A of Q2 with `M = 0`); the sentence after it ("smaller `b_k` at every `k`") is **wrong as stated** |
| Lemma A9 | **correct as stated** |
| Lemma A10 | **correct as stated** (two points of wording in the proof) |
| Proposition A11 | **correct as stated** |
| Theorem Z″ | **correct as stated, conditionally**, for every fixed `g > 0`; empty for `g ≥ ε*` (should be stated for `0 < g < ε*`); the constant of the proof is of order `(h/g)²`, not `h/g` |

Errors and slips (details and repairs in §3): (1) after Theorem Z′, "by Corollary A4 the
envelope schedule has the smaller `b_k` at every `k`" — false for `k ≤ 5` at `u = 1`, and not
what A4 gives; (2) A10/A6: "`b_j = τ_j`" is not an open question, it fails at `j = 3`
(`τ₃ = 0.3612a < b₃ = 0.3633a`); (3) A8: the factors `3.5, 7, 21` are against Theorem A of Q2, not
against every earlier bound (against the cut curves: `1.15, 1.07, 1.05`); (4) A8: "`0.9973` at
`k = 80`" is a grid artefact (`0.9982`), and the grid errs on the non-conservative side
(immaterial); (5) A9: "the constant grows like `1/g`" is the heuristic, the proof gives
`1/g²`; at a fixed rate the decay is `κ_g^k`, not `e^{−kg/h}`; (6)–(10) wording and rounding.

Replicated with my own code (§1): the constants; the slope map in two independent
ways; the envelope sequence in two ways (grid-free and on grids) for the cube at
`u = ½, 1, 2` and the Gaussian pair, with exact values by hand for the Gaussian pair; the
table of A6 (agrees, up to the last digit of the two entries at `j = 40`); the comparison
of A4 with the fixed-rate sequence (a hinge, in closed form) and with the cut chain;
Lemma A1 on envelope curves (72 cases per pair, with a negative control) and the
exponent-level inequality inside Proposition Z3 at finite `d` up to extensive rates (240
cases); A8 at the second and third level by brute force on the operator `R`; the table
of A9 (agrees, up to the last digit of one entry) and the profile; Lemmas A9, A10,
Proposition A11; the table of A8 (my own unrolling, the Q2 formulas imported).

Postscript (§5).  The addendum was changed while this review was in progress (findings
applied; sections A6a, A6b added).  The applied repairs are faithful except two slips
(a mis-citation of (P2) in the proof of A5; "`0.996, 0.998, 0.998`" for `0.996, 0.997, 0.998` in A8).
A6a and A6b are outside the brief and are not refereed here; one number in A6a is off
in the fourth digit (`τ₃ = 0.361184·a`, not `0.361296·a`: a grid of step `10⁻³` in `φ` at a kink), and
the certified tops of A6b are, as Corollary A4 requires, above my envelope tops at all 30
entries of its table (by at most `6·10⁻⁷·a`).

## 1. Log of findings (appended as the review proceeds)

### 1.1 First reading (paper proofs), before any computation — provisional

Read in full: the brief, `Z_ADDENDUM.md`, `Z_REPORT.md`, `R_REPORT.md`; the author's
`rlib.py`, `zetalib.py` (`EnvZ`), `z4_env.py`, `z5_extensive.py`, `z2_formula.py` and their
outputs.  Not read: `Z_REVIEW.md`, `experiments/workstreams/Z/review/` (as instructed).

Provisional verdicts after re-deriving every step by hand (details in §2):

* Lemma A1 — the step "`inf_e max_𝓔 Φ = max_𝓔 inf_e Φ ≤ sup{B − Σ(B, W_j(B))g : Σ < ∞}`" is exactly the
  part of the proof of Proposition U that does not involve `T`; I re-derived the three
  cases (a), (b), (c) and Sion's hypotheses.  A top `b_{j+1} ≥ b⁺` and (S2) on `[0, b_{j+1}]` only
  are enough.  Provisional: correct; one wording point on "base family of flat type `b₀`".
* Lemma A2, Lemma A3, Corollary A4, Proposition A5 — provisional: correct.
* Proposition A6 — every step re-derived (both cases `G_∞ > 1`, `G_∞ = 1`): provisional: correct.
* Propositions A7, A8 — provisional: correct (direction of A4 right; base case fine).
* Lemma A9, Lemma A10, Proposition A11 — provisional: correct at the exponent level;
  remarks on hypotheses to follow.
* Theorem Z′, Theorem Z″ — to be examined against `Q2_REPORT.md` (Theorem A with `M = 0`;
  Lemma U / Lemma Z2 at rates `e ≥ ε*`, i.e. at extensive accuracies).

### 1.2 Own code: basics (`ra_lib.py`, `ra01_basics.py` → `out_ra01_basics.txt`)

My library is written from the definitions and does not import `rlib.py`/`zetalib.py`.  The
slope map is computed in two independent ways — through `J` (`Σ = t′(1 − s)/(1 − t′)`,
`J(t′)/(1 − t′) = B/(1 − s)`; I re-derived this, and `J(t) = (1 − t)ln 2 − ln(1 + e^{tu}) + t·ln(1 + e^u)`
from `θ_na(e) = KL(ρ‖½)`, `KL(ρ‖p_u) = e`) and as the supremum over `e` computed from `θ_na` itself.

* Constants of the brief reproduced: cube `u = 1`: `a = 0.11094407`, `h = 0.02913914`, `L = 0.490034`,
  `θ_hint″(0) = 4.244978`, `c_*² = 0.07114732`.  (Also `u = 2`, `u = ½`, Gaussian pair.)
* `Σ` by the two routes: agreement to `1.5·10⁻¹¹` (relative) on 300 random regular points per
  pair (cube `u ∈ {½, 1, 2}`, Gaussian); Gaussian closed form `B(1 − s)/(1 − s − B)` to `3·10⁻¹⁵`.
* `J` closed form against `inf_e[(1 − t)θ(e) + te]` from `θ_na`: `4·10⁻¹⁶`.  `θ_hint` closed form against
  `sup_t[J(t) − tg]`: `2·10⁻¹⁶`, also beyond `ε*`.
* `Σ(B, s) ≥ s + B/h − 1` (used in A6): holds on 2 000 random points per pair (least slack `4·10⁻¹³`,
  attained near the fixed point as it must be); `Σ(h, L) = L`; `L < 1 − h/a`.
* Joint convexity/monotonicity of `Σ`: no violation in 3 000 random midpoints per pair.
* My convex-envelope routine (monotone chain) against a brute-force definition (minimum
  over all spanning chords): equal to `2·10⁻¹⁶` in 200 random cases.

### 1.3 Own code: the envelope sequence (`ra02_envelope.py` → `out_ra02_envelope_*.txt`)

Two implementations of my own: **(S)** "structural" — `W_{j+1} = Σ(·, W_j(·))` up to the tangency
point `B_t(j+1)`, then the tangent line through `(b_{j+1}, 1)` (this is the description of the
envelope in the proof of Lemma A10, which I checked by hand, §2); root finding in double
precision, no grid; **(G)** from the definition on grids — lower convex envelope of the grid
values of `min(1, Σ(B, W_j(B)))`, uniform grids of 4 000 and 16 000 points and a grid of 8 000
points refined quadratically at the top.  (S) and (G) agree as far as the grids resolve
the top (quadratic 8 000: `10⁻⁸·a` at `j ≤ 10`, `10⁻⁷·a` at `j = 80`; a *uniform* grid of 4 000 points
is off by `10⁻³·a` at `j = 80` — the tangent piece is then far below the grid spacing).

* **Gaussian pair, exactly.**  By hand: `W₁(B) = B` (the tangent from `(1, 1)` touches `Σ(B, 0) = B/(1 − B)`
  at `B = 0` — the degenerate case `B_t = 0`), `b₂ = ½`; `B_t(2) = ¼`, `W₂(¼) = 3/8`, slope `5/2`, `b₃ = 5/14`.
  (S) reproduces all of these to rounding.  `b_j ≥ 1/(4cos²(π/(2j + 1)))` for all `1 ≤ j ≤ 400`
  (`b₂ = 0.5` against `0.3820`, `b₃ = 0.35714` against `0.30798` and against `τ₃ ≥ 1/(2√2) = 0.35355`;
  the ratio `(b_j − h)/(lower bound − h)` is `1.11, 1.05, 1.025` at `j = 10, 20, 40`).
* **Cube, `u = 1`: the table of A6 is reproduced** (`b_j/a`: `1, 0.50041, 0.36330, 0.31279, 0.29138,
  0.28132, 0.27275, 0.26906, 0.26424, 0.26305` at `j = 1, 2, 3, 4, 5, 6, 8, 10, 20, 40`; `j²(b_j − h)/c_*²`: `1.1498, 1.4830,
  1.4126, 1.2511, 1.1200, 1.0484, 1.0083, 1.0008, 0.9958, 0.9969`) — every entry to the digits given,
  except the last digit of the two entries at `j = 40` (`0.2631` and `0.996` there; `0.2630` and
  `0.997` are the rounded values: a double rounding, and the grid of 4 000).
* **One number of A8 is a grid artefact:** "`0.9958, 0.9968, 0.9973` at `k = 20, 40, 80`" — (S) gives
  `0.99584, 0.99690, 0.99819`; the author's grid values are biased *downwards* (an envelope of
  grid values lies above the envelope of the function, so the next top comes out too
  small), by `9·10⁻⁸·a` at `k = 80`, which is `0.09` per cent of `b_k − h` there (the author's own two
  grids give `0.9940` and `0.9973`).  The conclusion drawn from it survives for the cube at
  `u = 1`: (S) has `0.99851, 0.99922, 0.99960, 0.99973, 0.99980` at `k = 100, 200, 400, 600, 800` — below one
  from `k = 11` on and increasing to one like `1 − 0.16/k` (these agree with the values
  `0.99873, 0.99903` at `120, 160` that `R_REPORT.md` §11 quotes from `dual_ub_cube.py`).  So
  "`h + c_*²/k²` beyond `k = 80`" over-states `b_k − h` by at most `0.2` per cent in the table of A8.
  **"Approached from below" is specific to the pair:** Gaussian pair `1.0044, 1.0010, 1.0003,
  1.00004` at `20, 40, 80, 200` (from above, like `1 + 1.7/k²`); cube `u = 2`: `0.948` at `k = 6`, `0.9736, 0.9926,
  0.9970` at `20, 80, 200` (from below); cube `u = ½`: above one up to `k = 30`, `0.99974` at `80`, `0.99983` at `200`.
* Family properties of the computed curves (convex, nondecreasing, values in `[0, 1]`,
  `W_j(b_j) = 1`, `W_{j+1} ≤ min(1, Σ(·, W_j))`): hold at all levels checked (to rounding).
* Consistent with A5–A7: `b₀ = b₁ = a`, tops strictly decreasing from there on and above `h`;
  `j²(b_j − h)/c_*² → 1` for the four pairs (to `2·10⁻⁴` at `j = 800`, cube `u = 1`).

### 1.4 Own code: comparison (A4), the fixed-rate sequence (A6), the cut chain (A7) (`ra03_comparison.py` → `out_ra03_comparison_*.txt`)

* **The fixed-rate sequence is a hinge.**  `V_j(B) = v_j·(B/h − 1)₊` with `v_{j+1} = (v_j + 1)/G_j`,
  `c_{j+1} = min(c_j, (1 + v_j)/(v_j/h + 1/a))` (the positive part always acts at `B = h`) — so it can be
  computed in closed form.  Cube `u = 1`: `c_j/a = 1, 1, 0.5756, 0.4384, 0.3729, 0.3358, …`, `G_j = 2.807, 1.616,
  1.231, 1.047, 1, 1, …`; `c_j ≤ c⁎ = ah/(a − h) = 0.3562a` from `j₀ = 5` on (Gaussian: `j₀ = 5`; cube `u = 2`: `j₀ = 4`).
  Checked on grids for 140 levels and three pairs: (S2) (`V_{j+1} ≤ Σ(·, V_j)`, no violation), values
  in `[0, 1]`, (S1) (irregular just beyond `c_{j+1}`), the bound `c_{j₀+i+1} − h ≤ h(1 − h/a)/(i + h/a)` (no
  violation; `(c_j − h)·j/h → 0.75` at `u = 1`, i.e. `c_j − h ≈ (1 − h/a)h/j` as the proof says), and the
  comparison `b_j ≤ c_j`, `W_j ≥ V_j` on `[0, b_j]` (no violation).
* **The cut chain** (my own implementation of §6 of `R_REPORT.md`; `s_t = L + 0.05`): cube `u = 1`,
  `b₀ = h + 0.003`: range condition holds at 60 levels (largest `W_{j+1}(b_{j+1}) = 0.818`), (S2) holds,
  `i²(b^cut_i − h)/c_*² = 1.3745, 1.5328, 1.4629` at `i = 10, 20, 40` — the numbers of `Z_REPORT.md` §7; the
  first level with `b_k ≤ h + ε₁` is `k₁ = 6`, and `b_{k₁+i} ≤ b^cut_i`, `W_{k₁+i} ≥ W^cut_i` on `[0, b_{k₁+i}]` for all
  `i ≤ 60` (`b_{k₁+i} − h` is `0.28, 0.38, 0.52, 0.60` of `b^cut_i − h` at `i = 10, 20, 40, 60`).  The same from
  `b₀ = h + 0.001` (`k₁ = 9`), for the Gaussian pair (`b₀ = h + 0.02`: range value `0.83` as in `R_REPORT.md`;
  `h + 0.005`) and for the cube at `u = 2`.  The direction of Corollary A4 in A7 is right.
* Random admissible sequences (random factors below one and random stretches of the
  envelope of the image, tops between `b⁺` and the previous top; 40 sequences of 12
  levels on grids): never below the envelope sequence in the top, never above it in the
  curve.  (A weak test of a two-line monotonicity argument; recorded for completeness.)

### 1.5 Own code: Lemma A1 on the envelope curves; A8 at the second level by brute force (`ra04_lemmaA1.py` → `out_ra04_lemmaA1_*.txt`, `out_ra04b_tau2.txt`)

* **Lemma A1.**  For `j ∈ {0, 1, 2, 3, 5, 8, 12, 20, 40}` and eight rates `g` from `0.003h` to `1.5ε*` (72 cases per
  pair; cube `u = 1`, Gaussian pair), with `θ_na` evaluated from its definition:
  `inf_φ max_{B ≤ b_j} Ψ_g(φ; B, W_j(B))` equals the minimax value `U_j(g) = sup{B − Σ(B, W_j(B))g : Σ < ∞}` to
  `5·10⁻¹⁰·a` (the identity in the proof), and `U_j(g) ≤ M_{W_{j+1}, b_{j+1}}(g)` in every case, with equality
  (to rounding) where the maximising line is on the un-cut part of the curve and a strict
  inequality where the cap or the tangent piece is active (up to `0.5a` at `j = 0`).  Negative
  control (`W_{j+2}` in place of `W_{j+1}`): the inequality fails in 51 of 72 cases (cube), 50 of 72
  (Gaussian).  *Note:* for `j = 0` the infimum over `φ` is not attained — it is the limit `φ → 1`
  (value `θ(g)`) — so "there is `φ ∈ (0, 1)` … `+ η`" is the right form of the statement, and
  my first scan (which stopped at `φ = 0.999`) missed it by `10⁻³`.
* **Proposition A8 at `j = 2`, by brute force on `R` itself.**  `R[θ](g)` minimised over `(φ, β)` on grids
  with zooms (any point is an upper bound) at 13 rates from `10⁻⁴h` to `1.2ε*`: `T₂(g) ≤ M_{W₂, b₂}(g)` in
  every case — strictly at positive rates (by up to `0.12a`: the optimal tolerance `β` is not
  small, and the cap is active), with equality in the limit `g → 0`:
  **`b₂` equals the closed form `τ₂ = min_φ max{(1 − φ)a, φa + (1 − φ)θ(φa/(1 − φ))}` of the theory report
  (remark after 11.58) to `2·10⁻¹⁶`** — `0.5004100181a` (cube `u = 1`), `0.5056154420a` (`u = 2`), `½` (Gaussian).
  So at `j = 2` the bound of A8 is an equality.  (`T₂` itself has a square-root singularity at
  zero — `T₂(10⁻⁴h) = 0.4957a` — so `M_{W₂, b₂}`, whose slopes are at least `−1`, is not `T₂`.)
* The theory report's `τ_k/a = 0.5004, 0.361, 0.311, 0.290, 0.280, …` (`k = 2 … 6`; numerical) against
  `b_k/a = 0.50041, 0.36330, 0.31279, 0.29138, 0.28132`: consistent with `τ_k ≤ b_k`.  (The third
  level on `R` itself: §1.8.)
* **A slip in the table of A6:** `b₄₀/a = 0.263047`, which rounds to `0.2630`; the table has `0.2631`
  (the script prints `0.26305`, rounded a second time).  Immaterial — but the theory
  report quotes `τ₄₀/a = 0.2631`, and with the table's digits the reader cannot see whether
  `τ₄₀ ≤ b₄₀`; at this precision neither number decides it.

### 1.6 Own code: extensive accuracies, A9 (`ra05_extensive.py` → `out_ra05_extensive_*.txt`)

`M_{W_k, b_k}(g)` is computed from the structural sequence by bisection on `W_k′(B) = 1/g` (no grid).

* **The table of A9 is reproduced** (cube `u = 1`; `k²(M_{W_k, b_k}(g) − θ_hint(g))/c_*²`):

  | `k` | `g = 0` | `0.01h` | `0.1h` | `0.5h` | `h` | `0.5ε*` |
  |---|---|---|---|---|---|---|
  | 2 | 1.483 | 1.475 | 1.398 | 1.040 | 0.547 | 0.0215 |
  | 5 | 1.120 | 1.068 | 0.5915 | 0.1028 | 0.0169 | `1.2·10⁻⁴` |
  | 10 | 1.001 | 0.7916 | 0.3007 | 0.0187 | `3.7·10⁻⁴` | `7·10⁻⁹` |
  | 20 | 0.9958 | 0.6303 | 0.1472 | `4.4·10⁻⁴` | `6·10⁻⁸` | |
  | 40 | 0.9969 | 0.5050 | 0.0387 | `8·10⁻⁸` | | |
  | 80 | 0.9982 | 0.3546 | 0.00221 | | | |

  Every entry of the addendum agrees to the digits it gives, except `k = 80`, `g = 0` (`0.997`
  there, `0.998` here: the grid artefact of §1.3).  `M_{W_k, b_k}(g) ≥ θ_hint(g)` everywhere (to rounding).
* **The profile.**  At fixed `ζ = kg/h` the scaled defect converges, as `k` grows, to `f(ζ)/(2π²)` with
  the `f` of Proposition S of `R_REPORT.md` (`ζ = 1`: `0.3007, 0.3022, 0.3032` at `k = 10, 40, 160` against
  `0.3036`; `ζ = 8`: `0.00196, 0.00219, 0.00221` against `0.00221`; Gaussian pair the same) — so the
  majorants `M_{W_k, b_k}` have the same scaled profile as the sketch claims for `T_k`.  The
  addendum's "`0.0022` predicted, `0.002` computed" at `ζ = 8` is right (`2ζ²e^{−ζ}/(2π²) = 0.00218`).
* **At a fixed rate the decay is not `e^{−kg/h}` but `κ_g^k`,** `κ_g = θ(e_g)/e_g = 1 − g/(J(t_g) + (1 − t_g)g)`,
  `J′(t_g) = g` — the multiplier of the slope map at the line that is tangent to `θ_hint` at `g`.
  Observed ratios of consecutive defects (cube `u = 1`): `0.3636` at `g = h` (`κ_g = 0.36356`, `e^{−1} = 0.3679`),
  `0.11626` at `g = 2h` (`κ_g = 0.11626`, `e^{−2} = 0.1353`), `0.00266` at `g = 0.9ε*` (`e^{−g/h} = 0.024`); `κ_g → e^{−g/h}`
  only as `g → 0`.  This is consistent with, and sharper than, the heuristic sentence after
  Theorem Z″; the number of levels with `n·(M_k(g) − θ_hint(g)) ≤ 1` grows like `ln n/ln(1/κ_g)`
  (`23` levels at `n = 10^{12}`, `g = h`; `181` at `g = 0.1h`).
* **Lemma A9:** `0 ≤ t₁ − p_i ≤ t₁λ_η^i` for six values of `η`, 40 intercepts each, `i ≤ 400`: no violation;
  `θ(e₁) = J − t₁J′`, `κ = 1 − J′/(B + (1 − t₁)J′)` and `∂Σ/∂s` at the fixed point agree to `7·10⁻¹⁵`; `J′(t₁) ≥ η/L`.
  The bound is crude (`κ(h − η) = 0.668` against `λ_η = 0.980` at `η = 0.01h`), as it may be.
* **Lemma A10:** for eight values of `η` and all `k ≤ 260` with `b_k − h < η(1 − L)/L` (1 971 cases): the
  tangency point is beyond `h − η`, always.  More is true numerically: `B_t(k) > h` for every
  `k ≥ 2` (cube; `B_t(2) = h` exactly for the Gaussian pair), while `B_t(1) = 0.157h` (cube) and
  `B_t(1) = 0` (Gaussian): the hypothesis is needed at `k = 1` only.  Independently of the
  structural description, on the grid sequence: envelope = image on `[0, h − η]` to `10⁻¹⁹`.
  `W_{k(η)+i} ≥ p_{i+1}` on `[0, h − η]`: no violation.
* **Proposition A11:** the inequality holds wherever the recipe of the proof could be
  evaluated; but the recipe is very weak — at `g = 2h` it gives `η = 0.0067h`, `λ_η = 0.9866`, `k(η) = 19`,
  `k₁ = 257` (the true ratio is `0.116`), at `g = h`: `λ_η = 0.99656`, `k₁ > 260` (true ratio `0.364`); `η ∝ g²`.
  So the constant `C(u, g)` *of the proof* is of the order `c_Z·hL/η ≈ 300·c_Z·(h/g)²`, not `c_Z·h/g`.
* **Rates `g ≥ ε*`:** `M_{W_k, b_k}(g) = 0` already for `k = 1` (`W₁′(0) = 1/ε*`), in both pairs.

### 1.7 The numbers of A8 (`ra06_formula.py` → `out_ra06_formula.txt`; `out_ra06_author_z2_formula_env_rerun.txt`; `ra03b_same_index.py` → `out_ra03b_same_index.txt`)

* **Is the formula what Theorem Z′ says?**  Yes.  I read `z2_formula.py` (mode `env`) against §6 of
  `Z_REPORT.md` with `M₁ = 0`: for `j = k, …, 1` a chain (`B′ = b_j`, accuracy `𝒳 = X₀(n) + 1`, `α = ε̂` at the top
  and `1` below; block by (4.1) of Q2 at the current `Λ̄`; `Λ̄ ← Λ̄ + j(n)q_T(n, Λ̄ + n·b_j)`; `+ A_T + j(n)Δ_T + 𝒳 + 1`),
  then a level (`+ ℓ₀(n, Λ̄) + X₀(n) + d_min·ln 2 + 2`; `Λ̄ ← Λ̄ + q(n, Λ̄)`), then the base `𝓔′₀(n; Λ̄)` (the chain
  on the base bracket at accuracy one and `E_𝔅`), entered with the final `Λ̄`.  The bound is
  `n·b_k +` this, `k` levels giving the top `b_k`.  Re-running the author's script reproduces
  `out_z2_formula_u1_env.txt` line by line.
* **Two rows and more, with my own unrolling and my own tops** (structural sequence, no
  grid; the Q2 formulas `A_T`, `q_T`, `Δ_T`, the block, `ℓ₀`, `q`, `𝓔′_M` imported read-only from `q2lib` — not
  re-derived): `n = 10⁴ … 10⁸` agree with the table to all digits given (`1 025 (2)`, `1 627 (3)`,
  `2 476 (4)`, `5 648 (6)`, `1.38·10⁴ (12)`, `3.333·10⁴ (24)`, with the same split into `n(b_k − h)` / chains
  / levels / base); `10⁹`: `7.866·10⁴` at `k = 51` (table: `7.87·10⁴` at `52`); `10^{10}`: `1.833·10⁵` at `k = 105` (table:
  `1.84·10⁵` at `104`) — a finer search over `k` and exact tops beyond `k = 80`; `10^{12}` and `10^{15}` at the `k`
  of the table (`ra06b_formula_large.py`): `9.676·10⁵` (484) and `1.128·10⁷` (4510), same split
  (`3.036·10⁵ / 5.856·10⁵ / 7.797·10⁴ / 514` and `3.498·10⁶ / 6.892·10⁶ / 8.913·10⁵ / 643`).  The per-level loss
  `(chains + levels)/(k ln n)` is `31, 34, 37, 40, 44, 47, 48, 49` at `n = 10⁴ … 10^{10}`: "about `37`–`50`" is
  right from `10⁵` on.
* **"Below every earlier bound from `n ≈ 3·10⁴` on" — true as a statement about formulas, and
  conservative:** scanning `n` between `10⁴` and `10⁵`, the envelope bound is below Theorem
  11.58a at every `n ≥ 10⁴` scanned, below Theorem A of Q2 from `n ≈ 1.2·10⁴`, and below the
  non-adaptive `n(a − h)` from `n ≈ 1.5·10⁴` on (`1 153` against `1 145` at `1.4·10⁴`; `1 214` against `1 309` at `1.6·10⁴`).
* **The factors quoted after the table are not against "every earlier bound".**  "`1.6` at `10⁵`,
  `1.9` at `10⁶`–`10⁷`, `3.5` at `10^{10}`, `7` at `10^{12}`, `21` at `10^{15}`" are the ratios to *Theorem A of Q2*
  (`1.59, 1.87, 1.89, 3.53, 6.98, 20.8`).  Against the best earlier bound *in the same table* —
  from `10⁷` on that is the cut-curve bound of `Z_REPORT.md` — the factors are `1.83, 1.47, 1.27,
  1.15, 1.07, 1.05` at `n = 10⁷, 10⁸, 10⁹, 10^{10}, 10^{12}, 10^{15}`: they tend to one, as they must (the
  two schedules have the same `c_*²` and the same `c_Z`; the envelope schedule saves the base
  and the early levels).  A wording matter; the numbers of the table are right.
* **The sentence after Theorem Z′ is wrong as stated:** "by Corollary A4 the envelope
  schedule has the smaller `b_k` at every `k`".  Corollary A4 compares sequences *from the
  same start*; the cut sequence of `Z_REPORT.md` starts at `h + ε₁`, the envelope sequence at `a`.
  What A4 gives is `b_{k₁+i} ≤ b^cut_i` (as in A7).  At the same index the envelope top is
  *larger* for `k ≤ 5` (cube `u = 1`, `(s_t, ε₁) = (L + 0.05, 0.003)`: `(b_k − h)/h = 2.81, 0.905, 0.383, 0.191, 0.109`
  at `k = 1 … 5` against `0.103`) and smaller from `k = 6 = k₁` on (numerically, to `k = 60`; the
  same picture for the Gaussian pair).  The intended statement — fewer levels in all,
  and no base — is true: `k₁ + i` envelope levels over the bracket against `i` cut levels
  over 43.
* The one-level test quoted in A8 (`out_z1_onelevel_u1_env.txt`): the numbers quoted (`1.2`, `15.6`,
  `51` nats, 66 cases) are those of the file.  I did not re-run it.  Its targets go up to
  `x̂ = X₀ + u·d`, so it is also a (one-level) test of Proposition Z3 at extensive accuracies.

### 1.8 Own code: the third level on the operator `R` itself (`ra07_tau3.py` → `out_ra07_tau3_*.txt`)

`T₂ = min(θ, R[θ])` on 1 200 rates (meshes over `(φ, β)` with zooms; every mesh point is an upper
bound), then `τ₃ = inf_φ sup_γ [min(γ, φa) + (1 − φ)T₂(γ/(1 − φ))]` and `T₃(g)` at eight rates, with `T₂`
interpolated (the uncontrolled part; the value of `τ₃` does not move when the grid is
refined to 4 800 rates).

* **`τ₃ = 0.361184·a` for the cube at `u = 1`** — the theory report's `0.361a`, found independently —
  **against `b₃ = 0.363301·a`**; Gaussian pair: `τ₃ = 0.355233` against `b₃ = 5/14 = 0.357143` (and above
  the lower bound `1/(2√2) = 0.353553` of `R_REPORT.md`).  So Proposition A8 holds at `j = 3`, and
  **strictly: `b₃ − τ₃ = 2·10⁻³·a`, `0.6` per cent** — far beyond the accuracy of either number.
* `T₃(g) ≤ M_{W₃, b₃}(g)` at all eight rates from `10⁻³h` to `3h`, by up to `0.05a` at small rates and by
  `3·10⁻⁶a` at `g = 3h` (where both are within `10⁻⁵a` of `θ_hint`).  *A warning from my own first
  attempt:* a coarse mesh missed the minimiser at `g = 3h` (it sits at `φ = 0.98` with `β/g ≈ 0`,
  next to the trivial branch `φ → 0, β → g`) and "found" a violation of `5·10⁻⁵a`; with a mesh
  that is fine at both ends the violation is gone.  A search over `(φ, β)` can only confirm
  the inequality, never refute it.
* **Consequence for A10 of the addendum.**  Its third item says that "the envelope dynamics
  is the *exact* dynamics of the best convex majorant of `T_k` (so that `b_j = τ_j`) is not
  proved".  The parenthesis is not merely unproved: `b_j = τ_j` holds at `j = 2` (closed form,
  §1.5) and **fails at `j = 3`** in both pairs (and at `j = 4, 5, 6` by the theory report's own
  `τ_k/a = 0.311, 0.290, 0.280` against `b_k/a = 0.3128, 0.2914, 0.2813`).  The reason is visible in
  §1.5: `T₂ < M_{W₂, b₂}` at positive rates (the optimal tolerance `β` is not zero, and `T₂` is not
  a maximum of lines of slope at most one), and `R` is monotone.  What survives is
  `τ_j ≤ b_j` with the same constant `c_*²` in the limit.

### 1.9 Own code: the exponent-level inequality inside Proposition Z3, at finite `d` and extensive rates (`ra08_z3_exponent.py` → `out_ra08_z3_exponent.txt`)

What Theorem Z″ needs of Lemma A1, Lemma Z1a and the discretisation of the outer
fraction: for the grid family `𝔏_j` of the envelope curve `W_j` (`N = d`) and `y = x̂ − X₀(d) ≥ 1`,

    min_{1 ≤ n_o ≤ d − d_min + 1} max_{𝔏_j} [(d − n_o)B + (1 − σ)·n_o·θ_na(y/n_o)]  ≤  d·M_{W_{j+1}, b_{j+1}}(y/d) + 1 + a·d_min.

`d ∈ {300, 10³, 3·10³, 10⁴}`, `j ∈ {0, 1, 2, 3, 5, 8, 12, 20}`, rates `y/d` from `0.03h` to `u` (so up to `x̂ ≈ u·d`, far
beyond `ε*`), `θ_na` from its definition: **240 cases, no violation; least slack `1.11` nats** (the
allowance is `1.22`; the left side equals `d·M_{W_{j+1}, b_{j+1}}` to `10⁻²` nats in 80 cases, where no
capping is active); the control with `W_{j+2}` fails in 33 cases.  This is check (C) of the
author's `z1_onelevel.py` re-done independently; it does not test the finite-`n` part of
Proposition Z3 (the level itself).

## 2. The paper proofs, statement by statement

Notation as in the addendum.  "By hand" means: I re-derived the step on paper before
running anything; the numerical confirmations are those of §1.

### 2.1 A1 — admissible sequences; Lemma A1, Lemma A2

**Lemma A1 — correct; one clause needs a word (repair below).**

*The step quoted from Proposition U.*  For a family `(W, b)` and `g > 0`:
`inf_{e>g} max_𝓔 Φ_g = max_𝓔 inf_{e>g} Φ_g ≤ sup{B − Σ(B, W(B))g : 0 ≤ B ≤ b, Σ(B, W(B)) < ∞}`.  I checked the
hypotheses of Sion's theorem (`𝓔` compact and convex because `W` is convex, continuous on
the closed interval and `≤ 1`; `Φ` affine in `(B, s)`; `{e : Φ ≤ c}` a sublevel set of a convex
function of `e` because `s ≤ 1`) and the three cases for `inf_{e>g} Φ = B − g·sup_{e>g} N(e)/e`,
`N = B − (1 − s)θ`: (a) a maximiser of `N/e` beyond `g`; (b) `N ≤ 0`; (c) `N/e` nonincreasing on `[g, ∞)`,
where the value `(1 − s)θ(g)` is `B″ − Σ(B″, s)g` for the intercept `B″ ≤ B` of the supporting line of
`(1 − s)θ` at `g`, and `(B″, s) ∈ 𝓔` because `W` is nondecreasing.  This part of the proof of
Proposition U indeed does not involve `T`.  The set over which the supremum is taken
is not empty (`B = 0`: `Σ(0, 0) = 0`).
*The two new points.*  (i) Every `B ≤ b_j` with `Σ(B, W_j(B)) < ∞` is `≤ b⁺(W_j, b_j) ≤ b_{j+1}`: a top
above `b⁺` is harmless, because beyond `b⁺` the image is `+∞` and no line of the supremum
lives there.  (ii) (S2) is used at exactly these `B`: on `[0, b_{j+1}]` is enough (on `(b⁺, b_{j+1}]`
it is void).  So `max_𝓔 inf_e Φ ≤ M_{W_{j+1}, b_{j+1}}(g)`, and an `e > g` within `η` of the infimum gives
`φ = g/e ∈ (0, 1)`.  The infimum need not be attained (`j = 0`: it is the limit `φ → 1`), which is
why the statement has "`+ η`" — and it is how Proposition Z3 uses it.
*The exponent-level clause* is Proposition U followed by the same two lines.
*Numerically:* §1.5.

*Repair (wording).*  "… hold for every admissible sequence with `b₀ ≤ a` over every base
family of flat type `b₀` …" needs **`W₀ ≡ 0`** (which Proposition Z1(1) has and the definition
of A1 does not), or "a base family of type `𝓗^∞(𝔏₀; E)`": a flat type `b₀` is the type of the grid
family of `W₀` only if `W₀` vanishes at the top.  Both sequences of the addendum have `W₀ ≡ 0`.
(What else §§4–6 of `Z_REPORT.md` use of the sequence: values in `[0, 1]`, monotone, `W_j(0) = 0`,
`0 < b_j ≤ a ≤ ln 2`, and a positive lower bound for the tops in the order of `A_T` — automatic:
by Corollary A4 and Lemma A3 every admissible sequence from a flat start has
`b_j ≥ min(b₀, h)`.  Lemma Z1a is stated for `B ≤ a`, so `b₀ = a` is allowed although the proof
of Proposition Z3 says "`< a`".)

**Lemma A2 — correct as stated.**  (`{B ≤ b : Σ(B, W(B)) < ∞} ⊂ {B ≤ c : Σ(B, V(B)) < ∞}`.)

### 2.2 A2 — Lemma A3

**Correct as stated.**  By hand: `b′ > 0`; `f` nondecreasing with `f(0) = 0` (`Σ(0, 0) = sup_e(−θ(e)/e) = 0`,
also if `θ(∞) > 0`); `0 ≤ env f ≤ f ≤ 1`; a nonnegative convex function vanishing at the left end
is nondecreasing; continuity at `0` and in the interior; the left limit at `b′` exists and
replacing the end value by it keeps convexity and gives continuity on the *closed*
interval; `W′ ≤ f ≤ Σ(·, W)` on `[0, b′]` including the end point.
*The right end.*  If `θ` has infinite slope at zero, `Σ(B, W(B)) → ∞` as `B ↑ b′` (lower
semicontinuity of `Σ`), so `f = 1` near `b′` and `W′(b′) = 1` whenever the cut is active.  If `θ` has
a finite slope at zero, `Σ(·, W(·))` is finite and continuous up to `b′ = ` the root of
`W(B) = 1 − B/a`, the end value is `min(1, Σ(b′, W(b′)))`, possibly below one — which is the
correction of referee A to remark (1) after Corollary U′, and the definition of A2
respects it.  Example by hand: `θ = (1 − 0.8e)₊`: `Σ(B, s) = 0.8B` on the regular region, `W₁(B) = 0.8B`,
`W₁(1) = 0.8`, `M_{W₁, 1} = θ`.
*The last claim* (`b′ ≥ min(b, h)`) uses `p_j(h) ≤ L < 1 − h/a`, i.e. consequence (ii) of (H1); under
(H0) alone it still holds (then `p_j(h) ≤ L₁ ≤ 1 − h/a`, and equality forces a finite slope at
zero, where the boundary is regular).

### 2.3 Corollary A4

**Correct as stated.**  Induction by hand; domains: `b_{j+1} = b⁺(W_j, b_j) ≤ b⁺(V_j, c_j) ≤ c_{j+1}`, so `V_{j+1}`
is defined on `[0, b_{j+1}]`, where it is a convex minorant of `f = min(1, Σ(·, W_j))` — at the end
point too, since (S2) for `V` holds on the closed interval `[0, c_{j+1}] ∋ b_{j+1}` (the proof says
"on `[0, b_{j+1})` … and at `b_{j+1}` by continuity", which is the same thing).  Numerically: §1.4.

### 2.4 A3 — Proposition A5

**Correct as stated** (under the standing (H0), (H1)).  `b₁ = a` in both cases of the slope at
zero; `W_{j+1} ≤ Σ(·, W_j) ≤ Σ(·, p_j) = p_{j+1}`; `b_j ≥ h` by Lemma A3 and induction; `b_j > h` by continuity
of `W_{j−1}` at `h` and `W_{j−1}(h) ≤ L < 1 − h/a`.  The strict inequality is where (H1) is needed:
for `θ = (1 − 0.8e)₊` (a corner of `J` at its maximum, `L = 1 − h/a`) the envelope sequence has
`b_j = h` for all `j ≥ 2`.

### 2.5 A4 — Proposition A6

**Correct as stated.**  By hand:
* `Σ(B, s) ≥ [B − (1 − s)θ(h)]/h = s + B/h − 1` — right (the rate `e = h`, `θ(h) = h`); numerically §1.2.
* The fixed-rate sequence is admissible: convex, nondecreasing, continuous, zero at
  zero; values at most `B(1/h − 1/a)/G_j ≤ 1` on `[0, c_{j+1}]` because `V_j ≤ 1 − B/a` there; (S1) from
  `Σ < ∞ ⇒ B ≤ (1 − s)a`; (S2) from the displayed bound and `G_j ≥ 1`.  (It is a hinge, §1.4.)
* Finitely many steps to `c⁎`: if `c_j > c⁎` for all `j`, then `G_j = c_{j+1}(1/h − 1/a) ↓ G_∞ ≥ 1` and
  `v_{j+1} = (v_j + κ)/G_j` at `B = c_∞`.  `G_∞ > 1`: `v_j → κ/(G_∞ − 1) > 1` (numerator minus denominator
  is `c_∞/a > 0`).  `G_∞ = 1`: `v_j → ∞` (if `v_j ≤ K` then `v_{j+1} − v_j ≥ (κ − (G_j − 1)K)/G_j → κ`; and once
  `G_j ≤ 1 + κ/K` the sequence cannot return below `K`).  Either contradicts
  `v_j = V_j(c_∞) ≤ 1 − c_∞/a`, which holds because `c_∞ ≤ c_{j+1}`.  (If `h > a/2` then `c⁎ > a` and `j₀ = 0`.)
* Afterwards `G_j = 1`, `V_{j₀+i} ≥ i(B/h − 1)` on `B ≥ h`, and every `B ≥ h` with `i(B/h − 1) ≤ 1 − B/a` has
  `B − h ≤ h(1 − h/a)/(i + h/a)`.
* `b_j ≤ c_j` by Corollary A4 (same start).
*On the remark* ("a second proof of `O(1/k)` for every pair with (H0)"): right — Lemma A3
(first part), Corollary A4, Lemma A1 and Proposition A8 use (H0) only, so
`τ_j ≤ b_j ≤ c_j ≤ h + h(1 − h/a)/(j − j₀ − 1 + h/a)`; but `j₀` is not explicit in this proof (the
a-priori bound of the theory report is), and "`b_j > h`" is not available without (H1).

### 2.6 A5, A6 — Propositions A7 and A8

**Proposition A8 — correct as stated.**  Base: for `x > 0` a supporting line of `θ` at `x` has
intercept `B_x ∈ [0, a]` and slope `−λ_x`, `λ_x ≥ Σ(B_x, 0)`; so `θ(x) ≤ B_x − Σ(B_x, 0)x ≤ B_x − W₁(B_x)x ≤ M_{W₁, a}(x)`
(`B_x = a` happens only if `θ` is affine near zero; then `B = a` belongs to the family and
"`0 ≤ B < a`" in the proof is a limit).  Step: Lemma A1 (the `T_k` are nonnegative and
nonincreasing).  Numerically: `j = 2` and `j = 3` on `R` itself (§1.5, §1.8); the step `j → j + 1` for
`j ∈ {0, 1, 2, 3, 5, 8, 12, 20, 40}` through the minimax identity (§1.5) — which with Lemma M
(machine-checked) is the step of the induction.  The inequality `τ_j ≤ b_j` is an equality
at `j = 2` and strict at `j = 3` (§1.8).

**Proposition A7 — correct as stated**, given Lemma RC, Lemma T and §8 of `R_REPORT.md`
(refereed there; not re-derived here).  *Is the cut sequence admissible in the sense of
A1?*  Yes: families by Lemma T(a) and the range condition (values in `[0, 1]` on `[0, b^cut_j]`),
(S1) with equality, (S2) by Lemma T(b); `W^cut_0 ≡ 0`.  *Direction of Corollary A4:* the
envelope sequence re-started at `k₁` (`b_{k₁} ≤ h + ε₁ = b^cut_0`, `W_{k₁} ≥ 0 = W^cut_0`) is the envelope
sequence of the corollary and the cut sequence is the admissible one: `b_{k₁+i} ≤ b^cut_i` —
right.  Then `(k₁ + i)²(b_{k₁+i} − h) ≤ ((k₁ + i)/i)²·i²(b^cut_i − h)`, and only `limsup i²(b^cut_i − h) ≤ c_*²` is
needed.  Lower bound: `b_j ≥ τ_j` (A8) and Theorem R.  Numerically: §1.3, §1.4.

### 2.7 A7 — Theorem Z′

**Correct as stated, conditionally** (on the statements `Z_REPORT.md` is conditional on, and
on Propositions Z3, Z4 and §6 of that report, which are another referee's subject; I
read them for what they use of the sequence — §2.1 — and did not referee their
bookkeeping of `Λ̄`).  The base is right: Theorem A of Q2 with `M = 0` is the chain on the
base bracket, flat type `a`, least accuracy `α^{(0)} ≤ 1`, error `A_T + E_𝔅 = O(ln n + ln(1/α))` (its
remark (2)); Proposition T needs `0 < B′ ≤ ln 2`, so `B′ = b₁ = a` is allowed.  `k` levels give the
top `b_k` (the first level turns the flat type into `W₁` with `b₁ = a`: no gain at `k = 1`, as the
text says).  `b_k − h ≤ C″/k²` and the limit are Propositions A6, A7.

**The sentence after the theorem is wrong as stated** — see §3, item 1.

### 2.8 A9 — Lemma A9, Lemma A10, Proposition A11, Theorem Z″

**Hypotheses.**  (H0), (H1), `θ(∞) = 0`, `J` differentiable on `(0, L)`: satisfied by the cube at
every slope (`J` analytic, `θ_na = 0` from `ε*` on) and by the Gaussian pair.  What is used of `J`:
concave, continuous on `[0, L]`, strictly increasing from `J(0) = θ(∞) = 0` to `h` (unique
maximiser), so `t₁(B)` exists for `0 ≤ B < h`, is continuous, increasing and tends to `L`; and
`Σ(B, t₁) = t₁` (by (Σ5): `D(B, s) ≤ 0` iff `J(s) ≥ B`, and `D(B, t₁) < 0` is impossible on the increasing
branch).  Differentiability is used only to name the subgradient; any supergradient
`e₁ − θ(e₁)` of `J` at `t₁`, `e₁` a minimiser of `(1 − t₁)θ(e) + t₁e` (one exists, and `e₁ ≥ h`, for `0 < t₁ < L`),
does the same.

**Lemma A9 — correct as stated.**  `e₁ := J + (1 − t₁)J′` is the minimiser, `θ(e₁) = J − t₁J′`, and
`[B − (1 − t₁)θ(e₁)]/e₁ = t₁ = Σ(B, t₁)`: so `e₁` attains the supremum and, evaluating the supremum
at `e₁`, `θ(e₁)/e₁` is a subgradient of `s ↦ Σ(B, s)` at `t₁`.  `κ = (J − t₁J′)/(J + (1 − t₁)J′) = 1 − J′/(B + (1 − t₁)J′)`.
Concavity: `J′(t₁) ≥ (h − B)/(L − t₁) ≥ η/L`.  `x ↦ x/(B + (1 − t₁)x)` increasing, `B ≤ h`, `1 − t₁ ≤ 1`:
`1 − κ ≥ η/(hL + η)`.  Monotone iteration below the fixed point.  (`B = 0`: trivial.)

**Lemma A10 — correct as stated.**  `H = Σ(·, W_{k−1}(·))` is convex, nondecreasing, finite and
continuous on `[0, b_k)`, `H(0) = 0`, `H(h) ≤ p_k(h) ≤ L`.  If `H > 1` somewhere on `[0, b_k]` it reaches one
at some `β < b_k` (if `H ≤ 1` on `[0, b_k)` then `H(b_k) ≤ 1` by lower semicontinuity).  The value at
`b_k` of the tangent line at `B` (right derivative) is nondecreasing in `B`; with
`B_t := sup{B ≤ β : that value ≤ 1}` there is a supporting line of `H` at `B_t` through `(b_k, 1)`
(at a kink: a subgradient between the one-sided derivatives), and "`H` on `[0, B_t]`, that
line on `[B_t, b_k]`" is convex, below `f`, and above every convex minorant of `f` (chord
argument on `[B_t, b_k]`): the description of the envelope is right.  Two things the
proof's wording does not say and the lemma does not need: at a kink "tangent" means
supporting line; and there may be *no* point with tangent value below one — then
`B_t = 0` and the envelope is the chord from the origin (this happens: Gaussian pair, `k = 1`,
`W₁(B) = B`).  Under the hypothesis, for `B ≤ h − η`: `H′(B+) ≤ (H(h) − H(B))/(h − B) ≤ L/η` and the
tangent value at `b_k` is `≤ H(h) + (L/η)(b_k − h) < 1`: so `B_t > h − η`.  The second claim: induction
with `W_{k(η)−1} ≥ 0 = p₀`, `b_k` nonincreasing.

**Proposition A11 — correct as stated.**  Left inequality: directly, `b_k > h` and
`W_k ≤ p_k ≤ t₁` on `[0, h)` give `M_{W_k, b_k}(g) ≥ sup_{B<h}[B − t₁(B)g] = θ_hint(g)`.  `m > 0` for every `g > 0`
(convexity and `θ_hint″(0) > 0`; also for `g ≥ ε*`, where `m = Lg − h`).  The two regions:
`B ≤ h − η`: `B − W_k(B)g ≤ B − t₁(B)g + gλ^i ≤ θ_hint(g) + gλ^i`; `h − η ≤ B ≤ b_k`: monotonicity of `W_k` and the
three thirds of `m`.  `k(η) ≤ k₁`.

**Theorem Z″ — correct as stated, conditionally (as Theorem Z′), for every fixed `g > 0`.**
*Does Proposition Z4 give the type at `x̂ = g·n`?*  Yes, as the propositions are stated:
Proposition Z3 is for all `x̂ ≥ 𝒳` with no upper limit (its proof uses `g = (x̂ − X₀)/d` only
through Proposition Z1(2), which is for every `g > 0`, and Lemma Z1a, whose constant does
not depend on `g`); the error functions `E⁺`, `Ê` do not depend on `x`; for `x ≥ 𝒳` the family `Ẑ`
is the level family.  Behind it: Lemma U of Q2 is stated for every rate `e ≥ 0` and every
threshold above `3(n_o + 1)e^{2u + e^u + n_o e}`, and Lemma 11.55(d) of the theory report for every
`e ≥ 0` (with `ρ_e` capped at `½`) — I read these statements, not their proofs.  The author's
exact one-level test covers targets up to `X₀ + u·d`.  `Z_REPORT.md` §0 says that Theorem Z
is "not a statement at extensive accuracies"; that is a statement about what was
analysed there (the tops only), not a restriction of Proposition Z3.
*The count:* `k = k₁ + ⌈ln(gn)/ln(1/λ_η)⌉ = O(ln n)`, `n·g·λ_η^{k−k₁} ≤ 1`, `k ≤ n^{1/2}` and `g·n ≥ 𝒳` for `n ≥ n₀(u, δ, g)`;
`k·c_Z·ln n = O((ln n)²)`.  Right.
*For which `g`?*  Every fixed `g > 0`; not uniformly (the constant of the proof is of order
`c_Z·hL/η ≈ 300·c_Z(h/g)²` at `u = 1`, §1.6; the true number of levels is `≈ ln n/ln(1/κ_g)`).  **For
`g ≥ ε*` the statement is true and empty:** `θ_hint(g) = 0`, and already `M_{W₁, a}(g) = 0` (§1.6), so the
theorem's own formula with `k = 1` gives `exp(O(ln n))` there (the non-adaptive exponent
`θ_na(g)` is zero from `ε*` on).  The theorem should be stated for `0 < g < ε*`, as Theorem
11.54 is.

## 3. Errors and slips, most serious first

None of them affects a numbered statement.

1. **A7, the paragraph after Theorem Z′: "by Corollary A4 the envelope schedule has the
   smaller `b_k` at every `k`" — wrong as stated.**  Corollary A4 compares sequences from
   the same start; here the starts differ (`a` against `h + ε₁`).  Counterexample: cube `u = 1`,
   `(s_t, ε₁) = (L + 0.05, 0.003)`: `b_k − h = 2.81h, 0.905h, 0.383h, 0.191h, 0.109h` at `k = 1, …, 5` against
   `b^cut_k − h = 0.103h` (§1.7).  *Repair:* "by Corollary A4, `b_{k₁+i} ≤ b^cut_i` for all `i`, `k₁` the first
   level with `b_{k₁} ≤ h + ε₁` (`k₁ = 6` at `u = 1`): `k₁ + i` envelope levels over the bracket do at
   least as well as `i` cut levels over the base of `M₁` epochs (43 levels)".  (At the same
   index the envelope top is the smaller one from `k = k₁` on in the cases computed; that
   is a numerical observation, not a consequence of A4.)
2. **A10, third item, and the sentence after the table of A6: `b_j = τ_j` is not an open
   question — it fails at `j = 3`.**  `τ₃ = 0.36118a < b₃ = 0.36330a` (cube `u = 1`; brute force on
   `R`, §1.8; the theory report's own `τ₃ = 0.361a`, and its `τ₄, τ₅, τ₆` likewise); Gaussian:
   `0.35523 < 5/14`.  Equality holds at `j = 2` (`b₂` is the closed form of `τ₂`).  *Repair:* say
   that the envelope sequence is the best *admissible* sequence (Corollary A4) — the
   best that Proposition U can give — and not the recursion: `τ₂ = b₂`, `τ_j < b_j` numerically
   for `j ≥ 3`, with the same constant `c_*²` in the limit (`R_REPORT.md` §8 already
   distinguishes the two: offsets `c ≈ 0.15`–`0.25` for the recursion, `c ≈ 0` for the majorant
   dynamics).  ("Within `0.1` per cent" at `j = 2` is the rounding of the quoted `τ₂ = 0.500a`.)
3. **A8, the sentence after the table: the factors "`3.5` at `10^{10}`, `7` at `10^{12}`, `21` at
   `10^{15}`" are against Theorem A of Q2, not against "every earlier bound".**  Against
   the cut-curve bound in the same table they are `1.15, 1.07, 1.05` (and `1.83, 1.47, 1.27` at
   `10⁷, 10⁸, 10⁹`).  *Repair:* name the bound compared with, or give both.
4. **A8: "`0.9958, 0.9968, 0.9973` at `k = 20, 40, 80`" — the last value is a grid artefact**
   (`0.9982` without a grid; the author's two grids give `0.9940` and `0.9973`).  The grid
   method errs *downwards* in the tops (the non-conservative side for an upper bound),
   by `10⁻⁷·a` at `k = 80` — immaterial in the table.  "Approached from below" is confirmed for
   the cube at `u = 1` to `k = 800` but is specific to the pair (Gaussian pair: from above),
   so the extrapolation `h + c_*²/k²` is an upper estimate only where that has been
   computed.  *Repair:* quote grid-free values, or say `0.998`.
5. **A9, after Theorem Z″: "The constant grows like `1/g`"** is the heuristic value; the
   constant *of the proof* grows like `1/g²` (`η ∝ g²`: `η = 1.7·10⁻³h` at `g = h`).  And at a fixed rate
   the decay is `κ_g^k`, `κ_g = 1 − g/(J(t_g) + (1 − t_g)g)`, which is `e^{−g/h}` only to first order in `g`
   (`0.364` against `0.368` at `g = h`; `0.116` against `0.135` at `g = 2h`).  *Repair:* state both.
6. **Lemma A1, the clause "Consequently …":** add `W₀ ≡ 0` (§2.1).
7. **Theorem Z″:** restrict to `0 < g < ε*`, or say that for `g ≥ ε*` it is empty (§2.8).
8. **Table of A6:** `b₄₀/a = 0.2630` (not `0.2631`: `0.263047` rounded twice).
9. **A8:** "about `37`–`50` times `ln n`" is `31`–`50` over the rows of the table (`31, 34` at `10⁴, 10^{4.5}`);
   "from `n ≈ 3·10⁴` on" is conservative (the formulas cross near `1.5·10⁴`).
10. **Wording of proofs:** Lemma A10 (supporting line at a kink; `B_t = 0`); Proposition A8
   (the supremum over `B < a` is a limit when `θ` is affine near zero); remark after A6
   (`j₀` not explicit; `b_j > h` needs (H1)).

## 4. What was not checked

* The finite-`n` statements that Theorems Z′ and Z″ are conditional on: Theorem 11.56,
  Lemma 11.55(d), Lemma U, Proposition T and Theorem A of Q2 — statements read (for the
  ranges of `e`, of the threshold and of `B′`), proofs not.  Propositions Z3, Z4 and §6 of
  `Z_REPORT.md` — read for what they use of the sequence and for their range in `x̂`; the
  bookkeeping of `Λ̄` and the orders were not re-derived (another referee's subject; I did
  not read `Z_REVIEW.md`).
* Lemma RC, Lemma T, Lemma PT, Theorem R of `R_REPORT.md` (used by A7): not re-derived; the
  cut chain was re-implemented and (S2) and the range condition checked numerically
  for the parameters used.
* Nothing is certified: floating point; no interval arithmetic.  The limit of A7 was
  followed to `j = 800` (cube `u = 1`), `400` (Gaussian), `200` (cube `u = 2, ½`).
* `R` itself by brute force only at the second and third level; `T₃` with an interpolated
  `T₂`.
* Pairs with a finite slope at zero: by hand only (`θ = (1 − 0.8e)₊`; `(1 − e)₊²`), no code.
* The Q2 formulas behind the table of A8 (`q2lib`): used, not re-derived.  The one-level
  test `z1_onelevel.py` (mode `env`) and the nests `z3_nest.py`: not re-run.
* Proposition S of `R_REPORT.md` (the profile): compared numerically only.
* No Lean file was opened; `lake` was not run.
* Sections A6a and A6b of the addendum (Propositions A12, A13, the certified tops,
  `z6_certified_tops.py`, `z7_exactness.py`, harness XVI.11) were added after the version
  reviewed: **not refereed** (§5 has three remarks on them, no verdict).

## 5. Postscript: the addendum changed while the review was in progress

At 21:50 I found `Z_ADDENDUM.md` modified (`git diff`, read-only): the ten items of §3 applied
in place, a note at its head describing this review, and two new sections, A6a
(Proposition A12, a table) and A6b (Proposition A13, certified tops), marked there as "not
seen by the referee".  That is accurate, and it stays accurate: **A6a and A6b are outside
the brief and I have not refereed them** (I read the two short proofs once and saw
nothing wrong; I did not open `z6_certified_tops.py` or the harness).  Three things only.

**5.1 The repairs as applied — two slips** (everything else I compared with §3 and found
faithful, including the numbers quoted from this report):

* A3, proof of Proposition A5, the new parenthesis "(`L < 1 − h/a` is (P2), which is where (H1)
  enters)": **(P2) is `p_j(h) ≤ L`**; `L < 1 − h/a` is consequence (ii) of (H1) in §1 of `R_REPORT.md`.
  Read: "(`L < 1 − h/a` is consequence (ii) of (H1) — the one place where (H1) enters)".
* A8, "`0.996, 0.998, 0.998` at `k = 20, 40, 80` without a grid (the referee …)": my values are
  `0.99584, 0.99690, 0.99819`, i.e. **`0.996, 0.997, 0.998`**.  (In the table of A6 the entry
  `0.996` at `j = 40` is likewise `0.997`.)

**5.2 `τ₃` in the new table of A6a is off in the fourth digit.**  The addendum now has
`τ₃ = 0.361296·a` (`z7_exactness.py`), "made here independently"; this report has `0.361184·a` (§1.8).
I recomputed it a second way (`ra07b_tau3_precise.py`): `τ₃ = a·τ₂/(a + x*)` with `x*` the first root of
`x + T₂(x) = τ₂`, `T₂` minimised at single rates with three levels of effort (stable to `10⁻⁷·a`):
`x* = 1.467642h`, **`τ₃ = 0.361184·a`** (Gaussian pair: `0.355233`), the same as before.  The cause of
the difference: `z7_exactness.py` takes the infimum over `φ` on a grid of step `10⁻³`, and the
function has a kink at the minimiser with one-sided slope `−τ₂ ≈ −0.5a`; its value is exactly
`(1 − 0.278)·τ₂ = 0.361296a`, the grid point next to the kink, whereas the infimum is at
`φ* = x*/(a + x*) = 0.27823`.  (The same grid gives its `τ(M_{W₂, b₂}) = 0.363303a` for what is
`b₃ = 0.363301a`.)  So `b₃ − τ₃ = 2.1·10⁻³·a`, not `2.0·10⁻³·a`.  Nothing depends on it.

**5.3 Two consistency checks that involve this report's numbers** (`ra09_postscript.py`).
* *The certified tops of A6b against my grid-free envelope tops.*  Corollary A4 requires
  `c_j ≥ b_j` for every admissible sequence from the same start.  For all 30 entries of the
  table of A6b (`u = 1`: `j = 2, …, 400`; `u = 2, ½`: `j = 2, …, 40`): `c_j ≥ b_j`, by `3·10⁻⁹·a` to `6·10⁻⁷·a`
  (`2·10⁻⁸` to `1.3·10⁻³` of `b_j − h`).  Two computations that share nothing sandwich the
  envelope tops to that accuracy; in particular the ratio at `k = 400`, `u = 1`, lies between
  `0.9996` (envelope, floating point) and `1.0009` (certified).
* *Proposition A12(b), (c), numerically:* `inf_x a(x + M_{W_j, b_j}(x))/(a + x) = b_{j+1}` to `10⁻¹⁵·a` for
  `j = 0, …, 12` (cube `u = 1`, Gaussian pair), and `M_{W₁, a} = max(θ, a − ·)` to `3·10⁻¹⁶·a` on 300 rates.
  Both agree with what I had found before these sections existed (`b₂ = τ₂` to rounding;
  `b₃ = a·b₂/(a + 1/m₂)` with `m₂` the slope of the tangent piece of `W₂`, while `τ₃ = a·τ₂/(a + x*)` with
  `x* = 0.356ε* > 1/m₂ = 0.349ε*`: the second level stays on the cap line `τ₂ − g` a little longer
  than its majorant does).
