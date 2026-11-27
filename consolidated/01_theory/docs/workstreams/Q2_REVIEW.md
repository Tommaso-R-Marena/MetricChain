# Internal review of `docs/workstreams/Q2_REPORT.md`

*Independent adversarial referee (AI; an internal review, not external peer review), 2026-11-26.
Brief: `docs/workstreams/Q2_review_brief.md`.  Scripts and outputs of this review:
`experiments/workstreams/Q2/review/` (own evaluator `rlib.py`; nothing imported from the workstream's
libraries).  No existing file was edited; `lake`, the audit script and state-changing git commands were not run.
The sections below are the review; the working notes N1–N8 after them are the record of the checks, in the
order in which they were made.*

## 0. Summary of verdicts

**No substantive error was found.**  Every statement was re-derived from the statements it quotes, and the
arithmetic of each was replicated with independent code; the findings are of the kind "wording / side remark".

| statement | verdict |
|---|---|
| **Lemma U** (§2) | **correct as stated.**  It also holds — same proof — for `R = ∞` with positive slopes (answer to the coordinator, §1.4) |
| Corollary U1 (§2) | **correct as stated** |
| Proposition D′ (§3) | **correct as stated** (its remark (2) for `R > 1` is incomplete; not used) |
| **Proposition T** (§4) | **correct as stated**, including "a chain costs `A_T` once" ((iii) with (iv)) |
| Theorem A (§5.2) | **correct as stated**, given its quoted inputs (Theorem 11.56 with rule (P), Lemma 11.55(c),(d), Q1, Q2, Q5, Q6, the epoch arithmetic) |
| Proposition A′ (§5.3) | **correct as stated**; one parenthetical side condition for the displayed form of `ℓ̄_T` is misstated (harmless, §5) |
| Theorem B (§5.3) | **correct as stated**, including `C_*′ = 3√(2(1 + r̄)c₁)`, the `O((ln n)² + ln(1/ε))` term and the sequences `ε_n` |
| Proposition N (§5.4) | **correct as stated** for what it states as proved (admissibility; the cost formula `𝓔^N_M`); its paragraph on the order is, by the report's own label, not written out in full |
| Proposition Q6(e) (§6) | **correct as stated** |
| Corollary Q6(e)-max (§6) | **correct as stated**; extends to `R = ∞` with positive slopes with `R′ = e` (§7) |

**Findings, most serious first** (none changes a statement):

1. *(C3) / Lemma U, the exclusion "all `σ_i = 0` if `R = ∞`" is not needed* — see §1.4.  More generally the range
   condition "`Ξ ≤ R·n_i`" is needed only for the *form* of (U): without it the same proof gives
   `ln C_max ≤ max_i[n_iB_i + n_oϑ − σ_i·min(n_oϑ, R_in_i)] + ℓ₀^b + E` (also for lines with different ranges `R_i`).
2. *Proposition A′, the parenthesis after the display of `ℓ̄_T`:* the condition "`9(ln 2/a − 1) ≤ 8(ln 2/h − 1)`" forgets that the
   base chain has `𝒳_B/(2u) ≈ 2 ln n/(2u)`, not `ln n/(2u)`; the condition that the display needs is
   `9(ln 2/a − 1) + (ln 2 − a)/u ≤ 8(ln 2/h − 1) + ln 2/(2u)`.  It holds with a factor 3.5–5 to spare at `u = ½, 1, 2`; nothing changes.
3. *Proposition D′, remark (2) (`R > 1`):* besides `K̄^b`, `ℓ₀^b` also `q^b` changes (`ln(4L) ≤ ln(4A_n^b)`), and the hypothesis
   "`Ξ ≤ n`" of Lemma U must be dropped with it.  The remark is not used.
4. *§4.3, remark 2, "the least `m` exists":* it does, but for small `N` it is `≥ N`; the chain then has no level and the family
   is the base bracket at `α̲` (covered by the proposition: `j ≡ 0`, error `e₀`).  The report says so only in §7.4(vi).
5. *§6.2, remark 2:* "`σ_i′ < 0` … (possible for `e < h`)" presupposes `B_i ≥ h`; "a type with range `R′` is also a type with
   any smaller range" needs `σ ≥ 0`.
6. *Wording:* Lemma U needs "`Ξ ≤ n`" only for `L ≤ n` in the constants; what its proof uses of (C2) is the
   nonnegativity of the majorant at the single point `(n_i, max(G, b))`; and (C2) serves one purpose (the outer sample)
   but in two proofs — Lemma U and Proposition T (`ln C₁ ≥ 0`).

**Answer to the coordinator's question (item 1 of the brief).**  **Yes.**  Lemma U holds, with the same proof and
the same constants, for an inner type that is a maximum of finitely many lines with slopes `0 ≤ σ_i ≤ 1` valid at
*all* accuracies `x ≥ x_min` (`R = ∞` with positive slopes), provided the maximum is nonnegative — it is enough that
`max_i[n_iB_i − σ_i·y*] + E(n, b; Λ + q^b) ≥ 0` at the one accuracy `y* = max(G, b) ≤ max(n_oϑ, b)`, which a flat line
or (C2) gives.  **Cap: any `Ξ` with `n_o·θ_na(e) ≤ Ξ ≤ n`**; the natural one is `Ξ = n_o·θ_na(e)`, i.e. the first rung
`x₁ = b + min{⌈n_oϑ − b⌉₊, ⌈2un_i − b⌉ − 1}` (a larger cap only adds rungs whose terms are dominated; for `Ξ > n` read
`A_n^b` for `n + 3` in `K̄^b`, `ℓ₀^b` and for `n + 1` in `q^b`).  The exclusion in (C3) is not needed.  Details and
proof: §1.4; numerical check: 353 184 levels with such families, no violation, least slack `2.0` nats.

## 1. Lemma U (§2)

### 1.1 Statement and conventions

The statement is precise and complete.  Two remarks.  (a) The hypothesis "`Ξ ≤ n`" serves only `L ≤ n` in part (b)
(the constants `K̄^b`, `q^b`, `ℓ₀^b`); the inequalities of the proof of (d) need `Ξ ≥ n_oϑ` and, for the form of (U),
`Ξ ≤ R·n_i`.  (b) Convention (C2) enters the proof at one point only, `(n_i, y*, δ′)` with `y* = max(G, b)`: one line must
satisfy `σ_i·G ≤ n_iB_i + E₁`.  If this fails, (U) is false (the outer sample alone costs `e^{Λ_lev}`, `Λ_lev ≈ n_oϑ`): the
negative control of `r01_lemmaU.py` gives violations of up to `8 551` nats.  So (C2) is a hypothesis, not a convenience;
the report says this correctly (§1.2, §7).

### 1.2 Checklist of the hypotheses of Theorem 11.56

Verified item by item against the theory report's statement and `K_REPORT.md` §2.2 (note N1): (H1)–(H9) hold;
`x_L = b`; `x₁ = b + k₁ < 2un_i`; the inner procedures are asked accuracies `≥ b ≥ x_min` in the dimension `n_i ≤ N`;
`δ′ = δ/(4LM̄)` does not depend on the inner costs, so there is no circularity.  The accuracy is the formula of (T)
with `e^λ(1+η)/(1−η) + η′ = 3·exp(1) + 1`.

### 1.3 Proof, step by step

