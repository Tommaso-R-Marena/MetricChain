# Review A1 — Theorem A′ / Corollary A′ in the bounded-differences form (`PHASE2_REPORT.md` §2.3)

*Referee: second internal AI referee (adversarial), 2026-11-28.  An internal review by an AI session, not peer
review.  Scope: Lemma 2.5 (iv), Theorem A′ (new form), its (O2) paragraph, the Note, Corollary A′, the table —
nothing else.  Scripts and outputs: `experiments/phase2/review/a1_*.py`, `a1_out_*.txt`.  No existing file was
edited; git was used read-only; `lake`/`lean`, `p2_checks.py`, the harness and the mutation tests were not run.*

**Which text.**  **(A)** `docs/phase2/PHASE2_REPORT.md` at commit `67956b7` (sha256 `2dd619fb…c571`, 805 lines;
§2.3 = lines 215–314; hypothesis `8 R m_r ln(2M/η) ≤ τ²`; first version of the theorem: `af43467^`): re-derived in
full; §§1–5 and all line numbers there refer to it.  **(B)** commit `ddae0c3` (sha256 `1cc9cb3a…08fc`), in which
the coordinator applied findings 1–7 while this file was being written (hypothesis `2 R m_r ln(2M/η) ≤ τ²`,
`δ ≤ ½`), and **(C)** commit `d6998d7` (sha256 `b0806429…0db5`, 836 lines; §2.3 = lines 217–345) = (B) plus a
Remark on homogeneous spaces: both re-read once, see §6 (line numbers there are those of (C)).

## 0. Verdict

**The new Theorem A′ (both oracle forms), Lemma 2.5 (iv) and Corollary A′ stand, with one correction to the
statement of Theorem A′ in text (A): it needs `δ ≤ ½` (finding 1).**  Every step of the proofs was re-derived
and is correct; the constants are what the arguments give; no hidden requirement on `r`, `L`, `τ`, `ε`, `M` or
on the dependence of the two bad events was found; every number of the table reproduces.  The removal of the
side condition `h̄(λ) > γ` is legitimate.  The rest is wording (findings 2–6) and one free improvement of the
constant `8 → 2` (finding 7).  **Texts (B) and (C) are correct as they stand**, the new Remark included (§6:
four residual points of wording).

## 1. Findings, by severity

**1. (error in a degenerate corner of the statement; one-word repair) — lines 246–252, 263.**  The displayed
bound is `(1 − 2δ)(1 − η − η″)·2ⁿ/(L V)`, "no side condition — where `η″` is not small, the claim is trivial".
Lemma 2.3 gives `(1 − 2δ)·W ≤ E|Q|·η″` with `W ≥ max(0, 1 − η − η″)`; replacing `W` by `1 − η − η″` needs
`1 − 2δ ≥ 0`.  For `δ > ½` and `η + η″ > 1` both factors are negative, the bound is **positive and false**:
`n = 4, u = 0.1, r = 1, L = 16, ε = 0.05, τ = 1, M = 1, η = ½` satisfy the hypotheses (`R = 0.10517 ≥ 0.10254`,
`8Rm_r ln 4 = 0.0077 ≤ 1`), `η″ = 1`; with probability `p = 8(1 − δ)` evaluate `w(x₀)` and return `ln w(x₀)` plus
a uniform point of an `ε`-grid of the interval of length `nu = 0.4` that contains `ln A(w) − ln w(x₀)` for every
admissible `w`, otherwise return `0`: this is `(ε/2, δ)`-correct with `E|Q| = 8(1 − δ)`; at `δ = 0.96`:
`E|Q| = 0.32 < 0.46 =` the displayed bound (`a1_recipe.py`, part F).  *Correction:* "…`(ε/2, δ)`-correct
randomised algorithm, `δ ≤ ½`, …" (the theory report writes `0 < δ < ½` in its theorems; §1 of this report has
no such convention), or write `(1 − η − η″)₊`.  The (O2) form `(1 − η − η″ − 2δ)` and Theorem A's
`(1 − η)(1 − 2δ)` are not affected.  (The first version had the same corner with `η′`.)  The corollary is not
affected (`δ < ½` fixed).

