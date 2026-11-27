# Workstream Z — the `1/k²` law at finite `n`: the adaptive cost without a hint is `exp(n·h + O(n^{1/3}(ln n)^{2/3}))`

*Coordinator, 2026-11-26 (written while the twenty-third checkpoint was being closed).  A
paper proof, assembled from statements of three workstream reports.  **Refereed
internally** (an AI referee; not external peer review): `docs/workstreams/Z_REVIEW.md`, with
its own code and outputs in `experiments/workstreams/Z/review/` — "no error of substance";
its seven findings are corrected below and listed in the note that follows.  See "Status"
for what the proof rests on.  Labels: **[V]** machine-checked, **[P]** paper proof,
**[N]** numerical.  Nothing here is machine-checked.  The sequel
`docs/workstreams/Z_ADDENDUM.md` replaces the schedule of this report by a better one
(the envelope sequence) with the same propositions.*

> **Coordinator's note after the review (2026-11-26).**  The referee re-derived every step
> of Propositions Z1, Z3, Z4, Lemmas Z1a, Z2 and §6 and attacked them with independent
> code (Z1(2) with two-sided brackets on 16 280 cases; Lemma Z2 and Proposition Z3 on
> about 200 000 exactly evaluated levels at slopes `¼ … 4`; nests of two to seven levels
> with chains: 5.26 million node checks) — no violation.  Its findings, all applied in
> place: **F1** the constants "`c_Z ≈ 50`, limsup `≈ 10.6`" were values in the range of the
> table, not limits — in the limit the per-level loss is `52.0·ln n` for `k ≍ n^{1/3}` (`52.9`
> for `k = n^{1/2}`), and the limsup constant that the proof gives is `10.9` (§0, §7);
> **F2** `q(n, Λ)` is `O(ln n + ln Λ)`, not `O(ln n + ln ln Λ)` — the proof uses only
> `q(n, Λ̂) = O(ln n)` for `Λ̂ ≤ n²` (§1, §6); **F3** the constants of Theorem Z are now
> quantified, and §9 says that `n₀`, `C′`, `C″` are not effective; **F4** the "barrier" of
> §0 is a heuristic, and its supporting sentence in §8.1 had a gap (a chain of `n/m` levels
> costs its additive term once) — reworded; **F5** the finiteness of `Σ` (§1); **F6** "the
> zero line has `0 ≤ E₁`" (§3); **F7** the level term is `5.7`–`6.3` times `ln n` (§7).  Its
> remarks: Proposition Z3 has a nat to spare in its accuracy (the `2` in `X₀` could be
> `1.23`); the crossovers of the table are properties of the illustrative parameters
> `(s_t, ε₁)` — with `(L + 0.10, h + 0.012)` the base needs six epochs and the bound is below
> Theorem A of Q2 a decade earlier (§7).  Not checked by the referee: the level theorem
> itself, the full design over Theorem A's base, the rows `10^{12}`, `10^{15}` of the table,
> and the addendum.

## 0. The result

Setting: the cube class `L_u(Q_n)` of the theory report §§11.18–11.19 (`n` binary sites, uniform
reference, residuals that change by at most `u` per flipped site; `A = ⟨e^{−ψ}⟩`), slope `u > 0`,
failure probability `0 < δ < 1`, bounded accuracy `0 < ε ≤ 1` (a bracket `L ≤ A ≤ U ≤ e^ε·L`).
`N(n; ε, δ)` is the least worst-case number of evaluations of an adaptive algorithm without a
hint; `θ_na` the non-adaptive exponent function, `a = θ_na(0)`, `h` its fixed point (the hinted
exponent at bounded accuracy), `c_*² = 2π²h²·θ_hint″(0)` the constant of the rate theorem
(theory report Theorem 11.53b).

**Theorem Z [P, conditional on the statements listed under "Status"].**  *Fix `u` and `δ`.
There are `n₀ = n₀(u, δ)` and constants `c_Z`, `C′`, `C″` depending on `u` only such that for all
`n ≥ n₀`, all `0 < ε ≤ 1` and all integers `1 ≤ k ≤ n^{1/2}`*

    ln N(n; ε, δ)  ≤  n·h  +  n·β_k  +  k·c_Z·ln n  +  C′·((ln n)² + ln(1/ε)),            β_k ≤ C″/k²,   k²β_k → c_*²,

*where `(β_k)` is a sequence of numbers that depends only on `u` (the top values of a chain
of convex families of lines, §2).  Consequently*

    ln N(n; ε, δ)  ≤  n·h  +  O( n^{1/3}·(ln n)^{2/3} ),
    limsup_{n→∞} ( ln N(n; ε, δ) − n·h ) / ( n^{1/3}(ln n)^{2/3} )   ≤   (3/2)·(2c_*²)^{1/3}·c_Z^{2/3}.

Theorem 11.58a of the theory report has `O(√(n ln n))` in place of `O(n^{1/3}(ln n)^{2/3})`; the
lower bound is `n·h − O(1)` (hinted).  **What the theorem is not:** the true order (nothing
is known between `n·h` and this bound); a statement at extensive accuracies; competitive
at small sizes (§7: the loss per level is about `50·ln n` at `u = 1`; there the bound, as a
formula, is above the non-adaptive `n·a` for `n` below about `10⁵` and above the bound of
Theorem A of workstream Q2 for `n` below about `10⁷`); a statement about algorithms
outside this nested family — for which, heuristically, `n·h + Ω(n^{1/3})` is a barrier of the
analysis (§8, remark 1: not a theorem); effective (`n₀`, `C′`, `C″` are not produced by the
proofs — §9).

**Status — what it rests on.**

