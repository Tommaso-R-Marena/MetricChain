# Workstream Q2 — the bounded levels without their `√n`

*Brief written by the coordinator after the twenty-second checkpoint of cycle 10
(2026-11-26).  A paper-proof workstream with exact numerical checks; no Lean.*

## 1. Where we are

Theory report §11.19, Theorem 11.58a (workstream Q, `docs/workstreams/Q_REPORT.md`, refereed:
`docs/reviews/R12_referee_report.md`): for adaptive algorithms without a hint on the class
`L_u(Q_n)`, at a bounded accuracy `ε` and failure probability `δ`,

    ln N(n; ε, δ)  ≤  n·B_M + 𝓔_M,      𝓔_M ≤ C₁(u, ε)·√n + (k_M − 1 − M)·ℓ_S + M·ℓ_D + ℓ_B,

with `ℓ_S = (a/h + 4) ln n + O(1)` per *slope step* and a term `C₁√n` that comes from the
*drops* (one per epoch) and from the base family: these work at a **bounded** closure
threshold `θ = c` on an outer block of a positive fraction of the sites, where the closing
radius is `p_u m − Θ(√m)` (Lemma Q3 = Lemma 11.55(c)).  The workstream's report (§6.2) says
that a `√n` remains for this family of algorithms in any case.

**The coordinator's sketch says it does not** (theory report, Theorem 11.58a, "What it is
not", item (ii); research log, "Resume here", item 0-zero-zero (b)).  Your job is to turn
the sketch into propositions with complete proofs and exact checks — or to find the step
at which it fails.

## 2. The sketch, in the notation of `Q_REPORT.md` (read its §§1–5 first)

Families and types as there: a certified family has type `𝓗(B, σ, R; E)` if
`b(d, x, δ) ≤ d·B − σ·min(x, R·d) + E(d, x; Λ)` for all `d`, all `x ≥ x_min`, all `δ`, all
`Λ ≥ ln(1/δ) + d ln 2`.

**(D′) A drop at a logarithmic accuracy.**  Let `𝔉` have `𝓗(B, 1, R; E)`, `0 < R ≤ h ≤ B`, least
accuracy `x_min ≤ 1`.  Take Algorithm 2L⁺ with `n_o = ⌊φn⌋`, `φ = R/(a + R)`, `λ = 1`, `η = ½`,
`η′ = 1`, `ν₁ = 1`, `b = 1`, the threshold `θ = 3(n_o + 1)e^{2u + e^u}` (or the least value that
Lemma Q4(b) needs at `e = 0`), and the ladder `2un_i > ⌈Rn_i⌉ > … > 2 > 1` served by `𝔉`.  Its
certified accuracy is `X(n) = ln[(2p_u)^n + e(3e + 1 + θ)] = ln n + O(1)`.  By Lemma Q4(b) at
`e = 0` (`ρ_0 = p_u`, `θ_na(0) = a`): `ln(1/π†) ≤ n_o·a + ln(n_o + 1)` — no `√`.  Then, as in the
proof of Proposition Q7 but without the shift: `Λ_lev ≤ P_M + R·n_i + ln(n+1)`, every rung
has the exponent `n_i·B`, and the family `D′[𝔉]` (accuracy-blind: it delivers `X(n)` for
every `x ≥ X(n)`; least accuracy `X(n)`) has `𝓗(B·a/(a + R), 0, ∞; E′)` with
`E′ = E + O(ln n)`.