**2. (wording) — line 244.**  "(that is, `L ≥ 8R²τ^{−2} ln(2M/η)`)" is algebraically equivalent but `R = L m_r`
contains `L`: for a given radius the condition is an *upper* bound, `L ≤ τ²/(8 m_r² ln(2M/η))`, and the two
hypotheses say `⌈2(e^ε − 1)/m_r⌉ ≤ L ≤ τ²/(8 m_r² ln(2M/η))`.  *Replacement:* "(equivalently
`m_r ≤ τ²/(8R ln(2M/η))`; for a given `r`: `2(e^ε − 1)/m_r ≤ L ≤ τ²/(8m_r² ln(2M/η))`)".

**3. (wording, the Note) — lines 270, 274.**  "`PHASE2_REVIEW.md` §1.3" is that file's paragraph on the
evaluations in Theorem E; the first referee's verdict on Theorem A′ is its §3.2 (O2 form: §3.3; table of
verdicts: §12).  "(at `u = 1`: `γ < 0.0154`)" holds for `β = 0` (root `0.015439`); say so.  Otherwise the Note is
accurate: the hypotheses, the bound and `η′` it quotes are those of `af43467^`; `η′ → 0 ⇔ h̄(λ) > γ`; "that
statement remains true" is the right wording (in constants the two versions are incomparable: the new
condition on `L` carries the factor `R² ≥ 4(e^ε − 1)²`, which exceeds one for `e^ε − 1 > ½`); "artefact" is
borne out (§3: the overlap part of the bias has mean `0 ± 0.002τ` and standard deviation `≤ 0.05τ` where the
overlaps themselves are `1.3τ–6.3τ`).

**4. (wording, Corollary A′) — lines 281, 291, and §5 row 1.**  (a) "`ln ln M = βn + o(n)`" excludes bounded `M`
when `β = 0`; write "`ln ln(M + 2) ≤ βn + o(n)`" as in Theorem A (c) (a bound for a family holds for its
subfamilies; the proof then needs the sentence of §6 (a)).
(b) "Let `r` be the largest radius with…" — add "for `n` large": such an `r ≥ 1` exists iff `m_1 = (e^u − 1)2^{−n}`
satisfies the condition, i.e. eventually, because `λ < a < ln 2`.  (c) The corollary is stated for (O1); the §5
table uses it for `q = e^{o(n)}` adaptive queries: say "the same with (O2), taking `η < 1 − 2δ`".

**5. (wording) — lines 258, 266–267, 314.**  "outside an event of probability `η`" → "of probability at most
`η`".  The (O2) sentence lists only `8Rm_r ln(2q/η) ≤ τ²`; it also needs `R ≥ 2(e^ε − 1)` — say "under the same
hypotheses, with `M` replaced by `q`".  "no lower bound at all" → "no lower bound from Theorems A, A′"
(deterministic algorithms have one, C′ (c)).

**6. (status labels) — lines 221, 241.**  Theorem A′ rests on a cited inequality: tag it "[P; uses the
bounded-differences inequality **[K]**]" as Lemma 2.4 is tagged; the header of Lemma 2.5 can say "(iv): the two
deterministic steps **[V]**" (§10 says both; the Lean statements `sum_tuples_sup'_bias_eq_zero`,
`abs_sup'_sub_sup'_le` were read and say exactly that — sum over all tuples of a finite abelian group, any
`e`, any `ψ` of zero sum; a maximum is 1-Lipschitz in one argument; not compiled by me).

**7. (not a defect: sharper constant, optional).**  Lemma 2.5 (iv) holds with `(sup ψ − inf ψ)·m_r` in place of
`2‖ψ‖_∞ m_r`: if only `c_j` varies, `w_c = w_{c∖j} + D`, `0 ≤ D ≤ e_r(·⊕c_j)`, so `G_ψ(c) = const + E_π[Dψ]` and
`E_π[Dψ] ∈ [m_r inf ψ, m_r sup ψ]` (`inf ψ ≤ 0 ≤ sup ψ`).  For `φ` with values in `[−1, 1]` the difference is
`2m_r`, not `4m_r`, and Theorem A′ holds with **`2 R m_r ln(2M/η) ≤ τ²`** (`P(|G_ψ| > τ) ≤ 2exp(−τ²/(2Rm_r))`).
`2m_r` is attained (two antipodal balls, `L = 1`) and never exceeded in the enumeration; in the Monte Carlo the
standard deviation of `G_ψ` reaches `0.88·√(R m_r)`, so (central-limit regime) a bound of this shape cannot have
a constant below about `2·0.88² ≈ 1.5`.  No effect on exponents.