| ingredient | where | status |
|---|---|---|
| (T) the level theorem (Algorithm 2L⁺) with the abort rule (P) | theory report Theorem 11.56 | [P], refereed (R8, R12; SCI-REV-0007); not machine-checked |
| (Q4) the closing radius at accuracy rate `t` | theory report Lemma 11.55(d) | [P], refereed (R12), exact arithmetic checks |
| Lemma U: one level over an inner family whose certified cost is a maximum of lines | `Q2_REPORT.md` §2 | [P], refereed internally (`Q2_REVIEW.md`: correct as stated; about a million levels with its own evaluator); used here in a form its convention (C3) excludes — §3 says why its proof covers it, **and the referee, asked in advance, confirms it** (its §1.4) |
| Proposition T: a chain of levels back to a bounded accuracy | `Q2_REPORT.md` §4 | [P], refereed internally (correct as stated, including "a chain costs `A_T` once"; 3.5 million chain levels) |
| Theorem A: a family of flat type `B_M` with bounded least accuracy | `Q2_REPORT.md` §5 | [P], refereed internally (correct as stated given its inputs) |
| Proposition U, Corollary U′, Lemma T, Proposition C, Lemma RC, Lemma PT | `R_REPORT.md` §§5–8 | [P], refereed internally by two referees |

## 1. Notation and what is quoted

Exponent level (from `R_REPORT.md`; `θ := θ_na`):

* `Φ_g(e; B, s) := B − (g/e)·[B − (1 − s)·θ(e)]` for `0 < g < e`, `0 ≤ s ≤ 1`, `B ≥ 0`.  With `φ = g/e ∈ (0, 1)`:
  `Φ = (1 − φ)·B + (1 − s)·φ·θ(g/φ) =: Ψ_g(φ; B, s)`.
* `Σ(B, s) := sup_{e>0} [B − (1 − s)θ(e)]/e` (the slope map); finite if `B < (1 − s)a`, infinite if
  `B > (1 − s)a`; at `B = (1 − s)a` it is `(1 − s)·|θ′(0+)|` — infinite for the cube, whose `θ_na` has
  infinite slope at zero, so that there `Σ(B, s) < ∞` iff `B < (1 − s)a` or `B = 0` ((Σ2), (Σ3) of
  `R_REPORT.md`).
* For `b > 0` and `W : [0, b] → [0, 1]`: `M_{W,b}(x) := max_{0≤B≤b} (B − W(B)·x)` and
  `𝓔(W, b) := {(B, s) : 0 ≤ B ≤ b, W(B) ≤ s ≤ 1}`.

Finite `n` (from `Q2_REPORT.md` §§1–2, with its conventions (C1), (C2)):

* A *certified family up to `N`* with least accuracy `x_min` assigns to every `1 ≤ d ≤ N`, `x ≥ x_min`,
  `0 < δ < 1` a bracket procedure for `L_u(Q_d)` of accuracy at most `x` and failure probability at
  most `δ`, with a certified bound `exp(b_𝔉(d, x, δ))`, `b_𝔉 ≥ 0`, on its evaluations in every run.
* **Types.**  For a finite set of lines `𝔏 = {(B_i, σ_i)}` with `B_i ≥ 0`, `0 ≤ σ_i ≤ 1`, **containing the
  zero line `(0, 0)`**, and an error function `E(d, x; Λ) ≥ 0`, nondecreasing in `d` and `Λ`,
  nonincreasing in `x`: the family has the type `𝓗_N^∞(𝔏; E)` if for all `1 ≤ d ≤ N`, `x ≥ x_min`, `δ`
  and `Λ ≥ ln(1/δ) + d·ln 2`

      b_𝔉(d, x, δ)  ≤  max_i [ d·B_i − σ_i·x ]  +  E(d, x; Λ).

  (This is Q2's `𝓗_N(𝔏, R; E)` with `R = ∞` and positive slopes — excluded by its convention
  (C3) — plus the zero line, which keeps the majorant nonnegative.)
* The functions `ℓ₀(n, Λ) = ℓ₀¹(n, Λ)`, `q(n, Λ) = q¹(n, Λ)` of `Q2_REPORT.md` §2 (`= 3 ln n + ln(Λ + ln n) + O(1)`
  and `2 ln n + ln(Λ + ln n) + O(1)`, i.e. `O(ln n + ln Λ)`), the constant `c₃ = 3·exp(1) + 1`, and the functions `A_T`, `q_T`, `Λ*`,
  `P̄_cnt`, `P̄_M` of its §4.

## 2. The exponent-level input

**Proposition Z1 [P; from `R_REPORT.md`: Lemma T, Proposition C, Lemma RC, the proof of
Proposition U, Corollary U′, Lemma PT and §8].**  *Let `θ = θ_na` of the cube (it satisfies (H0),
(H1) of that report).  There are `b₀ ∈ (h, a)` and, for every `j ≥ 0`, a number `b_j` and a function
`W_j : [0, b_j] → [0, 1]`, such that:*

1. *`b₀ ≥ b₁ ≥ b₂ ≥ … > h`; each `W_j` is convex, nondecreasing and continuous with `W_j(0) = 0`;
   `W₀ ≡ 0`.*
2. *For every `j ≥ 0`, every `g > 0` and every `η > 0` there is `φ ∈ (0, 1)` with*

       max_{(B,s) ∈ 𝓔(W_j, b_j)} Ψ_g(φ; B, s)  ≤  M_{W_{j+1}, b_{j+1}}(g) + η.

3. *`j²·(b_j − h) → c_*²`; in particular `C″ := sup_{j≥1} j²(b_j − h) < ∞`.*