**(T) Back to a bounded accuracy with outer blocks of logarithmic size.**  Let `𝔊′` have
`𝓗(B′, 0, ∞; E)` with least accuracy `X = X(n) = O(ln n)`.  For accuracies
`α_0 > α_1 > …` (bounded, `α_{j+1} = α_j − w(c_j)`, `c_j` as in Q's schedule) define levels `T_j`:
Algorithm 2L⁺ in dimension `d` with a **small** outer block `n_o = n_o(n) = Θ(ln n)`,
`λ = η = η′ = θ = c_j`, `ν₁ = 1`, tolerance `b = β_j = α_{j+1}`, and the ladder
`2un_i > X > β_j` (two rungs): rung `X` served by `𝔊′(d − n_o, X, δ′)`, rung `β_j` served by
`T_{j+1}(d − n_o, ·, δ′)`; below a dimension `d₀ = O(ln n)` enumeration.  With the trivial
bound `ln(1/π†) ≤ (n_o + 1) ln 2` (Lemma Q2(b)): `Λ_T := ln 2M̄ ≤ P_M + (n_o + 1) ln 2 = O(ln n)`,
and by Proposition Q1, with `t_j(d)` the logarithm of the certified cost of `T_j` in
dimension `d`,

    t_j(d)  ≤  ln 4 + max{ Λ_T ,  Λ_T + b_{𝔊′}(d − n_o, X, δ′) ,  min(Λ_T, X + P_cnt) + t_{j+1}(d − n_o) }.

If `n_o·B′ ≥ X + P_cnt + ln 4`, induction along the chain gives
`t_j(d) ≤ d·B′ + E + A`, `A = n_o(ln 2 − B′) + P_M + ln 8 = O(ln n)`: **every level of the
chain multiplies the cost by `e^{O(ln n)}` at its fine rung and removes `n_o` sites from the
dimension, which pays for it**; a chain of `≈ d/n_o` nested levels adds `A` in all, not
`A` per level.  Accuracies: `Σ_j w(c_j)` bounded as in Q; `ln(1/c_j) = O(ln n)` along a chain
of at most `n` levels.  Failure probabilities: the invariant (2.1) of Q grows by `O(ln n)`
per level, hence by `O(n)` over a chain — `K = O(n)`, `ln K = O(ln n)`.

**(Schedule.)**  Epoch `m`: `J_m` slope steps (Proposition Q6, unchanged, tolerance `1`), then
`D′`, then the chain `T`.  Claim: for every `n, ε, δ, M`

    ln N(n; ε, δ)  ≤  n·B_M + (k_M − 1)·O(ln n) + (M + 1)·O(ln n)        — no √n term —

and hence `ln N ≤ n·h + 2√((1 + r̄)c₁·n·ℓ′_S) + O((ln n)²)` with an explicit `ℓ′_S = O(ln n)`.
(The order `√(n ln n)` does not change: it comes from the rate `c₁/k`.  The point is that
the bounded levels are not what limits the method.)

**A trap to avoid.**  If `D′` is used *without* `T` — so that the next epoch's slope steps
are built on a family whose least accuracy is `X ≈ ln n` — the slope steps need the
tolerance `b = X`, their outer block is shorter by `X/h` sites, and each loses
`(B/h)·X = O(ln n)` more; and the least accuracy grows by `ln n + O(1)` per epoch, to
`O((ln n)²)` after `O(ln n)` epochs.  That variant is admissible but worse.  Say what it gives.

## 3. What to deliver

1. **Proposition D′ and Proposition T** in the style of Propositions Q6/Q7: every
   hypothesis of Theorem 11.56 checked for the parameters (the theorem and all constants:
   `docs/workstreams/K_REPORT.md` §2.2, with the abort rule in the form "before every query,
   every inner call counted with its certified bound" — theory report, Theorem 11.56), the
   certified accuracy of each level, the least accuracies along the nest, the
   pass-through / enumeration at small dimensions, the monotonicity that the error
   functions need, the bookkeeping of `Λ` through a chain of up to `n/n_o` levels.  Explicit
   error terms (like `c_S`, `q_S`, `c_D`, `q_D` of Q), not `O(·)` only.
2. **The theorem**: the explicit bound for the new schedule, its closed form under a
   condition like that of Proposition Q9a, and the consequence for `limsup` and for
   "for all `n ≥ 2`".  Does `C_*` change?  Which term is now second?
3. **Exact checks** with your own code or with the referee's one-level evaluator
   (`experiments/reviews/R12/r12lib.py`; the author's `experiments/workstreams/Q/qlib.py`,
   `qscheme.py` may also be used — both reproduce `experiments/reviews/R8/r8_flat.flat_run`):
   (i) Propositions D′ and T with saturating inner families (cost exactly the majorant),
   over `u ∈ {½, 1, 2}`, `n` from the first size at which each level exists to `10⁶`, `δ`
   from `0.5` to `e^{−n}`; (ii) the chain: the exact certified cost of `T_0` on top of a
   saturating `𝔊′`, by the recursion over the chain (it is a one-dimensional recursion in
   `d`: cheap), against `d·B′ + E + A`; (iii) the new formula evaluated like the table of
   Q's §7.4 (`u = 1`, `ε = 1`, `δ = 0.05`, `n = 10³ … 10^{12}`): where is it below the old one,
   and by how much; (iv) if feasible, the exact nest for `M ≤ 2` at `n ≤ 1.6·10⁴` as in Q's
   §7.3.
4. **"What is not proved"** and the weakest link; anything in `Q_REPORT.md`, in the
   referee report or in the theory report that you find wrong on the way.

If the sketch fails, the deliverable is the precise step, with a counter-computation,
and the best statement that survives.

## 3a. Part B (second priority; start it only when Part A is proved and checked)

**The slope step at a general outer rate.**  Proposition Q6 is the level whose outer block
has the accuracy rate `h` (`n_o ≈ x/h`; closing radius `ρ_h n_o`; `θ_na(h) = h`), and it turns
the type `𝓗(B, σ, R; E)` into `𝓗(B, σ + B/h − 1, Rh/(h + R); E + ℓ_S)`.  The coordinator's
analysis of the rate of the recursion (`docs/workstreams/R_brief.md`, written the same day:
read its §2) shows that the rate `c₁/k` of the present schedule is an artefact of using
the outer rate `h` at every slope step, and that the levels one needs are the same levels
at an outer rate `e ≠ h`, chosen according to the slope:

    outer block  n_o ≈ (x − O(ln n))/e,   closing radius  ρ_e·n_o  (Lemma 11.55(d) = Q4(b) at `e`:
    ln(1/π†) ≤ n_o·θ_na(e) + ln(n_o + 1)),   inner accuracy at the dominant rung  ≈ n_o·θ_na(e),

    type map (exponent level, machine-checkable from `StepLE.of_limit`):
        (B, σ, R)  ↦  ( B ,  σ′ = [B − (1 − σ)·θ_na(e)]/e ,  R′ = R·e/(θ_na(e) + R) ).

(Exponent level, one line: if `T(x) ≤ B − σx` for `0 < x ≤ R`, `σ ≤ 1`, then for `φ = g/e` and
`γ ≤ φθ_na(e)`, `γ + (1−φ)T(γ/(1−φ)) ≤ (1−φ)B + (1−σ)φθ_na(e) = B − σ′g`, provided
`φθ_na(e)/(1−φ) ≤ R`, i.e. `g ≤ R′`.  At `e = h` this is Q6.)

Deliver **Proposition Q6(e)**: for every `e` in a compact subinterval `[e₀, e₁] ⊂ (0, ε*)`
the finite-`n` statement with an explicit error term `ℓ_S(n; e)` (expected:
`(B/e + 4) ln n + O(1)` with constants uniform on `[e₀, e₁]`), the least accuracy of the new
family, the range, the hypotheses of Theorem 11.56 checked for the parameters, and the
exact one-level checks as for Part A (saturating inner families; `u ∈ {½, 1, 2}`; several
`e` on both sides of `h`).  Since the cost bound of a level is monotone in the bound of the
inner family, the statement for a type that is a **maximum of finitely many lines**,
`b(d, x, δ) ≤ max_i [d·B_i − σ_i·x] + E` on `x_min ≤ x ≤ R·d`, follows line by line with the same
parameters: state it as a corollary, with the range and the error term that it needs
(`E + ℓ_S(n; e)`, one loss for all lines).  This corollary is what the final theorem will
be built on; the schedule itself (which rates, how many lines) is the other workstream's
business — do not design it.

*Optional, only if Parts A and B are done:* the finite-`n` form of the third kind of level of
the rate proof — step (iii), outer fraction `g/(g + θ_hint(g))` at an extensive accuracy
rate `g` — and with it an explicit sub-exponential term for extensive accuracies
(Theorem 11.54): expected `n·θ_hint(g) + O(√(n ln n))`.

## 4. Rules

* Create only: `docs/workstreams/Q2_REPORT.md` and files under `experiments/workstreams/Q2/`
  (scripts with their stored outputs, commands in the report).  Do not edit any existing
  file.  Do not run `lake` or `scripts/audit_all.sh`.  No git command that changes state.
  Do not start further agents.
* Every statement labelled: proved here / quoted (from where, with its status) /
  numerical / heuristic / conjecture.  No claim without one of these.
* One Python process at a time, under about 1.5 GB; other work shares the machine.
  Foreground `sleep` is not available; wait with bounded loops if you must.

## 5. What to report back

At most 40 lines: the theorem proved (or the obstruction), the explicit error term or
its order, what the checks covered and their least slack, the weakest link, what you
found wrong elsewhere, the files created.