## 2. Line by line (what was re-derived)

* **Lemma 2.5 (iv).**  `E_μφ − E_πφ = (E_π[w_cφ] − A E_πφ)/A = E_π[(w_c − 1)ψ]/A` ✓.  For fixed `x`,
  `(x ⊕ c_j)_j` is again i.i.d. uniform, so `E_c max_j e_r(x ⊕ c_j) = κ` for every `x` and `E_c G_ψ = κE_πψ = 0`
  — exactly, for every `L`, `r`, `ψ`, equal and overlapping centres included ✓.  `|max − max′| ≤ |a_j − a′_j| ≤ a_j + a′_j`,
  mean `2m_r` ✓ (tight for general `ψ`).
* **McDiarmid.**  Two-sided form `P(|f − Ef| ≥ t) ≤ 2exp(−2t²/Σ_j d_j²)`, independent coordinates `c_j`,
  `d_j = 4m_r` (`‖ψ‖_∞ ≤ 2`): `2exp(−2τ²/(16Lm_r²)) = 2exp(−τ²/(8Rm_r))` ✓; `8Rm_r ln(2M/η) ≤ τ² ⇒ ≤ η/M` ✓;
  union over `M` ✓; `A(w_c) ≥ 1 ⇒ |bias| ≤ |G_ψ|` ✓.
* **Markov.**  `P(O_c ≥ R/2) ≤ 2E O_c/R ≤ (L − 1)V/2ⁿ ≤ η″` ✓ (`R > 0`; equality for `r = 1`, `L = 2`, so the
  non-strict "`≥`" matters and is handled); `O_c < R/2 ⇒ A − 1 ≥ R − O_c > R/2 ≥ e^ε − 1` ✓.
* **Lemma 2.3.**  Observables fixed first; baseline `1` with the exact answer `o₀ = (E_πφ_i)`; alternatives all
  `w_c` (all admissible) with weights `2^{−nL}`; good = `o₀` admissible and `ln A(w_c) > ε`, weight `≥ 1 − η − η″`
  (union bound; no independence used); cap `B = 1 − (1 − V/2ⁿ)^L ≤ η″` over *all* alternatives ✓.  Constant
  `(1 − 2δ)(1 − η − η″)` ✓ for `δ ≤ ½` (finding 1).  `τ ≤ 1` is not used.
* **(O2).**  Oracle at `w_c` defined as in Theorem A; per seed `ω` the queries of the run at `1` do not depend
  on `c`; `G_ω = {|G_{ψ_i^ω}| ≤ τ ∀i, O_c < R/2}` has `P_c ≥ 1 − η − η″`; on `G_ω ∩ {Q_ω ∩ D_c = ∅}` the two runs
  coincide and the targets are more than `ε` apart (this is why `O_c < R/2` must be in `G_ω` — it is), so
  `P_ω ≤ 2δ` for every `c`; integrate ✓.  Constant `(1 − η − η″ − 2δ)` ✓.
* **Corollary A′.**  `m_r ≤ τ²/(8(2e^ε − 1)ln(2M/η)) < 1/(8 ln 2)` ✓; `2(e^ε − 1) ≤ R < 2(e^ε − 1) + m_r ≤ 2e^ε − 1` ✓,
  hence the hypotheses ✓; `m_{r+1} ≤ (e^u + 1 + n)m_r` ✓ (equality at `r = 1`); `T/(e^u + 1 + n) < m_r ≤ T`,
  `T = e^{−λn+o(n)}` ✓; `r/n → ρ₀ − λ/u ∈ (p_u, ρ₀]` by monotonicity ✓ (`λ < a ⇔ ρ₀ − λ/u > p_u`); limit
  `ln 2 − λ − h₂(ρ₀ − λ/u)` ✓; `η″ = e^{−n h̄(λ)+o(n)} → 0` ✓.  `h̄′ = u^{−1}ln((1−ρ)/ρ) − 1`, `h̄″ = 1/(u²ρ(1−ρ))`,
  `h̄(a) = 0 = h̄′(a)`, decreasing, `> 0` on `[0, a)`, `h̄ ≥ h − (1 − ℓ)λ ≥ h − λ` ✓.