*Proof.*  Take `s_t ∈ (L, 1 − h/a)` satisfying (C1), (C2) of Lemma RC, `ε₁` from that lemma (with
`h + ε₁ < (1 − s_t)a`), `b₀ := h + ε₁`, `W_j` the cut orbit curves of §6 of that report and
`b_{j+1} := sup{B ∈ [0, b_j] : Σ(B, W_j(B)) < ∞}`.  (1): Lemma T(a) (`0 ≤ W_j ≤ p_j`, and `p_j(0) = 0`); the
values of `W_j` on `[0, b_j]` are in `[0, 1]` by the range condition, which holds for all `j` by Lemma
RC; `b_j > h` because `Σ(B, W_j(B)) ≤ Σ(B, p_j(B)) = p_{j+1}(B) < ∞` for `B ≤ h` ((P2) of that report: `p_j(h) ≤ L`),
and `Σ(·, W_j(·))` is finite up to `min(b_j, B_t(j)) > h` (there `W_j ≤ s_t`, and `(B, s_t)` is regular for
`B ≤ b₀ < (1 − s_t)a`).
(2): in the proof of Proposition U, with `W = W_j`, `b = b_j`: `F(e) := max_{𝓔} Φ_g(e; ·)` satisfies
`inf_{e>g} F(e) = max_𝓔 inf_{e>g} Φ_g ≤ sup{B − Σ(B, W_j(B))·g : 0 ≤ B ≤ b_j, Σ(B, W_j(B)) < ∞}` (Sion's theorem and
the three cases there; this part of the proof does not involve `T`).  Every `B` in that supremum
is at most `b_{j+1}`, and `W_{j+1}(B) ≤ Σ(B, W_j(B))` by Lemma T(b); so the supremum is at most
`M_{W_{j+1}, b_{j+1}}(g)` (Corollary U′).  `φ = g/e`.
(3): §8 of that report: `b_{j+1} − h ≤ E_j − h ≤ δ_t(j) + (1 − s_t)/m_j`, `j²δ_t(j) → c_*²`, `1/m_j = o(δ_t(j))`, so
`limsup j²(b_j − h) ≤ c_*²`; and `b_j ≥ τ_{k₁+j}` with `liminf k²(τ_k − h) ≥ c_*²`.  ∎

*Remark.*  Only `sup_j j²(b_j − h) < ∞` is needed for the order; the limit gives the constant of
the limsup.  `b₀ − h = ε₁` is a fixed positive number: nothing is asked of Lemma RC uniformly
in `n`.

**Lemma Z1a (the bracket is Lipschitz in the outer fraction) [P].**  *For `g > 0`, `0 ≤ B ≤ a`,
`0 ≤ s ≤ 1`, the function `φ ↦ Ψ_g(φ; B, s)` is convex on `(0, 1]` and `|Ψ_g(φ; B, s) − Ψ_g(φ′; B, s)| ≤ a·|φ − φ′|`.*
*Proof.*  `φ·θ(g/φ)` is the perspective of the convex function `θ`, hence convex in `φ`; its
one-sided derivatives are `θ(e) − e·θ′(e±)` at `e = g/φ`, the value at zero of a tangent line of `θ`
at `e`, which lies between `θ(e) ≥ 0` and `θ(0+) = a` (a convex function is above its tangents,
and `θ′ ≤ 0`).  So the one-sided derivatives of `Ψ_g` lie in `[−B, (1 − s)a − B] ⊂ [−a, a]`.  ∎

## 3. Lemma U for lines valid at all accuracies

**Lemma Z2 (= Lemma U of `Q2_REPORT.md` §2 for the types `𝓗_N^∞`) [P: its proof, read for this
case].**  *Let `N ≥ n ≥ 2`, and let `𝔉` be a certified family up to `N` of type `𝓗_N^∞(𝔏; E)` with least
accuracy `x_min ≤ 1`.  Let `1 ≤ n_o ≤ n − 1` with `2u·n_i > 1` (`n_i = n − n_o`), a rate `e ≥ 0`, `ϑ := θ_na(e)`, and
the threshold `θ := 3(n_o + 1)·exp(2u + e^u + n_o·e)`.  The level `𝖫(n; n_o, e)` — Algorithm 2L⁺ in dimension
`n` with `λ = 1`, `η = ½`, `η′ = 1`, `ν₁ = 1`, tolerance `b = 1`, this `n_o` and `θ`, the ladder of step one
from `x₁ = min{max(⌈n_oϑ⌉, 1), ⌈2un_i⌉ − 1}` down to `1`, and `I_l = 𝔉(n_i, x_l, δ′)` — is admissible for (T),
has accuracy `ln[(2p_u)^n + exp(1)·(c₃ + θ)]`, and for every `Λ ≥ ln(1/δ) + n·ln 2`*

    ln C_max  ≤  max_i [ n_i·B_i + (1 − σ_i)·n_o·ϑ ]  +  ℓ₀(n, Λ)  +  E(n, 1; Λ + q(n, Λ)),          (U∞)
    ln(1/δ′) + n_i·ln 2  ≤  Λ + q(n, Λ).

*Proof.*  This is Lemma U with `b = 1`, the cap `Ξ := n_o·ϑ` (`n_oϑ ≤ Ξ ≤ n` holds: `ϑ ≤ a < 1`) and
"`R = ∞`".  (The referee of Q2, to whom the question was put before this report was written,
answers it the same way: `Q2_REVIEW.md` §1.4 and note N2 — "what the proof uses of the inner
majorant is that it is nonincreasing and `x + T(x)` nondecreasing" — and checked it on
353 184 levels with such families: no violation, least slack `2.0` nats; without a
nonnegative line the inequality fails.)  Its parts (a)–(c) do not involve the type of `𝔉`.  In part (d) the type enters in
three places, each of which is an inequality for one line `(B, σ)` with `0 ≤ σ ≤ 1` and uses the
range only through `min(x_l, R·n_i)`:
(i) *rungs with `x_{l−1} ≤ x_l + 1`*: the auxiliary inequality `min{Λ_lev, y + 1 + P_cnt} − σy ≤ (1 − σ)G + 1 + P_cnt`
for every `y ≥ 0`, applied at `y = x_l = min(x_l, ∞)`;
(ii) *the first rung otherwise*: `x₁ ≥ max(Ξ, 1) ≥ G`, so `−σ·x₁ ≤ −σ·G`;
(iii) *the outer sample*: a line with `σ_i·G ≤ n_i·B_i + E₁` is needed — **the zero line** has
`0 ≤ E₁`.  (In Q2 this is where (C2) and a finite range are used: a type without a zero line
whose majorant is negative at `G` is the type of no family.)
The rest of the proof is unchanged, and so is the bookkeeping of `δ′` (part (b)).  ∎

