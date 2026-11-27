# Internal review of `docs/workstreams/Z_REPORT.md` (Theorem Z: `ln N ≤ n·h + O(n^{1/3}(ln n)^{2/3})`)

*Independent adversarial referee (AI; **an internal review, not external peer review**), 2026-11-26.
Brief: `docs/workstreams/Z_review_brief.md`.  Scripts and outputs of this review: `experiments/workstreams/Z/review/`
(own exponent-level library `zrev.py`, own finite-`n` layer `zlev.py`; the exact one-level evaluator is that of the referee
of Q2, `experiments/workstreams/Q2/review/rlib.py`, imported read-only; nothing imported from the coordinator's
`zetalib`/`q2lib`/`qlib`, the coordinator's `R/rlib.py` only for one comparison).  No existing file was edited; `lake`, the
audit script and state-changing git commands were not run.  Resources, honestly: the scripts as stored peak at `31`–`111` MB
(measured), and every stored run is below five minutes (eight nest runs were stopped by their own time limit and are
reported as unfinished); **but two first versions broke the rules of the brief** — `z06_lipschitz.py` allocated about
`3.9` GB for a few seconds in each of three invocations (a dense distance matrix; found when I measured, replaced by a
sorted search), and a first version of `z01_sigma_chain.py` ran for about five and a half minutes before I stopped it.
No file I read asked me to change permissions, spending or scope.  The sections below are the review; the working notes W1–W6 after them are
the record of the checks in the order in which they were made.*

*Reviewed: `Z_REPORT.md` as committed in `d3b4b84` (file time 19:28).  While the review ran the coordinator added
`docs/workstreams/Z_ADDENDUM.md` (the "envelope sequence") and a mode `env` to `z1_onelevel.py`, `z2_formula.py`, `zetalib.py`.
**The addendum is outside the brief and is not reviewed here**; where a check of mine bears on it I say so.*

## 0. Summary of verdicts

**No error of substance was found.**  Every step of Propositions Z1, Z3, Z4, Lemmas Z1a, Z2 and of §6 was re-derived from
the statements it quotes, and each was attacked numerically with independent code at parameters the coordinator had not
used.  What I found is one illustrative constant that is about three per cent too small, one wrong order symbol that the
proof does not use, and wording.

| statement | verdict |
|---|---|
| **Proposition Z1** (1)–(3) (§2) | **correct as stated**; a faithful extraction from `R_REPORT.md` (Lemma T, Proposition C, Lemma RC, the proof of Proposition U, Corollary U′, §8) |
| Lemma Z1a (§2) | **correct as stated** (Lipschitz constant `max(B, (1−s)a − B) ≤ a`, also where `θ_na = 0` and for `φ` near 0 and 1) |
| **Lemma Z2** (§3) | **correct as stated**: the proof of Lemma U covers lines valid at all accuracies; the zero line is enough; the cap `Ξ = n_o·θ_na(e)` is admissible |
| **Proposition Z3** (§4) | **correct as stated** (admissibility, accuracy for every admissible `n_o` and every `u > 0`, the type for all `1 ≤ d ≤ N`, `x̂ ≥ 𝒳`, `δ`, `Λ`) |
| Proposition Z4 (§5) | **correct as stated** (the hypotheses of Proposition T are met; the type on `α ≤ x < 𝒳` is right; the term `j(d)·Δ_T` is right and vanishes where the error is unrolled) |
| **§6 and Theorem Z** | **correct as stated, given its quoted inputs** (Theorem 11.56 with rule (P), Lemma 11.55(d), Lemma U, Proposition T, Theorem A of Q2, `R_REPORT.md` §§5–8) — after the repairs of wording F2, F3 below, which change no inequality |
| §7, the table | **reproduced** from the formulas with own code (five rows, every digit printed); `z2_formula.py` is the formula of §6 |
| §7, "`c_Z ≈ 50` … the constant of the limsup `≈ 10.6`" | **wrong as a statement about the limsup; repair: `≈ 52` and `≈ 10.9`** (F1) |
| §8, remark 1 | labelled correctly as heuristic; **§0 quotes it without the label** and its supporting sentence has a gap (F4) |

**Findings, most serious first** (none changes a proposition or the theorem):

* **F1 (a number in §7/§0; minor).**  "`c_Z ≈ 50` at `u = 1`, and the constant of the limsup is `≈ 10.6`."  The per-level loss
  divided by `ln n` is `47.1 … 50.0` over the table and still increasing at `n = 10^{15}`.  By the report's own formulas
  (block `m·h ≈ (8 + γ)ln n`, `A_T ≈ ϖ₃ − m·h + P̄_M`, `ℓ₀ ≈ (4 + γ)ln n`, with `Λ̄ = n^{1+γ+o(1)}`, `γ = ln k/ln n`) its limit is
  `(8+γ)(a/h − 1) + u√((8+γ)/(2h)) + 4/(3p_u) + (5+γ) + 1 + (4+γ) + 1`: **`52.0`** for `k ≍ n^{1/3}` and `52.9` for `k = n^{1/2}`
  (numerically `51.0 … 51.4` at `n = 10^{10} … 10^{50}` with the largest `Λ̄` of the proof; `z05_formula.py`).  So a constant `c_Z`
  for which §6 proves the inequality "for all `n ≥ n₀`, `1 ≤ k ≤ n^{1/2}`", as the theorem asks, is at least `52.9`, and the limsup that the proof gives
  is `(3/2)(2c_*²)^{1/3}·52.0^{2/3} = 10.9` (`11.0` with the `c_Z` of the theorem as stated), not `10.6`.  *Repair:* "`c_Z ≈ 50` in the
  range of the table; `52` in the limit; the bound reads `n·h + 10.9·n^{1/3}(ln n)^{2/3}`".
* **F2 (an order symbol; wording).**  §1: "`q(n, Λ)` … `O(ln n + ln ln Λ)`" and §6: "a level adds `q(n, Λ̄) = O(ln n + ln ln Λ̄)`".
  `q(n, Λ) = ln(4(n+1)) + ln A_n + c₂₄ + ln K̄(n, Λ)` with `K̄` *linear* in `Λ`: `q = 2 ln n + ln(Λ + ln n) + O(1)`, i.e.
  `O(ln n + ln Λ)`.  The proof uses only `q(n, Λ̂) = O(ln n)` for `Λ̂ ≤ n²`, which is true.  *Repair:* write `ln Λ`.
* **F3 (the statement of Theorem Z; wording).**  "There are `n₀` and a constant `c_Z = c_Z(u)` such that …": `C′` and `C″` are
  not quantified, and `n₀` depends on `δ` (§6 says `n₀(u, δ)`).  It should read: *there are `n₀ = n₀(u, δ)` and constants
  `c_Z, C′, C″` depending on `u` only*.  And none of `n₀`, `C″`, `M₁` (hence `C′`) is effective: they come from the `ε₁` of
  Lemma RC, the restart level `k₁` and the unquantified `o(1)` of the rate theorem.  §7 caveat (i) says this for the
  table; §0 or §9 should say it for the theorem.
* **F4 (the barrier; label).**  §0: "… this nested family — for which `n·h + Ω(n^{1/3})` is a barrier of the analysis (§8)" is
  stated as a fact; §8.1 is labelled "a heuristic remark", correctly.  Of its three ingredients, "`β_k ≥ τ_{k₁+k} − h`" is a
  theorem for every chain of convex sub-solutions (Corollary U′), but "a level of Algorithm 2L⁺ multiplies the certified cost
  by at least a constant, so no schedule … gives `o(n^{1/3})`" is not an argument as it stands: the chains of §5 consist of
  `≈ n/m` levels and cost `A_T` *once* in the type bookkeeping.  The inference needs "every level that lowers the exponent
  loses an additive constant against its type", which is plausible and unproved.  *Repair:* "heuristically" in §0.
* **F5 (wording, §1).**  "`Σ(B, s)` … finite iff `B < (1 − s)a` or the supremum is attained on the boundary": for the cube
  (infinite slope of `θ_na` at zero) `Σ(B, s) < ∞` iff `B < (1 − s)a` (or `B = 0`); `R_REPORT.md` (Σ2), (Σ3) has it right.
* **F6 (wording, proof of Lemma Z2 (iii)).**  "the zero line has `0 ≤ 0`": the inequality needed is `σ_i·G ≤ n_i·B_i + E₁`,
  i.e. `0 ≤ E₁`.
* **F7 (numbers, §7).**  "the level term is about `6.5·ln n`": the table gives `6.3` (at `10⁷`) to `5.7` (at `10^{15}`); the
  chain term is `41.6` to `44.3` ("about `43`": fine).

**Remarks that are not errors** (details in §7): R1 — Proposition Z3 has a full nat to spare in the accuracy (the `2` in
`X₀(d)` could be `1.23`).  R2 — the illustration of §7 is far from the best choice of `(s_t, ε₁)`: with `(L + 0.10, h + 0.012)` the
range condition holds at all 70 levels computed, the base needs 6 epochs instead of 10, and the formula of §6 gives
`9.4·10³, 1.87·10⁴, 3.93·10⁴, 8.58·10⁴` at `n = 10⁶ … 10⁹` instead of `1.15·10⁴, 2.52·10⁴, 4.91·10⁴, 9.97·10⁴` — below Theorem A of Q2
already at `10⁶`; so "from `n ≈ 10⁷` on" is a statement about the parameters, not about the method (the coordinator's
addendum, not reviewed, goes further in this direction).  R3 — for the first levels of the chain `b_j = b₀` (`j ≤ 5` at
`u = 1`): the rows `k = 1` of the table are the edge of the search range, as the report says ("nothing is gained").

## 1. Proposition Z1 and Lemma Z1a (§2)

**Z1(2) — the question of the brief.**  Yes: the proof of Proposition U gives
`inf_{e>g} max_{𝓔(W,b)} Φ_g = max_𝓔 inf_{e>g} Φ_g ≤ sup{B − Σ(B, W(B))·g : 0 ≤ B ≤ b, Σ(B, W(B)) < ∞}` **without any `T`**.  In that proof
the function `T` enters in the first line only (Lemma M: `R[T](g) ≤ inf_{e>g} F(e)`); everything after it is a statement
about `F(e) = max_𝓔 Φ_g(e; ·)`.  I re-derived it: `𝓔` is compact and convex (this is where `W` convex with values in `[0, 1]`
is used); `Φ_g` is affine in `(B, s)` and quasi-convex and continuous in `e` on `(g, ∞)`
(`{Φ ≤ c} = {g(1−s)θ(e) + (B−c)e − gB ≤ 0}`) — also at rates with `θ(e) = 0`, which Lemma M treats separately but Sion does not
need to; the three cases for `inf_{e>g} Φ = B − g·sup_{e>g} N(e)/e` are complete (quasi-concavity of `N(e)/e`, `N(e)/e → 0`); in
case (c) `B″ = (1−s)θ(g) + λg ≤ B`, `Σ(B″, s) = λ < ∞` and `(B″, s) ∈ 𝓔` because `W` is nondecreasing — also when
`B > (1−s)a` (a line that the level "drops").  Corollary U′ then turns the right side into `M_{W_{j+1}, b_{j+1}}(g)`: every `B` in
the supremum is `≤ b_{j+1}` by the definition of `b_{j+1}`, and `W_{j+1} ≤ Σ(·, W_j(·))` on `[0, b₀]` is Lemma T(b).  The infimum over
`e` need not be attained (it is not for `g ≥ ε*`), which is why (2) is stated with `η`: correct.

**The hypotheses of Proposition U for `W_j` on `[0, b_j]`.**  Convex, nondecreasing, continuous, `W_j(0) = 0`: Lemma T(a).
Values in `[0, 1]`: this is the range condition `W_j(b_j) ≤ 1`, and it is guaranteed **for all `j`** by Lemma RC for every
`b₀ ∈ (h, h + ε₁]` — for *some* `ε₁ > 0` that the proof does not quantify (I re-read its proof: cases (α), (β), the ratio of
consecutive slopes, the uniformity in `j`; no gap).  Z1 takes `b₀ = h + ε₁`: fine.  `b_{j+1} ≥ min(b_j, B_t(j)) > h`: right.

**Z1(3).**  §8 of `R_REPORT.md` is indeed for a fixed cut level `s_t` and a fixed restart height `b₀`:
`b_{j+1} ≤ E_j ≤ B_t(j) + (1−s_t)/m_j`, `j²δ_t(j) → c_*²` (Lemma PT for the same `s_t`), `1/m_j = o(δ_t(j))`; and `b_j ≥ τ_{k₁+j}`
(Proposition C) with `k₁` fixed gives the liminf.  `sup_{j≥1} j²(b_j − h) < ∞` follows.

**Lemma Z1a.**  The one-sided derivatives of `φθ(g/φ)` are `θ(e) − eθ′(e±)` at `e = g/φ`, the intercept at zero of a
tangent line, in `[θ(e), a]`; so the slopes of `Ψ_g` lie in `[−B, (1−s)a − B] ⊂ [−a, a]`.  Where `θ_na` vanishes (`e ≥ ε*`) the
perspective term is flat; nothing special happens at `φ → 0` (`e → ∞`) or `φ → 1`.  Numerically (`z06_lipschitz.py`):
1.8 million random `(g, φ, φ′, B, s)`, `u ∈ {¼, ½, 1, 2, 4}`, rates `g` from `10⁻⁷` to `3u`, half of the `φ` log-uniform towards 0 or
towards 1 (down to `10⁻⁹`), many with `B = a`, `B = 0`, `s = 0`: the largest difference quotient is `1.000000·a` (pairs closer than
`10⁻⁷` are left out: there the quotient is rounding noise); midpoint convexity holds to `2·10⁻¹³`.

**Numerically** (W2, W3, W5): the slope map by direct maximisation, the chain from the definitions (the coordinator's
numbers reproduced to seven digits), and Z1(2) with two-sided brackets on 4 940 cases of the chain (five chains, three
slopes, levels up to 30) and 11 340 adversarial cases: no violation; (2) holds with **equality** to the width of the
brackets (`≤ 2·10⁻⁷`) where the orbit part of the curve is active; the identity fails for non-convex or decreasing `W`.

## 2. Lemma Z2 (§3)

**Correct as stated.**  I compared with the proof of Lemma U (`Q2_REPORT.md` §2), read for the type `𝓗_N^∞`:
parts (a)–(c) do not involve the type.  In (d): rungs with `x_{l−1} ≤ x_l + 1` (all `l ≥ 2`; `l = 1` when the cap
`⌈2un_i⌉ − 1` is active) use the auxiliary inequality at `y = x_l` — no range; the first rung otherwise has
`x₁ = max(⌈Ξ⌉, 1) ≥ Ξ ≥ G`, so `−σx₁ ≤ −σG` — needs only `Ξ ≥ n_oϑ ≥ G`; the outer sample needs one line with
`σ_iG ≤ n_iB_i + E₁`.  **The zero line is enough** (it gives `0 ≤ E₁`), and it is needed: without a nonnegative line (U)
fails (negative control of `Q2_REVIEW.md`).  **The cap `Ξ = n_o·θ_na(e)` is admissible**: Lemma U asks `n_oϑ ≤ Ξ ≤ n`, and
`ϑ ≤ a < 1`; at rates `e ≥ ε*` it gives the one-rung ladder `x₁ = 1`.  This agrees with `Q2_REVIEW.md` §1.4 and note N2.
`B_i = 0` (excluded by (C3), which has `B_i > 0`) is harmless: the proof never divides by `B_i`.  The level is the level of
Lemma U with `b = 1`, the least threshold allowed, and needs `x_min ≤ 1`, which the statement has.
Numerically: (U∞) at about 200 000 levels of §4 (W4, `z10_horizon.py`) and, with the `δ′`-inequality, at every level of the nests (W6): no violation;
least slack `3.8` nats (at `d = 3`), so the lemma is sharp to `O(1)`.

## 3. Proposition Z3 (§4)

**Correct as stated.**  Point by point (the list of the brief):

* *Design and admissibility.*  `n_o ≤ d − d_min + 1` gives `n_i ≥ ⌊1/(2u)⌋ + 1 > 1/(2u)` and `1 ≤ n_o ≤ d − 1`, `d > d_min ≥ 2`:
  the hypotheses of Lemma Z2, hence (H1)–(H9) of Theorem 11.56, hold for every admissible `n_o`.
* *Accuracy.*  `ln[(2p_u)^d + e(c₃ + θ)] ≤ 1 + ln θ + (c₃+1)/θ`, `ln θ = ln(3(n_o+1)) + 2u + e^u + y`, `θ ≥ 6e²`: the accuracy is at most
  `x̂ − (1 − 0.23) − ln((d+1)/(n_o+1))` — **for every admissible `n_o` and every `u > 0`** (only `e^u ≥ 1`, `y ≥ 1`, `2p_u < 1` are used).
  Measured: `x̂ − x_out ≥ 1.0000` at all 96 742 levels (remark R1).
* *Rounding.*  The admissible fractions are `i/d`, `1 ≤ i ≤ d − d_min + 1`; for any `φ* ∈ (0, 1)` — however close to 0 or 1 —
  one of them is within `max(1, d_min − 1)/d ≤ d_min/d` (checked on a grid in `z06_lipschitz.py`: ratio exactly one in the
  worst case).  Lemma Z1a applies on `(0, 1]` to all `(B, s) ∈ 𝓔(W_j, b_j)` because `b_j ≤ b₀ < a`.
* *`𝔏_j ⊂ 𝓔(W_j, b_j)`*, the grid error (4.1) (uses that `W_{j+1}` is nondecreasing), the shift by `X₀(d)` (uses
  `0 ≤ W_{j+1} ≤ 1`, i.e. the range condition again), and `d/N + 1 + a·d_min ≤ 2 + d_min ln 2`: right.
* *Small `d`.*  `d ≤ d_min`: enumeration, `d ln 2 ≤ d_min ln 2 ≤ E⁺`.  `d = d_min + 1, …`: the level exists with `n_o ∈ {1, 2, …}`;
  tested from `d = d_min + 1` on (a third of the cases within 40 of `d_min`).
* *Error function.*  `E⁺` is nonnegative, nondecreasing in `d` and `Λ` (`ℓ₀`, `q`, `X₀` are) and constant in `x`.
* *What is needed of `𝔉` beyond its type:* that it is a family up to `N` (all dimensions `1 ≤ d′ ≤ N`) with least accuracy
  `≤ 1`; nothing else — the design uses the lines, and `C_max` is monotone in the inner bounds.

Numerically (W4, W5; own chain, the evaluator of the referee of Q2): 15 748 random cases / 96 742 levels evaluated
exactly, `u ∈ {¼, ½, 1, 2, 4}`, `d` from `d_min + 1` to `20 000`, horizons up to `10d`, `δ` down to `e^{−30d}`, levels `j ≤ 20`, targets
from `𝒳` exactly to `𝒳 + 10d`, four inner error functions, a second chain with slopes up to `0.94`: **no violation**;
least slack of the type `15.6` nats, of the exponent-level step `1.1`.  A further 1 672 cases at horizons far above the
dimension (`N = 100d … 3000d`, `d ≤ d_min + 120`), with **every** admissible `n_o` evaluated exactly (103 211 levels;
`z10_horizon.py`): no violation; there the `n_o` of the proxy costs at most `0.8` nats more than the `n_o` with the least
certified bound.  The coordinator's §7.1 rows are reproduced to the two decimals printed (`z07_crosscheck.py`).

## 4. Proposition Z4 (§5)

**Correct as stated.**  `Z[𝔉]` has the flat type `𝓗_N(b_{j+1}, 0, ∞; E⁺)` (`B ≤ b_{j+1}`, `σ ≥ 0`, `x ≥ 0`), `0 < b_{j+1} ≤ b₀ < a < ln 2`, least
accuracy `𝒳 = X₀(N) + 1 > 1`: the hypotheses of Proposition T.  The chain asks `Z[𝔉]` only for the accuracy `𝒳` in dimensions
`d − m ≥ ⌊𝒳/(2u)⌋ + 1`, where `y = 𝒳 − X₀(d − m) ≥ 1`: defined.  For `α ≤ x < 𝒳` the top line gives
`d·b_{j+1} ≤ max_{𝔏_{j+1}}[dB − σx] + 𝒳` (`W_{j+1}(b_{j+1}) ≤ 1`), so the chain obeys the type with `Ê` (the `+1` is spare); for `x ≥ 𝒳`,
`E⁺(d, x; Λ) ≤ Ê(d, x; Λ)` because `Λ* ≥ Λ`.  `Ê` is constant in `x` and nondecreasing in `d`, `Λ` (Proposition T(iii)).
The term `j(d)·Δ_T(d, Λ*)` is what Proposition T(iii) gives for an arbitrary block; it vanishes at `(n, Λ̄)` when the block
satisfies (4.1) of Q2 at an entry value `≥` the actual one (monotonicity of `P̄_cnt` in `Λ`), which is how §6 uses it.
Numerically (W6): the type of Proposition Z4 and Proposition T(iii) at every chain node of the nests, with blocks of the
design and with blocks divided by 4 and 6 (`Δ_T > 0`, up to 45 chain levels): no violation — but with a least slack of
`225` nats: `A_T` is loose, so this is a structural check, not a sharp one.

## 5. §6: the schedule and Theorem Z

**Correct as stated given its inputs** (with F2, F3).

* *Base.*  Theorem A's family `𝔊_{M₁}` with top accuracy `α^{(M₁)} = 1` is, by the claim in its proof, a family up to `n` of flat
  type `𝓗_n(B_{M₁}, 0, ∞; ·)` with least accuracy one; since `𝔏₀` contains `(b₀, 0)` and `(0, 0)` and `B_{M₁} ≤ b₀`, it has the type
  `𝓗_n^∞(𝔏₀; 𝓔′)`.  "`𝓔′_{M₁}(n; Λ̄)`" must be read as (A.1) *started at the final `Λ̄` of the unrolling*, with the blocks of the
  base's chains fixed by (4.1) at these values — this is what the text says and what `z2_formula.py` does.
* *Unrolling.*  Every error function is evaluated at `d = n` only (each proposition passes `E(d, ·)` at the same `d`); the
  chain is entered with `Λ̄`, its block is chosen there, `Δ_T = 0`, `Λ* ≤ Λ̄ + j(n)q_T(n, Λ̄ + n·b_j)`; only monotonicity in `Λ` is
  used.  The blocks are determined top-down; no circularity.  Right.
* *Growth of `Λ̄`.*  There are `k + k_{M₁} − 1` increments `q(n, Λ̄) ≤ q(n, Λ̂)` and `k + M₁ + 1` chains, each adding less than `n·a`:
  `Λ̄ ≤ Λ̄₀ + (k + k_{M₁})q(n, Λ̂) + (k + M₁ + 1)·n·a ≤ (k + M₁ + 3)Λ̄₀ ≤ Λ̂` by induction, provided `(k + k_{M₁})q(n, Λ̂) ≤ Λ̄₀`; for
  `k ≤ n^{1/2}`, `Λ̂ = O(n^{3/2})`, `q(n, Λ̂) = O(ln n)` and the left side is `O(√n·ln n)`: "`k ≤ n^{1/2}`" is enough, with `n₀(u, δ)`.
  (`Λ̂` dominates with much room: in the unrolling `Λ̄_final = 4.6·Λ̄₀` at `k = 121`, against `135·Λ̄₀`.)
* *Orders.*  `ℓ₀(n, Λ̂) ≤ 5 ln n + O(1)`; `A_T(n, Λ̄) ≤ ℓ_T(n, Λ̂; b_j, 𝒳, α)` needs `Λ̄_in + n·b_j ≤ Λ̂`, which the count above gives for
  every chain; `ℓ_T` is decreasing in `B′ ≥ h`, so `c_Z` depends on `u` only; `𝓔′_{M₁} = O(ln n)` with `M₁`, `k_{M₁}` fixed.
* *`ε`* enters through the top chain only (`α = ε̂` at `j = k`; every other chain and the base have `α = 1`); what the top
  chain adds to `Λ̄` is `< n·a` whatever `ε`; so `n₀`, `c_Z`, `C′` do not depend on `ε` or `k`.
* *Choice of `k` and the limsup.*  `k = ⌈(n/ln n)^{1/3}⌉ ≤ n^{1/2}`; with `A = (1+η)c_*²`, `k ≈ (2An/(c_Z ln n))^{1/3}`:
  `An/k² + k·c_Z ln n = (2^{−2/3} + 2^{1/3})A^{1/3}c_Z^{2/3}n^{1/3}(ln n)^{2/3} = (3/2)(2A)^{1/3}c_Z^{2/3}n^{1/3}(ln n)^{2/3}`: right.

## 6. Numerical replication (own code; all in `experiments/workstreams/Z/review/`)

| script → output | what | result |
|---|---|---|
| `zrev.py`, `z01_sigma_chain.py` → `out_z01_sigma_chain.txt` | (i) `Σ` by direct maximisation (900 points, three slopes) against a first-order solver, a brute-force grid and the coordinator's `rlib`; the chain `(W_j, b_j)` from the definitions, `j ≤ 62`; Lemma T(b) | agree to `7·10⁻¹¹`; the coordinator's `B_t(j)`, `m_j`, `E_j`, `b_j` to seven digits; range condition holds |
| `z02_minimax.py` → `out_z02_minimax_{A0,A12,A34,B,C}.txt` | (ii) Z1(2) and the minimax identity with two-sided brackets: 4 940 cases on five chains; 11 340 adversarial cases (630 convex curves, `W′ = min(1, Σ(·, W))`); controls | no violation; equality within `2·10⁻⁷`; controls fail as they must |
| `z06_lipschitz.py` → `out_z06_lipschitz.txt` | Lemma Z1a (1.8 million points); the rounding step of Z3 | constant `1.000000·a`; rounding exact |
| `zlev.py`, `z03_onelevel.py` → `out_z03_onelevel_u{0.25,0.5,1,2,4}.txt`, `…_u1_st015.txt`; `z10_horizon.py` → `out_z10_horizon.txt` | (iii) Lemma Z2 and Proposition Z3 on exact levels: 15 748 + 1 672 cases, 96 742 + 103 211 levels | no violation; least slacks: (U∞) `3.8`, `δ′` `2.2`, exponent step `1.1`, type `15.6`, accuracy `1.0000` |
| `z07_crosscheck.py` → `out_z07_crosscheck.txt` | nine rows of the coordinator's §7.1 table with own chain and another evaluator | reproduced to the two decimals printed |
| `z04_nest.py` → `out_z04_nest_{A…Q}.txt` | (iv) nests of two to seven levels of §4, each followed by the chain of §5, over saturating bases (flat `b₀`; sloped), exact, every node checked | **about 5.26 million node checks, no violation**; nine runs finished (largest: flat base, `u = 2`, `n = 3000`, five levels, 734 663 checks: exact `n·b₅ + 1 065` against `n·b₅ + 2 677`), eight stopped at the time limit |
| `z05_formula.py` → `out_z05_formula.txt` | (v) the formula of §6 from the text: rows `10⁵, 10⁷, 10⁸, 10⁹, 10^{10}` of the table; the per-level loss for large `n` | every digit reproduced; limit of the per-level loss `52.0·ln n` (F1) |
| `z08_range.py`, `z09_parameters.py` → `out_z08_range.txt`, `out_z09_parameters.txt` | range condition to level 320; the illustration with other `(s_t, ε₁)` | holds; remark R2 |

## 7. What the report says it is not (§0, §7 caveats, §8, §9); remarks

**Complete?**  Nearly.  §0, the caveats of §7 and §9 say what matters: not the true order; not extensive accuracies; a
formula, no algorithm run; (T) used in a regime no simulation covers; no machine check; Lemma U read beyond its stated
convention.  Missing or too strong:

1. *Effectiveness* (F3): Theorem Z is an asymptotic statement with constants `n₀`, `C′`, `C″` that the proofs do not
   produce (they hang on `ε₁` of Lemma RC, on `k₁`, and on the rate in `k²β_k → c_*²`).  For a given `k` the range condition is a
   finite check (`j ≤ k`), so a certified `β_k` for the illustrative chain is within reach of interval arithmetic; it has not
   been done, and §9 should list it.  (By my code it holds for all `j ≤ 320` at `(L + 0.05, h + 0.003)`; the rows `10^{12}`,
   `10^{15}` of the table use `k = 484` and `4510`: `b_j` extrapolated beyond level 160 and, for `k = 4510`, a range condition
   that nobody has computed beyond level 600; caveat (i) says so.)
2. *The barrier* (F4): §0 should carry the word "heuristic".
3. *The constant* (F1): `10.6` is the value at `n = 10^{15}`, not the limsup.
4. The table's crossovers ("below the non-adaptive cost from `10⁵` on, below Theorem A from `10⁷` on") are properties of the
   illustrative parameters (remark R2), which the text could say.

**Is remark 1 of §8 labelled correctly?**  Yes ("a heuristic remark"), and it should stay so: see F4.

**Remarks.**

* **R1.**  In Proposition Z3 every level is at least one nat more accurate than its target (`x̂ − x_out ≥ 1.0000` at all
  levels tested; the minimum is at `n_o = d − 1`, large `d`): `X₀(d) := 1 + (c₃+1)/(6e²) + ln(3(d+1)) + 2u + e^u` would do
  (`(c₃+1)/(6e²) = 0.23`).  Worth three quarters of a nat per level.
* **R2.**  `z09_parameters.py`: the formula of §6 at `u = 1` for other chain parameters for which the range condition holds
  at all 70 levels computed.  `(s_t − L, b₀ − h) = (0.05, 0.003)` [the report's]: `M₁ = 10`; `1.146·10⁴, 2.521·10⁴, 4.909·10⁴, 9.961·10⁴`
  at `n = 10⁶, …, 10⁹`.  `(0.15, 0.003)`: `j²(b_j − h)/c_*² = 0.957 … 0.999` for `10 ≤ j ≤ 160` (against `1.17 … 1.53`); `2.31·10⁴` at `10⁷`.
  `(0.10, 0.012)`: `M₁ = 6` (17 base levels instead of 43); `9.42·10³, 1.87·10⁴, 3.93·10⁴, 8.58·10⁴` — below Theorem A of Q2
  (`1.06·10⁴` at `10⁶`) one decade earlier.  With `(0.05, 0.02)` and with `(0.20, 0.003)` the range condition **fails** at an early
  level (`1.04`, `1.01`): the restart near `h` is needed, as `R_REPORT.md` says.  Nothing here is certified.
* **R3.**  With the report's parameters `b_j = b₀` for `j ≤ 5`: the first five levels gain nothing (they turn the flat family
  into a sloped one), so for `k ≤ 5` the bound of Theorem Z is worse than that of its own base; the table's `k = 1` at
  `n ≤ 10⁶` is the edge of the search range.  The report says "nothing is gained" there; fine.
* **R4.**  What the nests show about the mechanism: with a flat base and up to four levels every inner call is at an
  accuracy below `𝒳` (outer blocks of a few sites) and is served by a chain; from the fifth level on, or above a sloped
  base, the outer blocks are extensive (`n_o = 502` at `d = 1861`) and inner calls at accuracies up to `64 > 𝒳 ≈ 23.5` go to the
  levels `Z_j`.  The exact cost of a finished nest is `52`–`75` per cent of the unrolled error term (blocks of the design).
* **R5 (on the addendum, not reviewed).**  Its Lemma A1 needs of a sequence exactly what Z1(2) uses; my adversarial test
  (ii)B — `inf_φ max_{𝓔(W,b)} Ψ_g ≤ M_{W′,b′}(g)` for `W′ = min(1, Σ(·, W(·)))` on 630 convex curves — is a numerical test of
  that statement for the uncapped-then-capped image (the convex envelope of `W′` only enlarges `M`).  I did not check
  anything else of the addendum.

## 8. What was not checked

* **Theorem 11.56 itself** (the algorithm, its events, the abort rule (P)), Lemma 11.55, Proposition 11.57(a): taken as
  quoted.  My numerics evaluate certified bounds `C_max` from the formulas; **no run of any algorithm was simulated**.
* Of `Q2_REPORT.md`: I re-read the proofs of Lemma U and Proposition T against their use here and relied on
  `Q2_REVIEW.md` for the rest (Q1–Q5, Proposition A′, Theorem A as a theorem).  **Theorem A's family as the base of the nest**
  was not evaluated: my nests stand on saturating bases (the brief's item (iv)).  So the full design of §6 — 43 base
  levels at `u = 1`, then `k` levels and chains — was not evaluated by me, and the report evaluates no nest (its caveat (ii));
  the nest scripts that the coordinator wrote during this review are not reviewed.
* Of `R_REPORT.md`: the proof of Proposition U re-derived; Lemmas T, RC, Proposition C, §8 re-read; Lemma PT, (Σ6) and
  the lower bound not re-derived (two referees did).  The range condition "for all `j`" rests on Lemma RC; numerically
  I have it for `j ≤ 320` only, in floating point.
* The constants `n₀`, `C′`, `C″` (not explicit in the report); the rows `10^{12}`, `10^{15}` of the table (extrapolated `b_j`);
  the columns "Theorem 11.58a" and "Theorem A of Q2" (the latter was reproduced by the referee of Q2).
* Nests beyond `n = 10⁵` and beyond seven levels; slopes outside `u ∈ [¼, 4]`; the unfinished nest runs are incomplete
  evaluations (all nodes reached were checked).
* `Z_ADDENDUM.md` and the `env` mode of the coordinator's scripts (written during this review; outside the brief).
* Floating point throughout; the two-sided brackets of (ii) are rigorous up to rounding only.

---

# Working notes (appended as the review proceeds; the verdicts of §0 are final, these notes are the record)

## W1. First pass on paper (before any code) — what was read and re-derived

Read in full: `Z_REPORT.md`; `R_REPORT.md` §§0–8; `Q2_REPORT.md` §§1, 2, 4, 5; `Q2_REVIEW.md`; theory report
Lemma 11.55 and Theorem 11.56 (lines 5505–5630).

* **Z1(2), re-derived from the proof of Proposition U.**  `F(e) = max_𝓔 Φ_g(e; ·)`; Sion (𝓔 compact convex because `W_j` is convex
  with values in `[0,1]` on `[0, b_j]`; `Φ` affine in `(B, s)`; quasi-convex and continuous in `e` on `(g, ∞)` because
  `{Φ ≤ c} = {g(1−s)θ(e) + (B−c)e − gB ≤ 0}`); the three cases for `inf_{e>g} Φ = B − g·sup_{e>g} N(e)/e` re-derived
  (case (c): `λ = −[(1−s)θ]′(g+)`, `B″ = (1−s)θ(g) + λg ≤ B`, `Σ(B″, s) = λ`, `(B″, s) ∈ 𝓔` because `W` is nondecreasing).
  The function `T` enters Proposition U only through Lemma M (`R[T](g) ≤ inf_{e>g} F(e)`); the inequality
  `inf_{e>g} F(e) ≤ sup{B − Σ(B, W(B))g : Σ(B, W(B)) < ∞}` is free of `T`.  **First-pass: (2) is a faithful extraction.**
* **Z1(1), (3):** follow from Lemma T(a), Lemma RC (range condition for all `j`, for `b₀ ∈ (h, h+ε₁]`), (P2), and §8 (fixed `s_t`, `b₀`).
  `b_{j+1} ≥ min(b_j, B_t(j)) > h`.  For (3): `b_{j+1} ≤ E_j ≤ B_t(j) + (1−s_t)/m_j`, `j²δ_t(j) → c_*²`, `1/m_j = o(δ_t(j))`;
  `b_j ≥ τ_{k₁+j}` (Proposition C) with `k₁` fixed.  ok.
* **Z1a:** derivative of `φθ(g/φ)` in `φ` is `θ(e) − eθ′(e±) ∈ [θ(e), a] ⊂ [0, a]`; so the slopes of `Ψ_g` are in
  `[−B, (1−s)a − B] ⊂ [−a, a]` for `0 ≤ B ≤ a`, `0 ≤ s ≤ 1`; at rates `e ≥ ε*` (`θ = 0`) the perspective term is flat; ok on `(0, 1]`.
* **Z2:** the three places of Lemma U(d) where the range enters, re-read: step-one rungs (auxiliary inequality at `y = x_l`),
  first rung (`x₁ ≥ max(Ξ, 1) ≥ G`), outer sample (needs a line with `σ_iG ≤ n_iB_i + E₁`: the zero line).  Cap `Ξ = n_oϑ ≤ n`.  ok.
* **Z3:** admissibility (`n_i ≥ ⌊1/(2u)⌋ + 1`), accuracy (`≤ 1 + ln θ + (c₃+1)/θ ≤ X₀(d) + y`; `(c₃+1)/θ ≤ 0.23`), rounding
  (`|φ − φ*| ≤ max(1, d_min − 1)/d`), grid (4.1), shift by `X₀(d)`: each re-derived; no gap found on paper.
* **Z4, §6:** hypotheses of Proposition T (`0 < b_{j+1} ≤ a ≤ ln 2`, `𝒳 > 1`, flat type) met; unrolling and growth of `Λ̄`
  re-derived (`k + k_{M₁} − 1` increments `q`, `k + M₁ + 1` chains, each `< n·a`): `Λ̄ ≤ (k + M₁ + 3)Λ̄₀`.

Numerical replication follows (W2 …).

## W2. Replication (i): the slope map and the chain, own code (`zrev.py`, `z01_sigma_chain.py` → `out_z01_sigma_chain.txt`)

* Own library `experiments/workstreams/Z/review/zrev.py`: `θ_na` of the cube through `ρ` (`KL(ρ‖p_u) = e`, `θ = KL(ρ‖½)`); the slope map
  `Σ(B, s) = sup_e [B − (1−s)θ_na(e)]/e` (a) by **direct maximisation** over `e` (scan + golden section), (b) through the
  first-order condition (tangent line of `(1−s)θ` with intercept `B`), (c) a brute-force grid of 200 001 rates.  900 random
  `(B, s)`, `u ∈ {½, 1, 2}`: (a) = (b) to `5·10⁻¹¹` (relative), (c) never above (a); the coordinator's `rlib` (which goes through
  the dual function `J`) agrees to `7·10⁻¹¹`.  `θ_na` convex and nonincreasing on a grid of 20 001 rates; `Σ(h, L) = L` to `10⁻¹⁴`;
  constants `h, L, ϑ, c_*²` as in `R_REPORT.md` (`u = 1`: `0.02913914, 0.490034, 4.244977, 0.0711473`).
* The chain `(W_j, b_j)` of the cube at `u = 1`, `s_t = L + 0.05`, `b₀ = h + 0.003`, from the definitions of `R_REPORT.md` §6
  (cut point by Newton on `p_j(B) = s_t`, `m_j` by the chain rule, `b_{j+1} = min(b_j, E_j)`): `B_t(j) − h`, `m_j`, `E_j − h`,
  `b_j − h` at `j = 3, 6, 10, 20, 50` agree with `experiments/workstreams/R/out_r2_chain_cube1.txt` to all seven digits printed;
  `(b_j − h)/h` for `j ≤ 12` agrees with the header of `out_z1_onelevel_u1.txt`; `j²(b_j − h)/c_*² = 1.3745, 1.5328, 1.4629` at
  `j = 10, 20, 40` (the report's caveat (i)).  Range condition for `j ≤ 62`: holds, largest `W_j(b_j) = 0.8177` (at `j = 5`).
  Lemma T(b) (`W_{j+1} ≤ Σ(·, W_j(·))` on `[0, b₀]`, 3001 points, `j < 40`): no violation; `W_j` convex, nondecreasing, `W_j(0) = 0`.

## W3. Replication (ii): Proposition Z1(2) and the minimax identity (`z02_minimax.py` → `out_z02_minimax_A*.txt`, `_B.txt`, `_C.txt`)

Notation: `LHS(g) = inf_φ max_{𝓔(W,b)} Ψ_g(φ; ·)`, `MID(g) = sup{B − Σ(B, W(B))g : Σ(B, W(B)) < ∞}` (right side of Proposition U),
`RHS(g) = M_{W′,b′}(g)`.  Every quantity is **bracketed**: a lower value (maximum over sample points of the convex curve) and an
upper value (sample points plus the intersections of consecutive tangent lines — on a cell the convex curve lies above both
tangents), so "`LHS_up ≤ RHS_lo`" proves the inequality at that `g` up to rounding, and "`LHS_lo > RHS_up`" would be a proven
violation.  `inf_φ` by golden section on `[10⁻¹², 1 − 10⁻¹²]` (the function is convex in `φ`: Lemma Z1a).

* **Part A — the chain** (`W = W_j`, `W′ = W_{j+1}`; 52 values of `g` from `10⁻⁷` to `3u` per level):
  `u = 1` (`s_t = L+0.05`, `b₀ = h+0.003`) levels `0…30`; `u = ½` (`L+0.05`, `h+0.0008`) and `u = 2` (`L+0.05`, `h+0.01`) levels `0…20`;
  `u = 1` with `(L+0.15, h+0.003)` levels `0…12` and with `(L+0.05, h+0.012)` levels `0…8`: **4 940 cases**.
  Z1(2): no proven violation (`LHS_lo − RHS_up ≤ 1.1·10⁻¹³`, the residue of `φ ≤ 1 − 10⁻¹²` at rates where the infimum is not
  attained); `LHS_up − RHS_lo ≤ 9.7·10⁻⁸`, which is the width of the brackets (`≤ 1.9·10⁻⁷`, i.e. `2·10⁻⁶` of `h` at `u = 2`) at the
  rates where (2) is an **equality** (the orbit part of the curve is active); where it is strict the slack is up to
  `3·10⁻³`.  The minimax identity `LHS = MID` holds within the brackets in every case (midpoints agree to `2.7·10⁻⁸`).
  So (2) is confirmed on these curves, with equality (not just `≤`) at small `g`.
* **Part C — controls**: for a concave `W`, a step, and a decreasing `W` the identity fails (`LHS − MID` up to `0.11a`, `0.17a`,
  `0.08a`): convexity and monotonicity are needed, as `R_REPORT.md` says.
* Part B (other convex nondecreasing `W`): see W5 below.

## W4. Replication (iii): Lemma Z2 and Proposition Z3 against an exact level evaluator (`zlev.py`, `z03_onelevel.py` → `out_z03_onelevel_u*.txt`)

Evaluator: the one of the referee of Q2 (`Q2/review/rlib.py`: tables of the outer cube, `r†`, `π†`, the constants of Theorem
11.56), imported read-only; `ℓ₀`, `q`, `X₀`, the level of Lemma Z2 and the design of Proposition Z3 written from the text;
the chain from W2.  Random cases: `d` from `d_min + 1` to `20 000` (30 % of them within 40 of `d_min`), horizons `N ∈ {d, 2d, 3d, 10d}`,
chain levels `j ∈ {0, …, 20}`, `δ ∈ {½, 0.05, 10⁻³, 10⁻¹², e^{−d}, e^{−30d}}`, targets `x̂` from `𝒳` exactly to `𝒳 + 10d`
(including `𝒳 + 10⁻⁹`, `h·d`, `ε*·d`, `2u·d`), inner families **saturating** the type `𝓗_N^∞(𝔏_j; E)` with
`E ∈ {0, 3√d, Λ/7, 5/x + ln Λ}`.  Per case: `Π_j` for **all** admissible `n_o`; the level evaluated exactly at the design's `n_o`,
at `n_o = 1, 2`, at the largest admissible one and at three random ones.

| `u` (`d_min`) | cases / levels | (A) accuracy `≤ x̂` | (B) (U∞) least slack | (B′) `δ′` least slack | (C) exponent, least slack | (D) type of Z3, least slack |
|---|---|---|---|---|---|---|
| `¼` (4) | 2 200 / 13 193 | 0 viol. | 4.47 | 2.92 | 1.12 | 16.3 |
| `1` (2) | 3 617 / 22 317 | 0 viol. | 3.82 | 2.32 | 1.29 | 16.7 |
| `2` (2) | 2 169 / 13 646 | 0 viol. | 4.33 | 2.24 | 1.65 | 21.8 |
| `4` (2) | 651 / 4 116 | 0 viol. | 5.25 | 2.24 | 2.05 | 55.4 |

(`u = ½`, `d_min = 3`: 4 059 cases / 24 626 levels; no violation; least slacks `3.94`, `2.67`, `1.17`, `15.6`.  `u = 1` on a second chain,
`s_t = L + 0.15`: 3 052 / 18 844; no violation; `3.82`, `2.32`, `1.29`, `16.7`.)  **No violation of any of (A)–(D).**  The worst cases of (B), (D) are at `d = 3` or `5`; the accuracy has exactly one nat to
spare at `n_o = d − 1` (`x̂ − x_out ≥ 1.0000`: the `2` in `X₀(d)` could be `1 + (c₃+1)/θ`); (C) is tight to about `1.1` (its
allowance is `1 + a·d_min + d/N`).  Controls: (D) without `ℓ₀ + X₀` fails in thousands of cases; (C) with `W_{j+2}` in place of
`W_{j+1}` fails; a target lowered by `1.3` is missed by thousands of levels.

## W5. More of (ii) and (iii); replication (v)

* **(ii) Part B — adversarial `W`** (`out_z02_minimax_B.txt`): 630 convex nondecreasing curves with values in `[0, 1]` — powers `top·(B/b)^p`
  (`p ∈ {1, 1.5, 2, 4, 10}`, `top ∈ {1, 0.6, 0.2}`), flat-then-linear curves with a kink, `W ≡ 0`, exponentials — on intervals `[0, b]` with
  `b` from `0.3h` to `3a` (capped at `0.999 ln 2`; so also intervals that reach beyond the regular region), `u ∈ {½, 1, 2}`, 18 rates
  each: **11 340 cases**.  Tested: `LHS ≤ M_{W′,b′}` with `W′ := min(1, Σ(·, W(·)))` on `[0, b′]`, `b′ = sup{B ≤ b : Σ(B, W(B)) < ∞}` (the
  curve of remark (1) of `R_REPORT.md` §5 — it need not be convex; `M` is a supremum of lines in any case), and the identity
  `LHS = MID`.  No proven violation (`LHS_lo − RHS_up ≤ 7·10⁻¹³`); `LHS_up − RHS_lo ≤ 3.6·10⁻⁸` (bracket width); identity within the
  brackets (midpoints to `8·10⁻⁸`); slack of `LHS ≤ M_{W′,b′}` up to `0.13` where the cut at one is active.
* **(iii), `u = ½`** (`d_min = 3`): 4 059 cases / 24 626 levels, no violation (numbers added to W4).
* **(v) the table of §7** (`z05_formula.py` → `out_z05_formula.txt`): the unrolling of §6 written from the text (own `ℓ₀`, `q`, `X₀`, own
  (A.1) for the base; chain functions of the referee of Q2, which I compared with `Q2_REPORT.md` §4 line by line; own chain `b_j`):
  the rows `n = 10⁵, 10⁷, 10⁸, 10⁹, 10^{10}` are reproduced **to every digit printed** (total, `n·β_k`, chains, levels, base, per-level
  loss): e.g. `10⁷`, `k = 13`: `2.521·10⁴ = 6152 + 8712 + 1325 + 9018`; `10⁹`, `k = 61`: `9.971·10⁴`.  `M₁ = 10`, `k_{M₁} = 43` confirmed;
  `k = 13` is the minimiser at `10⁷` (neighbours `25 364`, `25 225`).  `z2_formula.py` **is** the formula of §6 (closed update
  `Λ̄ ← Λ̄ + j(n)q_T(n, Λ̄ + n·b_j)`, then `A_T` at the updated `Λ̄`, the base entered with the final `Λ̄`).  (I read the version of
  commit `d3b4b84`, which produced `out_z2_formula_u1.txt`; the coordinator has since added a mode `env` — the function `E_Z`
  is untouched by that change.)
  The largest `Λ̄` of the unrolling is far below the `Λ̂ = (k + M₁ + 4)Λ̄₀` of the proof (`4.6·Λ̄₀` against `135·Λ̄₀` at `k = 121`).
* **The constant `c_Z` and "10.6"** — see finding F1 in §0/§7: the per-level loss divided by `ln n` is `47.1 … 50.0` over the table
  and still increasing; its limit by the report's own formulas is `52.0` for `k ≍ n^{1/3}` (`52.9` for `k = √n`), so the constant of
  the limsup that the proof gives is `(3/2)(2c_*²)^{1/3}·52.0^{2/3} = 10.9`, not `10.6`.

## W6. Replication (iv): a nest of §§4–6 evaluated exactly (`z04_nest.py` → `out_z04_nest_*.txt`)

The nest: a base that saturates a type (`J0 = 0`: the flat type `b₀`, as the brief asks; `J0 > 0`: the type `𝓗_n^∞(𝔏_{J0}; E₀)` of a later
level of the chain, so that the levels above work with sloped lines, extensive outer blocks and inner calls at accuracies
`≥ 𝒳`), then `k` times "level of §4 + chain of §5" (`𝔉_{j+1} = Ẑ[𝔉_j; α]`), output `𝔉_{J0+k}(n, ε̂, δ)`.  Every level — the
levels of Lemma Z2 at the `n_o` of the design, and every level of every chain — is evaluated exactly with the constants of
Theorem 11.56 (evaluator of the referee of Q2), each with its own `δ′` handed down; the chains use the real base bracket of Q
below `d₀`; nothing is cached across failure probabilities.  **At every node**, at its own `(d, x, δ)` and `Λ = ln(1/δ) + d ln 2`:
accuracy; (U∞) with the inner error function; the `δ′`-inequalities of Lemma Z2 and of Proposition T(ii); the type of
Proposition Z3; Proposition T(iii); the type of Proposition Z4 (at `x = α` and just below `𝒳`).  At the top: exact `≤ n·b_k + Ê_k`
(composed error functions) `≤` the unrolled bound of §6.

| run | `u` | `n` | base `J0`, `E₀` | `k` | blocks | `ε̂`, `ln δ` | exact − `n·b_k` | bound − `n·b_k` (composed / unrolled) | node checks | violations |
|---|---|---|---|---|---|---|---|---|---|---|
| H | 2 | 3 000 | 0 (flat), `ln Λ` | 4 | design | 1, `ln 0.05` | 1 120.8 | 2 147.8 / 2 147.8 | 152 | 0 |
| — | 2 | 5 000 | 6, `0` | 3 | design | 1, `ln 0.05` | 946.8 | 1 753.4 / 1 753.4 | 6 879 | 0 |
| E | 2 | 8 000 | 6, `Λ/7` | 3 | design | 1, `ln 0.05` | 1 649.0 | 2 814.1 / 2 814.5 | 57 125 | 0 |
| F | 2 | 5 000 | 8, `5/x + ln Λ` | 3 | design/4 | 0.01, `−5000` | 1 745.7 | 5 557.6 / 5 557.6 | 33 100 | 0 |
| M | 2 | 6 000 | 12, `Λ/7` | 2 | design/6 | `10⁻⁶`, `ln 0.05` | 3 963.7 | 8 078.9 / 8 078.9 | 5 394 | 0 |
| G | 1 | 20 000 | 6, `0` | 2 | design | 1, `ln 0.05` | 683.1 | 983.4 / 983.4 | 997 | 0 |
| L | ½ | 100 000 | 6, `0` | 2 | design | 1, `−40 000` | 742.0 | 994.6 / 994.6 | 1 827 | 0 |
| I | 4 | 2 500 | 5, `0` | 3 | design | 0.3, `−20` | 822.1 | 1 386.8 / 1 386.8 | 139 | 0 |
| A, B, D, J | 2 | 2 500 – 4 000 | 0 (flat), `0` / `ln Λ` | 5 – 7 | design | 1, `ln 0.05` | (stopped at the time limit) | — | 628 228 + 636 555 + 994 588 + 1 016 680 | 0 |
| C, K | 2, 1 | 12 000, 40 000 | 6 / 8, `Λ/7` / `ln Λ` | 3 | design | 1, `ln 0.05` | (stopped at the time limit) | — | 105 955 + 52 868 | 0 |

**No violation in any run** (about 3.5 million node checks in the runs of this table; 5.26 million with the addendum below).  Least slacks over all runs: (U∞) `5.7` nats; `δ′` of Lemma Z2 `6.1`; type of
Proposition Z3 `23.3`; accuracy of a level of §4 `1.03`; accuracy of a chain level `0.011` (by design); Proposition T(iii) `225`;
type of Proposition Z4 `240`; top `252`.  So the level statements are tested sharply, the chain statements only structurally
(`A_T` is a loose bound — the referee of Q2 says the same; with the blocks of the design the exact cost of a nest is
`52`–`75` per cent of the unrolled error term).  With a flat base and `k ≤ 4` every inner call is at an accuracy below `𝒳` (the levels have outer blocks of a few sites)
and goes to a chain; from the fifth level on, and above a sloped base, the outer blocks are extensive (`n_o` up to `502` at
`d = 1861`) and the inner calls at accuracies up to `64 > 𝒳` go to the levels `Z_j` — the number of nodes then grows by a
factor of `10`–`60` per level, which is why the deep flat-base runs did not finish in five minutes; all their nodes passed.
Cross-check of the evaluators (`z07_crosscheck.py`): nine rows of the coordinator's table of §7.1 (`ln C_max` at its `n_o`,
the type of the next curve) are reproduced to the two decimals printed.

*Addendum to W6.*  Run N — **flat base**, `u = 2`, `n = 3000`, `k = 5`, blocks of the design — finished: exact `n·b_5 + 1 065.0`
against `n·b_5 + 2 677.1` (composed and unrolled), **734 663 node checks, no violation** (`out_z04_nest_N.txt`; 81 175 + 43 856 +
2 420 + 72 + 4 levels of §4 and 35 640 chain levels).  The run "—" of the table is stored as `out_z04_nest_Q.txt`.  Two more
runs stopped at the time limit with all nodes passing: O (flat base, `n = 3000`, `k = 6`, `E₀ = ln Λ`: 925 521 checks), P (`u = 1`,
`n = 30 000`, base `J0 = 6`, `k = 3`: 54 716 checks).  Total: about **5.26 million node checks, no violation**.
One-level test on another chain (`u = 1`, `s_t = L + 0.15`, `b₀ = h + 0.003`, slopes up to `0.94`): 3 052 cases / 18 844 levels, no
violation (`out_z03_onelevel_u1_st015.txt`).  Range condition by own code (`z08_range.py`): holds for all `j ≤ 320` at the
report's `(L + 0.05, h + 0.003)` (`j²(b_j − h)/c_*² = 1.170, 1.117, 1.090` at `j = 160, 240, 320`), and for all `j ≤ 200` at
`(L + 0.15, h + 0.003)`, where `j²(b_j − h)/c_*² = 0.957, 0.985, 0.994, 0.998, 0.999` at `j = 10, 20, 40, 80, 160` — see remark R2 of §7.