## 3. Replication (own code; the coordinator's scripts were read afterwards, not run)

**Exact enumeration** (`a1_enum.py`, 118 configurations: `n = 4, 5, 6`; `r = 1, 2, 3`; `L = 1…4`;
`u = ¼, 1, 2` in floating point and `u = ln 2` in exact integers; all `(2ⁿ)^L` tuples, seven runs with
`16 777 216`; 9–10 observables; cross-checked against a pure-Python brute force, max difference `3·10⁻¹⁴`).
No check fails.  Mean of `G_ψ` over all tuples: `0` exactly in integers (36 configurations), `≤ 2·10⁻¹⁴R` in
floating point (rounding).  One-centre oscillation: at most `2.0000·m_r` (attained), never above `osc(φ)·m_r`.
Identity `bias = G/A`: error `≤ 7·10⁻¹⁶`.  Exact tails: `sup_t P(|G| ≥ t)/[2exp(−2t²/(L(4m_r)²))] ≤ 0.57`, and
`≤ 0.022` on the range where the bound is below one (with `d = 2m_r`: `0.82` and `0.66`; with the exact
oscillation: `0.82`).  `E O_c`/bound `∈ [0.32, 1]`; `P(O_c ≥ R/2) ≤ (L−1)V/2ⁿ` (equality whenever `r = 1`,
`L = 2`); `A − 1 ≥ R − O_c` and `O_c < R/2 ⇒ A − 1 > R/2` for every tuple.  Where the hypotheses can be met
(`M = 9, 10`, `η = 0.5, 0.9`, `τ` = the least value allowed; 93 parameter sets with the constant 8, 125 with
the constant 2 of text (B)): `P(∃i |G_i| > τ) = 0` (constant 8), `≤ 0.011` (constant 2), `P(not good) ≤ 0.1(η + η″)`.
*Caveat:* with `L ≤ 4` the bound with `4m_r` is `≥ 1` on almost the whole support of `G`; the enumeration tests
the lemma exactly and the inequality only weakly (less weakly with `2m_r`).

**Monte Carlo** (`a1_mc.py`; `n = 16–20`, 7 regimes, 14 500 instances, 8 fixed observables; `τ` = least
tolerance allowed by text (A) for `M = 8`, `η = 0.1`; sparse code checked against a dense one):

| regime (`n, u, r, L`) | `η″` | `E Õ_c/τ` | first version | max `\|bias\|/τ` | `P(not good)` vs `η + η″` |
|---|---|---|---|---|---|
| 20, 1, 2, 10⁴ | 0.200 | 1.31 | void (`η′ = 3.05`) | 0.31 | 0 vs 0.30 |
| 20, 1, 1, 2·10⁵ | 0.191 | 6.29 | void (`11`) | 0.37 | 0 vs 0.29 |
| 20, 0.3, 2, 2·10⁴ | 0.40 | 3.68 | void (`3.3`) | 0.34 | 0 vs 0.50 |
| 20, 1, 3, 10³ | 0.201 | 0.37 | void (`1.1`) | 0.30 | 0 vs 0.30 |
| 18, 2, 2, 3·10³ | 0.217 | 0.64 | void (`4.7`) | 0.16 | 0 vs 0.32 |
| 16, 1, 2, 300 (control) | 0.078 | 0.09 | usable (`0.08`) | 0.39 | 0 vs 0.18 |
| 16, 1, 3, 10³ (`η″ = 2.1`) | — | 2.22 | void | 0.05 | theorem void; lemma tested |