*Remark.*  The certified bound of a family is a number computed from its design; a type is
an inequality about it.  Adding the zero line to a type weakens the inequality only
where the other lines are negative, i.e. where they claim less than one evaluation.

## 4. One level over a grid of lines

Fix the horizon `N ≥ 2` and put

    d_min := ⌊1/(2u)⌋ + 2,        X₀(d) := 2 + ln(3(d + 1)) + 2u + e^u,        𝒳 := X₀(N) + 1.

For `j ≥ 0` let `𝔏_j` be the **grid family of `W_j`**: the lines `(B, W_j(B))` for `B ∈ G_j := {i/N : 0 ≤ i ≤ N·b_j} ∪ {b_j}`.
It contains the zero line (`W_j(0) = 0`), all its points lie in `𝓔(W_j, b_j)`, and for every `x ≥ 0`

    M_{W_j, b_j}(x) − 1/N  ≤  max_{B ∈ G_j} (B − W_j(B)·x)  ≤  M_{W_j, b_j}(x)                       (4.1)

(for `B ≤ b_j` take the grid point `B′ ≤ B` with `B − B′ ≤ 1/N`; `W_j(B′) ≤ W_j(B)`).

**The family `Z[𝔉] = Z_j[𝔉]`.**  Let `𝔉` be a certified family up to `N` with least accuracy at most
one (in the application: of type `𝓗_N^∞(𝔏_j; E)`; the design uses the lines `𝔏_j`, not the
certified bounds of `𝔉`).  For `1 ≤ d ≤ N`, `x̂ ≥ 𝒳` and `δ`:

* `d ≤ d_min`: enumeration (`2^d` evaluations, exact).
* `d > d_min`: put `y := x̂ − X₀(d) ≥ 1`.  For `1 ≤ n_o ≤ d − d_min + 1` let `e(n_o) := y/n_o` and

      Π_j(n_o) := max_{(B,σ) ∈ 𝔏_j} [ (d − n_o)·B + (1 − σ)·n_o·θ_na(y/n_o) ]

  (the main term of (U∞); a computation with the curve `W_j` alone).  `Z[𝔉](d, x̂, δ)` is the level
  `𝖫(d; n_o, e(n_o))` of Lemma Z2 over `𝔉` for an `n_o` that minimises `Π_j` over that range.  (A design
  may instead take the `n_o` with the least certified bound `C_max`; it obeys the same
  inequality.)

**Proposition Z3 [P, from Lemma Z2, Proposition Z1(2), Lemma Z1a].**  *Let `𝔉` have the type
`𝓗_N^∞(𝔏_j; E)` and least accuracy at most one.  Then `Z[𝔉]` is a certified family up to `N` with least
accuracy `𝒳`, and it has the type `𝓗_N^∞(𝔏_{j+1}; E⁺)` with*

    E⁺(d, x; Λ)  :=  E(d, 1; Λ + q(d, Λ))  +  ℓ₀(d, Λ)  +  X₀(d)  +  d_min·ln 2  +  2.

*Proof.*  *Admissibility and accuracy.*  For `d > d_min` and `n_o ≤ d − d_min + 1`: `n_i ≥ d_min − 1 = ⌊1/(2u)⌋ + 1`, so
`2u·n_i > 1`, and `1 ≤ n_o ≤ d − 1`; Lemma Z2 applies.  The accuracy of the level is
`ln[(2p_u)^d + exp(1)(c₃ + θ)] ≤ 1 + ln(c₃ + 1 + θ) ≤ 1 + ln θ + (c₃ + 1)/θ`, and
`ln θ = ln(3(n_o + 1)) + 2u + e^u + n_o·e(n_o) ≤ ln(3(d + 1)) + 2u + e^u + y`, `(c₃ + 1)/θ ≤ 10.2/(6·exp(2)) < 1`
(`2u + e^u + y ≥ 2`); so the accuracy
is at most `X₀(d) + y = x̂`.  Enumeration is exact.
*The type.*  Let `d > d_min`, `Λ ≥ ln(1/δ) + d ln 2`, `g := y/d > 0`.  By (U∞), for each admissible `n_o`, with
`φ = n_o/d` and `e(n_o) = g/φ`:

    ln C_max(n_o)  ≤  Π_j(n_o)  +  ℓ₀(d, Λ)  +  E(d, 1; Λ + q(d, Λ)),          Π_j(n_o) = d·max_{(B,σ)∈𝔏_j} Ψ_g(φ; B, σ),

because `n_i·B + (1 − σ)·n_o·θ(e) = d·[(1 − φ)B + (1 − σ)φ·θ(g/φ)]`.  By Proposition Z1(2) with `η = 1/d` there is
`φ* ∈ (0, 1)` with `max_{𝓔(W_j, b_j)} Ψ_g(φ*; ·) ≤ M_{W_{j+1}, b_{j+1}}(g) + 1/d`.  The admissible fractions are the multiples
of `1/d` in `[1/d, 1 − (d_min − 1)/d]`; one of them, `φ`, has `|φ − φ*| ≤ d_min/d`.  By Lemma Z1a (all `B ≤ b_j ≤ b₀ < a`)
and since `𝔏_j ⊂ 𝓔(W_j, b_j)`:

    max_{𝔏_j} Ψ_g(φ; ·)  ≤  max_{𝓔(W_j, b_j)} Ψ_g(φ*; ·) + a·d_min/d  ≤  M_{W_{j+1}, b_{j+1}}(g) + (1 + a·d_min)/d.