Note N1.  I re-derived the constants from the formulas (not from Q's restatement): `ν₀ = 2(e−1)(J+1)`,
`P_M = ln(J+1) + c₂₄ + ln K`, `P_cnt = 2 ln(J+1) + c₁₈ + ln K`, `Λ_lev = P_M + ln(1/π†)`; part (b) (each of its eight
inequalities), (2.1), part (c) (Lemma Q4(b) with the hypothesis as corrected by R12, `c_η^{-1} = 3`), the auxiliary
inequality (three cases; uses `0 ≤ σ ≤ 1`), the three kinds of rung, the outer sample, and the passage to the maximum
over the lines (the classification of the rungs does not depend on the line, so the maximum commutes).  **No gap.**
Numerically: 973 668 levels with saturating families, parts (b), (c) at every level (8.76 million checks), no
violation; least slack of (U) `2.0`–`3.4` nats — so the lemma is sharp to `O(1)`; `ℓ₀^b ≈ 4 ln n` cannot be lowered
uniformly by more than about two nats under the convention `Λ ≥ ln(1/δ) + n ln 2` (the worst cases are at `δ = e^{-n}`
or tiny `n`; at `δ = 0.05` and `n ≥ 2500` the least slack found is `9` nats — there the slack sits in `K̄^b` (`Λ ≥ n ln 2` against
`ln(1/δ)`) and in `L + 2 ≤ n + 3`; `r01b_general.py`).

*Two sharper forms that the same proof gives* (for the coordinator's plan; not in the report).  (a) The proof ends with
`ln C_max ≤ ln(L+2) + 1 + P_cnt + E₁ + max_i[n_iB_i + (1−σ_i)·G]`, `G = (Λ_lev − 1 − P_cnt)₊`, with the level's own `L`, `P_cnt`,
`Λ_lev`; (U) is this with `G ≤ n_oϑ` and the uniform constants.  Since `G = (ln(1/π†) − ln((3e/4)(J+1)))₊`, every gain on
`ln(1/π†)` passes to the bound with the factor `1 − σ_i`.  (b) Lemma Q4(b) is far from sharp at the rate `0` on exact
tables: at the threshold of `D′` the closing radius exceeds `p_un_o` by `977` (about `0.6·√(n_o ln n)`) and
`ln(1/π†) − n_oa = −959` at `n = 10⁶`, `u = 1`, `φ_0` (reproduced, §3) — the report mentions this "negative `√`-term" and does not use it.

### 1.4 The coordinator's question: `R = ∞` with positive slopes

Note N2 has the argument in full.  In short: in the proof of (d) the range enters in two places — "`x_l ≤ R n_i`" for
the step-one rungs (only to replace `min(x_l, Rn_i)` by `x_l`: void for `R = ∞`), and "`Rn_i ≥ Ξ ≥ G`" for the first rung
(for `R = ∞`: `x₁ ≥ max(Ξ, b) ≥ G` is all that is used) — and the outer sample needs one line with `σ_iG ≤ n_iB_i + E₁`,
which a flat line gives outright and (C2) gives in general.  The auxiliary inequality does not know the range.  Hence
(U) holds verbatim with any cap `n_oϑ ≤ Ξ ≤ n`.  What the proof really uses of the inner majorant
`T(x) = max_i[n_iB_i − σ_i·min(x, R_in_i)]` is that `T` is nonincreasing and `x + T(x)` nondecreasing; for any such `T`,
`ln C_max ≤ ℓ₀^b + E₁ + Y + T(Y)`, `Y = max(n_oϑ, b)`, with no range condition (for lines: `max_i[n_iB_i + n_oϑ − σ_i·min(n_oϑ, R_in_i)]`).
Checked: `r01_lemmaU.py` (`R = ∞`, positive slopes, with a flat line: 244 512 levels, least slack `2.45`; without a
flat line but with `B_i ≥ 2uσ_i`: 108 672 levels, `1.99`; caps `n_oϑ`, `2n_oϑ + 5`, `n`), `r01b_general.py` (no range condition,
different ranges: 108 360 levels, `3.3`).  Consequences the coordinator may want: Proposition D′ then holds for every
`0 < φ < 1` (cap `n_o·a`; the condition `φ ≤ R/(a+R)` disappears), and Proposition Q6(e)/Q6(e)-max hold with `R′ = e`
(11 496 levels as built, least slack `4.6`).  A slope `σ_i > 1` must still be cut to one first (it is a weaker valid line);
with `σ > 1` (U) fails, as the report found.  Note also that the image of a slope step has the finite range `R′ = e`
even if `R = ∞`: "valid at all accuracies" is not preserved by a step at one rate.

## 2. Corollary U1

**Correct as stated** (note N5).  The level of Q6 is the level of Lemma U with `b = 1`, `e = h`, `Ξ = x̂`; the ladders coincide;
`c_S − c_S′ = (1 − σ)(1 + c_log(n) + h)`.  `r07_U1.py`: 5 776 levels of Q6 as built, no violation with `c_S′`, least slack
`3.6` nats, gain up to `26.9` nats.  The consequence for the constant (average slope `(J_m + 1)/(2d_m) → ½` over an
epoch, hence `(9/2)·ln n` per step) is right; the excess `J_m(J_m+1)/(2d_m) − J_m/2 < a/h` per epoch is correctly moved to `ℓ̄_D`.

## 3. Proposition D′ (§3)

**Correct as stated** (note N5).  The hypotheses of Lemma U hold for the level as built (threshold through
`𝒳 ≥ 𝒳_D^b(N; φ)` and `(2p_u)^n e^{−b} ≤ 1`; range condition ⇔ `φ ≤ R/(a + R)`; accuracy exactly `𝒳`); the rounding term
`τ[B_i − (1−σ_i)a]` and the pass-through where the level is not defined are right; the horizon is what makes one `𝒳`
serve all `n ≤ N`.  `r04_built.py`: 15 156 cases (tolerances `1, 2.5, 17.3`; horizons `n, 3n`), no violation, least
slack `4.1` nats; the number of §3 (`ln(1/π†) − n_oa = −959` at `n = 10⁶`, `u = 1`, `φ_0`) is reproduced (`−959.3`, `r† = 56 920`
against `p_un_o = 55 943`).  Remark (2) is incomplete (finding 3); remark (3) is a sketch, labelled as such, not reviewed.

## 4. Proposition T (§4)

**Correct as stated** (note N4).  Points the brief asks about:

* *The design rule.*  (4.1) is monotone in `m` as claimed; a least block always exists (finding 4).  The blocks of
  the `M + 1` chains are fixed top-down in the unrolling, each from the value `Λ̄` at which the chain is entered; no
  circularity.  The type (iii) holds for every block and every `(d, Λ)`; (4.1) is only what makes `Δ_T` vanish at the
  point `(n, Λ̄)` where the unrolled bound is evaluated.
* *The induction over a chain of unbounded length* is an induction on the dimension (`d` uses only `d − m`), so the
  length plays no role; base case (`d < d₀`, Q5(a)) and step (Q1 with `L = 2`) are right; the identity
  `Λ*(d − m, F_d(Λ)) ≤ Λ*(d, Λ)` and the monotonicity of `U` are right.
* *The bookkeeping of `Λ` and of the failure probabilities:* (ii) gives `Λ₁ = Λ + q_T(d, Λ) ≥ ln(1/δ′) + (d − m) ln 2`, which is
  exactly what licenses the induction hypothesis at `(d − m, δ′, Λ₁)`; (iv): `Λ* ≤ Λ + j(d)q_T(d, Λ + dB′) < Λ + dB′` because
  `q_T < 𝒳 + P̄_cnt + ln 4 ≤ mB′` and `j(d)·m < d`.
* *The bottom:* `e₀` is needed and correct (`min{d ln 2, da + E_base} − dB′ ≤ e₀` for `d ≤ d₀ − 1`); it is attained with
  equality in some cases of the stress test.
* *"`A_T` once":* proved by (iii)+(iv); confirmed by exact recursion.

Numerically: `r02_chain.py` — eight parameter sets with the block of the design and blocks `½×`, `2×`, `1/7×`
(23 927 levels; parts (i), (ii) at every level, the claim (iii) at 3 631 of them, each at its own `(d, δ)`): no violation, least
slack `57.9`; the rows of §7.2 are
reproduced to the digit (`u = 1`, `B′ = a`, `N = 10⁶`: `m = 1099`, 909 levels, exact `126.62`, `A_T = 230.71`).
`r05_chain_stress.py` — 10 962 random chains away from the design (blocks from one site, `B′` up to `ln 2`, `α` down to
`10^{-9}`, `u` from `0.2` to `4`; 3.5 million levels, the claim at 323 001 of them): no violation, least slack `3.4` nats.  `r06_base_chain.py` — the chain
over the real base bracket: `ln cost/(Na) = 1.3190, 1.0067, 0.9381, 0.9191` at `N = 10³ … 6.4·10⁴` (the report's numbers).

*For a sharper bound* (the coordinator's plan): at the block of the design the slack of `A_T` is almost entirely
`ϖ(m; c) − ln(1/π†)` — `289.4` against `199.9` at `u = 1`, `m = 1099`, of which the second-order Taylor term
`(4/(3p_u))(ℓ_c + 2) = 75` nats of Lemma Q3 is the bulk; `P̄_M − P_M` and the sum of the terms account for about `15`.
Where `ϖ` is attained the induction is tight to `3` nats, so nothing is to be gained in the induction itself, only in
`ϖ`, in `P̄_cnt` (through `c`, i.e. through the uniform `c = α/(13⌈N/m⌉)`: `4 ln(1/c)` of it) and in the design (§8, item 5 of the report).

## 5. Theorem A, Proposition A′, Theorem B (§5)

**All three correct as stated.**

* *The schedule and the least accuracies* (table of §5.1): checked family by family — each family is asked only
  accuracies at or above its least accuracy (`𝔅`: `𝒳_B`; `D′`: `𝒳_m`; chains: `1` resp. `ε̂`; slope steps: `≥ 1` or pass-through).
* *Types:* `𝔅` has `𝓗_n(a, 0, ∞; E_𝔅)` by Q5(b) at `e = 0` (`x ≥ c′_n ≥ c′_d`; `η = ½` because `x ≥ 2 ln 3`); the step `m → m + 1` uses
  Q6 (hypotheses `B_m ≥ h`, `σ ≤ 1` for `j ≤ J_m − 1`, `R ≤ h`, least accuracy `≤ 1`), "slope `≥ 1` implies slope one", Proposition D′
  (`R_m ≤ h < 1`), Proposition T (`B_{m+1} ≤ a ≤ ln 2`).  (C1) is right: every proof uses a family only in dimensions `≤ n`.
* *(A.1):* the composition of the error functions is right (each term at the current `Λ̄`, the inner function at the
  increased one; for a chain both at `Λ*`, bounded by `Λ̄ + j(n)q_T(n, Λ̄ + nB_e)` through T(iv)); only monotonicity in
  `(d, Λ)` is used.  `r03_formula.py` (written from the text): the rows `n = 10³, 10⁴, 10⁶, 10⁸, 10^{10}, 10^{12}` of the table of
  §7.3 are reproduced (`M`, `k_M`, bound, ratio, the four parts of `𝓔′_M`).
* *Proposition A′:* growth of `Λ̄` (`k_M − 1` steps and drops at `q_S ≤ q_S(n, Λ̂)`, `M + 1` chains at `< n·a` each;
  `2 + (M+1)a/ln 2 ≤ M + 3`), the slope sum `J_m(J_m+1)/(2d_m) < J_m/2 + a/h`, the block `m_e ≤ m̄`, `A_T ≤ ℓ_T`: right.
  `r03b_closed_trap.py`: in all 732 cases with the hypothesis, (A.1) ≤ first closed form ≤ second.  Finding 2 concerns the
  parenthesis only.
* *Theorem B:* (b) follows as in Q9(b) with `ℓ̄_S` evaluated at `Λ̂ = (M̄_n + 3)Λ̄_0` (not circular); `c₂ ≥ 0`;
  `k†/(1 + r̄) < k_M ≤ k†`; the hypothesis of A′ does not involve `ε`; `ε` enters through the top chain only, and
  `ℓ_T(…, ε)` is `O(ln n + ln(1/ε))` uniformly in `0 < ε ≤ 1` (also when `ln(1/ε) ≫ n`: then the chain has no level and the
  bound is the base bracket's; the claim is still true, if void).  Hence the `O((ln n)² + ln(1/ε))` term and the limsup
  for `ln(1/ε_n) = o(√(n ln n))`.  `ℓ̄_S = (9/2) ln n + ln ln n + O(1)`, so `C_*′ = 2√((9/2)(1 + r̄)c₁)`: `3.495, 6.560, 10.568,
  12.286` at `u = ½, 1, 2, 4` (recomputed; `C_* = 4.646, 8.641, 13.524, 14.789`).  The epoch arithmetic used was checked
  numerically for 60 epochs (`r08_epochs.py`).
* *The nest:* beyond the brief's list I evaluated the nested design exactly with own code (note N8): `M = 1` at
  `n = 10³ … 1.6·10⁴` (`u = 1`), `2·10³, 4·10³` (`u = 2`); `M = 2` at `2·10³, 4·10³` and ("proof" variant) `8·10³`; `M = 3` at `4·10³` (one epoch more than
  the workstream): the report's table of §7.4 is reproduced to the last digit wherever recomputed, and the
  inequality of the induction holds at every one of about 729 000 nodes.

## 6. Proposition N (§5.4)

**Correct as stated** in what it claims as proved: the least accuracies fit (`𝔑_m` has least accuracy `b_m`; the slope
steps and the drop of epoch `m` are built with the tolerance `b_m`; `b_{m+1} = 𝒳_D^{b_m}(n; φ_m)`), the types are those of
Theorem A, and the cost formula is the unrolling with `q^{b_m}`, `ℓ₀^{b_m}`, `σ′(b_m + c_log + h)` and
`B̃ = max{1, b_mφ_m/(2u(1−φ_m))}B_m`.  The levels with tolerances are covered by my checks of Lemma U, D′ and Q6(e)
(`b` up to `17.3`); the formula reproduces the report's column (`(M, bound/na) = (5, 0.5758), (9, 0.3559), (12, 0.2900),
(16, 0.2714)` at `n = 10⁵ … 10⁸`).  The paragraph "What it gives" (`n·h + O(√n ln n)`, `b_M ≈ (3/8)(ln n)²/ln ρ`) is labelled
by the report as proved only up to the bookkeeping of `Λ̄`, with heuristic constants; I agree with the label and did
not go beyond it.  The variant was not evaluated as a nest (neither by the report nor by me).

## 7. Proposition Q6(e) and Corollary Q6(e)-max (§6)

**Both correct as stated** (note N5).  Checklist (in particular: `n_o < x̂/e ≤ n`; `2un_i > b` for `e ≤ 2u`; the threshold;
the range condition ⇔ `x̂ ≤ R′n`), the identity `n_iB + (1−σ)n_oϑ = nB − n_oeσ′`, both signs of `σ′`, the pass-through:
right.  `r04_built.py`: 85 626 cases at six rates on both sides of `h` and tolerances `1, 2.5, 17.3`: no violation,
least slack `4.1` nats.  The remarks of §6.2: 1, 3, 4, 5 are right; 2 is right with the two small provisos of finding 5.
The two reductions for images outside `0 ≤ σ ≤ 1` (slope `> 1` → slope one; slope `< 0` → the flat line `B − σ′R′`) keep
the common range `R′`, so the corollary can be iterated; they lose only in the form of the majorant.  As the report
says (§8, item 7), this gives levels, not a schedule.

## 8. The report's §9 (what it found wrong elsewhere)

* **Item 1 (`Q_REPORT.md` §6.2, "A `√n` remains in any case for this family of algorithms at a bounded accuracy"):
  the criticism is right.**  What Q's §2.3 shows is a `√`-loss for a bounded-threshold outer block of `Θ(n)` sites and
  for the plain two-sample bracket at a bounded accuracy (I measure `ln cost − d·a = 0.88√d` at `d = 6.4·10⁴`, accuracy `1`,
  `u = 1`).  It does not follow that the family of nested levels needs such a block: Proposition T reaches the
  accuracy `≤ 1` from the accuracy `≈ 2 ln n` with bounded-threshold blocks of `Θ(ln n)` sites, and Theorem A at `M = 0`
  gives `n·a + O(ln n + ln(1/ε̂))`.  With my own code the certified cost of that design is *below* `e^{n·a}`:
  `ln cost − N·a = −110` nats at `N = 1.6·10⁴` and `−574` at `6.4·10⁴` (the plain bracket: `+118`, `+223`).  (Like the
  report's, this is the certified bound `C_max`, not a simulation of runs.)
* Item 2: right — Q9a does bound `c_S(n, ·; B_m)` by `c_S(n, ·; a)`; with Q's own Q6 the constant would be
  `2√(5(1 + r̄)c₁) = 0.80·C_*` at `u = 1`, and with Corollary U1 `0.76·C_*`.
* Item 3 (a)–(d): right ((a) the induction needs uniform bounds on `P_cnt`, `P_M` along the chain; (b) the bottom
  term; (c) the horizon).  Items 4–6: nothing to add.

## 9. Replication (own code; all in `experiments/workstreams/Q2/review/`)

| script → output | what | result |
|---|---|---|
| `rlib.py`, `r00_selftest.py` | own tables (`|B|`, `E_r`, `T_m`, `κ`, `Γ̃`, `Γ″`), `r†`, `π†`, the constants of Theorem 11.56; against brute force for `m ≤ 150` | agree to `2·10^{-13}`; `κ`, `r†` exactly |
| `r01_lemmaU.py` | (U) and parts (b), (c): 973 668 levels, incl. maxima of lines and `R = ∞` with positive slopes | no violation; least slack `2.0`–`3.4` nats; negative control violates |
| `r01b_general.py` | (U) without the range condition, lines with different ranges: 108 360 levels | no violation; `3.3` |
| `r02_chain.py` | chains by exact recursion, 8 parameter sets × 4 blocks: 23 927 levels (claim (iii) at 3 631) | no violation; least slack `57.9`; report's rows reproduced |
| `r05_chain_stress.py` | 10 962 random chains off the design: 3 506 109 levels (claim (iii) at 323 001) | no violation; least slack `3.4` |
| `r06_base_chain.py` | `M = 0` design over the real base bracket, `N = 10³ … 6.4·10⁴` | `1.3190, 1.0067, 0.9381, 0.9191` (report: same) |
| `r03_formula.py` | (A.1), six rows of the table of §7.3 | reproduced |
| `r03b_closed_trap.py` | Proposition A′ (732 cases); the formula of §5.4 | no violation; column reproduced |
| `r04_built.py` | D′ and Q6(e) as built: 15 156 + 85 626 + 11 496 cases | no violation; least slack `4.1` |
| `r07_U1.py` | Corollary U1 on Q6 as built: 5 776 levels | no violation; `3.6` |
| `r08_epochs.py` | epoch arithmetic, 60 epochs, five slopes | holds |
| `r10_nest_M1.py`, `r11_nest_M.py` | the nested design exactly, `M = 1, 2, 3` (note N8) | report's §7.4 reproduced; no violation |
| workstream's `q2_01_levels.py`, `q2_03_formula.py` (re-run with `python3 -B`) | | identical to the stored outputs up to timing fields |

Memory: every process of this review stayed far below 1 GB (the largest resident size I observed for my own scripts was
`0.13` GB); every run below five minutes (two runs of `r11_nest_M.py` at `n = 8 000` were stopped by their own 285-second limit;
they are reported as unfinished in note N8).

## 10. What was not checked

* **Theorem 11.56 itself** (the algorithm, its events, the abort rule (P)), Lemma 11.55 and Proposition 11.57(a) as
  theorems, Harper's theorem, the Chernoff bounds, the Lean proofs behind (R): all taken as quoted.  My numerics
  evaluate the certified bound `C_max` from the formulas; **no run of the algorithm was simulated**.
* Of `Q_REPORT.md`: I re-derived Q1, Q2, Q4 (both parts), Q5(b), the constants of Q7(3) and the steps of the proof of Q6
  that Corollary U1 uses; Q3 and Q5(a) were checked on my own tables only (at every chain level / every bottom of a chain),
  not re-proved.
* The nest beyond `M = 3`, `n = 8·10³` (`M = 1`: `1.6·10⁴`), i.e. everywhere Theorem A says something new (`n ≳ 10⁶`):
  there the theorem rests on the paper induction, which I re-derived, and on the one-level and one-chain checks.
* Proposition N as a nest; `n₀`, `C′` of Theorem B (not explicit in the report); the remark (1) after Theorem A (mixtures
  with Q's drop; "not written out" in the report); remark (3) of §3 (a sketch); the heuristic on the hinted lower bound.
* The workstream's scripts `q2_02`, `q2_04`, `q2_05`, `q2_06` were not re-run (time and memory limits); their
  subject matter is covered by my own scripts except for the size of the samples.  The "old" column of the table of §7.3
  (formula (5.2) of Q) was not recomputed.  Slopes outside `u ∈ [0.2, 4]`.

---

# Working notes (appended as the review proceeds; the verdicts of §0 are final, these notes are the record)

## N1. Lemma U — line-by-line re-derivation (done on paper, first pass)

Constants of (T) at `λ = 1, η = ½, η′ = 1, ν₁ = 1` (re-derived from the formulas of Theorem 11.56 / Q §1.2):
`J = ⌈2un + b + n_o ln 2⌉`; `ν₀ = 2·max{(J+1)(e−1), 1} = 2(e−1)(J+1)`; `c_η = ⅓`; `M̄ = 6e·ν₀·K/π†`;
`P_M = ln(12e) + ln ν₀ + ln K = ln(J+1) + c₂₄ + ln K`; `P_cnt = ln(J+1) + ln(9e) + ln ν₀ + ln K = 2 ln(J+1) + c₁₈ + ln K`;
`Λ_lev = ln 2M̄ = P_M + ln(1/π†)`; `(J+1)·cnt(x) = e^{x + P_cnt}` for `x ≥ 0`.  All as the report says.

* (b) `J + 1 ≤ A_n^b`: ok (`n_o ≤ n`).  `m_max + 1 ≤ log₂(6e ν₀) + n_o + 3 ≤ m̄^b(n)`: ok (`n_o ≤ n − 1`).
  `L ≤ ⌈Ξ⌉ ≤ n`: ok (`b ≥ 1`: `⌈Ξ − b⌉ + 1 ≤ ⌈Ξ⌉`; `Ξ ≤ n`).  `K ≤ K̄^b(n, ln(1/δ))`: ok.
  `P_M + ln(n_o+1) ≤ 1 + P_cnt` ⇔ `n_o + 1 ≤ (3e/4)(J+1)`, and `J + 1 ≥ n_o ln 2 + 2`: ok (`1.41 n_o + 4.08`).
  (2.1): `ln(1/δ′) = ln(1/δ) + ln 2L + Λ_lev`, `Λ_lev ≤ P_M + (n_o+1) ln 2`: ok; so `ln(1/δ′) + n_i ln 2 ≤ Λ + q^b(n, Λ)`: ok.
* (c) Lemma Q4(b) with the corrected hypothesis `(1−η)ν₀ ≥ 1` (here `(e−1)(J+1) ≥ 1`), `c_η^{-1} = 3`: ok.
  `G ≤ n_o ϑ`: ok.
* (d) auxiliary inequality: three cases re-derived, uses `0 ≤ σ ≤ 1`: ok.  Rungs `l ≥ 2`: `x_l ≤ b + ⌈Ξ − b⌉ − 1 < Ξ ≤ R n_i`: ok.
  Rung 1 with the cap `⌈2un_i − b⌉ − 1` active: `x₀ ≤ x₁ + 1`, `x₁ < Ξ`: ok.  Rung 1 otherwise: `x₁ ≥ max(Ξ, b) ≥ G`,
  `R n_i ≥ Ξ ≥ G`, multiplier `≤ Λ_lev ≤ G + 1 + P_cnt`: ok (uses `σ ≥ 0`).  Outer sample: needs one line with
  `σ_i G ≤ n_i B_i + E₁`; obtained from `b_𝔉(n_i, y*, δ′) ≥ 0` (C2) at `y* = max(G, b)`: ok.
  The classification of the rungs does not depend on the line (common `R`), so the maximum over lines commutes: ok.
* Checklist (H1)–(H9): ok (`x_L = b`; `x₁ = b + k₁ < 2un_i`; inner accuracies `≥ b ≥ x_min`; no circularity:
  `δ′ = δ/(4LM̄)` does not depend on the inner costs).

First-pass verdict: **no error found in Lemma U** (statement and proof).  Numerical replication: §9 / N-notes below.

## N2. The coordinator's question (`R = ∞` with positive slopes) — worked answer

Go through the proof of Lemma U(d) with the type "`b_𝔉(d, x, δ) ≤ max_i[d·B_i − σ_i·x] + E(d, x; Λ)` for **all** `x ≥ x_min`",
`0 ≤ σ_i ≤ 1` (so `min(x, R·d)` is `x`):

* the auxiliary inequality `f(y) = min{Λ_lev, y + 1 + P_cnt} − σy ≤ (1−σ)G + 1 + P_cnt` does not involve the range;
* rungs with `x_{l−1} ≤ x_l + 1` (all `l ≥ 2`; `l = 1` when the cap `⌈2un_i − b⌉ − 1` is active): the term is
  `≤ f(x_l) + n_iB + E₁ ≤ V` — the condition "`x_l ≤ R n_i`" was only there to replace `min(x_l, Rn_i)` by `x_l`, and is void;
* rung `l = 1` otherwise: `x₁ = b + ⌈Ξ − b⌉₊ ≥ max(Ξ, b) ≥ G`, so the term is `≤ Λ_lev − σx₁ + n_iB + E₁ ≤ G + 1 + P_cnt − σG + n_iB + E₁ = V`;
  this needs only `Ξ ≥ G`, which follows from `Ξ ≥ n_oϑ` (part (c));
* the outer sample: one line with `σ_i·G ≤ n_iB_i + E₁` is needed.  A flat line (`σ_i = 0`) is such a line; in general the
  nonnegativity of the majorant at the single point `(n_i, y*)`, `y* = max(G, b)` — which (C2) gives — is enough, exactly as in the report.

So **yes: Lemma U holds verbatim, with the same proof, for `R = ∞` with slopes in `[0, 1]`**, with **any cap
`n_o·ϑ ≤ Ξ ≤ n`** (the upper bound only for `L ≤ n` in the constants; the natural choice is `Ξ = n_o·ϑ`, i.e. the first rung
`x₁ = b + min{⌈n_oϑ − b⌉₊, ⌈2un_i − b⌉ − 1}`), and (U) reads `ln C_max ≤ max_i[n_iB_i + (1−σ_i)n_oϑ] + ℓ₀^b + E(n, b; Λ + q^b)`.
The exclusion "all `σ_i = 0` if `R = ∞`" in (C3) is **not needed**; it is inherited from Q's definition for a single line (a single
line of positive slope and infinite range is negative for large `x` and is the type of no family).  What is needed is exactly
what the coordinator states: the maximum must be nonnegative — and only at `y* = max(G, b) ≤ max(n_oϑ, b)` in dimension `n_i`
(plus `E₁`).  Without it (U) is false: negative control in `r01_lemmaU.py`.

*A remark that makes this transparent (referee's; not in the report).*  The proof uses of the inner majorant
`T(x) := max_i[n_iB_i − σ_i·min(x, Rn_i)]` only that (1) `T` is nonincreasing and (2) `x + T(x)` is nondecreasing (slopes in
`[−1, 0]`).  For any such `T` on `[b, ∞)` with `ln C_l ≤ T(x_l) + E₁`, a step-one ladder from `b` up to a cap `Ξ ≥ n_oϑ`, and
`T(y*) + E₁ ≥ 0`:

    ln C_max ≤ ln(L+2) + 1 + P_cnt + E₁ + [ y* + T(y*) ]  ≤  ℓ₀^b + E₁ + [ Y + T(Y) ],      y* = max(G, b),  Y = max(n_oϑ, b)

(rungs `x_l ≤ y*`: `x_l + T(x_l) ≤ y* + T(y*)`; rungs `x_l > y*`: `Λ_lev + T(x_l) ≤ G + 1 + P_cnt + T(y*)`; first rung and outer sample
as above).  For lines, `Y + T(Y)` may be replaced by `max_i[n_iB_i + (1−σ_i)n_oϑ]` by the report's auxiliary inequality (which
extrapolates each line below `b`).  In this form **no range condition is needed at all**: with a finite common range `R` and
`n_oϑ > R·n_i` the bound is `max_i[n_iB_i + n_oϑ − σ_i·min(n_oϑ, R n_i)]`; the hypothesis `Ξ ≤ R·n_i` of Lemma U only serves to write
this as `(1−σ_i)n_oϑ`.  Lines with different ranges `R_i` are covered in the same way (`n_oϑ − σ_i·min(n_oϑ, R_in_i)`).

## N3. Replication with own code — results so far (scripts in `experiments/workstreams/Q2/review/`)

Own evaluator `rlib.py`: tables of the outer cube (`|B|`, `E_r`, `T_m`, `κ`, `Γ̃`, `Γ″`) in log-space, `r†`, `π†`, and the constants
`J, ν₀, m_max, K, M̄, δ′, cnt, C_max` from the formulas of `K_REPORT.md` §2.1–2.2 / Theorem 11.56; nothing imported from the
workstream.  `r00_selftest.py`: the tables agree with brute-force sums for `m ≤ 150` to `2·10^{-13}` (and `κ`, `r†` exactly).

* **(i) Lemma U** — `r01_lemmaU.py` → `out_r01_lemmaU.txt`: `u ∈ {½, 1, 2}`, `n = 2 … 40 000`, outer blocks from one site to `0.8n`,
  rates `e/h ∈ {0, ½, 1, 2}` and `e ∈ {0.97, 1.4}·ε*`, thresholds at the least value allowed and `e⁷` above it, tolerances
  `b ∈ {1, 3.7, 12}`, caps `Ξ ∈ {n_oϑ, R·n_i}` (finite `R`) resp. `{n_oϑ, 2n_oϑ + 5, n}` (`R = ∞`), `δ ∈ {0.5, 0.05, 10^{-12}, e^{-n}}`,
  error functions `0, 3√d, Λ/7, 5/x + ln Λ`; inner families saturating.
  **973 668 levels; 8.76 million checks of parts (b), (c); no violation.**  Least slack of (U):
  `3.32` nats (one line, finite `R`), `3.34` (maxima of two/three lines, finite `R`),
  **`2.45` (`R = ∞`, positive slopes, with a flat line; 244 512 levels)**,
  **`1.99` (`R = ∞`, positive slopes, no flat line but `B_i ≥ 2uσ_i`, so the majorant is `≥ 0` at every accuracy a level can ask; 108 672 levels)**.
  Negative control (`R = ∞`, one line of slope one with `B = a/2`, cost cut at `0` — a family that does *not* have the type):
  531 violations in 17 124 levels, up to `8 551` nats: the nonnegativity hypothesis is needed, as the report says.
* **(ii) Proposition T** — `r02_chain.py` → `out_r02_chain.txt`: eight parameter sets (`u ∈ {½, 1, 2}`, `B′ = a` and `B_e`,
  `e ∈ {2, 4, 8, 12}`, `α ∈ {1, 0.1, 0.01, 0.001}`, `N = 10⁴ … 10⁶`, `δ ∈ {0.5, 0.05, e^{-N}}`, three error functions), each with the block of
  the design (4.1) and blocks `½×`, `2×`, `1/7×`: **23 927 chain levels by exact recursion, the claim `t(d, δ) ≤ d·B′ + E_T(d; Λ)` checked (3 631 times)
  at the level's own `(d, δ)` (every level, or ≥ 150 per chain), parts (i), (ii) at every level: no violation; least slack `57.9` nats.**
  The report's rows of §7.2 are reproduced to the digit: `u = 1`, `B′ = a`, `N = 10⁶`: `m = 1099`, 909 levels, `c = 8.45·10^{-5}`,
  exact `126.62`, `A_T = 230.71`; `N = 10⁴`: `741`, 13, `81.74`, `160.65`; `u = 2`, `B′ = 0.302a`, `N = 10⁶`: `1119`, 893, `426.48`, `729.53`;
  `u = ½`, `B′ = a`: `3759`, 266, `111.70`, `181.07`.  (iv): `Δ_T = 0` and `Λ* − Λ = 0.49 … 0.63·N·B′` for the blocks of the design.
* **(iii) Formula (A.1)** — `r03_formula.py` → `out_r03_formula.txt`: written from the text of §5.2 with own formulas; `u = 1`, `ε = 1`,
  `δ = 0.05`, minimised over `M`: the rows `n = 10³, 10⁴, 10⁶, 10⁸, 10^{10}, 10^{12}` of the table of §7.3 are reproduced
  (`M`, `k_M`, bound, ratio, and the four parts of `𝓔′_M`: e.g. `10⁶`: `M = 9`, `k_M = 34`, `0.3581`, `[2.849]`, `6588 = 33 + 24×86 + 9×65 + 10×390`;
  `10⁸`: `17, 268, 0.2690, [1.636]`, `37122 = 42 + 250×98.5 + 17×84 + 18×613`).  `[bound(ε) − bound(1)]/ln(1/ε) = 24.7 … 25.0` at `10⁶`, `27.0` at `10⁸`.
* Constants: `C_* = 4.646, 8.641, 13.524, 14.789`, `C_*′ = 3.495, 6.560, 10.568, 12.286` at `u = ½, 1, 2, 4`; `w(c) ≤ 6c` on `(0, ⅓]`.

## N4. Proposition T — line-by-line re-derivation (paper)

* Design arithmetic: `j(d) = j(d−m) + 1` for `d ≥ d₀` (both cases `d − m ≥ d₀`, `d − m < d₀`): ok.  `j(d) ≤ (d − d₀)/m + 1 < N/m`
  because `d₀ > m`, so `j(d) ≤ N_T − 1`, `a_d ≤ α − w`, `b_d ≥ α̲`: ok.  `w(c) ≤ 6c` on `(0, ⅓]` (numerically; the report's `6.25c`
  is true), so `α̲ ≥ 0.538α`.
* Checklist: (H1) `d₀ ≥ m + 1`; (H2)–(H4) `c ≤ 1/13`; (H8) `d − m ≥ ⌊𝒳/(2u)⌋ + 1 > 𝒳/(2u)`, `𝒳 > 1 ≥ α > b_d`; (H9) the fine rung is
  the chain in dimension `d − m`, accuracy `≤ a_{d−m} = b_d` (or the base bracket at `α̲ ≤ b_d`): ok — the induction on `d` is
  well founded (the level in dimension `d` only uses the dimension `d − m`), so the unbounded length is not a problem.
* (i) accuracy: `e^{b_d}(e^c(1+c)/(1−c) + 2c) = e^{a_d − c}`; `(2p_u)^d ≤ 5c/6 ≤ 1 − e^{−c}` for `d ≥ d₀`, `c ≤ 1/13`: ok.
* (ii) constants (re-derived, not copied from Q7): `J + 1 ≤ ((2u + ln 2)d + 1 + 2c)/c ≤ A_d/c`; `ν₀ ≤ 1.5·max{1.2A_d/c, 2e^u m/c} ≤ ν̄_D`
  (`m ≤ d`); `m_max + 1 ≤ log₂(5.6ν̄_D) + m + 3 ≤ m̄_D` (`m ≤ d − 1`); `K ≤ K̄_D(d, ln(1/δ); c)` (`3(1+c) ≤ 4`, `L + 2 = 4 ≤ d + 4`);
  the numerical constants `5.6, 7.45, 11.17, 1.2` are the values at `c = ⅓` (`5.582, 7.443, 11.165, 1.187`): ok.
  Lemma Q3: `θ = c ≤ 2e^{u(m₀+2)}`, `ν₀ ≥ ν₁/(1−η) = 2e^u m/(θ(1−η))`, `u m₀ < u + ln((1+c)/(1−c)) ≤ u + 2.25c`: ok.
  (2.1) with `ln(4L) = ln 8`: ok.
* (iii) monotonicity of `q_T, a_T, e₀, Δ_T, F_d, Λ*, U` in `(d, Λ)`: ok (`P̄_M`, `P̄_cnt` are nondecreasing in `d`, `Λ`; `e₀` does not
  depend on `d`; `q_T ≥ 0`).  `Λ*(d − m, F_d(Λ)) = F_{d−m}^{j(d)−1}(F_d(Λ)) ≤ F_d^{j(d)}(Λ)`: ok.
  Base case `d < d₀`: `min{d ln 2, d a + E_base(d, α̲; Λ)} − dB′ ≤ e₀(Λ)` uses `B′ ≤ ln 2`, `d ≤ d₀ − 1`, `E_base` nondecreasing in `d`: ok.
  Step: `t ≤ ln 4 + max{Λ_lev + ln C₁, 𝒳 + P_cnt + ln C₂}` (Q1 with `L = 2`; `ln C₁ ≥ 0`): ok; first term `≤ dB′ + E(d, 𝒳; Λ*) + a_T(d, Λ*)`
  (`Λ₁ = F_d(Λ) ≤ Λ*` as `j(d) ≥ 1`): ok; second term by the induction hypothesis at `(d − m, δ′, Λ₁)`, legitimate because
  `Λ₁ ≥ ln(1/δ′) + (d − m) ln 2` by (ii): ok; `U ≤ E_T` since `E ≥ 0`: ok.
* (iv) `q_T < 𝒳 + P̄_cnt + ln 4` (as `P̄_cnt − P̄_M ≥ ln 39 − 0.41`, `𝒳 > 1`), `j(d)·m < d`, induction on the iterate: ok.
* Design rule (4.1): the right-hand side is nonincreasing in `m` (`c` is nondecreasing in `m`, `P̄_cnt` nonincreasing in `c`): ok;
  a least `m` always exists (possibly `m ≥ N`: then the chain has no level and the family is the base bracket at `α̲` — a
  legitimate, if useless, case; the report says so in §7.4(vi) only).
* Use in Theorem A: the type of the chain holds for *every* `(d, Λ)` with the deficit term; (4.1) is needed only at the
  point `(n, Λ̄)` at which the unrolled bound is evaluated, where it gives `Δ_T = 0`.  The blocks `m_e` are determined
  top-down (`m_M` from `Λ̄_0`, then `Λ̄`, then `m_{M−1}`, …): no circularity.

Paper verdict: **no error found in Proposition T**; the claim "a chain costs `A_T` once" is what (iii)+(iv) prove.

## N5. Corollary U1, Proposition D′, Proposition Q6(e), Corollary Q6(e)-max — paper checks

* **Corollary U1.**  The ladder of Q6 (`x₁ = min(⌈x̂⌉, ⌈2un_i⌉ − 1)`, step one down to `1`) is the ladder of Lemma U with `b = 1`, `Ξ = x̂`
  (`x̂ ≥ X₀(n) > 1`); `n_oh ≤ x̂ − 1 − c_log(n) ≤ x̂ ≤ R·n_i` (Q6, step (4)); `x̂ ≤ hn < n`; threshold by Q6 steps (1), (2).  (U) gives
  `nB − σ′n_oh + ℓ₀ + E₁`, `σ′ = σ + B/h − 1 ≥ 0` (as `B ≥ h`), and `n_oh ≥ x̂ − 1 − c_log − h`; pass-through `(σ′ − σ)x̂ ≤ σ′X₀(n)`: ok.
  `c_S − c_S′ = (1 − σ)(1 + c_log + h)`: ok.  **Correct as stated.**
* **Proposition D′.**  Hypotheses of Lemma U for the level as built: `n_o = ⌊φn⌋ ≥ 1`, `n_o ≤ φn < n`; `(2p_u)^n e^{−b} ≤ 1` so
  `θ ≥ e^{𝒳−b} − c₃ − 1 ≥ 3(φN + 1)e^{2u+e^u} ≥ 3(n_o + 1)e^{2u+e^u}`; `n_o a ≤ φna ≤ R(1−φ)n ≤ R n_i` (⇔ `φ ≤ R/(a+R)`), `R n_i ≤ n` (`R ≤ 1`);
  accuracy `ln[(2p_u)^n + e^b(c₃ + θ)] = 𝒳` exactly: ok.  Rounding: `n_iB_i + (1−σ_i)n_o a = n[(1−φ)B_i + (1−σ_i)φa] + τ[B_i − (1−σ_i)a]`,
  `τ ∈ [0, 1)`: ok.  Pass-through only needed for `φn < 1` or `n ≤ b/(2u(1−φ))`; `nφ ≤ max{1, bφ/(2u(1−φ))}`: ok.  The two displayed
  cases (`B′ = Ba/(a+R)`, `B̃ = max{1, R/(2ua)}B`; `B′ = [a/(a+R)](B + (1−σ)R)`): ok.  **Correct as stated.**
  Wording: remark (2) (`R > 1`) must also replace `ln(4(n+1))` by `ln(4A_n^b)` in `q^b` (it names `K̄^b`, `ℓ₀^b` only) and drop
  "`Ξ ≤ n`" from Lemma U; not used anywhere.  Remark (3) is a sketch, labelled as such, not reviewed.
* **Proposition Q6(e).**  Checklist: `n_o ≥ 1` (`x̂ ≥ X₀^e`); `n_o < x̂/e ≤ R′n/e ≤ n` (`R′ ≤ e`); `n_i ≥ (b + c_log)/e`, `2un_i > b` for `e ≤ 2u`;
  `e^{c_log(n)} = 6(n+1)e^{2u+e^u} > 2(c₃ + 1)` so `θ ≥ e^{x̂−b}/2 ≥ 3(n_o+1)e^{2u+e^u+n_oe}`; range condition
  `n_oϑ ≤ (x̂/e)ϑ ≤ R(n − x̂/e) ≤ Rn_i` ⇔ `x̂ ≤ R′n`: ok.  Type: `n_iB + (1−σ)n_oϑ = nB − n_oeσ′`; both signs of `σ′` handled
  (`σ′ ≥ 0`: `n_oe ≥ x̂ − b − c_log − e`; `σ′ < 0`: `n_oe ≤ x̂`); pass-through `σ′x̂ ≤ σ′₊X₀^e`: ok.  **Correct as stated**, with the
  caveat the report itself makes: the image `(B, σ′, R′)` is a *type* in the sense of the definition only if `σ′ ≥ 0`
  (and in the class of Lemma U only if `σ′ ≤ 1`); the proposition states the inequality, which is what is proved.
* **Corollary Q6(e)-max.**  Same level, (U) for the maximum, line by line; pass-through `nB_i ≤ [nB_i − σ_i′x̂] + σ′_{i,+}x̂`: ok.
  **Correct as stated.**  §6.2 remark 2 (the two reductions: `σ′ > 1` → slope one; `σ′ < 0` → the flat line `B − σ′R′`) is right;
  "possible for `e < h`" presupposes `B_i ≥ h`; "a type with range `R′` is a type with any smaller range" needs `σ ≥ 0`.
  *Extension (referee):* by N2 the corollary also holds for `R = ∞` with positive slopes (and a flat line, or (C2)),
  with `R′ = e` — the checklist needs no range condition then.  Note that the image has the *finite* range `R′ = e` in any
  case: "valid at all accuracies" is not preserved by one slope step at one rate.

## N6. More replication (own code)

* `r04_built.py` → `out_r04_built_u{0.5,1.0,2.0}.txt`: levels **as built**.  Proposition D′ (`b ∈ {1, 2.5, 17.3}`, horizons `N ∈ {n, 3n}`,
  schedule types, single lines, maxima; `n` from 2 to `10⁵`): 15 156 cases (4 904 pass-through only), **no violation**, least slack
  `4.1` nats; accuracy `= 𝒳` to `10^{-9}`, threshold, range condition, Lemma Q4(b), (2.1): 61 512 checklist items, no failure.
  The number of §3 is reproduced: `u = 1`, `n = 10⁶`, `φ_0`: `n_o = 208 013`, `r† = 56 920` (`p_un_o = 55 943`), `ln(1/π†) − n_oa = −959.3`.
  Proposition Q6(e)/Q6(e)-max (`e/h ∈ {0.2, 0.5, 1, 2, 3}`, `e = 0.97ε*`; `b ∈ {1, 2.5, 17.3}`; `n ≤ 10⁵`): 85 626 cases (47 726 pass-through
  only), **no violation**, least slack `4.1`; 257 980 checklist items, no failure.  Q6(e)-max for `R = ∞` with positive slopes and a
  flat line, `R′ = e` (the extension above): 11 496 cases, no violation, least slack `4.6`.
* `r06_base_chain.py` → `out_r06_base_chain.txt`: the design `M = 0` exactly — the chain over the **real** base bracket at the
  accuracy `𝒳_B(N)`, `u = 1`, `α = 1`: `ln cost/(N·a) = 1.3190, 1.0067, 0.9381, 0.9191` at `N = 10³, 4·10³, 1.6·10⁴, 6.4·10⁴` (`δ = 0.05`) —
  the report's `1.319, 1.007, 0.938, 0.919`; `ln cost − N·a = −110` at `1.6·10⁴` and `−574` at `6.4·10⁴`; the claim of Proposition T and the
  type of `𝔅` hold at every level (least slacks `106` and `35` nats).
* The workstream's `q2_01_levels.py` and `q2_03_formula.py` were re-run (`python3 -B`, outputs to the review directory,
  `out_ws_*`): identical to the stored outputs up to the timing fields.  No bytecode cache was written.
* `out_r09_plain_base.txt` (inline computation with `rlib.base_lcost`): the plain two-sample bracket at the accuracy `1`, `u = 1`,
  `δ = 0.05`: `ln cost − d·a = 37.4, 65.0, 117.9, 222.8, 432.2` at `d = 10³, 4·10³, 1.6·10⁴, 6.4·10⁴, 2.56·10⁵` (`1.18 … 0.85` times `√d`).

## N7. Further replication and stress tests (own code)

* `r05_chain_stress.py` → `out_r05_chain_stress.txt`: Proposition T **away from the design** — 200 s of random chains:
  `u ∈ {0.2, 0.5, 1, 2, 4}`, `N = 30 … 4000`, blocks `m` from **one site** to 600, `B′ ∈ {0.3h, h, (h+a)/2, a, (a + ln 2)/2, ln 2}`,
  `𝒳 ∈ {1.01, 3, 𝒳_B, 40}`, `α` down to `10^{-9}`, `δ` down to `e^{-50N}`, four error functions:
  **10 962 chains, 3 506 109 levels (parts (i), (ii) at every level; the claim (iii) at 323 001 levels — at least 40 evenly
  spaced levels per chain and the last three), no violation**; least slack of the claim `3.36` nats (`u = 4`, `m = 600`, the trivial `ϖ`
  attained); the bound for the bottom (`d·B′ + e₀`) is attained with equality in some cases (enumeration at `d = d₀ − 1`).
  So the induction of Proposition T has no hidden slack to hide an error: it is tight to 3 nats where `ϖ` is tight.
* `r07_U1.py` → `out_r07_U1.txt`: **Corollary U1** on the level of Q6 *as built* (ladder capped at `⌈x̂⌉`): 5 776 levels
  (types along 13 epochs and off the schedule, `n` up to `3·10⁵`, `δ` down to `e^{-50n}`): no violation of
  `ln C_max ≤ nB − σ′x̂ + σ′(1 + c_log + h) + ℓ₀ + E`; least slack `3.6` nats; `c_S − c_S′` up to `26.9` nats.
* `r01b_general.py` → `out_r01b_general.txt`: the generalised form of (U) of note N2 **without the range condition** (levels with
  `n_oϑ > R·n_i`, lines with different ranges `R_i`, cap `Ξ = n_oϑ`): 108 360 levels, no violation; least slack `3.3` nats.
* `r03b_closed_trap.py` → `out_r03b_closed_trap.txt`: Proposition A′ — in all 732 of 902 cases in which its hypothesis holds
  (`u ∈ {½, 1, 2}`, `n = 10³ … 10^{10}`, `M ≤ 25`, `ε ∈ {1, 10^{-3}}`): `Λ̄_end ≤ (M+3)Λ̄_0` and (A.1) ≤ first closed form ≤ second closed form
  (the closed form is up to `17.3×` (A.1), as the report says).  The formula of §5.4 (no chains): `(M, bound/na) = (5, 0.5758), (9, 0.3559),
  (12, 0.2900), (16, 0.2714)` at `n = 10⁵, 10⁶, 10⁷, 10⁸` — the report's column.
* `r08_epochs.py` → `out_r08_epochs.txt`: the epoch arithmetic used by Proposition A′ and Theorem B (60 epochs, `u ∈ {¼, ½, 1, 2, 4}`):
  `d_m ≤ J_m < d_m + 1`, `B_{m+1} = (1 − φ_m)B_m`, `B_m − h ≤ c₁/(k_m + c₂)` (ratio ≤ 0.85), `k_{m+1} < (1 + r̄)k_m` (ratio ≤ 3.0),
  `J_m(J_m+1)/(2d_m) < J_m/2 + a/h`, `M ≤ 1 + ln(k_M + 1)/ln(1 + κ)`, `c₂ ≥ 0`: all hold.

## N8. The nested design of Theorem A, exactly, with own code (beyond the brief's list)

`r10_nest_M1.py`, `r11_nest_M.py` (own evaluator, the real base brackets inside, every level with its own failure
probability; on every node the inequality of the induction with the error functions of §§2–5; no caching of families):
the design `𝔊_M(n, 0.8715, 0.05)` for the epochs with one slope step (`J_m = 1`: `m ≤ 2` at `u = 1`).
In units of `n·a`: "proof" (the level whenever built) / "min" (the families as defined) / bound of Theorem A.

| `u` | `n` | `M` | referee: proof / min / bound | report §7.4 | node checks (both variants), violations |
|---|---|---|---|---|---|
| 1 | 1 000 | 1 | 1.9950 / 1.8872 / 4.4747 | 1.995 / 1.887 / 4.475 | 46, 0 |
| 1 | 2 000 | 1 | 1.6090 / 1.5205 / 2.7627 | 1.609 / 1.521 / 2.763 | 410, 0 |
| 1 | 4 000 | 1 | 1.2634 / 1.1955 / 1.8436 | 1.263 / 1.196 / 1.844 | 3 246, 0 |
| 1 | 8 000 | 1 | 1.0154 / 0.9885 / 1.3538 | 1.015 / 0.989 / 1.354 | 22 607, 0 |
| 2 | 2 000 | 1 | 1.1057 / 1.0746 / 1.4539 | 1.106 / 1.075 / 1.454 | 9 237, 0 |
| 2 | 4 000 | 1 | 0.9215 / 0.9024 / 1.1354 | 0.922 / 0.902 / 1.135 | 64 077, 0 |
| 1 | 2 000 | 2 | 1.9531 / 1.8101 / 3.9086 | 1.953 / 1.810 / 3.909 | 1 047, 0 |
| 1 | 4 000 | 2 | 1.5261 / 1.4138 / 2.3774 | 1.526 / 1.414 / 2.377 | 64 517, 0 |
| 1 | 4 000 | **3** | 1.7108 / 1.5990 / 2.9910 | (not in the report) | 92 391, 0 |
| 1 | 8 000 | 2 | 1.1025 / (stopped) / 1.5615 | 1.103 / 1.055 / 1.562 | 315 321 ("proof" only), 0 |
| 1 | 16 000 | 1 | 0.8699 / 0.8576 / 1.0895 | 0.870 / 0.858 / 1.090 | 156 316, 0 |

(Two runs were stopped by their 285-second limit: the "min" variant of `M = 2`, `n = 8 000`, and `M = 3`, `n = 8 000`.)
**Every number of the report's table that I recomputed agrees to the last digit shown, and no inequality of the
induction is violated on about 729 000 node checks**; least slack of the induction: `5.3` nats (the type of `𝔅`, Q5(b)),
`60`–`126` (chains), `81`–`175` (slope steps), `141`+ (drops).  `M = 3` goes one epoch beyond what the workstream evaluated.
Outputs: `out_r10_nest_M1_{a,b,c}.txt`, `out_r11_nest_M_{a,…,f}.txt`.  Small sizes (`out_r11_nest_small.txt`): `n ∈ {1, 2, 3, 7, 30, 100,
300, 700}`, `M = 1, 2, 3`, both variants: no violation; for `n ≤ 300` the chains have no level and the design is the base
bracket at `α̲` (enumeration, `n ln 2`, for `n ≤ 30`), as the report says in §7.4(vi).