Means of `G_ψ`: all 56 z-scores within `±2.4`.  `sd(G_ψ) ≤ 0.88√(R m_r)`; `P(|G_ψ| > 2√(Rm_r)) ≤ 0.020`,
`P(> 3√(Rm_r)) ≤ 0.0005` (bound of (A): `1`, `0.65`; with `d = 2m_r`: `0.27`, `0.022`).  1400 single-centre
replacements: `|ΔG_ψ| ≤ 2.00 m_r`.  The first version needs `O_c ≤ τ/5`: frequency `0` in the first five regimes.
With the constant 2 of text (B) the least tolerance is `τ/2`: in the same runs `E Õ_c` is `2.6, 12.6, 7.4, 0.74,
1.3, 0.18` times it, max `|bias|` is `0.63, 0.74, 0.67, 0.59, 0.32, 0.79` of it, and again no instance leaves
the good event.

**Numbers** (`a1_recipe.py`, 40 digits).  `a, ρ₀, h, ℓ` and all 30 table entries reproduce to the printed
digits; `a/2 = 0.055472`, `h/2 = 0.014570`, `1 − ℓ = 0.509966`; `h̄` on a 2001-point grid for `u = ½, 1, 2`.
Recipe of Corollary A′ in log-space, `u = 1`, `η = 0.1`, `M = 1`, `ε = 1` (hypotheses of Theorem A′ verified at
each `n`):

| `γ` | `h̄(2γ)` | `n⁻¹ln(2ⁿ/(LV))` at `n = 2·10³, 2·10⁴, 2·10⁵, 2·10⁶` | `ln η″` | `ln η′` (first version) |
|---|---|---|---|---|
| 0.030 | 0.006364 | 0.007224, 0.006506, 0.006384, 0.006367 | −14.4, −130, −1277, −12733 | +48 … +47269 |
| 0.045 | 0.001098 | 0.002389, 0.001285, 0.001122, 0.001101 | −4.8, −25.7, −224, −2202 | +87 … +87800 |

The finite-`n` exponent tends to `h̄` from above, at rate `O(ln n / n)`; the same with `ε = 0.1`, `M = 2ⁿ`,
`ln ln M = βn` (`γ = 0.02, β = 0.05`), and with the constant 2 of text (B) (`0.007340 … 0.006367`,
`0.002436 … 0.001101`).  With the coordinator's parameters (`M = 100`) my values equal those of
`out_p2_checks.txt` (A4h) to all printed digits, for the constant 8 and for the constant 2.  The value
`h̄(0.09) = 0.001104` quoted in my brief is not reproduced (`0.001098`); it does not occur in the report.

## 4. Attempts to break it

`L = 1` (no overlaps; in (A) the uniform answers are then admissible for *every* `c`, since `2m_r ≤ 0.85τ`); `r = 1`
(points with multiplicity; Markov step tight); equal centres (`A − 1 = m_r`, excluded from the good event as
it must be); `ε → 0`, `ε` large, `τ = 1`, `M = 1`; `η″ > 1`; dependence of the two bad events (none needed).
Consistency with upper bounds: `h̄(2γ) ≤ (1 − γ/ln 2)h` on `[0, a/2]` ✓; the full-oracle collapse C′ (a) needs
`ln ln M ≈ n ln 2 > a`, outside the range.  Only the corner of finding 1 breaks a displayed inequality.

## 5. Not checked

* McDiarmid's inequality itself (cited, not formalised); no numerical test can reach its tail at `τ`
  (probabilities `< 10⁻¹²`), and for `L ≤ 4` it is nearly vacuous.
* Lean: statements read, nothing compiled; `p2_checks.py`, harness XXVIII.2 and its six mutations not run.
* The (O2) argument: on paper only (no simulated adaptive algorithm); Lemma 2.3: its five-line proof
  re-derived, the Lean statement read.
* The upper-bound column of the table beyond arithmetic (Corollary C), §1's cited theorems, and every part of
  the report outside §2.3; the copies of this section in `MANUSCRIPT.md`, `FINAL_REPORT.md`.
* Whether `h̄(2γ)` is the true exponent (open problem 1) — only that it is a valid lower bound.
* Texts (B), (C): one pass (§6).  The coordinator's checks as changed in `ddae0c3` (A4e–A4h, harness XXVIII.2,
  mutation M7 with the sharp constant) were read in the diff, not run.