The design takes an `n_o` with the least `Π_j`, so with (4.1) for `j + 1`

    b_{Z[𝔉]}(d, x̂, δ)  ≤  d·max_{B∈G_{j+1}} [B − W_{j+1}(B)·g]  +  d/N + 1 + a·d_min  +  ℓ₀(d, Λ) + E(d, 1; Λ + q(d, Λ)),

and `d·[B − W_{j+1}(B)·(x̂ − X₀(d))/d] ≤ d·B − W_{j+1}(B)·x̂ + X₀(d)` because `0 ≤ W_{j+1} ≤ 1`.  With `d ≤ N` and `a < ln 2`
this is the type.  For `d ≤ d_min`: `d·ln 2 ≤ d_min·ln 2 ≤ E⁺`, and the maximum over the lines is
nonnegative (zero line).  `E⁺` is nonnegative, nondecreasing in `d` and `Λ` and constant in `x`.  ∎

*What the proposition does.*  For every target accuracy the designer chooses the outer
fraction for which the *worst line of the inner family* is cheapest — the minimax over
the outer rate of the exponent-level proof (Sion), which is where convexity of the
family is used — and the lines of slope above one that such a level produces are simply
not claimed (a smaller slope is a weaker bound).  The level is `X₀(d) ≈ ln d` less accurate
than the exponent-level accounting; this costs `X₀(d)` because slopes are at most one.

## 5. Back to the least accuracy one

`Z[𝔉]` has least accuracy `𝒳 ≈ ln N`.  If the next level were built over it with the tolerance
`𝒳`, its inner calls at the dominant rung would cost `e^{σ𝒳}` more than their type says at the
accuracy asked for, and after `j` levels the least accuracy would be `≈ j·ln N` and the
accumulated loss `≈ ½j²·ln N` — which gives back `√(n ln n)` (the "trap" of `Q2_REPORT.md` §5.4).  The
chain of Proposition T repairs the accuracy at an additive cost.

**The family `Ẑ[𝔉; α]`.**  Let `0 < α ≤ 1`, and let `m` be a block for which Proposition T(iv) of
`Q2_REPORT.md` holds with `B′ = b_{j+1}`, the accuracy `𝒳` and the entry value of `Λ` of the unrolling (its
(4.1)).  Put

    Ẑ[𝔉; α](d, x, δ)  :=  𝒯[Z[𝔉]; α, m](d, δ)   for α ≤ x < 𝒳,          Z[𝔉](d, x, δ)   for x ≥ 𝒳.

**Proposition Z4 [P, from Proposition Z3 and Proposition T].**  *In the situation of Proposition
Z3, `Ẑ[𝔉; α]` is a certified family up to `N` with least accuracy `α` and of type `𝓗_N^∞(𝔏_{j+1}; Ê)`,*

    Ê(d, x; Λ)  :=  E⁺(d, 𝒳; Λ*(d, Λ))  +  A_T(d, Λ*(d, Λ))  +  j(d)·Δ_T(d, Λ*(d, Λ))  +  𝒳  +  1

*(`j(d)`, `Δ_T` of Proposition T; `Δ_T = 0` at the values of `(d, Λ)` for which the block was
chosen — part (iv) — and these are the values at which the error is unrolled in §6).*

*Proof.*  `Z[𝔉]` has the flat type `𝓗_N(b_{j+1}, 0, ∞; E⁺)` of Q2 with least accuracy `𝒳 > 1`, because every
line of `𝔏_{j+1}` has `B ≤ b_{j+1}` and `σ ≥ 0`; and `0 < b_{j+1} ≤ a ≤ ln 2`.  By Proposition T(i), (iii) the chain
has accuracy at most `α` and `b_𝒯(d, ·, δ) ≤ d·b_{j+1} + E⁺(d, 𝒳; Λ*) + A_T(d, Λ*) + j(d)·Δ_T(d, Λ*)`.  For `x < 𝒳` the top line of the
grid, `(b_{j+1}, W_{j+1}(b_{j+1}))`, has `d·b_{j+1} − W_{j+1}(b_{j+1})·x ≥ d·b_{j+1} − 𝒳`; so the chain obeys the type with
`Ê`.  For `x ≥ 𝒳`: Proposition Z3, and `E⁺(d, x; Λ) ≤ Ê(d, x; Λ)` (`Λ* ≥ Λ`).  ∎

## 6. The schedule and the proof of Theorem Z

Fix `u`, `δ`, `ε`; `ε̂ := min(ε, 1)`; the horizon is `N := n`.  Let `(b_j, W_j)` be as in Proposition Z1 and
`M₁` the least number of epochs with `B_{M₁} ≤ b₀` in the epoch arithmetic (R) of `Q2_REPORT.md` — a
constant that depends on `u` only.

    𝔉̂_0 := 𝔊_{M₁}                         (the family of Theorem A of Q2 with M₁ epochs and top accuracy 1),
    𝔉̂_{j+1} := Ẑ[𝔉̂_j; 1]   (0 ≤ j < k − 1),        𝔉̂_k := Ẑ[𝔉̂_{k−1}; ε̂];        output: the bracket of 𝔉̂_k(n, ε̂, δ).

