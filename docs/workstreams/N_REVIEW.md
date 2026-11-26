# Internal review of `docs/workstreams/N_REPORT.md`

*AI referee (internal review, adversarial; not external peer review), 2026-11-26.
Brief: `docs/workstreams/N_review_brief.md`.  Own scripts and outputs:
`experiments/workstreams/N/review/`.  Verdict vocabulary: **correct as stated** /
**correct after a repair** / **gap** / **wrong**.*

Status of this file: complete.  Sections follow the brief's order of priority (§1 Theorem N1; §2 the
obstructions; §3 Theorem N4; §4 the other statements; §5 instances; §6 the table; §7 literature).

## 0. Summary of verdicts

| statement | verdict |
|---|---|
| **Theorem N1** | **correct as stated** — every step re-derived (§1.1); the Chernoff events at the fixed pairs `(j, M)` suffice to apply (TU), (TL) at the random `q`, `p̲`; the cube's constants are reproduced (§1.2); own implementation: 512 runs, no violation |
| Lemma N.0 (used by N9, N3, N4) | correct after a repair: `Ξ_ρ(1) := +∞` |
| **Theorem N9** | **correct as stated** (formulas derived and checked to `10⁻¹³`; exactness checked) |
| **Proposition N10** | (b) **correct as stated**, as a bound on the outer *points* (not queries; needs "valid tail functions"); (a) the inequality is trivial and right, it concerns the cost *bound* only, and its premise is a transposition of Corollary N5 that is not written out |
| **Proposition N11** | **correct as stated** (one skipped sign argument supplied in §2.3) |
| **Proposition N12** | **correct as stated**; false bracket reproduced with own code (120/120 runs) |
| **Proposition N13** | **correct after a repair**: the proof of (a) covers sure certificates only — the step for randomised procedures is in §2.5; (c) is true only in a weaker form |
| **Theorem N4** | **correct as stated** (formula for `ι` and attainment checked numerically) |
| Theorem N1′ | correct as stated (negligible branch now exercised: §4.1) |
| Proposition N2 | correct as stated |
| Theorem N3 | correct as stated |
| Corollary N5 | correct as stated (definition of a scale family should bound `c_ref`, `C₀`) |
| **Proposition N6** | **gap** — a sound plan by substitution into Proposition E, not a proof; two missing pieces named in §4.5 |
| Proposition N7 | correct as stated; **the interpretation of (c) in §3.1/§4(e) is wrong about the algorithm** (§4.6) |
| Proposition N8 | correct as stated |

**Errors and gaps found, most serious first.**

1. **§3.1, §4(e), row 8 — the transport tail function (wrong as a statement about the algorithm).**  "At every
   accuracy rate below `0.589u` Algorithm A does not close with it before the atom" and "the exponent of the
   level is `ln 2`" confuse the closing level `π†` of Theorem N1 (a supremum over all smaller `q`) with what the
   run does.  Counterexample: `Q_30`, `Q_60`, `u = 1`, threshold rates `0.50` (the report's own example) and `0.30`:
   `π_* = 2^{−m}`, `M̄ = 5.7·10¹⁴` resp. `1.3·10²⁴`, and the run closes — validly — with `888 … 3 552` resp. `976` points.  True statement (with `Θ = id`): below the
   rate `u²/8` (hence below `ε*`) no closure before the atom; above it — for `m` large, the finite-`m` threshold is
   `≈ u²/8 + 0.589u/√m` — closure at once.  §4.6.
2. **§6, the table.**  Rows 7 and 25 carry "P" and rows 21 (lower bound) and 22 carry "E" without evidence (the
   rows themselves say "not known"/"open"); rows 1 and 9 lack "X"; row 2 and the paragraph "(2)" call (F2) "the
   only"/"the one" hypothesis whose failure gives a false certificate, which contradicts the report's own audit
   ((TL), `ℓ₀`, `V_max`/`u₀`, the inner brackets and the sampling law are validity hypotheses as well).  §6.
3. **Proposition N6 is not a proof** (as the report says of its weakest link), and two things are missing even
   from the plan: the scale family must give `Ξ_d` as a tail function of the class itself (base family), and
   Proposition E(b) yields `h + η`, not `θ_hint(ξ) + η` (needs E(a), (R) and the Lipschitz continuity of
   `θ_hint`).  §4.5.
4. **Proposition N13(a)**: the impossibility argument is for certificates that are valid for every consistent
   instance; for procedures with failure probability `δ` a two-line argument with one fixed alternative is
   needed (given).  §2.5.
5. **Proposition N10**: (b) bounds points drawn; with a rung 0 that uses the reference query only (allowed by
   (S4)) my runs draw `6.9·10⁶` points and make `5.6·10³` queries.  The sentence "the worst case of a level is
   never below the base family's" holds for one query per outer point (Theorem N3's bracket) and for `n_o ≫ L²`.
   (a) is about the bound, not the algorithm.  §2.2.