## 6. Texts (B) and (C): the revision made while this review was being written

Read once (diff of `d6998d7` against `67956b7`: header paragraph, §2.3, §10, §11.1); the changed mathematics
was re-derived and the numerics were repeated with the new constant (§3).

* **Lemma 2.5 (iv)** (lines 229–246) with `(sup ψ − inf ψ)·m_r`: `w_c − 1 = b + D`, `D = (e_r(·⊕c_j) − b)₊ ∈
  [0, e_r(·⊕c_j)]`, `E_π[Dψ] ∈ [m_r inf ψ, m_r sup ψ]` ✓; "attained" ✓ (`2(r − 1) < n`, `ψ = 1_{B(c)} − 1_{B(c̄)}`).
* **Theorem A′** (248–274): `δ ≤ ½` ✓; `d_j = 2m_r`: `2exp(−2τ²/(4Lm_r²)) = 2exp(−τ²/(2Rm_r)) ≤ η/M` under
  `2Rm_r ln(2M/η) ≤ τ²` ✓; the equivalent forms of lines 255–256 ✓; (O2) with `2Rm_r ln(2q/η) ≤ τ²`, "no
  restriction on `δ`" ✓.
* **Corollary A′** (310–329): `m_r ≤ τ²/(2(2e^ε − 1)ln(2M/η)) < 1/(2 ln 2) < 1` ✓; hypotheses of the theorem ✓;
  `η < 1 − 2δ` ✓; existence of `r` for large `n` ✓; exponent and table unchanged ✓.  Note, §10: accurate.
* **Remark (homogeneous spaces)** (280–291, tagged "not seen by a referee") — **correct as stated.**  The proofs
  of Lemma 2.5 and Theorem A′ use: admissibility of maxima of dips (any metric space); the uniform reference;
  and that `#{y : d(x, y) = k}` does not depend on `x` — whence `E_π e_r(d(·, c)) = m_r` for every `c`,
  `|B(x, r−1)| = V` for every `x` (overlap bound, hitting probability), and the same law of `(d(x, c_j))_j` for
  every `x` (mean zero).  McDiarmid, Markov and Lemma 2.3 do not see the space.  Checked by enumeration of all
  tuples (`a1_homog.py`: Petersen graph, `J(6,3)`, `H(3,3)`, `C_9`; 42 configurations, `L ≤ 4`: mean zero,
  oscillation, (ii), Markov and hitting steps, exact tails — no failure) with negative controls (a path, a
  star: `m_r` depends on the centre and the mean of `G_ψ` is up to `0.15`).  Precisions: only distances `< r`
  matter; for a metric that is not integer-valued read `V(r−1)` as `#{d < r}`; the Corollary stays a
  statement about the cube.

**Residual points (wording), line numbers of (C).**
(a) *Corollary, lines 310, 326.*  The hypothesis is now "`≤ βn + o(n)`" (my 4a) but the proof still says "Hence
`m_r = e^{−λn+o(n)}`", which needs equality.  Add: "It suffices to treat equality: an algorithm may ignore
observables (or make fewer queries), so a bound for a larger family holds for every subfamily."
(b) *Line 278.*  The (O2) sentence should say that `R ≥ 2(e^ε − 1)` is kept (finding 5, written after the revision).
(c) *Line 255.*  "every single dip is far below the tolerance": the hypotheses give `m_r² ≤ R m_r ≤
τ²/(2 ln(2M/η))`, i.e. `m_r < 0.85τ` — "below"; "far below" needs `L` or `M` large.  (With the constant 8 a single
dip, `L = 1`, was admissible for every centre; with 2 it is not: for `φ = 2·1_{B(c₀,r−1)} − 1` and `c = c₀` the
bias is `≈ 2m_r`, up to `1.7τ`.  The probabilistic statement is unaffected.)
(d) *Lines 303, 307–308, 280; §10.*  "overlaps … 0.4 to 6 times the tolerance" is relative to the least
tolerance of text (A); relative to that of (B) it is `0.7` to `12.6` times.  "Not re-read by a referee" / "not
seen by a referee": (B) and the Remark have now been read once by this referee (this section).