*Types.*  `𝔉̂_0` has the flat type `𝓗_n(B_{M₁}, 0, ∞; 𝓔′)` with least accuracy one (Theorem A), hence the
type `𝓗_n^∞(𝔏_0; 𝓔′)`: `𝔏_0` consists of flat lines, among them `(b₀, 0)` and `(0, 0)`, and `B_{M₁} ≤ b₀`.  By
Proposition Z4 and induction, `𝔉̂_j` has the type `𝓗_n^∞(𝔏_j; Ê_j)` and least accuracy `≤ 1` (`ε̂` for `j = k`).
So the output has accuracy at most `ε̂ ≤ ε`, failure probability at most `δ`, and makes in
every run at most `exp(max_{𝔏_k}[n·B − σ·ε̂] + Ê_k) ≤ exp(n·b_k + Ê_k(n, ε̂; Λ̄₀))` evaluations,
`Λ̄₀ := ln(1/δ) + n·ln 2`.  **So `β_k := b_k − h` in the theorem.**

*The error, unrolled at `d = n` from the top* (as (A.1) of Q2): start with `Λ̄ := Λ̄₀`, `𝓔 := 0`; for
`j = k, k − 1, …, 1`:

    the chain (B′ = b_j, accuracy 𝒳, α = 1 or ε̂):   m_j by (4.1) of Q2 at Λ_in = Λ̄;   Λ̄ ← Λ̄ + j(n)·q_T(n, Λ̄ + n·b_j);   𝓔 ← 𝓔 + A_T(n, Λ̄) + 𝒳 + 1;
    the level:                                        𝓔 ← 𝓔 + ℓ₀(n, Λ̄) + X₀(n) + d_min·ln 2 + 2;                 Λ̄ ← Λ̄ + q(n, Λ̄);

then `Ê_k(n, ε̂; Λ̄₀) ≤ 𝓔 + 𝓔′_{M₁}(n; Λ̄)`, the error of Theorem A entered with the final `Λ̄`.  (Each
proposition's error function is nondecreasing in `Λ` and in `d`; the chain replaces `Λ` by
`Λ*(n, Λ) ≤ Λ + j(n)q_T(n, Λ + n·b_j) < Λ + n·b_j` by Proposition T(iv), the level by `Λ + q(n, Λ)`.)

*The growth of `Λ̄`.*  As in Proposition A′ of Q2: a level adds `q(n, Λ̄) = O(ln n + ln Λ̄)` — `O(ln n)` for `Λ̄ ≤ n²`, which is all that is used —, a chain
less than `n·a`.  With `Λ̂ := (k + M₁ + 4)·Λ̄₀`: as long as `(k + k_{M₁})·q(n, Λ̂) ≤ Λ̄₀` — true for `k ≤ n^{1/2}` and
`n ≥ n₀(u, δ)` — every `Λ̄` of the unrolling is at most `Λ̄₀ + (k + k_{M₁})q(n, Λ̂) + (k + M₁ + 1)·n·a ≤ Λ̂`
(`a < ln 2`, `Λ̄₀ ≥ n ln 2`).

*The orders* (fixed `u`, `δ`; `k ≤ n^{1/2}`; `Λ̂ ≤ n²` for large `n`):
`ℓ₀(n, Λ̂) = 3 ln n + ln(Λ̂ + ln n) + O(1) ≤ 5 ln n + O(1)`; `X₀(n), 𝒳 = ln n + O(1)`;
`A_T(n, Λ̄) ≤ ℓ_T(n, Λ̂; b_j, 𝒳, α)` of Q2 §5.3, which is `O(ln n + ln(1/α))` with a constant that depends on
`u` through `ln 2/h` (`b_j ≥ h`); `𝓔′_{M₁} = O(ln n)` (finitely many levels, drops and chains, each
`O(ln n)`: Proposition A′ of Q2 with `M = M₁`).  So there is `c_Z(u)` with

    Ê_k(n, ε̂; Λ̄₀)  ≤  k·c_Z·ln n  +  C′·(ln n + ln(1/ε̂))            for all 1 ≤ k ≤ n^{1/2},  n ≥ n₀,

where the `ln(1/ε̂)` comes from the top chain alone.  (The theorem's `C′((ln n)² + ln(1/ε))` leaves
room for a base with `M₁` growing like `ln n`; with `M₁` fixed, `ln n` suffices.)

*The theorem.*  `ln N(n; ε, δ) ≤ n·b_k + Ê_k = n·h + n·β_k + Ê_k`, with `β_k = b_k − h ≤ C″/k²` and `k²β_k → c_*²` by
Proposition Z1(3).  For the order take `k = ⌈(n/ln n)^{1/3}⌉`.  For the limsup: given `η > 0` let `k₀` be
such that `k²β_k ≤ (1 + η)c_*²` for `k ≥ k₀`, and take `k = ⌈(2(1 + η)c_*²·n/(c_Z ln n))^{1/3}⌉ ≥ k₀` for large `n`; then
`n·β_k + k·c_Z·ln n ≤ (3/2)·(2(1 + η)c_*²)^{1/3}·c_Z^{2/3}·n^{1/3}(ln n)^{2/3}·(1 + o(1))`; let `η → 0`.  ∎

## 7. The constant, and where the bound says nothing