6. **Theorem N9, profile paragraph, and row 9**: closing at `t = L + O(1)` at a bounded threshold needs
   `ν₁ ≳ L/θ` in Theorem N1′ (the workstream's runs used `ν₁ = 4`, unstated); with `ν₁ = 1`, `L = 2.5`, `θ = ½` the
   closing level is `3.6·10⁻¹³`, not `1.3·10⁻³`.  §2.1.
7. **Lemma N.0 and Lemma N16 at `q = 1`**: the formulas give finite values there; `Ξ(1) = +∞` must be imposed
   (the code does).  §2.1.
8. Minor: N12(d) prose ("the bulk has `V ≤ 1.2·10⁻⁷`" holds for `|a| ≤ 9` only; with the true class the runs end by
   rule (c0), they do not "close at the atom"; the "mechanism … iff" is a heuristic); N11's numerical range
   "0.94 to 0.9999" is specific to its triples (`0.839` at `(3, 3, 165)`); (R5) is not a case of Theorem N1.

**No error was found in Theorems N1, N1′, N3, N4, N9, Propositions N2, N7, N8, N11, N12, Corollary N5.**

## 1. Theorem N1 (abstract level theorem), §2.2–2.4

*(own re-derivation of every step from the algorithm text of §2.2 of the report; the comparison with
`K_REPORT.md` and Theorem 11.56 is in §1.2, the verdict in §1.3)*

### 1.1 Step-by-step check

* **Good event, probability.**  Thresholds `s_j = κ₀ℓ₀e^{jλ}`, `s_je^{−b}`, `s_je^{−x_l}` are deterministic by (S3),
  the outer points are i.i.d., so `X_t(M) ~ Bin(M, p(t))` for each fixed `(t, M)`.  (V2): if `Mp > K/(1−η)` then
  `P(X < (1−η)Mp) ≤ e^{−η²Mp/2} ≤ e^{−η²K/(2(1−η))} ≤ e^{−η²K/(3(1+η))}`.  (V3): if `Mp ≥ K/(1+η)` then
  `P(X > (1+η)Mp) ≤ e^{−η²Mp/(2+η)} ≤ e^{−η²K/((1+η)(2+η))} ≤ e^{−η²K/(3(1+η))}` (`η ≤ 1`); if `Mp < K/(1+η)`,
  monotonicity in `p` reduces `P(X ≥ K)` to the previous case at `p′ = K/((1+η)M) ≤ 1`.  Count
  `(J+1)(m_max+1)·[1 + (L+1)] = (J+1)(m_max+1)(L+2)`: with the stated `K` the total is `≤ δ/2`.  (V1):
  `L·K2^{m_max}·δ′ < 2LM̄·δ/(4LM̄) = δ/2` because `K2^{m_max} < 2M̄`.  **Correct.**
* **Is the Chernoff event enough to apply (TU) at the random `q`?  Yes.**  (TU) is a deterministic implication for
  every pair `(s, q)`; (V2) is a finite family of events indexed by the *deterministic* pairs `(j, M)`,
  `M ∈ {K2^m}`, and on it the realised `q = max(N,K)/((1−η)M)` satisfies `p(s_j) ≤ q` (either `Mp ≤ K/(1−η)`, or
  `p ≤ X_{s_j}(M)/((1−η)M) ≤ N/((1−η)M)`, using `X_{s_j}(M) ≤ N` from Step 1 on (V1)).  (TU) is then applied
  pointwise in `ω` at the pair `(s_j, q(ω))`.  No uniformity over `q` beyond the finite union over `(j, M)` is
  needed, and none over `s` because the ladder is fixed in advance.  The same for (TL) at `(s_je^{−b}, p̲(ω))`:
  `N ≥ K ⟹ X_{s_je^{−b}}(M) ≥ K ⟹ p(s_je^{−b}) ≥ N/((1+η)M) = p̲` by (V3), and `p̄ ≥ p`.
* **Step 1.**  Correct (rung `L` has ratio `≤ e^{x_L} ≤ e^b`; intersection of valid brackets is valid with ratio at
  most that of the last; high ⟹ `L_i > s_je^{−b}`).
* **Step 3.**  Correct: `A = ∫₀^∞p ≤ s₀ + Σ_{i<j}(s_{i+1}−s_i)p(s_i) + E(V−s_j)₊`; lower end by disjointness of
  `(t_{i−1}, t_i]`, `t_i − t_{i−1} = (1−e^{−λ})e^{−b}s_i`.
* **Step 4 (width, every run).**  Re-derived: populated `(s_{i+1}−s_i)q_i ≤ c_η^{−1}e^{λ+b}·(1−e^{−λ})e^{−b}s_ip̲_i`;
  negligible `(s_{i+1}−s_i)q_i ≤ (e^λ−1)e^bℓ_i/((1−η)ν₀) ≤ η′e^bℓ/(J+1)`; at most `J` levels are left.  Sum:
  `U ≤ L·[κ₀ + e^b(c_η^{−1}e^λ + η′ + θ)]`.  **Correct**, and it uses nothing random.  (Within a level `ℓ` is
  changed only in a populated pass, which ends the level; so `ℓ = ℓ_j` in every unpopulated pass — used tacitly
  in Steps 4, 5.)
* **Step 5 (closing level, every run).**  Negligible exit: `q ≤ K/((1−η)M) ≤ e^bℓ_j/((1−η)ν₀s_j)` and failed test
  give `Ξ(q) > θ(1−η)ν₀q`.  Populated exit: `c_ηq ≤ p̲`, `s_je^{−b}Θ̄(p̲) ≤ ℓ` after (b), failed test gives
  `Ξ(q) > θΘ̄(p̲) ≥ θΘ̄(c_ηq)` — uses that `Θ̄` is nondecreasing (it is part of the definition of a lower tail
  function).  Both contradict [N] ∧ [P] unless `q ≥ π_*`.  **Correct.**  The two conditions are exactly what the
  two exits need; neither can be dropped (a negligible exit only tests [N], a populated one only [P]).
* **Step 6.**  Re-derived all three cases (`M₀^neg = νκ₀e^{−b}`; after negligible `≤ e^λM†`; after populated
  `≤ νe^λ/(c_ηπ_*) = (1+η)e^λν₀M†`); `M ≤ max{K, 2M_j^neg} ≤ M̄ ≤ K2^{m_max}`.  **Correct.**
* **Step 7.**  Correct (uses `(1−η)ν₀ ≥ ν₁ ≥ 1` in the negligible case, `κ₀ ≤ 1` in the case `s_je^{−x} < s₀`);
  the count: `(1+η)M_jp(t) ≤ (1+η)max{K, 2c_η^{−1}e^λνe^x} ≤ cnt(x)`.
* **Steps 8, 9, abort rule.**  Correct.  On `𝒢` none of the four abort conditions can occur (count: Step 8 gives
  `c_ref + M̄C₀ + Σ_l min{M̄,(J+1)cnt(x_{l−1})}C_l ≤ C_max`; rung `L`: Step 1; `M`: Step 6; `L > U`: validity).  Off
  `𝒢` the abort bracket `[ℓ₀, V_max]` is true but its ratio is not `e^{x_out}`; the theorem only claims the
  ratio outside probability `δ`, so this is consistent.

*Own simulation of the theorem* (`review/r6_theorem_n1_cube.py`; my implementation of §2.2, not the workstream's):
512 runs on `Q_{10} … Q_{13}` with radial `u`-Lipschitz outer integrands (flat, cone, anticone, dips, random,
bulk + spike), Harper's two functions, bounded / small / extensive thresholds, `η ∈ {½, ¼}`, `κ₀ ∈ {1, (2p_u)^m}`:
no abort, every bracket valid and within `e^{x_out}`, every sampled certificate true, (V2), (V3) hold on every
realised sample, `q_j ≥ π_*` at each of the 12 149 levels left (261 of them negligible), `M ≤ M̄`, stop at a level
`≤ J`; the count (v) — `M_j^neg·p(s_je^{−x}) ≤ c_η^{−1}e^λνe^x` for seven values of `x`, and at most `cnt(x_l)` points
above `s_je^{−x_l}` — holds at all 12 629 levels reached.  (In 8 runs with `κ₀ = (2p_u)^m` and `2um/λ` an integer, `s_J = V_max` exactly and my floating-point
comparison resolved rule (c0) one level late — the "structural tie" the report mentions in §7.3; not a
discrepancy.)

### 1.2 Comparison with Theorem K1 / Theorem 11.56

I read `K_REPORT.md` §§1.2–1.3, 2.1–2.4, 3.1–3.3 and the statement and proof sketch of Theorem 11.56 in the theory
report.  The proof of Theorem N1 is the proof of Theorem K1 with these and only these changes: Lemma K.1(a) → (TU)
with `Ξ`; Lemma K.1(b) and Markov → (TL) with `Θ̄ = max{id, Θ}`; `(2p_u)^n → κ₀`; the termination argument of K1's
Step 9 (atoms) → rule (c0); the minimal-radius inequality (2.3) of K1's Step 5 is not needed because `Ξ` is
evaluated at `q` itself.  Nothing else in K1's nine steps uses the cube; I confirm the audit's claim on this point.

*The cube's constants.*  With `Ξ(q) = 2^{−n_o}E_{r(q)}` (`0` below the atom, `+∞` at `r(q) = n_o`) and
`Θ(p) = 2^{−n_o}T(k(p))`, the algorithm's steps (b), (c) are literally those of Algorithm 2L⁺.  The closing
conditions: on the step `q ∈ (|B(r−1)|, |B(r)|]·2^{−n_o}`, `Ξ` is constant and the right-hand sides of [N], [P]
are nondecreasing and right-continuous at the left end, so [N] holds on the whole step iff
`E_r ≤ θ(1−η)ν₀|B(r−1)|`, i.e. `Γ̃(r) ≤ θ(1−η)ν₀`, and [P] iff `E_r ≤ θ·max{c_η|B(r−1)|, T(κ(r))}`, i.e.
`min{Γ̃(r)/c_η, Γ″(r)} ≤ θ` (`k(c_ηq) → κ(r)` as `q ↓ |B(r−1)|2^{−n_o}` because `x ↦ max{k : |B(k)| ≤ max(1,x)}` is
right-continuous); at `r = 0` the step is the single point `q = 2^{−n_o}` and the same holds with `Γ̃(0) = e^u − 1`,
`κ(0) = 0`.  Hence `sup π_* = 2^{−n_o}|B(r†)|` for `r† ≥ 0` and `2^{−n_o}` for `r† = −1` (K1 uses the admissible
smaller value `2^{−n_o−1}`).  With `J := J_K` all constants coincide by inspection of the formulas; the
workstream's script `n2_cube_constants.py` (which I re-ran: output identical to the stored one) confirms it on
ten parameter sets against workstream Q's independent evaluator.  **The claim "the cube comes out as the special
case with the constants of Theorem 11.56" is correct.**

### 1.3 Verdict and remarks on the statement

**Verdict: Theorem N1 is correct as stated.**

Remarks (wording, none affects the theorem):

1. (R5) is not a case of the theorem: with `Ξ ≡ +∞` no `π_* > 0` is admissible, so `m_max`, `K`, `δ′` are undefined.
   The claim "`M ≤ max{K, 2ν(V_max/ℓ₀)e^{−b}}` in every run" is true, but then `K` has to be defined from this cap.
2. The closing level is a supremum over **all smaller** `q` (claim (iii) is about levels that are *left*).  For a
   tail function whose ratios `Ξ(q)/q`, `Ξ(q)/Θ̄(c_ηq)` are not monotone it can be astronomically smaller than the
   `q` at which runs actually close (§4.6 below: transport bound, `M̄ = 10²⁴` against 976 points).  The report's
   §3.1/§4(e) draw a conclusion about the algorithm from it that is not right.
3. Lemma N.0 needs `Ξ_ρ(1) = +∞` (§2.1 above); Lemma N16's formula likewise (at `q = 1` it gives `e^R − 1 < ∞`).
4. The sentence in §6 "(F2) — the one hypothesis whose failure produces a false certificate" contradicts the
   audit of §1 and the proof: validity also uses (TL) (a too large `Θ` makes `ℓ > A`), the reference data
   (`ℓ₀ ≤ A`, `V ≤ V_max` resp. `A ≤ u₀`), the validity of the inner brackets under the right law, and sampling from
   `μ_o`.  (F2) is the *structural* hypothesis on the class whose silent failure gives a false certificate.
5. The theorem allows a rung 0 that costs no query (only "at most `C₀`"); this matters for the reading of
   Proposition N10(b) (§2.2).

## 2. Obstructions, §5

### 2.1 Theorem N9

**Verdict: correct as stated** (given the Gaussian isoperimetric inequality, which is quoted correctly, §7).

*Own derivation.*  For `V` with `−ln V` `L`-Lipschitz, `D = {V > s}` (open, `γ(D) ≤ q < 1`, so `Dᶜ ≠ ∅` is closed) and
`g = dist(·, Dᶜ)`: `V − s ≤ s(e^{Lg} − 1)` on `D`; `∫(e^{Lg} − 1)dγ = ∫₀^∞Le^{Lr}γ{g > r}dr`, and
`{g > r} = (Dᶜ + rB̄₂)ᶜ` has measure `≤ 1 − Φ(Φ^{−1}(γ(Dᶜ)) + r) ≤ Φ(−t − r)` with `t = Φ^{−1}(1−q)`.  Integrating by
parts, `∫₀^∞Le^{Lr}Φ(−t−r)dr = −Φ(−t) + ∫_t^∞e^{L(y−t)}φ(y)dy = e^{L²/2−Lt}Φ(L−t) − Φ(−t)`.  ✓.  Lower function:
`min(V,s) ≥ s·e^{−L·dist(·,S)}`, `∫e^{−Lg}dγ = ∫₀^∞Le^{−Lr}γ(S + rB̄₂)dr ≥ ∫₀^∞Le^{−Lr}Φ(c+r)dr = Φ(c) +
∫_c^∞e^{−L(y−c)}φ(y)dy = p + e^{Lc+L²/2}Φ(−c−L)`.  ✓.  Both are attained by the half-space dips named in the theorem
(direct integration), so they are the least/greatest tail functions of the class, and they do not depend on `n`.
`Ξ_L(1) = +∞`, `Ξ_L`, `Θ_L` nondecreasing, `Θ_L ≤ 1`: the formal requirements of §2.1 hold.

*Profile paragraph.*  `1 + Ξ_L(q)/q = e^{L²/2−Lt}Φ(L−t)/Φ(−t)`.  Upper bound `3(1+t)e^{(L−t)₊²/2}`: for `t ≤ L` from
`Φ(L−t) ≤ 1` and the Mills bound `Φ(−t) ≥ e^{−t²/2}/(3(1+t))` (which holds: `Φ(−t) ≥ 2φ(t)/(t + √(t²+4))` and
`√(2π)(t + √(t²+4)) ≤ 5.02(1+t)`); for `t > L` the exponent cancels exactly and the bound is `(3/2)(1+t)`.  Lower
bound `e^{(L−t)²/2}` on `[0, L]`: ✓.  `Θ_hint(e) = (L/2 − e/L)²/2`, `Θ_na(X) = (L − √(2X))₊²/2`: ✓ (inverse of
`w(Θ) = L²/2 − L√(2Θ)`, resp. of `w + id = (L − √(2Θ))²/2`).  `Ξ_L(q)/q ~ L/(t−L)` as `t → ∞`: ✓ (numerically
`0.0713` against `0.0714` at `L = 2`, `t = 30`).  The sentence on [P] at a bounded threshold is labelled [sketch]
and is plausible (`Ξ_L/Θ_L(c_ηq) ≤ c_η^{−1}e^{−(t−L)²/2}` for `t > L`, up to the shift of `t` by `ln(1/c_η)/t`).
One thing the paragraph does not say: the *other* closing condition, `Ξ(q) ≤ θν₁q` of Theorem N1′ (or [N]), needs
`L/(t−L) ≲ θν₁`, i.e. `t − L ≳ L/(θν₁)` — at a bounded `θ` with `ν₁ = 1` this is `t = L(1 + 1/θ)`, a closing level
`e^{−L²(1+1/θ)²/2}` whose exponent is *not* `L²/2`; in my run with `L = 2.5`, `θ = ½`, `ν₁ = 1` the closing level is
`3.6·10⁻¹³` (`t − L = 4.68`).  The quoted `π_* = 0.0013` for `L = 2.5`, `θ = ½` therefore presupposes `ν₁ ≥ 3.7`
(`Ξ_L(q)/q = 1.86` there).  With `ν₁ ≍ L/θ` — the analogue of `ν₁ = 2e^un_o/θ` in Theorem K2 — the closing level is
`t = L + O(1)`, at a polynomial price in `K`.  This should be said where "the analogue of the `O(√m)` of Lemma
11.55" is claimed (and in row 9 of the table).

*Numerical* (`review/r2_gauss.py`, G-A…G-D): closed forms against quadrature, 30 pairs, relative difference
`≤ 9.5·10⁻¹⁴`; (TU), (TL) for 400 random piecewise-linear `L`-Lipschitz functions on `ℝ`, exact integration, 8 173
levels: largest `E(V−s)₊/(sΞ_L)` `= 1.0000000000`, smallest `E min(V,s)/(sΘ_L)` `= 1.0000000000` (equality at
half-lines, never beyond); dips on balls, complements of balls (`n = 2 … 50`) and strips: `≤ 0.871` of `Ξ_L`
(upper), `≥ 1.000001` of `Θ_L` (lower); the two profile inequalities on 24 060 pairs `(L, t)`: no violation.

**Lemma N.0, on which it rests: correct after a one-word repair.**  The proof is right.  The formula
`Ξ_ρ(q) = sup{… : μ(D) ≤ q, D ≠ X}` is not a tail function at `q = 1` on a space where the supremum is finite
(every finite space): for `s < inf V` the set `{V > s}` is `X`, which the supremum excludes, and
`E(V−s)₊ = A − s` is not bounded by `s·Ξ_ρ(1)`.  The lemma must set `Ξ_ρ(1) := +∞` (as §2.1 says in general, and as
`nlib.envelope_tails` does: its last step has the value `INF`).  Consequence if overlooked: a pass with `q = 1`
could close.  Not an error of the workstream's code.

### 2.2 Proposition N10

**Verdict: (a) correct, but it is a statement about the cost bound only, and its first sentence is a
transposition, not a proof; (b) correct as stated — as a bound on the number of outer points drawn — with two
qualifiers that should be in the statement.**

(a) The inequality `inf_B sup_{γ≥B}[min(γ, Θ_na(G−B)) + T(γ)] ≥ max{Θ_na(G), T(G−0)}` is trivial and right
(`γ → ∞` gives `Θ_na(G−B) ≥ Θ_na(G)`; `γ = B` gives `T(B) ≥ T(G−0)`), for every nonincreasing `T ≥ 0`.  That
"the exponent of a level is `sup_{γ≥B}[min(γ, Θ_na(G−B)) + T(γ)]`, without factors `φ`, `1−φ`" is the right reading of
claim (vi) of Theorem N1 here: the outer tail function is `Ξ_L` whatever `n_o` is (the worst outer integrand,
`ψ = ψ(a)`, is `L`-Lipschitz), the closing level for a threshold `e^{G−B}` is `e^{−Θ_na(G−B)}` up to `poly(L)`
(profile inequalities of Theorem N9), `cnt(x) ∝ e^x`, and the inner class is the full `L`-Lipschitz class of
`ℝ^{n_i}`.  It is, however, not "the computation of Corollary N5": that corollary is about a scale family with
`n → ∞`; here the large parameter is `L²/2` and the family is not a scale family (its tail function does not
scale).  The asymptotic statement in `L` is not written out (what `o(·)` means, which of `G, B, γ` scale with
`L²`).  I regard (a) as a correct heuristic computation of the *bound*; nothing depends on it, because (b) is
the real statement.  **(a) says nothing about the algorithm**: the supremum treats the worst outer integrand and
the worst fibres as if they occurred together, which a single `L`-Lipschitz `ψ` cannot do
(`|∇_aψ|² + |∇_bψ|² ≤ L²`).

(b) Checked from (R7).  (R7) itself is right: on `𝒢`, `L ≥ e^{−x_out}A`; every populated level has
`p(t_i) ≥ p̲_i ≥ K/((1+η)M_max)`, so `t_i ≤ t* := sup{t : p(t) ≥ K/((1+η)M_max)}`; `Σ ≤ ∫₀^{t*}p = E min(V,t*)` and
every raised value of `ℓ` is `≤ E min(V, t_i)` by (TL); hence `e^{−x_out}A ≤ max{ℓ₀, E min(V,t*)}`, so `t* ≥ t_x`
when `ℓ₀ < e^{−x_out}A`, and `p(t_x − 0) ≥ K/((1+η)M_max)`.  For `V = e^{La₁}`:
`E min(V, e^{Lt}) = A[Φ(t−L) + e^{Lt−L²/2}Φ(−t)] ≤ Ae^{−(L−t)²/2}` on `[0, L]` (two applications of
`Φ(−x) ≤ ½e^{−x²/2}`), so `t_x ≥ L − √(2x_out) > 0` and `p(t_x − 0) ≤ ½e^{−(L−√(2x_out))²/2}`.  ✓.
Numerically (`r2_gauss.py` G-E): the inequality on 5 050 pairs; the exact root `t_x` against `L − √(2x_out)`
and `1/Φ(−t_x)` against `2e^{(L−√(2x_out))²/2}` for twelve `(L, x_out)`: the bound holds with factors `1.4 … 336`.
G-F: my own implementation of the unbounded variant on this instance (four parameter sets, 48 runs): all
closed, all valid, all within `J` levels, `M_max` between `75` and `1 400` times the bound.

Qualifiers.  (1) "any tail functions" must read "any *valid* tail functions with a closing level" (the good event
of Theorem N1′ is what is used; with an invalid `Ξ` the event `𝒢` does not give `U ≥ A`).  (2) The conclusion is
about **outer points drawn**, not about queries.  In setting (S) drawing is free, and (S4) only bounds the
queries of rung 0 from above.  A rung-0 rule "if the bracket
`e^{−ψ(x₀)}·[E_be^{−L|(a,b)−x₀|}, E_be^{L|(a,b)−x₀|}]` extrapolated from the reference query has ratio `≤ e^{x₀}`, use
it (no query); otherwise query the fibre" satisfies (S4).  With it, for a low-dimensional outer block
(`n_o = 1`, `n_i = 0`, `a₀ = 0`) a point needs a query at the level `e^{Lt}` only if `|a| > t`, so a level with
`M ≈ K/Φ(−t)` points makes about `2K` queries: the number of *queries* of a run is of order `K·J`, not
`e^{Θ_na}` — the "grids win in low dimension" phenomenon in another guise.  The sentence "So with a fixed split
the worst case of a level is never below the base family's" is therefore right for the point bracket of Theorem
N3 (one query per outer point) and in general only as a statement about the outer sample; for `n_o ≫ L²` the
extrapolated bracket is useless (`e^{L|a−a₀|} ≫ e^{L²}` for typical `a`) and the two readings agree.  The
summary's wording ("every run on its good event draws at least … outer points") is the accurate one.
(3) The hypothesis `⟨a₀, ω⟩ ≤ 0` (so that `ℓ₀ ≤ 1`) is needed and is stated; the proposition is a worst-case
statement over rotations of the instance, not a statement about every linear instance.

*Scope.*  The obstruction is to *this algorithm with a fixed coordinate split*.  It does not show that nesting
with data-dependent or random blocks fails, nor that any adaptive algorithm is confined to `Θ_na`; the report says
so.  The title "coordinate nesting gains nothing" is justified in the sense: no level, whatever its inner
procedures, has an outer sample below `e^{Θ_na(x_out)}` on the worst instance.

### 2.3 Proposition N11

**Verdict: correct as stated** (given the cap bound and the median of `χ²`, both quoted correctly).

Checked line by line.  *Geometry:* `|x − r₀ω|² < ρ² ⟺ ⟨x/r, ω⟩ > (r²+n)/(2rr₀)`, and `(r²+n)/(2r) ≥ √n`, so the
threshold is `≥ t/√n`; cap bound at `s = t/√n ≤ ½` gives the hit fraction `≤ e^{−t²/2}`.  ✓  *Effect:* the identity
`|x − r₀e₁|² = ρ² − y`, `y = 2r₀(x₁−t) − (|x|²−n)` uses `r₀t = n` ✓; `√(ρ²−y) ≤ ρ − y/(2ρ)` ✓; on
`{|x_⊥|² ≤ n−1} ∩ {t < x₁ ≤ T}`: `y ≥ 2r₀(x₁−t) − T²`, depth `≥ (x₁−t) − T²/(2ρ)` (`r₀ ≥ ρ`) ✓;
`ρ ≥ (√3/2)·n/t` under `n ≥ 4t²`, so `LT²/(2ρ) ≤ LT²t/(√3 n) ≤ 0.5774` under `n ≥ LT²t` ✓.  One step is silently
skipped: the integrand `e^{−0.578}e^{L(x₁−t)} − 1` is negative near `x₁ = t`, so multiplying by
`P(|x_⊥|² ≤ n−1) ≥ ½` needs the remark that `A(g) − 1 ≥ 0` anyway (if the `x₁`-integral `I` is negative the claim
`A − 1 ≥ I/2` is trivial; if not, `A − 1 ≥ P·I ≥ I/2`).  With it, `A(g_ω) − 1 ≥ ½[e^{−0.578}e^{L²/2−Lt}(Φ(T−L) −
Φ(t−L)) − Φ(−t)]` and `Φ(1.2816) − Φ(t−L) ≥ 0.4`, `½·0.4·e^{−0.578} = 0.1122` ✓.  *Averaging:* coupling and Fubini
over `ω`; no output is `ε/2`-correct for both `0` and `g_ω` because `ln A(g_ω) > ε` ✓.  *Exponent remark:* with
`L²/2 − Lt = ε + 2.2` the condition on `ε` holds (`0.112e^{2.2} = 1.011`), and `t²/2 = Θ_hint(ε + 2.2)` ✓ (the
restriction "`ε ≥ 1`" is not needed; `t > 0` needs `ε + 2.2 < L²/2`).

*Numerical* (`r2_gauss.py` G-G): exact cap measure (incomplete beta) against `e^{−ns²/2}` for `n = 2 … 10⁵`:
ratio `≤ 0.5`; `median(χ²_k)/k < 1` for `k ≤ 1999` and `10⁴, 10⁵, 10⁶`; for eleven triples `(L, t, n)` (ten satisfy
the hypothesis): the exact maximal hit fraction over radii is `0.0012 … 0.33`, always below `e^{−t²/2}` (by a
factor `3.6 … 9`); the effect of the ball dip by two-dimensional quadrature is above the proved bound in all ten,
and is `0.84 … 1.05` of the half-space's.  **The report's range "0.94 to 0.9999 of the half-space's effect for `n`
between 100 and 10⁵" is specific to its triples**: at `(L, t, n) = (3, 3, 165)` and `(2, 2, 44)` — both admissible —
I get `0.839` and `0.876`.  Nothing in the proposition depends on this.

*Wording.*  "the hinted lower bound holds in high dimension" — what is proved is the exponent
`Θ_hint(ε + 2.2)` for `n ≥ L(L+1.29)²t`, i.e. the hinted bound with an additive loss `2.2` in the accuracy and a
dimension condition cubic in `L`; that is how the "what is shown" paragraph states it.  Fine.

### 2.4 Proposition N12 (false bracket)

**Verdict: correct as stated** ((a)–(c) proofs correct; (d) reproduced independently).  One inaccurate number in
the prose of (d), below.

*Own reproduction* — `experiments/workstreams/N/review/r1_n12_false_bracket.py` → `out_r1_n12_false_bracket.txt`
(13 s; nothing imported from the workstream; the instance, Harper's tables, the closing level, the constants and
the outer loop of Algorithm A written from the text of §2.2/§5.2; the oracle returns valid brackets of the
promised ratio around the exact `V(a)` in four placements).

* The instance.  `V(|a|) = (1 − p + pe^{−1})^{16}`: `1.1254·10⁻⁷` for `|a| ≤ 7`, `1.2043·10⁻⁷` at `9`,
  `2.2185·10⁻⁶` at `10`, `0.28552` at `11`, `0.97528` at `12`.  `A = 1.074731·10⁻³`; the 13 points with
  `|a| ≥ 11` carry `99.986 %`.  Largest edge ratio `e^{11.7652}` `= e^{k·c(J,u)}`, `c = 0.73533` (the identity
  `ln[V(11)/V(10)] = k·c` holds to all digits).  **Agrees with the report**, except: "the bulk has
  `V ≤ 1.2·10⁻⁷`" is true for `|a| ≤ 9` only; the 66 points with `|a| = 10` have `V = 2.2·10⁻⁶` (the script's
  output says "`V(|a| ≤ 9)`"; the report's sentence dropped the qualifier).  Immaterial.
* (c): `E(V−s)₊ = 1.0746·10⁻³ ≥ sμ(D)(e^{kc}−1) = 9.06·10⁻⁴`, `sΞ_u(μ(D)) = 1.46·10⁻⁸ ≤ sμ(D)(e^{2u}−1) = 4.5·10⁻⁸`
  at `s = V(10)`: both inequalities of (c) verified; the proof of (c) is right (`D` is a Hamming ball of radius
  `m − τ − ½` around `1^m`, and `E_r ≤ |B(r)|(e^{u(r+1)} − 1)`).
* (TU) for Harper's function of slope `u`: the ratio `E(V−s)₊/(sΞ_u(p(s)))` is `7.35·10⁴` at `s = V(10)`
  (`q = 13/4096`) and **`1.747·10⁵` at `s = V(9)`** (`q = 79/4096`) — the report's `1.7·10⁵` is the maximum over
  levels, attained one layer below the threshold; even the top level `s = V(11)` violates (`1.41`).
* The algorithm (reference data `ℓ₀ = e^{−uk}`, `V_max = 1`, `κ₀ = 1`; the report's two parameter sets and a third
  of mine: `λ = ½, η = ¼, η′ = ½, θ = 2, ν₁ = 1, b = ¼, δ = 0.01`):

  | tail function | parameters | runs | invalid | `A/U` (min / median / max) | outer points (median) | false sampled certificates | Chernoff events violated |
  |---|---|---|---|---|---|---|---|
  | assumed class, slope `1` | `θ = 20` | 40 | **40** | 286 / 302 / 302 | 776 | 0 | 0 |
  | assumed class | `θ = 1` | 40 | **40** | 2779 / 4582 / 4582 | 6816 | 0 | 0 |
  | assumed class | referee's | 40 | **40** | 2824 / 2824 / 2824 | 6384 | 0 | 0 |
  | true class, slope `11.765` | all three | 36 | 0 | 0.16 … 0.63 | `4.7·10⁵`, `9.2·10⁵`, `3.3·10⁶` | 0 | 0 |

  In all 120 runs with the assumed class the algorithm closes at level `j ∈ {1, 2}` (i.e. `s_j ≤ e^{−14}`, far
  below the spike), every sampled certificate `p(s_i) ≤ q_i`, `p(s_ie^{−b}) ≥ p̲_i` is **true**, (V2) and (V3)
  hold literally on the realised sample, the width inequality holds — and `U < A` by the factors above, because
  the true excess `E(V − s_j)₊` exceeds the certified `s_jΞ_u(q)` by factors between `330` and `2.2·10⁴`.
  With the tail function of the true class the runs are valid, never close by the test (`r† = −1`,
  `π_* = 2^{−12}`), climb the whole ladder and stop by rule (c0) after `10⁵ … 6.6·10⁶` points.  The workstream's
  constants (`π_* = 0.194`, `M̄ = 9.54·10⁵`; `0.00317`, `8.66·10⁷`; `2.44·10⁻⁴`, `7.92·10⁸`, `5.63·10¹³`) are
  reproduced digit for digit by my code; its medians (`294`, `3 680`; `1 164`, `6 816` points) are within the
  run-to-run variation of mine.

**Is it a failure of the hypothesis and not of the implementation?  Yes.**  The outer integrand has an edge ratio
`e^{11.77}`, so it is not in the class whose tail function is used; (S2) of Theorem N1 fails, by direct
evaluation of (TU), at every level between two distinct values of `V` (ratios from `1.41` to `1.7·10⁵`).  Two independent
implementations of the loop (the workstream's and mine) produce the same false brackets, with all probabilistic
certificates true.  The theorem is not contradicted; what is refuted is the tacit use of (F2) when the two
blocks are dependent — this is what the proposition claims.

*Remarks.*  (1) The statement "`c(J,u) ↑ u`" and the orders of the pointwise influence (`kJ/2` at the threshold,
`≈ kJ` away) are right (`σ(J/2)/σ(−J/2) = e^{J/2}`).  (2) "(F2) fails by the factor `e^{kc−u}`" compares Lipschitz
constants, not tail functions; the quantitative failure of (TU) is the table above.  (3) The "mechanism (general)"
sentence is a heuristic, not a proved equivalence ("iff"); it should be labelled so.  (4) With the true class the
run does not "close at the atom": it never passes the closure test at all and ends by the cap rule (c0) — in my
36 runs every stop was `cap` at level `J`; "as the closing level falls to the atom" describes the constant
`π_* = 2^{−12}`, not the behaviour of the run.

### 2.5 Proposition N13

**Verdict: (a) correct after a repair of the proof (the claim is true); (b) correct (a restatement of Theorem
N1′); (c) true only in a weaker form than written.**

(a) The identity `sup A = e^{−ψ₀}∫e^{d(x₀,x)}dμ`, the member `ψ₀ − d(x₀,·)`, the transfer between base points and
the one-query bracket are right.  The impossibility argument as written ("the instances consistent with a finite
set of evaluations have unbounded `A`") proves it for **sure** certificates (an upper bound valid for every
instance consistent with the answers).  For the objects of this report — randomised procedures that may fail
with probability `δ` — one more step is needed, because the set of queried points depends on the random bits:
run the algorithm on `ψ ≡ ψ₀`; choose `R` and `U*` with `P(all queries in {d(x₀,·) ≤ R}, U ≤ U*) > δ` (possible:
finitely many queries and a finite output, almost surely); the function
`ψ′ = ψ₀ − min{(d(x₀,·) − R)₊, R′}` is in the class (maxima and minima of members and constants are members),
equals `ψ₀` on `{d(x₀,·) ≤ R}`, and `A(ψ′) ≥ e^{−ψ₀}∫_{d>R}e^{min(d−R,R′)}dμ → ∞` as `R′ → ∞` since the exponential
moment is infinite; for `A(ψ′) > U*` the algorithm fails on `ψ′` with probability `> δ`.  (Also: the envelope
instance of the report has `A = ∞`; if the class is restricted to `A < ∞`, as in Theorem N3, truncate it as
here.)  With this the statement "necessary and sufficient for any certified upper bound" stands, for
finite-valued `d`.

(b) Nothing to check beyond Theorem N1′ (§4.1 below).  "A cap … is available without any moment condition if the
class is restricted to functions bounded below on the outer block" needs a *known* lower bound of `ψ`.

(c) "every negligible level is left with a failed test" does not follow from "`Ξ(q)/q` does not stay below the
threshold": at the last pass of an unpopulated level `M ∈ [M_j^neg, 2M_j^neg)`, and the test
`s_jΞ(q) ≤ θe^bℓ` reads `Ξ(q) ≤ θ(1−η)ν₀·q·(M/M_j^neg)`; it can succeed when `Ξ(q)/q` is between one and two times
the threshold.  What is true: if `Ξ(q) ≥ 2θ(1−η)ν₀q` for all small `q` (and `Θ = id`), no unpopulated pass with a
small `q` closes, the levels above the bulk are left as negligible, `M_j^neg` grows like `e^{jλ}` and the theorem
gives no bound.  This is a remark about what the theorem cannot give, not a proved non-termination statement,
and should be worded so.

## 3. Theorem N4 (dependence), §2.7

**Verdict: correct as stated.**

* *The definition of `ι`.*  `ι(a,a′) ≥ 0` with `∫w dμ(·|a) ≤ e^{ι(a,a′)}∫w dμ(·|a′)` for all `w ∈ 𝒲`; the least such
  function is `ι*(a,a′) = sup_{w∈𝒲} ln[∫w dμ(·|a)/∫w dμ(·|a′)]₊`, it vanishes on the diagonal and satisfies the
  triangle inequality, so `ρ = d_o^T + ι*` is an envelope with the triangle inequality whenever `d_o` has it (which
  Lemma N.0 needs for "attained", not for validity).  The theorem only needs `ι(a,a) = 0`, which should be said
  (an envelope has `ρ(x,x) = 0`).
* *The proof.*  `V_ψ(a) = ∫e^{−ψ(a,b)}μ(db|a) ≤ e^{d_o(a′,a)}∫e^{−ψ(a′,b)}μ(db|a)` by (F2′) pointwise in `b`, and
  `≤ e^{d_o(a′,a)+ι(a,a′)}V_ψ(a′)` by the influence bound applied to the single weight `w = e^{−ψ(a′,·)} ∈ 𝒲`.  ✓  The
  order of the arguments is right (`ρ(a,a′) = d_o(a′,a) + ι(a,a′)`, class `V(a) ≤ V(a′)e^{ρ(a,a′)}`).  Disintegration
  gives `A = ∫V_ψdμ_o`.  The rest is the verification of (S): the tail functions must be those of `𝒱_ρ` **under the
  marginal `μ_o`**, which need not be a product measure (for a chain it is not) — the theorem says "under `μ_o`",
  and the cost side (a closing level for `(X_o, μ_o, ρ)`) is not addressed; this is stated for the chain in §4(f)
  and should be stated in the theorem: N4 is a validity theorem.
* *The inner procedures.*  (F1′) as stated is what (S4) needs: for every `a`, procedures for `∫w dμ(·|a)` with a
  cost bound in every run and failure probability `δ′`, with random bits independent of the outer points.  The
  remark that this is hidden in the brief's "(F1) is unchanged" is right.
* *Attained.*  For `μ(·|a) = Bernoulli(p(a))^{⊗k}` and `u`-Lipschitz fibres the formula
  `ι(a,a′) = k·max_± ln[(1 + p(a)(e^{±u}−1))/(1 + p(a′)(e^{±u}−1))]` is right: changing the law of one coordinate
  changes `E[g(b₁)]` by the factor `(1 + p(r−1))/(1 + p′(r−1))`, `r = g(1)/g(0) ∈ [e^{−u}, e^{u}]`, which is monotone
  in `r`; the conditional expectations along the hybrid remain log-`u`-Lipschitz; equality for `f = ∓u|b|`.
  **Checked** (`review/r3_finite.py` F-C): 40 random `(k, u, p, p′)`, 8 000 random `u`-Lipschitz fibres of four
  kinds: `ln[E_pw/E_{p′}w] − ι ≤ 9·10⁻¹⁶`, uniform fields attain it; on a dependent instance `Q_3 × Q_3` with
  `p = p(|a|)`, 1 200 members: `ln[V(a)/V(a′)] ≤ u + ι(a,a′)` with equality (to `10⁻¹⁵`) for additive members.
  So the envelope `d_o + ι` cannot be improved for that pair (class, known part).  "Sharp" is proved for this
  example, not in general (in general the supremum over `w` and the supremum over the `a`-dependence need not be
  attained by the same `ψ`); the text says "for `μ(·|a) = Bernoulli…`", which is accurate.
* *Lemma N18.*  (a) correct with the convention `Ξ_ν(x) = +∞` for `x ≥ 1`.  (b) correct (`V̂ = rV`,
  `ρ̂ = ρ + ln r(x) − ln r(z)`; needs `r > 0`).

## 4. Theorem N1′, Theorem N3, Proposition N2, Corollary N5, Proposition N6; Propositions N7, N8

### 4.1 Theorem N1′

**Verdict: correct as stated.**  The potential circularity (`J` depends on `π_*`, `ν₀` on `J`, [N] on `ν₀`) is
avoided by asking `Ξ(q) ≤ θν₁q`, which implies [N] for every `J` because `(1−η)ν₀ ≥ ν₁`.  Termination: Step 6
(every run) gives `M_j^neg ≤ (1+η)e^λν₀M†` at every level reached; if level `j` is reached on `𝒢`, the value
`ℓ_j` was certified at levels `< j ≤ J+1`, all covered by (V2), (V3), so `ℓ_j ≤ A ≤ u₀` and
`νs_j/(u₀e^b) ≤ (1+η)e^λν₀M†`, i.e. `s_j/s₀ ≤ (u₀/s₀)e^{b+λ}(1+η)/((1−η)π_*)`, `j ≤ J`.  (The induction over the
levels — the good event for level `J+1` is not needed to exclude it — is implicit; it is fine.)  Width: at most
`J` levels are left before a stop at a level `≤ J`, and off `𝒢` the extra abort rule keeps it so.  All other steps
do not use the cap.

*Own runs of the unbounded variant* (own implementation, outer law `N(0,1)`, exact tail functions `Ξ_L`, `Θ_L`,
oracle brackets in three placements).  `r2_gauss.py` G-F and `r3_finite.py` F-H: 60 runs on `V = e^{La}`, all closed,
valid, within `J` levels (I did not record there how the levels were left).  **The negligible branch, which the report says it did not
exercise in the unbounded variant (§9), is exercised in `r5_unbounded_negligible.py`**: dips
`V = e^{L(a−c)₊}` (a bulk at `V = 1` and a thin tail), small `θ` and `ν₁` chosen so that [N] fails at the first
levels above the bulk — 36 runs on six (instance, parameter) cells with **40 levels left as negligible** and 68
as populated, plus 24 runs without negligible levels: all 60 closed, all valid, width within `e^{x_out}`,
`q_j ≥ π_*` at every level left (smallest ratio `1.09`), `M ≤ M̄`, no level above `J`.  So the caveat of §9 can be
weakened: the negligible branch of N1′ has now been run (on one-dimensional Gaussian outer spaces, with a
simulated inner oracle).
*Remark.*  The condition `Ξ(q) ≤ θν₁q` is a real restriction on Gauss space at a bounded `θ` (see §2.1): `ν₁`
must be taken `≳ L/θ`, or the closing level is far below `e^{−L²/2}`.

### 4.2 Proposition N2

**Verdict: correct as stated.**  Re-derived: `p(t̂) ≤ q₊` fails only if fewer than `K` of the first sample are
`≥ t⁺ := inf{s : p(s) ≤ q₊}`, a binomial with mean `≥ K/(1−η)`: probability `≤ e^{−η²K/2}`; `p̄(t̂) ≥ q₋` fails
only if at least `K` are `> t⁻ := sup{s : p̄(s) ≥ q₋}`, mean `≤ K/(1+η)`: `≤ e^{−η²K/((1+η)(2+η))}`; given `t̂`,
`min(V,t̂)/t̂ ∈ [0,1]` has mean `≥ p̄(t̂) ≥ q₋`, two-sided Chernoff `≤ 2e^{−η²K/(3(1+η))}`; total
`≤ 4e^{−η²K/(3(1+η))}`.  Then (TU) at `(t̂, q₊)`, (TL) at `(t̂, q₋)` — the same pointwise use of the tail
inequalities at random arguments as in Theorem N1.  Simulated (`r3_finite.py` F-E): 3 600 brackets on
`(ℝ, γ₁)` with three instance shapes and exact `A`: no miss, none above the ratio bound.

### 4.3 Theorem N3

**Verdict: correct as stated** (it is a verification of (S)).  `V_ψ(a) ≤ V_ψ(a′)e^{ρ_o(a,a′)}` with
`ρ_o(a,a′) = sup_b d((a′,b),(a,b))` term by term ✓; the reference bound and the point bracket ✓ (directions of the
quasi-metric are right).  Two tacit requirements: the point bracket must have a ratio bounded *uniformly in `a`*
(`x₀ < ∞`; true for translation-invariant `d`), and `ρ_o` may be `+∞` (then Lemma N.0 gives nothing).

### 4.4 Corollary N5

**Verdict: correct as stated**, with one omission in the definition of a scale family.  Checked: `x_out = Gn`
exactly; `c_η = ⅓`, so `3Ξ(q) ≤ θq` implies [P] (with `Θ = id`) and [N] (and the condition of N1′);
`ln θ = n_o(e_∞ − o(1))`; for `q ≤ e^{−n_oθ₁}`, `θ₁ = θ_na(e_∞ − 3ε) + ε`, (U) and the monotonicity of `x̄` give
`Ξ(q)/q ≤ e^{n_o(e_∞−2ε)}`; `J, ν₀, m_max, K = O(n)`; so `ln M̄ ≤ n_oθ₁ + O(ln n)`, and the left limit in `μ` is what
`ε → 0` gives.  Omission: the definition does not bound `c_ref` and `C₀` (they must be `e^{o(n)}`), and (U) is
used for `Ξ_{n_o}` only — see N6 for the base family.

### 4.5 Proposition N6

**Verdict: gap (small, fillable) — it is a correct plan of proof by substitution, not a proof.**  I went through
Proposition E of `K_REPORT.md` §3.3 with the report's substitutions.  What I found:

1. *The base family needs a tail function of the class itself.*  Step (1) applies Proposition N2 to `e^{−ψ}`,
   `ψ ∈ 𝒞_d`, on `(X_d, μ_d)` with `Ξ_d`.  The definition of a scale family only says that `Ξ_{n_o}` is a tail
   function of the *fibre averages* `V_ψ` for splittings `n = n_o + n_i` with `n_i ≥ 1`.  That `Ξ_d` is a tail
   function of `e^{−ψ}`, `ψ ∈ 𝒞_d`, must be added to the definition (the case `n_i = 0`); it holds in every instance
   of §4.
2. *The conclusion is stronger than Proposition E(b).*  E(b) gives the exponent `h + η = θ_hint(0) + η` at every
   rate `ξ`; N6 claims `θ_hint(ξ) + η`.  This needs E(a) at `g = ξ − η/3`, `g′ = ξ`, `ζ = η/3`, the statement (R)
   at `g`, and the `1`-Lipschitz continuity of `θ_hint` (Proposition N7(a)): `T_F(ξ) ≤ T_k(g) + η/3 <
   θ_hint(g) + 2η/3 ≤ θ_hint(ξ) + η`.  Two lines, but they are not Proposition E and are not in the report.
3. *The induction step* goes through as claimed: the choice of `(φ, β)`; the ladder with `ū ∈ (E, ξ₀)` in place
   of `u`, `ξ₀` in place of `2u` (`T_k ≤ θ_na = 0` on `[ū, ∞)` because `ū > E = x̄(0+)`); Corollary N5 in place of
   K1.b — its `μ` carries a left limit, harmless because `G − (1−φ)ξ_L ≥ g′ − β − (1−φ)ι > g − β` strictly;
   (E0) for the finitely many small `n`.  The recursion (R) has the same form because the outer block of `φn`
   sites has the profile of `Ξ_{n_o}` and the inner family lives in dimension `n_i` — both are in the definition
   of a scale family.
4. *(R) itself* is quoted from Lean (`iterates_lt_hint_add`, `exactRec_reaches_hint_of_pair`).  I compared the
   nine fields of `HintPair` in `proofs/Frontiers/HintRecursion.lean` with Proposition N7(a): all nine follow
   (`hint_lower` with `L = 1`).  I did not check the Lean proofs or that the recursion defined in Lean is the one
   used here beyond the statement.
5. `θ_na` of §2.8 (`inf{θ > 0 : x̄(θ) ≤ x}`) and of Proposition N7 (`min{θ : x(θ) ≤ x}`) agree under (P1); for a
   profile that is not monotone they differ, and it is the first that Theorem N1 certifies (see §4.6).

With 1 and 2 added, I believe the proposition; the report's own label ("the reduction: proved here by checking …
not rewritten in full — the weakest link") is accurate and should stay until the induction is written out for
the abstract setting.

### 4.6 Proposition N7

**Verdict: correct as stated.**  (a): `w(θ′) − w(θ) ≤ −(θ′−θ)`; `θ_hint = w^{−1}` is strictly decreasing and
`1`-Lipschitz; `θ_na` is the inverse of `x` on `[0,a]` and `0` beyond `E`; the identity follows from
`x(θ_hint(e)) = e + θ_hint(e)` and strict monotonicity of `x` on `[0,a]`; all fields of `HintPair` checked against
the Lean structure.  (b): `J` concave, `J(0) = J(1) = 0`, `0 ≤ J ≤ min{Et, a(1−t)}` (`θ + tw = (1−t)θ + tx ≥ 0`),
`J(t)/t → E`; the two dual formulas by Sion on `[0,a]` (for `θ > a`, `(1−t)θ + tx(θ) ≥ (1−t)a`, so restricting to
`[0,a]` does not change `J`) — re-derived, both right.  (c) the transport counter-profile: `x_T` increases, the
identity fails (numerically: deviation `0.495` at `u = 1`; `r3_finite.py` F-F, which also confirms the identity to
grid accuracy for the cube's profile, `h = 0.02914`, `E = 0.12011`, and for the Gaussian one).

**But the interpretation attached to (c) in §3.1 and §4(e) is wrong about the algorithm.**  The report says that
with the transport tail function "the closing condition at the accuracy `e + θ_hint,T(e)` fails for all smaller
sets down to the atom — the exponent of the level is `ln 2`", and (§4(e)) that "at every accuracy rate below
`0.589u` … Algorithm A does not close with it before the atom".  What is at the atom is the closing level `π†` of
Theorem N1, a supremum over **all smaller** `q`; the algorithm examines `q` from large to small and stops at the
first pass whose test succeeds.  For a threshold rate `X > x_T(0) = u²/8` (asymptotically) the test succeeds at
the first passes: `review/r4_transport.py` (own implementation, exact `V`, `Θ = id`, `u = 1`):

| `m` | `X` | instance | `π_*` of Theorem N1 | `M̄` | the run |
|---|---|---|---|---|---|
| 30 | **0.50** (the report's own accuracy `e + θ_hint,T(e)` at `e = 0`, for which `n5` P3 prints "closing exponent `ln 2`, i.e. only below the atom") | flat, dip | `2^{−30}` | `5.7·10¹⁴` | closed with `888` points (`q = ½`), valid, width ok |
| 60 | **0.50** | cone, dip | `2^{−60}` | `1.3·10²⁴` | closed with `976` points (`q = ½`), valid |
| 30 | 0.30 | flat, cone, dip | `2^{−30}` | `5.7·10¹⁴` | closed with `888 … 3 552` points, valid, width ok |
| 60 | 0.30 | flat, dip | `2^{−60}` | `1.3·10²⁴` | closed with `976` points (`q = ½`), valid |
| 30 / 60 | 0.20 / 0.14 | flat, dip | atom | | not closed up to `1.6–2.9·10⁷` points (finite-`m` terms: `(1/m)ln Ξ_T(½) ≈ u²/8 + 0.589u/√m + …`) |
| 16 | 0.05, 0.10 | flat, dip | atom | | not closed up to `2.7·10⁷ > 2^{16}K` points |

So (with `Θ = id`, as in the report's discussion): below the rate `u²/8` (which contains every rate below
`ε* = ln cosh(u/2) ≤ u²/8`) the run indeed cannot close before the atom, because `x_T ≥ u²/8` everywhere — this,
not the growth of `Ξ_T(q)/q` as `q → 0`, is the reason; between `u²/8` and `0.589u` the run closes at once and correctly (the problem is easy there), while the
bound `M̄` of Theorem N1 is astronomically pessimistic.  The conclusions "useless below the threshold" and
"concentration alone does not give a closing level" survive; the sentences quoted, row 8 of the table
("closing only at the atom … proved") and the reading "the exponent of the level is `ln 2`" need this
correction.  It also shows a feature of Theorem N1 worth stating: for a tail function whose ratios are not
monotone the closing level can be far from what the algorithm does.

### 4.7 Proposition N8

**Verdict: correct as stated** (with `J_β(0) = 0`, part of "game function", made explicit).  (a) `J_α(t) ≤
(1−t)μ + t(G−B)` (definition of `μ`), `J_β(t) ≤ R̂_β(γ₀) + tγ₀`, sum, `γ₀ = max(B, μ) ≤ B + μ`; `t = 1` separately.
(b) homogeneity gives `Θ_na^{φν}(x) = φΘ_na^ν(x/φ)`, `R̂_{(1−φ)ν}(γ) = (1−φ)R̂_ν(γ/(1−φ))`; with
`φ = G/(G + R̂_ν(G))`: `μ₀ = φR̂_ν(G)`, `μ₀/(1−φ) = G`, and the two cases `γ ≤ μ₀`, `γ ≥ μ₀` give `≤ R̂_ν(G)`; `B → 0`
by continuity of the convex function `Θ_na^ν`.  Numerically (F-G): 400 random splits, margin `≥ 3.8·10⁻⁵`.
The two-level table of §3.2 is numerical and I did not reproduce it.

## 5. Instances (§4), spot checks

**(e′) Gauss space with the sum metric — correct.**  `c`-Lipschitz for `ℓ₁` implies `c√m`-Lipschitz for `ℓ₂`, so
`Ξ_{c√m}`, `Θ_{c√m}` are tail functions; `V = e^{±c(Σx_i − t√m)₊}` has `−ln V` `c`-Lipschitz for `ℓ₁` and, since
`Σx_i/√m ~ N(0,1)`, is the extremal half-space dip for `L = c√m`: the functions are exact for the class, for every
`m`.  Fibres and fibre averages stay in the class (term by term), so the outer tail function is
`Ξ_{c√n_o}`.  Profile: `x̄(θ) = ((c − √(2θ))₊)²/2`, `w(θ) = c²/2 − c√(2θ)` on `[0, c²/2]` and `−θ` beyond; (P0)–(P2)
hold (`w` is `C¹` at `c²/2` with slope `−1`, convex).  (U): from the two-sided profile inequality and
`t = √(2 ln(1/q))(1 + o(1))` uniformly on `q ≤ e^{−mθ₁}`; for `t ≥ 2L` use `Ξ_L(q)/q ≤ 1 + 2/t²` (Mills ratios), not the bound
`3(1+t)`, which is not `e^{o(m)}` uniformly in `q` — a detail the text skips.  `E e^{c|x|₁} = (2e^{c²/2}Φ(c))^m`, `ln(u₀/ℓ₀) = m ln(Φ(c)/Φ(−c))` ✓.
`θ_hint(ξ) = (c²/2 − ξ)²/(2c²)`, `θ_na(ξ) = (c/√2 − √ξ)²` ✓.  The conclusion "adaptive upper bound = the Gaussian
pair exactly" inherits the status of Proposition N6 (§4.5), and Theorem N1′ at extensive accuracies needs no
special `ν₁`.  "Open: lower bounds" is the right label.

**(f) The nearest-neighbour chain — correct.**  Flipping a non-boundary outer letter does not change `μ(·|a)`:
slope `≤ u`.  Flipping the boundary letter changes `ψ` by `≤ u` and the law of the first inner letter; the
function `b₁ ↦ E[w | b₁]` is log-`v^{(k)}`-Lipschitz with `v^{(1)} = u`, `v^{(j+1)} = u + g(v^{(j)})` (induction from
the far end; the Möbius map `r ↦ ((1−p)r + p)/(pr + 1 − p)` is monotone), so the class-relative influence is
`g(v^{(k)})`.  Recomputed: `u + g(v^{(6)}) = 1.525944`, `2.740225`, `1.128162` for the report's three `(p, u)`, and
`u + K = 1.8473`, `3.1972`, `1.8863` — as reported.  Own enumeration (`r3_finite.py` F-D; `c = 3`, `k = 5`, four
`(p, u)`, 160 random members and the uniform fields each): boundary slope `≤ u + g(v^{(5)})` with equality for the
uniform field to six digits, other letters `≤ u`.  I did not re-run the 360 runs of S6 with my own loop (the
workstream's script reproduces its stored output).  The assessment "validity only; no cost statement" is
accurate.

Not spot-checked: (b), (c), (d) beyond Lemma N14 (correct: a point at Hamming distance `k` from `Dᶜ` has
`ρ(x→Dᶜ) ≤ U_k`, then Harper), Lemma N15 (correct), Lemma N16 (correct for `q < 1`; McDiarmid's constant is
right), Lemma N17 (correct); Proposition N19 was read, not verified (it leans on the uniformity of Theorem
11.101 in the composition).

## 6. The assumption table (§6), row by row

"Supported" = the category follows from the evidence cited (statements of this report as reviewed above, or of
the theory report with the label it has there — for rows 3, 4, 19 I read the cited sentences (Theorem 11.51(b),
Proposition 11.65(b), the deterministic bound after Theorem 11.25), for rows 5, 6, 20, 24 only that the cited
theorems exist; no proof of the theory report was re-checked).

| # | category in the report | supported? | comment |
|---|---|---|---|
| 1 | W, then F | **partly; add X** | W: Theorem N4 is a *validity* statement; the cost changes (slope `u → u + ι` on the outer block, inner procedures under every conditional law, tail functions under the marginal), which is category X and is said in the text below the table but not in the row.  F: supported (Proposition N12, reproduced) |
| 2 | E, F | F yes; E **in a weaker sense** | Without *any* tail function the algorithm is still valid and costs `e^{D−b}` (remark R5): what is essential is that the function used is valid.  The evidence sentence "the only step whose failure makes the bracket false" is **wrong** (see §1.3, item 4).  The mutation `Ξ/50` giving only 4 invalid runs of 48 shows how weak a test simulation is here |
| 3 | E (method), P (exponent) | yes | Theorem 11.51(b) (radial class, another algorithm, exponent `θ_hint`) is as cited |
| 4 | W, X | yes (quoted) | not re-derived |
| 5 | W, X | yes (quoted) | not re-derived |
| 6 | W | yes, given Theorem 11.101 | Lemma N14 checked; Proposition N19 read, not verified |
| 7 | P, X for the algorithm | **X yes; P no** | Proved: this algorithm with a fixed split gains nothing on Euclidean Gauss space (N10(b)).  "Required only by the present proof technique" would need evidence that the *result* holds without additivity; the row itself says "not known".  Should read: **X for the algorithm (proved, one instance); for the complexity: not known** |
| 8 | W, X | yes, with a correction | "transport: closing only at the atom (proved)" is true below the rate `u²/8` only; above it the run closes at once (§4.6) |
| 9 | W | yes; **add X (for the algorithm)** | With `Θ = id` the level closes only at extensive accuracies (Lemma 11.55(a): the one-sided ratio is never small), i.e. Theorems 56/58 are lost for this method.  The Gauss clause ("closing at `t = L + O(1)`") holds with `ν₁ ≳ L/θ` only (§2.1) and is a sketch |
| 10 | W, F | yes | F after the repair of the proof of N13(a) for randomised procedures (§2.5) |
| 11 | C | yes for 52, 56 | for the families (54, 58) the enumeration fallback becomes the hypothesis (E0) |
| 12 | C | yes | exactness at every cardinality is numerical (`m ≤ 4`, reproduced: step/exact up to `3.86` at `u = 1`) plus Harper's theorem |
| 13 | C | yes | Theorem N1 |
| 14 | C | yes | rule (c0) |
| 15 | C | **plausible, not shown** | the row says "not written out"; a category without a written argument should be marked so |
| 16 | P | plausible | the row says "not known"; Proposition N2 (a data-dependent threshold with a second sample) shows that fixed thresholds are not forced in general |
| 17 | P | yes | on the uniform cube (Theorems 11.56, 11.58) |
| 18 | X | partly ("partly known" is honest) | only the lower-bound side is argued |
| 19 | E, X | yes | "`≈ 2ⁿ`" is the bound for `ε = o(n)`; at an extensive accuracy the quoted bound is `exp(n(ln 2 − h(ε₁/u)))` |
| 20 | E, X | yes (quoted) | |
| 21 | E (lower), P (upper) | **E no** | "the factor `1 − 2δ`" shows where the *proof* uses `δ < ½`.  For the hinted problem the bound is indeed false at `δ = ½` (answer `A(0)` or the common value of the dips with probability ½ each), but rows 54/58 are about algorithms correct on the whole class, where nothing is shown for `½ ≤ δ < 1`: **P / not known** |
| 22 | E | **no** | the evidence is "not shown … open"; by the report's own rule this is **not known** |
| 23 | — (not known) | yes | |
| 24 | P | yes | lower bounds without transitivity are quoted; Proposition N11 uses rotation invariance in its place, so "a family of alternatives with a uniformly small hit fraction" is the weaker condition (W would also fit) |
| 25 | C on the cube, P elsewhere | C yes; **P no** | heterogeneous sites: the split is immaterial in the limit of many levels (Proposition N8, proved) and changes the two-level constant by about 1 % (numerical); Gauss space: open.  "P elsewhere" should be "C in the limit for additive families; not known for Gauss space" |

With these changes the counts become: E 4 (2, 3, 19, 20), P 5 (3, 16, 17, 21, 24), C 6, W 7, X 9 (adding 1, 9),
F 3, "not known" in rows 4, 5, 7, 9, 15, 16, 21, 22, 23, 25 (and partly 18).  The stated counts of the report are
arithmetically consistent with its own table (checked).

The paragraph "three most consequential entries": (1) is supported.  (2) is supported except for "the one
hypothesis" (above).  (3) "for every other instance … the bounded-accuracy theory is open for this reason and no
other" is an assertion I cannot confirm from what I read; "for this reason" is supported, "and no other" is not
argued.

## 7. Literature quoted from memory

* **Gaussian isoperimetric inequality**, `γ_n(A + rB₂) ≥ Φ(Φ^{−1}(γ_n(A)) + r)` for Borel `A`, `r ≥ 0`
  (Sudakov–Tsirel'son 1974; Borell 1975): correct as stated, and it is used in exactly this form (for the closed
  set `Dᶜ` and the closed set `S`).  Equality for half-spaces — used for "attained" — is elementary.
* **Cap bound**, `σ_{n−1}{ω : ⟨ω, θ⟩ ≥ s} ≤ e^{−ns²/2}` for `0 ≤ s < 1` (Ball 1997, Lemma 2.2): correct as stated;
  checked against the exact cap measure for `n = 2 … 10⁵` (ratio `≤ ½`).
* **McDiarmid's inequality**, `P(g − Eg ≥ t) ≤ exp(−2t²/Σc_i²)` (and the same for the lower tail): correct, the
  constant `2` is right; the derivation `Eg ≤ σ√(ln(1/(1−q))/2)` from the lower tail is right.
* **Median of `χ²_k` below `k`**: correct (checked for `k ≤ 1999` and three large `k`).
* **Harper's theorem** in the form used in Lemma K.1 / 11.43: standard; my enumeration on `Q_4` agrees at ball
  sizes and at every cardinality with the step functions as bounds.
* **Chernoff bounds** in the forms `e^{−η²μ/2}`, `e^{−η²μ/(2+η)} ≤ e^{−η²μ/3}` (`η ≤ 1`), Sion's minimax theorem:
  correct as used.
* Bollobás–Leader (discrete torus): not used; not checked.

## 8. What was verified numerically (own scripts)

All in `experiments/workstreams/N/review/`, run with `python3 <script>` from that directory; nothing is imported
from the workstream's code (`r5` imports two functions of my `r2`, `r6` the loop of my `r1`).  `r2`–`r6` exit with
status 0 iff they found no violation; `r1` exits with 0 iff the *valid* setting (true class) shows none — the
invalid brackets with the assumed class are its finding and are printed.

| script → output | time | what | key numbers |
|---|---|---|---|
| `r1_n12_false_bracket.py` → `out_r1_…txt` | 13 s | Proposition N12 from the description: instance, (TU) violation, own Algorithm A, both tail functions, three parameter sets | `A = 1.074731·10⁻³`; edge ratio `e^{11.7652}`; (TU) violated by `1.747·10⁵`; **120/120 invalid brackets** with the assumed class (`A/U` from 286 to 4582), 0 false sampled certificates, 0 Chernoff violations; true class: 36/36 valid |
| `r2_gauss.py` → `out_r2_gauss.txt` | 42 s | Theorem N9 (closed forms, 400 exact random Lipschitz functions, non-half-space sets, profile inequalities), N10(b) (formula, quantile, own unbounded runs), N11 (cap, median, ball dips by quadrature) | `9.5·10⁻¹⁴`; ratios `1.0000000000`; `≤ 0.871`; N10(b) bound exceeded by `1.4 … 336` (exact) and `75 … 1 400` (runs); ball/half-space `0.84 … 1.05` |
| `r3_finite.py` → `out_r3_finite.txt` | 27 s | Lemma N.0 on random quasi-metric spaces; `Q_4` all subsets; Theorem N4 formula and attainment; chain slack; Proposition N2; Proposition N7 identity; Proposition N8(a); outer points against queries | `q = 1` convention needed (296 violations of the literal formula); step/exact `3.86`; `ι` attained to `10⁻¹⁵`; 3 600 base brackets, 0 misses; `M_max = 6.9·10⁶` with `5.6·10³` queries |
| `r4_transport.py` → `out_r4_transport.txt` | 18 s | Algorithm A with the transport tail function on `Q_m`, `m ∈ {16, 30, 60}`, `u = 1`, threshold `e^{mX}` | at `X = 0.50` and `0.30` the run closes with `888 … 3 552` points, validly, although `π_* = 2^{−m}` (`M̄` up to `1.3·10²⁴`); at `X ≤ 0.20` (`m = 30`), `0.14` (`m = 60`), `0.10` (`m = 16`) no closure up to `1.6–2.9·10⁷` points |
| `r5_unbounded_negligible.py` → `out_r5_…txt` | 8 s | Theorem N1′ with levels left as negligible | 60 runs, 40 negligible levels, all claims hold |
| `r6_theorem_n1_cube.py` → `out_r6_…txt` | 49 s | Theorem N1 in valid settings with my own loop: `Q_m`, `m = 10 … 13`, radial `u`-Lipschitz outer integrands of eight shapes, Harper's functions, four parameter sets, `κ₀ ∈ {1, (2p_u)^m}`, four oracle placements | **512 runs: 0 invalid, 0 width violations, 0 false certificates, 0 Chernoff violations, (iii), (iv) and the count (v) never violated, no abort**; 11 888 levels left as populated, 261 as negligible, 32 stops by rule (c0) |

The workstream's five scripts were re-run (`python3 -B`): all exit 0 and reproduce their stored outputs exactly
apart from the timing line.  The numbers quoted in the report from them that I compared (2 624 runs; 1 296 + 192
+ 576 + 120 + 80 + 360; 70 208 populated and 163 negligible levels; 24 cap stops; `0.607`; S4 lines; S6 slacks; ten
rows of constants) agree with the outputs.

## 9. What was not checked

* The Lean theorems quoted in Propositions N6, N7 (only the fields of `HintPair` were compared with N7(a)); the
  proofs of the theory report's Theorems 11.25, 11.45, 11.51, 11.59–11.65, 11.97–11.101, 11.116 on which §4(b),
  (c), (d), (f) and rows 3–6, 19, 20, 24 rely; Proposition N19; the numerical table of §3.2 (two-level splits) and
  the scripts `n5` beyond re-running them.
* Theorem N1 end to end with real inner procedures (neither the workstream nor I ran one outside the cube); my
  runs, like the workstream's, use an oracle for the inner brackets, so (V1) holds by construction.
* The asymptotic statement behind Proposition N10(a) (it is not written out) and the [sketch] on the closing
  level of Gauss space at a bounded threshold.
* The induction of Proposition E in the abstract setting was checked for uses of the cube and for the two gaps
  named in §4.5, not rewritten.
* §1 of the report (the audit table of 31 uses of the cube) was used, not audited line by line; I confirm that
  K1's nine steps use the cube only through the items the abstract proof replaces.
* §8 of the report (errors found in the brief and in the theory report): item 7 (ball dips) is confirmed by
  Proposition N11; the other items were not examined.