**The loss per level.**  In the unrolling of §6 a level costs `ℓ₀ + X₀ + d_min·ln 2 + 2` and a chain
`A_T + 𝒳 + 1`.  Evaluated with the formulas of `Q2_REPORT.md` (`experiments/workstreams/Z/z2_formula.py`,
which calls the workstream's `q2lib`): at `u = 1` the level term is `5.7` to `6.3` times `ln n` over
the table, the chain term `41.6` to `44.3` times `ln n` — the chain is seven eighths of the loss —
so the loss per level is `47` to `50` times `ln n` in the range of the table.  *In the limit*
(the referee's evaluation of these formulas, `Z_REVIEW.md` F1: with a block `m·h ≈ (8 + γ)ln n`,
`γ = ln k/ln n`) it is `[(8+γ)(a/h − 1) + u√((8+γ)/(2h)) + 4/(3p_u) + (5+γ) + 1 + (4+γ) + 1]·ln n`: **`52.0·ln n`**
for `k ≍ n^{1/3}` and `52.9·ln n` for `k = n^{1/2}` (numerically `51.0`–`51.4` at `n = 10^{10} … 10^{50}`); so
`c_Z = 52.9` serves in the theorem at `u = 1`, and the constant of the limsup is
`(3/2)(2c_*²)^{1/3}·52.0^{2/3} ≈ 10.9`: the bound reads
`n·h + 10.9·n^{1/3}(ln n)^{2/3}` against `n·h + 6.56·√(n ln n)` (Theorem B of Q2) and `8.64·√(n ln n)` (Theorem
11.58a).  (An earlier version said `c_Z ≈ 50` and `10.6`: the values at `n = 10^{15}`.)  The referee of Q2 notes that almost all of `A_T` is slack of one inequality (its
§4: `289` nats bounded against `200` attained at `u = 1`, `m = 1099`), and remark 3 of §8 would
divide the number of chains; neither is used.

**In numbers [N — an illustration; see the caveats].**  `u = 1` (`h = 0.02914`, `a = 0.11094`,
`c_*² = 0.07115`), `δ = 0.05`, `ε = 1`.  Every entry is `ln(evaluations) − n·h` in nats; each column is
minimised over its own parameter (`M` epochs; `k` levels of this report over a base of 10
epochs, 43 levels).  `out_z2_formula_u1.txt`.

| `n` | non-adaptive: `n(a − h)` | Theorem 11.58a | Theorem A of Q2 | **Theorem Z** (`k`) | of which `n·β_k` / chains / levels / base |
|---|---|---|---|---|---|
| `10⁵` | `8.18·10³` | `3.94·10³` | `3.95·10³` | `7.47·10³` (1) | `300` / `469` / `79` / `6 618` |
| `10⁶` | `8.18·10⁴` | `1.21·10⁴` | `1.06·10⁴` | `1.15·10⁴` (1) | `3 000` / `560` / `90` / `7 805` |
| `10⁷` | `8.18·10⁵` | `3.67·10⁴` | `2.61·10⁴` | **`2.52·10⁴`** (13) | `6 152` / `8 712` / `1 325` / `9 018` |
| `10⁸` | `8.18·10⁶` | `1.16·10⁵` | `7.02·10⁴` | **`4.91·10⁴`** (30) | `1.20·10⁴` / `2.35·10⁴` / `3 407` / `1.02·10⁴` |
| `10⁹` | `8.18·10⁷` | `3.74·10⁵` | `2.06·10⁵` | **`9.97·10⁴`** (61) | `2.61·10⁴` / `5.45·10⁴` / `7 643` / `1.15·10⁴` |
| `10^{10}` | `8.18·10⁸` | `1.22·10⁶` | `6.47·10⁵` | **`2.10·10⁵`** (121) | `5.91·10⁴` / `1.21·10⁵` / `1.66·10⁴` / `1.27·10⁴` |
| `10^{12}` | `8.18·10^{10}` | `1.27·10⁷` | `6.76·10⁶` | **`1.04·10⁶`** (484) | `3.55·10⁵` / `5.87·10⁵` / `7.80·10⁴` / `1.52·10⁴` |
| `10^{15}` | `8.18·10^{13}` | `4.25·10⁸` | `2.35·10⁸` | **`1.19·10⁷`** (4510) | `4.09·10⁶` / `6.89·10⁶` / `8.91·10⁵` / `1.90·10⁴` |

So, as formulas: the bound of this report is below the non-adaptive cost from `n ≈ 10⁵` on,
below that of Theorem A of Q2 from `n ≈ 10⁷` on, and its excess over `n·h` is smaller by the
factors `3`, `6.5`, `20` at `n = 10^{10}, 10^{12}, 10^{15}`.  At `n ≤ 10⁶` the fixed base (ten epochs to
reach `h + ε₁`) costs more than the whole bound of Theorem A with its best number of epochs:
there a design takes the cheaper schedule, and nothing is gained.  These crossovers are
properties of the illustrative parameters, not of the method (the referee's remark R2):
with `(s_t, ε₁) = (L + 0.10, 0.012)` the range condition holds at the 70 levels the referee
computed, the base needs six epochs, and the same formula gives `9.4·10³, 1.87·10⁴, 3.93·10⁴,
8.58·10⁴` at `n = 10⁶ … 10⁹` — below Theorem A of Q2 from `10⁶` on; with `(L + 0.05, 0.02)` or
`(L + 0.20, 0.003)` the range condition fails at an early level.  The envelope sequence of
`Z_ADDENDUM.md` removes the parameters.

*Caveats.*  (i) The chain `(b_j)` is computed in floating point for `(s_t, ε₁) = (L + 0.05, 0.003)`
and `j ≤ 160`; the range condition holds at every level computed (and at the 600 levels of
`experiments/workstreams/R/out_r2_chain_cube1.txt`), but the proof gives it for *some* `ε₁ > 0`, not
for this one.  Beyond `j = 160` the table extrapolates `b_j − h = 1.17·c_*²/j²` with the last
computed ratio (the limit of the ratio is one; `1.37, 1.53, 1.46, 1.30, 1.17` at `j = 10 … 160`).
(ii) These are evaluations of formulas.  No algorithm is run, and the nest is not
evaluated exactly; what is evaluated exactly is one level (§7.1).  (iii) A bound that
improves on the previous one from `n = 10⁷` on, with `k ≥ 13` nested levels over a base of 43,
is not a practical algorithm at any size at which the cube class is computed with.

### 7.1 One level, exactly (`z1_onelevel.py` → `out_z1_onelevel_u1.txt`)

Proposition Z3 tested with the exact one-level evaluators (those of Q and of referee R12,
through `q2lib.Ev`; they agree to `1.1·10⁻¹³`).  The inner family *saturates* its type: its
certified cost is exactly `max(0, max_{𝔏_j}[d′B − σx])`.  For `u = 1`, horizons `d = N ∈ {300, 10³, 3·10³, 10⁴}`,
chain levels `j ∈ {0, 3, 5, 6, 8, 11}` and nine target accuracies from `𝒳` to `X₀ + u·d`, the level
`𝖫(d; n_o, y/n_o)` is evaluated for every admissible outer block (a stride of at most
`⌈d/400⌉` at the larger sizes, with the corresponding allowance): 89 208 levels.

| check | result |
|---|---|
| (A) the accuracy of every level is at most the target | 0 violations |
| (B) (U∞): `ln C_max(n_o) ≤ d·max_{𝔏_j} Ψ_g(n_o/d) + ℓ₀(d, Λ)` for every `n_o` | 0 violations; least slack `13.9` nats |
| (C) exponent level: `min_{n_o} d·max_{𝔏_j} Ψ_g ≤ d·M_{W_{j+1}, b_{j+1}}(g) + 1 + a·d_min` | 0 violations; least slack `1.2`; equality to `10⁻³` where the orbit part of the curve is active |
| (D) the type of Proposition Z3, at the `n_o` of the design (the minimiser of `Π_j`) | 0 violations; least slack `25.4` nats; the design's `n_o` costs at most `6.4` nats more than the `n_o` with the least certified bound |
| control: (D) without `X₀ + ℓ₀ + …` | fails in 216 cases |
| control: (C) with `W_{j+2}` in place of `W_{j+1}` (two levels' gain claimed for one) | fails in 5 cases |

The measured loss of a level — certified cost minus the type of the next curve — is `19`–`39`
nats at `d = 10³ … 10⁴`, about half of the `52`–`64` that `X₀ + ℓ₀` allows there.  (The referee's
independent test — its own chain, another evaluator, slopes `¼ … 4`, `d` up to `20 000`,
horizons up to `3000·d`, failure probabilities down to `e^{−30d}`: about 200 000 levels — has
no violation either, with least slacks `3.8` for (U∞), `1.1` for the exponent-level step and
`15.6` for the type; and it finds that every level is at least one nat more accurate than
its target, so that the `2` in `X₀(d)` could be `1.23`.)

## 8. Remarks

1. **Why `n^{1/3}`, and why not less by this method [a heuristic remark].**  The bound is `min_k [n·β_k + k·ℓ]` with a loss
   `ℓ = Θ(ln n)` per level.  `β_k ≥ τ_{k₁+k} − h ≥ c/(k + k₁)²` for *every* chain of families of this kind
   (the lower bound of the rate theorem is for the exact recursion; this half is a theorem —
   Corollary U′ for every chain of convex sub-solutions).  The other half is not an
   argument as it stands (the referee's finding F4): "a level multiplies the certified
   cost by at least a constant" does not give an additive loss per level in the type
   bookkeeping — a chain of `≈ n/m` levels costs its additive term once.  What the
   inference needs is "every level that lowers the exponent loses an additive constant
   against its type", which is plausible and unproved.  If it holds, no schedule
   analysed level by level through types gives `n·h + o(n^{1/3})`; with a loss `O(1)` per level
   the method would give `n^{1/3}` without the logarithm.  Whether the true cost is
   `n·h + O(1)` (the hinted lower bound) is the open problem of the theory report §12.
2. **What is new against Theorem 11.58a.**  There the family of every level has one line, and
   the schedule follows the epochs of the `O(1/k)` proof; here every family carries the
   grid of a convex curve, the outer fraction of a level is chosen per accuracy against
   the worst line, and the exponent-level inequality that controls it is the minimax
   identity of the rate proof.  The finite-`n` ingredients (Lemma U, the chain) are those of
   workstream Q2, used for a new purpose.
3. **The chain after every level** is the simplest repair and probably wasteful: a chain
   every `r` levels costs `A_T/r + (r/2)·σ̄·ln n` per level, which is smaller for `r ≈ √(2A_T/(σ̄ ln n))`
   — a constant.  Not done: it changes `c_Z`, not the order.
4. **The constant of the limsup is not optimised** and is not claimed to be sharp for the
   method.

## 9. What is not proved; the weakest links

0. **Nothing in Theorem Z is effective** (the referee's finding F3): `n₀`, `C″` and the number
   `M₁` of base epochs (hence `C′`) come from the `ε₁` of Lemma RC, the restart level `k₁` and
   the unquantified `o(1)` of the rate theorem.  For a given `k` the range condition is a
   finite check (`j ≤ k`), so a certified `β_k` for a given chain is within reach of interval
   arithmetic; it has not been done.  (The envelope sequence of the addendum has no range
   condition; its tops are floating-point numbers all the same.)
1. Everything of `Q2_REPORT.md` that is used (Lemma U, Proposition T, Theorem A) has been
   refereed internally (`Q2_REVIEW.md`); Lemma Z2 extends Lemma U beyond its stated
   conventions by reading its proof — both referees (of Q2 and of this report) confirm it.
2. (T), the level theorem, is a paper proof (refereed, simulated at small sizes), used
   here — as in Theorem 11.58a — in a regime no simulation covers: `k ≈ n^{1/3}` nested
   levels and `k` chains of `≈ n/ln n` levels each.
3. The unrolling of `Λ̄` in §6 follows Proposition A′ of Q2 and is written in less detail
   than there.
4. No machine check of any step.
