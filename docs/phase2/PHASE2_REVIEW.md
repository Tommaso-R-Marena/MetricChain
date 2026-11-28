# Internal adversarial review of `docs/phase2/PHASE2_REPORT.md`

*Referee: internal AI referee (adversarial), 2026-11-28.  This is an internal review by an AI session,
not peer review.  Scripts and their outputs: `experiments/phase2/review/` (`r1`–`r6`, each with an
`out_*.txt`).  Nothing else was created and no existing file was edited; `lake`, `lean` and the audit
script were not run; git was used read-only.*

Verdict vocabulary: **correct as stated** / **correct after a repair** / **gap** / **wrong**.

**Which text was reviewed.**  The report changed several times while this review was running (not by
the referee):

* **v1** — the 614-line text of commit `8e2d8e6` (sha256 `b892cc0c…`), the text the brief describes.
  It was read whole and every statement in it was re-derived.  **Line numbers "L n" below are v1 line
  numbers**; §13 maps them to the next text.
* **pre-revision** — the 693-line text of commits `4b77c0b`/`76e3218` (sha256 `7e0d70b7…`): v1 plus §5.1
  (Lemma 5.1, "attenuated bias", added in `d267d15`), §2.5 (Proposition 2.7, "absorption", added in
  `4b77c0b`), one row in each of two tables, and three one-line edits.  Nothing else of v1 was changed
  — in particular none of the passages criticised below.  The two additions were checked (§11), with
  less depth than v1.
* **revised** — commit `e4991d7` (750 lines, sha256 `10345a25…`), in which the coordinator applied
  §§1–10 of this file while it was still being written.  What was checked of it, and the one thing in
  it that still has to change, is in §11b.

`docs/phase2/MANUSCRIPT.md` is not under review and was not read (only searched, §4.4).

## 0. Summary

Every numbered theorem of v1 survives.  Two statements of §2.4 are **wrong** — both are numerical
claims ([N]) about the flat family with a field, and they are wrong in opposite directions; they have
been propagated as a "negative result" to four other files.  One theorem statement has a constant
that its own proof does not give; one lemma lacks a proviso.  The rest is wording.

| # | where (v1 line) | what | kind |
|---|---|---|---|
| 1 | L298–304, L30 | "with a field the flat family is **void** at the constant baseline, `−ln P_hit/n → 0`": **false**.  The limit is `KL(κ*‖θ) > 0` (`0.0109` at `p=0.3,u=1`; `0.0056` at `p=0.1,u=2`), by a two-line Chernoff bound valid for every `n` | **wrong** (substance of an [N] claim) |
| 2 | L286, L304–309 | the product weights of `e^{−γ|x|}` are **inverted** (in the text and in `p2_field_flat.py`); the "flat" numbers `0.0236`, `0.0203` belong to a family that is **not flat**.  Correct best values: `0.0122`, `0.0106`; "40 %–95 %" should be "22 %–49 %".  The comparison values `0.0253`, `0.0489` are `0.0250`, `0.0481` (closed form of Theorem 11.59) | **wrong** (formula and numbers) |
| 3 | L139–140 | Theorem A for adaptive statistical queries: "the same holds" — the proof gives `(1 − η − 2δ)`, not `(1−η)(1−2δ)` (the proof says so itself, L172) | correct after a repair |
| 4 | L202 | Lemma 2.5(iii) is false as stated when `O_c ≥ 1 + L m_r` (the bound is negative); needs the proviso or `Õ` | correct after a repair |
| 5 | L469, L34, L527 | Theorem E is proved for `ε < ln(11/8)` only; §0 and §7 quote it for "bounded accuracy" | correct after a repair (K against CK dips) |
| 6 | L443 | §5 table uses Theorem A′ for adaptive queries (O2); A′ is stated and proved for (O1) only | gap (small; closed in §3.3 below) |
| 7 | L405–406, L424–425 | "`b` halving queries": the stated guarantee needs both halves at each level (`2b` queries) | correct after a repair |
| 8 | L576 | novelty table: Proposition C′(b) (one exact point probability) is in the archive (A8: "the full law at one point: 0", "`θ = 0` for `K = n`"; A7) | omission |
| 9 | L28, L36–39, L430–433, L300–301, L31, L597, L122 | wording that says more (or something else) than the proofs: "iff", "honest error bars … and nothing more", the trichotomy of the "Reading", "the flat mixture is unique", "attained", "every identity and inequality … checked", "Lemma 1" | wording |

Verdicts per statement are in §12.

---

## 1. Theorem E (samples), §6 — **correct as stated**

Re-derived in full; the argument is sound.  The steps, with what makes each legitimate.

**1.1 The ideal model and the good event.**  For a list `c` of `K_i` centres the ideal mixture
`μ̃_c = (π + Σ_j e_r(·⊕c_j)π)/(1 + K_i m_r)` is: "floor" (a uniform point) with probability `1/(1+K_i m_r)`,
otherwise a uniformly chosen index `J` and the point `c_J ⊕ z`, `z ~ ν`.  The event `E_i` = {no floor
label, all indices distinct} depends on the labels only, **not on the centres**; `P(E_iᶜ) ≤ m/(1+K_i m_r) + C(m,2)/K_i`.
Conditionally on `E_i` the index sequence is a uniform injective sequence independent of `(c, z)`, so
`(c_{J_1},…,c_{J_m})` are i.i.d. uniform, the other `K_i − m` centres are i.i.d. uniform and independent of
them, and the displacements are i.i.d. `ν`.  **So the sentence of L485–487 is true, for both experiments.**
(`K ≥ 40m² ≥ m`, so there are unsampled centres.)

**1.2 One probability space.**  `Ω*`: `c′_1..c′_m`, `d_1..d_{2K−m}` i.i.d. uniform, `z_1..z_m` i.i.d. `ν`, seed `ω`;
`x_k = c′_k ⊕ z_k`; `W′_0` built on `{c′, d_1..d_{K−m}}`, `W′_1` on `{c′, d_1..d_{2K−m}}`.  Then
`Law*(W′_i, x) = Law_ideal,i((W, X) | E_i)`, and
`TV(Law_true,i(W,X), Law*(W′_i,x)) ≤ t_i := P(E_iᶜ) + m·E_c TV(μ_{w_c}, μ̃_c)` (per-instance coupling of `m`
i.i.d. samples, then `TV(P, P(·|E)) = P(Eᶜ)`).  With `Õ ≤ O` and the cases `O ≤ R_i/2`, `O > R_i/2`:
`E TV ≤ 2E O/R_i ≤ K_i V/2ⁿ` — the report's `2K_i V/2ⁿ` is correct (and loose by 2).
`t_0 ≤ 1.55η₁`, `t_1 ≤ 0.85η₁`.

**1.3 Evaluations.**  `W′_1 = W′_0` off the balls `B(d, r−1)` of the `K` extra centres, pointwise (a maximum).
The extras are independent of `(ω, x, W′_0)`, hence of the whole adaptive run on `(x, W′_0)`; so
`P*(run hits an extra ball) ≤ E*|Q′_0|·K V/2ⁿ`, and if it does not, the run on `(x, W′_1)` is the same run
(induction over the steps).  This answers three questions of the brief: (i) adaptivity and dependence
on the samples are harmless, because the bound is conditional on everything the run depends on;
(ii) evaluations near a *sampled* centre teach nothing about the instance label, because the two
weights are equal there unless the point lies in an extra ball, which has the same probability
`≤ K V/2ⁿ` for every point; (iii) "the value of the maximum" is `e^{ur}` in both.
*One step the text does not spell out:* `E*|Q′_0|` is the cost in the coupled experiment, the theorem
is about the true one.  Couple `(W′_0, x)` maximally with the true `(W, X)` and draw the extras
independently of both: `P*(hit) ≤ t_0 + E_true|Q_0|/N*`.  This is the term `1.55η₁` in the display of L497,
so the bookkeeping already contains it; a sentence should say so.

**1.4 Values and conclusion.**  In `Ω*`, `W′_1` has `2K` i.i.d. uniform centres (the prior), so
`P*(O_1 > R/4) ≤ 8/N* ≤ η₁/5`; `A(W′_0) ≤ 1 + R`; ratio `≥ (1+7R/4)/(1+R) ≥ 11/8` (`R ≥ 1`; in fact
`R ≥ 40`, ratio `≥ 71/41`).  Then
`1 − t_0 − E|Q_0|/N* − 0.2η₁ ≤ P*(err_0) + P*(err_1) ≤ 2δ + t_0 + t_1`, i.e.
`E|Q_0| ≥ (1 − 2δ − 4.15η₁)·N*`.  The report has `4.25η₁` and states `12η₁`: **correct** (with room).

**1.5 Exponents.**  `m_r ≈ 1/m` ⇒ `r/n → ρ₀ − ν/u` (needs `ν < a`; true since `ν* < h < a`);
`n^{−1}ln N* → ln 2 − 2ν − h₂(ρ₀ − ν/u) = h̄(ν) − ν`; `N* ≥ 40m/η₁` ⇔ `h̄(ν) > 2ν`; `h̄(ν) − ν` is decreasing, so
"samples + evaluations ≥ `e^{ν*n}`" follows for `ν < ν*` and trivially for `ν ≥ ν*`.  Checked at finite `n`
(`r1`: `ln N*/n = 0.02315` at `n = 8000`, `ν = 0.004` against `h̄(ν) − ν = 0.02313`).  `ν* = 0.003097, 0.011726,
0.038738` and `0.404h, 0.402h, 0.398h` reproduce.

**1.6 Attempts to beat the bound on this family.**  (a) *Number of samples with `w(x) = 1`*: its mean is
`m/(1+R) ≤ η₁` and `m/(1+2R) ≤ η₁/2` — invisible; this is exactly why the theorem needs `R ≥ m/η₁`
(equivalently: the harmonic-mean identity `1/A = E_μ[1/w]` needs about `R` samples here).  (b) *Distances
between samples*: two samples share a dip with probability `≤ m²/2K ≤ η₁/2`; otherwise the sampled centres
are i.i.d. uniform in both experiments.  (c) *Values `w(x_i)`*: functions of the displacements, law `ν` in
both.  (d) *Local search around sampled centres, probing between them*: covered by 1.3.  (e) *Blind
search for unsampled dips*: `N*` evaluations per find — the bound.  No attack found.
Numerically (`r4`, `n = 13–15`, Monte Carlo over instances, everything else exact): the total-variation
distance between the laws of `(x_1 ⊕ x_2, floor flags)` under `K` and `2K` dips equals the ideal-model
prediction (`0.0294` against `0.02945`; `0.0348` against `0.0349`; `0.1997` against `0.1993`) and is below
the proof's bound in every run; `E TV(μ_w, μ̃) ≤ K_i V/2ⁿ` and `P(O_1 > R/4)` as claimed.

**1.7 Minor.**  (i) The theorem is stated for `ε < ln(11/8)` only, while §0 (row E, L34) and §7 (L527)
quote the exponent for "bounded accuracy".  *Repair:* compare `K` with `CK` dips: the ratio is at least
`(1 + (C − ¼)R)/(1 + R) ≥ (40C − 9)/41` (increasing in `R ≥ 40`), which exceeds `e^ε` for `C = ⌈2e^ε⌉`; there are
`(C−1)K` extra centres; the constants change by factors depending on `C` only (hypothesis
`N* ≥ 40C²m/η₁` for the overlap of `CK` centres, bound `(1 − 2δ − O(η₁))N*/(C − 1)`), the exponent does
not.  Or restrict the two quotations.  **Correction of an earlier version of this paragraph:** it
proposed `C = ⌈e^ε⌉ + 1`, which is enough only for `e^ε < 31` (at `R = 40`, `ε = 4`: `C = 56`, ratio bound
`54.4 < e^4 = 54.6`); the revised report (Remark (4) of §6 in the working tree at 01:53 UTC) copied
that constant and should use `⌈2e^ε⌉`.  (ii) Remark (2), "`N ≳ N₀/m^{2−ℓ}`", is first order in `ν`
(the inequality direction is right by convexity of `h̄`).

## 2. Theorem A, §2.2 — **(a) for (O1), (b), (c): correct as stated; (a) for (O2): correct after a repair**

**Quantifiers.**  Order: observables fixed → algorithm (correct for every instance and every fixed
admissible answer vector, probability over the seed only) → adversary draws `c ∈ X^L` independently of
the seed.  The answer `o₀ = (E_πφ_i)` is used at the constant weight (exact, admissible) and at `w^c`
only for `c ∈ G`, where it is admissible by the definition of `G`; alternatives with `c ∉ G` carry no
weight in Lemma 2.3 ("good").  So the uniform-answer oracle is legitimate for every instance *used*.
The Lean lemma quantifies exactly this way (`hcorr : ∀ g o, G g → valid g o → …`, fixed `o`).

**Hoeffding.**  `μ_w = A^{−1}π + (1 − A^{−1})ν`, so `Y_j(φ) − A^{−1}E_πφ ∈ [−(1−A^{−1}), 1−A^{−1}]`: length
`2(1 − e^{−Δ_k})` — attained (`r2`, B3: observed range equals the bound to 5 digits).  Two-sided
Hoeffding: `2exp(−2Lτ²/(2(1−e^{−Δ}))²)`; union over `M`: `≤ η` iff `L ≥ 2τ^{−2}(1−e^{−Δ_k})² ln(2M/η)`.  ✓.
`E Y_j = E_πφ` by (2.1) ✓ (`r2`, A5).  Hitting probability `≤ L·V(n,k)/2ⁿ` ✓.  Simulation (`r2`, B4):
`n = 10`, `M = 40`, `τ = 0.05`, `η = 0.2`, `L = 88`: no bad `c` in 300 draws.

**(O2).**  The proof is right and gives `(1 − η − 2δ)`; the *statement* (L139–140, "the same holds
with `M` replaced by `q`") claims `(1−η)(1−2δ)`, which the argument does not give (the proof admits it
at L172).  The proof also needs one sentence it does not have: "the run at `w^c` in which the oracle
gives the same answers" is an admissible oracle behaviour only for seeds with `c ∈ G_ω`.  Define the
oracle at `w^c` once and for all — *answer a query `φ` by `E_πφ` if `|E_πφ − E_{μ_{w^c}}φ| ≤ τ`, by the
true mean otherwise* — it is admissible, does not depend on the seed, and coincides with the
uniform answers on the run of every seed with `c ∈ G_ω`.  Then `P_ω(c ∈ G_ω, Q_ω ∩ D_c = ∅) ≤ 2δ` as
claimed.
*Replacement for L139–140:* "With an oracle (O2) making at most `q` statistical queries and
`L ≥ 2τ^{−2}(1 − e^{−Δ_k})² ln(2q/η)`: `E|Q| ≥ (1 − η − 2δ)·2ⁿ/(L·V(n,k))`."

**(b).**  `w_i^c` admissible, `A(w_i^c) = A(w_i)`, difference set `∪_j(D ⊕ c_j)`, `2M` events, intervals of
length 2: `4M e^{−Lτ²/2} ≤ η` ✓.  The Lean lemma allows the query set to depend on the seed and on the
oracle's answer (`Q : Ω → Θ → Finset X`), and `o₀` need not be admissible for anything but the good
pairs.  ✓.

**(c).**  ✓.  The §0 table (L28) says "Both exponents unchanged **iff** `ln(1/τ) = o(n)` and `ln ln M = o(n)`".
What is proved: sufficiency for every family; and *neither condition can be dropped* (specific
families, Corollary C).  The literal "only if" is false for particular families (`M` copies of one
observable).  *Replacement:* "… unchanged if `ln(1/τ) = o(n)` and `ln ln M = o(n)`, and neither condition
can be dropped (row C)".

**Model remark (wording, L36).**  The tolerance is adversarial ("any value inside the bar").  For error
bars in the statistical sense (independent noise of size `τ` on each reported mean) the count enters
differently — `M` noisy copies of one observable average to `τ/√M` — and the theorem says nothing.
"Honest error bars" in the one-sentence summary should read "error bars that may hide any value
within `τ`".

## 3. Lemma 2.5, Theorem A′, Corollary A′ — **A′, Cor. A′: correct as stated; Lemma 2.5(iii): correct after a repair**

**3.1 Lemma 2.5.**  (i) ✓.  (ii) with the order statistics `a_(1) ≥ a_(2) ≥ …`:
`Σ_{j<j′} min = Σ_{k≥2}(k−1)a_(k)`, so `Σ − Σ_{pairs} min = a_(1) − Σ_{k≥3}(k−2)a_(k) ≤ max ≤ Σ` ✓; expected overlap:
`min(a,b) ≤ a·1{b>0}` and independence ✓ (`r2`, C6: exact value `0.67–0.82` of the bound).  (iii): the
computation `‖μ_{w_c} − μ̃_c‖₁ ≤ 2Õ/(1 + Lm_r − Õ)` is right, and `Õ ≤ O_c`; but the stated bound
`TV ≤ O_c/(1 + Lm_r − O_c)` is **false when `O_c ≥ 1 + L m_r`** (negative right-hand side): `L = 40` equal
centres, `n = 10`, `u = 2`, `r = 4`: `O_c = 7756`, `1 + Lm_r = 399`, stated bound `−1.05`, true `TV = 0.077`
(`r2`, C7).  The coordinator's own harness test guards this with `if O < 1 + L m_r`.
*Replacement for L202:* "`TV(μ_{w_c}, μ̃_c) ≤ Õ_c/(1 + Lm_r − Õ_c)`, `Õ_c = E_π(Σ_j e_j − max_j e_j) ≤ O_c`; hence
`≤ O_c/(1 + Lm_r − O_c)` whenever `O_c < 1 + Lm_r`."  Neither use of the lemma is affected (A′: `O_c ≤ τ/5`;
E: by cases, §1.2).

**3.2 Theorem A′.**  `E_{μ̃_c}φ − E_πφ = (Lm_r/(1+Lm_r))(L^{−1}ΣZ_j − E_πφ)` ✓; Hoeffding at `τ/2` with range 2:
`2Me^{−Lτ²/8}` ✓; Markov `P(O_c > τ/5) ≤ 5·C(L,2)m_rV/(2ⁿτ) ≤ η′` ✓; on `G`: `τ/2 + 2·(τ/5)/(1 − τ/5) ≤ τ` for
`τ ≤ 1` ✓; `A(w_c) ≥ 1 + Lm_r − τ/5 > e^ε` ✓.  Simulated in three regimes where `1 − η − η′ > 0`
(`r2`, D1–D2).

**3.3 The (O2) version (used in the §5 table, L443, but not stated).**  The per-seed argument of
Theorem A applies verbatim with `G_ω` = {the `τ/2`-concentration for the queries of the seed `ω`, and
`O_c ≤ τ/5`}: `E|Q| ≥ (1 − η − η′ − 2δ)·2ⁿ/(L·V(n,r−1))`, `L ≥ 8τ^{−2}ln(2q/η)`.  The row of the table is then
justified; the theorem should say it.

**3.4 Corollary A′ and the table.**  `h̄′(λ) = u^{−1}ln((1−ρ)/ρ) − 1` at `ρ = ρ₀ − λ/u`, `h̄″ = 1/(u²ρ(1−ρ))`,
`h̄(a) = 0 = h̄′(a)`, `h̄(0) = h`, `h̄′(0) = −(1−ℓ)` — all confirmed (`r1`, 40 digits, grid of 400 points for
monotonicity/convexity/tangent bound).  Side condition `h̄(2γ) > γ` up to `γ = 0.015439` (bound `0.01544`
there); `h/2 = 0.014570`; table entries `0.027133, 0.024252, 0.019795, 0.016154` and
`0.029055, 0.028929, 0.028719, 0.028530` reproduce.  Asymptotics `n^{−1}ln m_r → u(ρ − ρ₀)` and
`n^{−1}ln(2ⁿ/V) → KL(ρ‖½)` checked with exact big-number sums at `n = 500, 2000, 8000`.

## 4. Lemma 2.6, Theorem A″, Corollary A″, §2.4 (3) — **theorem and corollary correct; one formula and the numerical claims of (3) wrong**

**4.1 Lemma 2.6, Theorem A″.**  ✓ (`r2`, E3–E6, arbitrary random `π` on a cube of 8 sites).  Constants:
`Y_j ∈ [−ε₀, ε₀]` (range `2ε₀`), `e_j ∈ [0, ε₀]`; Hoeffding at `τ/4`: `2e^{−Lτ²/(32ε₀²)}` and `2e^{−Lτ²/(8ε₀²)}`; union
`≤ (2M+2)e^{−Lτ²/(32ε₀²)}` ✓; on the event `|S_φ − E_πφ·S_1| ≤ τ/4 + τ/4 + 2ξ̄ ≤ τ` ✓; `A ≥ 1 + ε₀ − ξ̄ − τ/4 > e^ε` ✓.
(For a product reference the hypothesis `ξ̄ ≤ τ/4` holds at the exponential scale whenever `P_hit` is
exponentially small: `ξ̄ ≤ P_hit + ε₀·P(x ∉ B_c)` under the joint law of a centre and a point of its cone
ensemble, and that ensemble sits inside `B_c` with a margin `KL(cone‖π) > 0` per site.)

**4.2 Corollary A″.**  The reduction (kernel `λ(c)e^{−u d(x,c)}/w₀(x)`, reference `μ_{w₀}`) is right, and
`max(w₀, H(c)e^{−u d(·,c)})` *is* what the lemma produces (`r2`, E10–E11).  **The product weights at L286
are wrong.**  Per site, `λ₀(1, e^{−u}) + λ₁(e^{−u}, 1) ∝ (1, e^{−γ})` gives

    λ₁/λ₀ = (e^{−γ} − e^{−u}) / (1 − e^{−(u+γ)})        (nonnegative iff |γ| ≤ u),

not `(1 − e^{−(u+γ)})/(1 − e^{−(u−γ)})`.  (For relative cones normalised to 1 at their centres the ratio is
`(1 − e^{−(u−γ)})/(1 − e^{−(u+γ)})` — the report's expression is the reciprocal of this one.)  Check
(`r2`, E8–E9, `n = 8`): with the referee's ratio `Σ_c λ(c)e^{−u d(x,c)}/w₀(x)` is constant; with the
report's it varies by a factor `600` (`γ = 0.5`), `40` (`γ = −0.3`).  `u = 1`, `γ = ½`: correct ratio `0.3072`,
report's `1.974`.  The same inverted ratio is the line `lam = …` of `experiments/phase2/p2_field_flat.py`;
with it the "hiding law" has `θ` increasing in `γ` where it must decrease, and the relative mixture is
not flat (`r3`, Part 0: it ranges over `[0.34, 19.8]·ε₀` at `p = 0.3`, `u = 1`, `γ = 0.4`, `n = 9`).

**4.3 §2.4 (3): the claim "void at the constant baseline" is false.**  For `π = Bernoulli(p)ⁿ` and the
baseline `e^{−γ|x|}`: `μ_{w₀} = Bernoulli(p′)ⁿ`, `logit p′ = logit p − γ`; `z₀ = e^{−(u−γ)}`, `z₁ = e^{−(u+γ)}`;
`s₀ = 1 − p′ + p′z₀`, `s₁ = p′ + (1−p′)z₁`; the hiding law is `Bernoulli(θ)ⁿ`, `θ = (1−z₀)s₁/(1−z₀z₁)`
(`= s₁/(s₀+s₁)` at `γ = 0`); `x ∈ B_c` iff `ln ε₀ + Σ_i ln(k(x_i,c_i)/s_{c_i}) > 0`, `k` the relative cone.
Chernoff, for every `n`, every query `x` and every `t ≥ 0`:

    q({c : x ∈ B_c})  ≤  ε₀^t ∏_i E_q (k(x_i,c_i)/s_{c_i})^t  ≤  ε₀^t · max( ρ_t(0), ρ_t(1) )ⁿ ,
    ρ_t(0) = θ(z₁/s₁)^t + (1−θ)s₀^{−t},     ρ_t(1) = (1−θ)(z₀/s₀)^t + θ s₁^{−t} ,

so `−n^{−1}ln P_hit ≥ max_t min_a(−ln ρ_t(a)) − O(1/n)`, with equality in the limit (Cramér).  Two
general facts.  (i) *The exponent is positive for every product reference and every tilt `|γ| < u`:*
flatness is exactly `ρ_1(a) = θ k(a,1)/s₁ + (1−θ)k(a,0)/s₀ = 1` for both letters `a`, and `ρ_0(a) = 1`; `t ↦ ρ_t(a)`
is strictly convex (a moment generating function of a non-constant variable when `0 < p′ < 1`), so
`ρ_t(a) < 1` on `(0, 1)` and already `t = ½` gives `P_hit ≤ ε₀^{1/2}·max_a ρ_{1/2}(a)ⁿ`, exponentially small.
(ii) *At `γ = 0`, `p < ½`, the binding query is the mode, for every `u`:*
`ρ_t(0) − ρ_t(1) = (1 − e^{−ut})(s₀^{1−t} − s₁^{1−t})/(s₀ + s₁) ≥ 0` on `[0, 1]` because `s₀ > s₁`; the rate is that of
the binomial tail `P(Bin(n, θ) < κ*n)`, i.e. `KL(κ*‖θ)`, `κ* = ln(1/s₀)/(u + ln(s₁/s₀)) < θ` (the margin `θ − κ*`
vanishes only as `p → 0`).  In the two examples `−ln ρ_{t*}(1) = 0.057`, `0.323` against
`−ln ρ_{t*}(0) = 0.0109`, `0.0056`.

| | `θ` | `κ*` | limit | exact `−ln P_hit/n` at `n = 160, 480` (all queries) | mode query at `n = 10³, 10⁴, 10⁵, 10⁶` |
|---|---|---|---|---|---|
| `p = 0.3`, `u = 1` | `0.40758` | `0.33589` | **`0.010881`** | `0.02141, 0.01519` | `0.01350, 0.01126, 0.01093, 0.01089` |
| `p = 0.1`, `u = 2` | `0.19536` | `0.15473` | **`0.005562`** | `0.01535, 0.00929` | `0.00780, 0.00588, 0.00560, 0.00557` |
| `p = 0.5`, `u = 1` | `0.5` | — | `h = 0.029139` | `0.04332, 0.03442` | `0.03230, 0.02957, 0.02919, 0.02915` |

(`r3`, Parts 1, 1b.)  The referee's exact sums reproduce the coordinator's four values at `n ≤ 160`
(`0.04198, 0.02919, 0.02073, 0.01535`) to all digits; the error is the extrapolation.  The same slow
`(ln n)/n` approach is visible on the uniform cube, where nobody doubts the limit `h`.  So Theorem A″
is **not** void at the constant baseline: for `M = exp(e^{o(n)})` observables at sub-exponential tolerance
it gives the exponents `0.0109` and `0.0056` there.

**4.4 §2.4 (3): the tilted-baseline numbers.**  With the correct weights (dual formula of 4.3; checked
against a brute-force grid over types, against exact sums at `n ≤ 320`, and against the mode query at
`n = 10⁵`; `r3`, Parts 2, 2c):

| | flat family at `γ = 0` | best over `γ` (correct weights) | report (inverted weights) | class exponent (Theorem 11.59 (b), `max_{γ,t} F`) | report |
|---|---|---|---|---|---|
| `p = 0.3`, `u = 1` | `0.0109` | **`0.0122`** at `γ ≈ −0.31` | `0.0236` at `γ = +0.1` | **`0.02503`** | `0.0253` |
| `p = 0.1`, `u = 2` | `0.0056` | **`0.0106`** at `γ ≈ −1.17` | `0.0203` at `γ = +1.0` | **`0.04813`** | `0.0489` |

The report's numbers are reproduced by the referee's code *when the ratio is inverted*: on a `121³`
grid of types `0.02360` at `γ = +0.1` (`p = 0.3`, `u = 1`) and `0.02007` at `γ = +0.8` (`p = 0.1`, `u = 2`) — the digits of
the coordinator's output — and `0.02351`, `0.01997` for the maxima by the dual formula.  They are hit
exponents of a family whose mean ensemble is not the reference, to which Corollary A″ does not apply.  The class exponents were
computed in two independent ways (the closed form of Theorem 11.59 (b); the referee's own
large-deviation programme for centres of one type; `r6`): `0.02503`, `0.04813`; the report's values come
from a `121³` grid and are 1–2 % high (its script says "not checked against Theorem 11.59").  So the
flat family keeps **49 % and 22 %** of the class exponent at the best tilt (43 % and 12 % at the
constant baseline), not "between 40 % and 95 %".

*Replacement for L298–309* (and, accordingly, for the last sentence of row A″, L30: "…with a field a
positive but smaller exponent at every baseline `e^{−γ|x|}`, the constant one included (§2.4)"):

> (3) **For a non-uniform reference the theorem gives a positive but smaller exponent.**  For
> `π = Bernoulli(p)ⁿ` and the baseline `e^{−γ|x|}` the hiding law is `Bernoulli(θ)ⁿ` and, for every `n`,
> `P_hit ≤ ε₀^t max_a ρ_t(a)ⁿ` (Chernoff; notation of [4.3]), with equality at the exponential scale
> [P].  At the constant weight the worst query is the mode and
> `−n^{−1}ln P_hit → KL(κ*‖θ)`, `κ* = ln(1/s₀)/(u + ln(s₁/s₀))`: `0.0109` at `p = 0.3`, `u = 1` and `0.0056` at
> `p = 0.1`, `u = 2` (the convergence is slow: `0.0214` and `0.0153` at `n = 160`).  The best values over `γ`
> are `0.0122` and `0.0106`, against `0.0250` and `0.0481` for the class (Theorem 11.59): 49 % and 22 %.
> So with a field a positive exponent survives every family of `exp(e^{o(n)})` observables at
> sub-exponential precision [P]; whether the class exponent itself is invariant is open.

*Note added while this file was being written:* the coordinator has since rewritten
`experiments/phase2/p2_field_flat.py` and `p2_field_flat_exact.py` (their headers cite this section); the
new outputs — an implementation independent of the referee's code — give `0.010881`, `0.005562`,
`0.01220` at `γ = −0.31`, `0.01064` at `γ = −1.17`, `0.02503`, `0.04813`, i.e. the numbers above.  Seen, not
reviewed; the report text at commit `76e3218` still has the old statements.

**Where the false statement has been copied** (searched, not reviewed): `docs/phase2/MANUSCRIPT.md`
(the same paragraph and the same ratio), `docs/THEORY_REPORT.md` §11.34 ("void at the exponential
scale at the constant weight with a field; D71"), `docs/DEAD_ENDS.md` (D71, item 1 — registered as a
dead end on the evidence of `n ≤ 160`), `docs/collaboration/messages/theory/THY-MSG-0023.md` ("One
negative result that concerns anyone working with non-uniform references…").  All four need the
correction; D71 item 1 should be withdrawn.

**4.5 "The flat mixture is unique" (L300–301).**  The kernel is invertible (`r2`, E2: least eigenvalue
`(1 − e^{−u})ⁿ`), so the *coefficient vector* `q(c)H(c)` of a flat superposition is forced to be constant.
The hiding law `q` itself is not: every `q̃ > 0` with heights `ε₀/(Σ₀q̃(c))` is flat (`r2`, E7).  What singles
out `q ∝ m` is the normalisation "all members have the same `π`-mass" — equivalently, it minimises
`E_q̃[mass²] = ε₀²Σ_c q(c)²/q̃(c)` (Cauchy–Schwarz), the quantity the concentration step pays for.  Row A″ of
the §0 table says this correctly ("the unique law for which *mass-normalised* cones add up to a
constant"); L300–301 should say the same, and the inference "this *forces* centres near the mode"
holds for mass-normalised families only.  (Whether unequal masses with a second-moment bound do
better with a field was not examined — outside this brief.)

## 5. Theorems B, B′, Corollary B′ — **correct as stated**

**B.**  Lemma 3.1 uses no boundedness, so "arbitrary real observables through their joint spectrum" is
right (`r2`, F5: an observable with coefficients of size 50).  Subgroup average: admissible, `A`
preserved, `C`-invariant, `= 1` off `|C|` balls ✓ (F3–F6).  (b): averaging keeps `|ln A(w₁) − ln A(w₀)|`
exactly — cleaner than the archive's Theorem 4′, which loses `ln|C|` in the accuracy.  (c): `C^⊥ ∩ W = {0}`
⇒ `dim C ≥ d` ✓ (F7, exhaustive for `n = 6`, `d = 3`).  The §0 table's "the bound on `|C|` is attained"
(L31) is loose: what is shown is `min|C| = M + 1` for these `S`, against the general bound `< 2(M+1)` —
tight up to the factor 2, and only for the subgroup method (Theorem C shows the *complexity* there is
`(1−θ)h`, far above what any subgroup gives).

**B′.**  Random generators and the **multiset** of all `K` combinations: for two distinct index sets the
overlap depends only on `c ⊕ c′`, a non-trivial combination, hence uniform (also when the generators
are dependent — coincident elements are counted in `E O` with their probability `2^{−n}`) ✓;
`E O ≤ ½K²m_rV/2ⁿ ≤ Km_r/8` uses `4KV ≤ 2ⁿ` ✓; the two failure probabilities `≤ ¼ + ¼` ✓; `C`-invariance of
the maximum over the multiset (translation by `c₀ ∈ C` permutes index sets) ✓; `O` independent of `a` ✓.
Simulation `n = 12`, `M = 6`, `K = 32`: `P(C^⊥ ∩ S ≠ ∅) = 0.17 ≤ 0.19`, `P(O > Km_r/2) = 0.007`; for every good
draw `w_a` is admissible, invariant, has no component on `S`, and `A − 1 ≥ Km_r − O` (`r2`, F8–F10).
Exponent `h̄(λ)` for `λ < a` ✓ (no side condition: the invariance is exact).

**Corollary B′.**  `α₀ = 0.004562`, `α₁ = 0.023387` ✓.  Upper bound: the archive's (A8) ✓, acknowledged.
Rao: a subgroup with `C^⊥` free of words of weight `≤ αn` is an orthogonal array of strength `αn`, so
`|C| ≥ V(n, ⌊αn/2⌋)` ✓; and `h̄(h₂(α/2)) < (1−α)h` on the whole range where the left side is positive
(`r1`: least margin `7·10⁻⁵` at `u = 1`, attained as `α → 0`) — so "no construction of this kind can
close it" is right for every fixed `α > 0`.

## 6. Theorem C, Corollary C, Proposition C′ — **correct; one protocol count to repair**

**C (a).**  Cylinders: admissible on `X`, `A(w) = A(v)`, block law uniform ✓ (`r2`, G4); a non-adaptive
algorithm stays non-adaptive after the restriction (its points depend on the seed and the fixed
answer "uniform").  **(b).**  `A(w) = 2^{−b}E_y w(s,y)/ν_w(s)` ✓ (G1); `P_{s~ν̂}(|ν_w(s)/ν̂(s) − 1| > κ) ≤ ‖ν̂ − ν_w‖₁/κ`
✓ (G3); `κ = 1 − e^{−ε/4}` gives `|ln(ν_w/ν̂)| ≤ ε/4` because `2 − e^{−x} ≤ e^{x}` ✓; `ε/4 + ε/4`, `δ/2 + δ/2` ✓.
**(c)** ✓.

**Corollary C.**  (i) unions at `τ/4` ⇒ `‖·‖₁ ≤ τ` ✓ (`‖·‖₁ = 2 max_S|·|`).  (ii) cells at tolerance `τ2^{−b}`:
a *law* consistent with the reports is within `2τ` (the reports themselves within `τ`); harmless
("`e^{−γn−O(1)}`").  "With (O2), `b` queries suffice (halving, keeping the heavier half)": the guarantee
`m_{i+1} ≥ m_i/2 − τ′` uses a reported mass for **both** halves — `2b` queries.  With one query per level
and the other half's mass obtained by subtraction, the error of the running estimate grows by `τ′`
at each level at which the unqueried half is kept.  *Replacement:* "`2b` queries".

**C′ (a).**  `P(bad term) ≤ τ/κ`; the median fails only if at least `k/2` terms are bad:
`≤ 2^k(τ/κ)^{k/2} = (4τ/κ)^{k/2}` ✓.  The §0 table's hypothesis "`τ ≤ cεδ`" is not what the median argument
needs (`τ < κ/4`); with `τ ≤ κδ` one evaluation suffices.  **(b)** ✓ — but it is the archive's (§8 below).
**(c), lower bound.**  The wells are admissible, `= 1` on `Q`, `= e^Δ` exactly off the balls ✓ (`r2`, H1);
`A > e^Δ(1−p)` ✓; in fact `TV(μ_w, π) ≤ p` (off the balls the density ratio is `e^Δ/A ≥ 1`), so the
report's `p/(1−p)` is correct and loose; the threshold `p ≤ τ/3` could be `τ/2`.  **(c), upper bound.**  With
both halves reported at each step, `m_b ≥ 2^{−b} − 2τ ≥ 8τ/κ − 2τ ≥ 6τ/κ` ✓, relative accuracy `κ/6` ✓,
`2^{n−b} ≤ (16τ/κ)2ⁿ` ✓ — again `2b` queries, not `b` (L424).

## 7. Numbers (independent replication)

All with the referee's own code, written from the definitions; the coordinator's scripts were read
(after the referee's own derivations, to locate the source of a discrepancy) and neither run nor
imported.

| quantity | report | referee | script |
|---|---|---|---|
| `a, ρ₀, h, ℓ` at `u = 1` | `0.110944, 0.379885, 0.029139, 0.4900` | `0.11094407, 0.37988549, 0.029139139, 0.490034` | `r1` |
| the same at `u = ½`, `2` | (in `out_p2_checks.txt`) | `0.030300, 0.438140, 0.007673, 0.4974`; `0.327813, 0.283110, 0.097281, 0.4645` | `r1` |
| Chernoff information `max_t J(t)` and its maximiser | `h`, `ℓ` | `h`, `ℓ` (10 digits, three values of `u`) | `r1` |
| table of §2.3 | 10 entries | all reproduce to 6 digits | `r1` |
| side condition of Cor. A′; `h/2` | `0.01544` (`0.0154`); `0.01457` | `0.0154391`; `0.0145696` | `r1` |
| `α₀`, `α₁` (`u = 1`) | `0.00456`, `0.02339` | `0.0045617`, `0.0233873` | `r1` |
| `ν*` (`u = ½, 1, 2`) and `ν*/h` | `0.003097, 0.011726, 0.038738`; `0.404, 0.402, 0.398` | `0.003097163, 0.01172613, 0.03873799`; `0.40365, 0.40242, 0.39821` | `r1` |
| slopes of §5 | `−1.02`, `−0.042` | `−1.0199`, `−0.04204` | `r1` |
| `h(¾)`, `h(5/4)` (new Cor. 2.7) | `0.0169`, `0.0439` | `0.01689`, `0.04388` | `r5` |
| §2.4 (3): `−ln P_hit/n` at `n = 160` | `0.015` | `0.01535` (and all four values of the coordinator's output) | `r3` |
| §2.4 (3): its limit | **`0`** | **`0.005562`** (`p=0.1,u=2`), **`0.010881`** (`p=0.3,u=1`) | `r3` |
| §2.4 (3): best flat exponent over `γ` | **`0.0236`, `0.0203`** | **`0.0122`, `0.0106`** | `r3` |
| §2.4 (3): class exponent with a field | `0.0253`, `0.0489` | `0.02503`, `0.04813` | `r6` |
| Corollary A″: `λ₁/λ₀` at `u = 1`, `γ = ½` | **`1.974`** (formula of L286) | **`0.3072`** | `r2` |

Exact enumeration on cubes of 8–12 sites (`r2`, 148 checks, none failing): Lemma 2.2 and (2.1);
Theorem A's range and good event; Lemma 2.5 (i)–(iii) with clustered and random centres and the
counterexample to (iii) without proviso; Theorem A′ on its good event; Lemma 2.6, Theorem A″'s two
expectations, Corollary A″ with both ratios; Lemmas 3.1, 3.2, Theorem B (a)–(c), Theorem B′; the zoom
identity, the sampling bound, the cylinders; the wells.

## 8. Novelty table (§9) — **accurate, with one omission**

Read in the archive: `INFERENCE_LIMITS.md` Lemma 1, Theorem 4; addenda A1, A7, A8, A9, A10, A12.

* Row 1 ("Theorem B (d): nothing in substance — S2's corollary is theirs"): accurate, and modest.
  Theorem 4 + A1 give `k = o(n/ln n)` for both exponents; A8's `h − h(α) ≤ θ` for `K = αn` gives `k = o(n)`
  for the adaptive exponent by letting `α → 0` (the archive states `o(n/ln n)`; the inference is
  immediate, as the report says).  For the *non-adaptive* exponent and `n/ln n ≲ k = o(n)` the archive
  has no statement (A1 uses BCH codes); it follows from A1 with Gilbert–Varshamov codes, or from
  Theorem B (b).
* Rows 2–6: accurate.  A10's mechanism is an *average over the translates of a code* plus the
  attenuation `tanh(u/2)^j`; "a different mechanism (random translates)" is fair.  The archive's
  Theorem 4 already takes the **maximum** of a dip over a coset (`g_a^C = −c(r − d_H(x, a+C))₊`); what
  Theorem B′ adds is the *narrowing* of the radius until the `K` dips together carry the excess, and
  the random multiset.  A10 remark (2) does say "the crossover — tolerance `e^{−γn}` — is open".
* Row 7 ("Theorems C, C′, E"): **omission.**  Proposition C′ (b) — one exact point probability and one
  evaluation — is in the archive: A8's table ("the full law at one point | `0`"), A8's "`θ = 0` for
  `K = n`", and the identity of A7 with the `n`-body marginal in the denominator.  (The exact-oracle
  zoom of Theorem C (b) is A8's upper bound, and the table says so.)  New in C/C′: the tolerant
  versions, the cylinder lower bound for a block, C′ (a), C′ (c), Theorem E.
* Lemma 2.3's parenthesis (L122), "the science division's Lemma 1, `lemma1a`, `lemma1b`": this is
  Lemma 1 of the division's **workstream F** report (`SF_REPORT.md`, machine-checked in
  `OracleLowerBound.lean`), not Lemma 1 of `INFERENCE_LIMITS.md` (the orthogonal-array lemma), which
  is what "Lemma 1 (dual distance)" in the novelty table means.  Say which.
* "S1 — correct", "S2 — correct": the texts of S1 and S2 are not in the repository; what was
  checked is that the statements *as rendered in §9* follow from Theorems A and B.  They do.
* Prior art outside the programme: citations from the author's memory; not checked (no network).

## 9. Lean versus text

Read: `proofs/Frontiers/ObservationInvariance.lean` (645 lines at v1; 764 after `d267d15`, which adds
Part 7 — `abs_log_le_of_abs_sub_one_le`, `random_cell_failure_le`, `chebyshev_iid_mean` — not cited by
any [V] label of the report).  Not compiled by the referee.

| label in the report | Lean statement | agreement |
|---|---|---|
| Lemma 2.1 [V] | `LogLip.comp_isometry`, `.convex_comb`, `.max`, `.sup'`, `.cone`, `.dip` | yes; `LogLip` = positive and `w x ≤ e^{u d x y} w y`; `cone`/`dip` need a symmetric `d` with the triangle inequality and `H > 0` |
| Lemma 2.2 [V] | `massOf_convex_comb_eq`, `ensOf_convex_comb`, `massOf_comp_equiv`, `ensOf_comp_equiv`, `sum_translates_eq` | yes for the four identities (any `π`-preserving bijection; equal masses are a hypothesis of `ensOf_convex_comb`).  The displayed consequence (2.1) is not a Lean statement (two lines from the last two) |
| Lemma 2.3 [V] | `tolerant_oracle_packing`, `…_nonadaptive` | **yes, exactly**: `valid` a relation; correctness for every `g` in the class and every `o` valid for it; `good j` ⇒ in the class, `o₀` valid, targets `> ε` apart; cap over *all* alternatives; conclusion `(1−2δ)Σ_{good} wgt ≤ E|Q(g₀;o₀)|·B`.  Finite seed space, finitely many alternatives, the abstract `QueryAlgorithm` (query set + output + consistency).  Non-adaptive: the query set may depend on the seed and the answer |
| Lemma 2.4 [K; form used: V] | `hoeffding_iid_mean` | one-sided, for the sum: `P(Σ(Y−EY) ≥ t) ≤ exp(−t²/(2L((b−a)/2)²))`; the two-sided mean form of the report is twice this with `t = Ls` (not in Lean; trivial) |
| Lemma 2.5 (i) [V] | `LogLip.sup'` + `LogLip.dip` | yes, given `1 + max_j e_r = max_j max(1, e^{u(r−d_j)})` (not in Lean) |
| Lemma 2.6 [V] | `hiding_law_sum`, `flat_mixture`, `flat_mixture_truncated` | yes; any kernel with constant non-zero row sums, any `π` summing to one, non-zero column masses |
| Lemma 3.1 [V] | `sum_mul_char_eq_zero`, `ensemble_mean_eq_of_spectrum` | yes; the observable is *given* as `a₀ + Σ_{s∈S}a_sχ_s`, and `a₀ = E_πφ` is not in Lean |
| Lemma 3.2 [V] | `parity_balanced`, `exists_separating_tuple`, `exists_generators_cube` | yes for the existence of `r` generators when `|S| < 2^r`; "`|C| ≤ 2^r`, `C^⊥ ∩ S = ∅`, `|C| < 2(M+1)`" are not Lean statements (trivial) |
| §1 (i), (ii) [V] | `cube_exact_dip_randomized` (`QueryRefinements.lean`), `nonadaptive_expected_queries_ge` | present; the cube statement has the two finite sums as hypotheses (as the theory report says) |

The header comment of the Lean file cites "Lemmas 2.1–2.4, 3.1–3.3"; the report has no Lemma 3.3.

**Not machine-checked between the cores and the displayed theorems.**  Theorem A: the product
measure on `X^L` and the independence of the `Y_j`; the range `2(1 − e^{−Δ_k})`; identity (2.1) as the
mean; the two-sided form and the union bound; the hitting probability; `ln A` of a dip; the
instantiation of `tolerant_oracle_packing` with `J = X^L`; **the whole (O2) argument** (Lemma 2.3 does
not cover adaptive statistical queries); the exponents.  Theorem A″: the concentration step and the
algebra after Lemma 2.6.  Theorem B: the Walsh expansion of an arbitrary observable, the subgroup
generated by the tuple, the count of centres.  **Nothing** of Lemma 2.5 (ii)–(iii), Theorems A′, B′,
C, C′, E, Lemma 5.1, Proposition 2.7 is machine-checked beyond closure of the class under maxima and
(since `d267d15`) the two elementary inequalities of Theorem C (b).  The report's §10 and §11.6 say
as much; the phrase "the reductions to the lemmas are short" (L596) is fair for A, A″, B and not a
description of A′, B′, E.

## 10. Overclaiming

1. **L36–39 (the "one sentence").**  "worth a factor `τ^{−2}ln M` and nothing more": proved is *at most*
   that factor (no family is shown to be worth it in the sub-exponential regime).  "whatever is
   measured": on the uniform cube (and, relative to its dip-packing bound, on vertex-transitive
   spaces); with a field only a positive exponent is proved, not invariance.  "honest error bars":
   adversarial tolerance (§2 above).
2. **L28 "iff"** — §2 above.
3. **L430–433 ("Reading").**  "negligible, a constant fraction of the exponent, or everything,
   according to whether `ln(τ^{−2}ln M)` is `o(n)`, `Θ(n)`, or `n ln 2`."  `τ^{−2}ln M` governs the *lower*
   bound.  The known upper bounds weight `ln(1/τ)` once, not twice: with the indicators of the cells
   of `n/2` coordinates at `τ ≈ 2^{−n/2}` one has `ln(τ^{−2}ln M) ≈ n ln 2` and the exponent is exactly `h/2`
   (Theorem C), not `0`.  The collapse is proved for `ln ln M ≈ n ln 2` (all indicators) and for
   `τ ≈ 2^{−n}`, i.e. `ln(τ^{−2}) ≈ 2n ln 2`.
4. **L523 (§7).**  "in `[h̄(λ), (1 − γ/ln 2)h]`": the lower bound needs `h̄(λ) > γ` (otherwise `h − λ`); the
   upper bound is for particular families and is trivial when `γ = 0`, `β > 0`.  (Prefix cells times
   unions inside a cell give `(1 − (γ+β)/ln 2)h`.)
5. **L597 (§10).**  "every identity and inequality of §§2–6 on small cubes": not checked by
   `p2_checks.py` (as its output lists): the product weights of Corollary A″ (they are wrong),
   Theorem B′ (ii), the chain of Theorem A′, the halving guarantee, the median bound, and anything
   of Theorem E beyond `ν*`.
6. **L559–561 (§9).**  "Strengthened: … any reference measure (flat mixture); the exponent
   `h̄(2γ + β)` in place of `h − 2γ − β`": for a non-uniform reference the strengthening is a weaker
   exponent, not the invariance; `h̄` holds under the side condition, for (O1) as stated, for the
   adaptive exponent only.
7. **§2.5 (added after v1): "The flat mixture is the wrong tool for a non-uniform reference."**
   With §4.3–4.4 this is not supported for product references: at `p = 0.3`, `u = 1` (field strength
   `κ = 0.847`) absorption gives `h(u − κ) = 0.00073`, the flat family `0.0109` (constant baseline) and
   `0.0122` (best tilt); at `p = 0.1`, `u = 2` (`κ = 2.197 ≥ u`) Proposition 2.7 does not apply at all
   and the flat family gives `0.0056`/`0.0106` (`r5`, Part D).  Proposition 2.7 is the only statement
   for *interacting* known parts — that claim stands.

## 11. Material added to the report during the review

**Lemma 5.1 (attenuated bias), §5.1 — correct as stated.**  `E_{ν_{Γ⊕a}}φ = Σ_s φ̂(s)ρ̃_Γ(s)ν̃(s)χ_s(a)`, Parseval in
`a` and in `s` ✓; verified by brute force over all shifts on a cube of 10 sites (`r5`, Part A).
`|ν̃(s) − t^{|s|}|` at the critical radius: `3.6·10⁻³, 1.4·10⁻⁴, 3.0·10⁻⁷, 1.9·10⁻¹²` at `n = 100…800`, `u = 1`
(`r5`, Part B), consistent with the archive's bound `τ₀`.  Two remarks on the text around it: "not
hidden … if `β(Γ) > τ`" holds up to the factor `1 − 1/A` between the excess measure and the
ensemble; "**no hiding family of this kind has fewer than about `τ^{−2}` atoms**" is a statement about
the three listed constructions and their unions of cosets (for which the cost `V(n,J/2)τ^{−2}t^{2J}` is
concave in `J` on `[0, k_τ]`, so its minimum is at an end — the argument is complete for these), not a
lower bound for hiding families.  The table and the closing paragraph are heuristic and were not
examined further.

**Proposition 2.7, Corollary 2.7 (absorption), §2.5 — correct as stated.**  `we^{−f} ∈ 𝒲_{u+κ}`,
`ve^{f} ∈ 𝒲_u`, equal ensembles, targets shifted by `ln Z_f`, evaluations in bijection ✓ (`r5`, Part C, field
plus pair interaction on 9 sites).  `h` and `a` are increasing in `u` ✓; `h(¾) = 0.01689`, `h(5/4) = 0.04388`
✓.  In the new summary row "with or without observations" applies to the upper bound always and to
the lower bound in the regime of Theorem A only (the corollary says so; the row does not).  See
§10.7 for its first sentence.

## 11b. The revision of commit `e4991d7` (750 lines, sha256 `10345a25…`)

The coordinator revised the report from §§1–10 of this file while it was being written ("the internal
referee's findings applied").  The changed passages were read once (the diff against commit
`76e3218`); they were not re-derived with the depth of v1.  Found correct: the (O2) statement and the oracle "defined once and for all" in its proof; Lemma
2.5 (iii) with `Õ_c`; the (O2) paragraph after Theorem A′; the product weights
`(e^{−γ} − e^{−u})/(1 − e^{−(u+γ)})`; the new §2.4 (3) — including its general sentence "at the constant weight
and `p < ½` the worst query is the mode", which is true for every `u` (§4.3 (ii) above) — and §2.4 (4);
the new Remark (1) of §2.5 (`h(u − κ) = 0.00073` at `κ = 0.847`); Corollary C (ii) with `τ2^{−b−1}` and `2b`
queries; C′ (a)–(c) (`TV ≤ p`, `p ≤ τ/2`, `2b` queries); the rewritten "Reading"; the §7 row with
`(1 − (γ+β)/ln 2)h`; the novelty row; §10.
**One thing to change:** Remark (4) of §6 (lines 636–637 of that revision, `C = ⌈e^ε⌉ + 1`) — the
referee's own slip, see §1.7: use `C = ⌈2e^ε⌉` and say that the constants depend on `C`.
Two wording points: row A″ of the §0 table (line 40) now begins "The exponent of the uniform cube
for homogeneous references" — what is proved there is the factor `L` in the dip-packing bound of the
space (§2.4 (2)); row C′ (line 44) has `ln(ε/τ)` where the proof has `ln(κ/τ)`, `κ = 1 − e^{−ε/2} ≤ 1` (they
differ for large `ε`).  Theorem B (c) as reworded ("tight up to the factor 2 … about the subgroup
method") is right.  The scripts `p2_field_flat.py`, `p2_field_flat_exact.py` as rewritten give the referee's
numbers; they were read, not run.

## 12. Verdicts

| statement | verdict |
|---|---|
| Lemma 2.1, 2.2, 2.3, 2.4, 2.6, 3.1, 3.2 | correct as stated (and the Lean statements say what the report says, §9) |
| Theorem A (a) for (O1), (b), (c) | **correct as stated** |
| Theorem A (a) for (O2) | **correct after a repair**: the constant is `(1 − η − 2δ)`; add the definition of the oracle off the good event (§2) |
| Lemma 2.5 (i), (ii) | correct as stated |
| Lemma 2.5 (iii) | **correct after a repair**: proviso `O_c < 1 + L m_r`, or state it with `Õ` (§3.1) |
| Theorem A′, Corollary A′, the table of §2.3 | **correct as stated** (for (O1); the (O2) form of §3.3 is what the §5 table needs) |
| Theorem A″ | **correct as stated** |
| Corollary A″ | reduction **correct**; the product weights (L286) **wrong** — replacement in §4.2 |
| §2.4 (1), (2) | correct |
| §2.4 (3) | **wrong**: "void at the constant baseline" (counter-evidence: a Chernoff bound for every `n`, exact sums to `n = 10⁶`); the tilted numbers are those of a non-flat family; replacement text in §4.4 |
| Theorem B (a)–(d), Theorem B′, Corollary B′ | **correct as stated** |
| Theorem C (a)–(c) | **correct as stated** |
| Corollary C (i), (iii) | correct as stated |
| Corollary C (ii) | correct after a repair: `2b` queries; a constant 2 in the tolerance |
| Proposition C′ (a), (b) | correct as stated ((b) is the archive's) |
| Proposition C′ (c) | correct after a repair: `2b` halving queries |
| Theorem E | **correct as stated** (for `ε < ln(11/8)`); the quotations for "bounded accuracy" need the `K`-against-`CK` variant |
| §5 table, §7 table, §8 | correct given the above, with the wording points of §10 |
| §9 novelty table | accurate; add C′ (b) to "what the archive has" |
| Lemma 5.1; Proposition 2.7, Corollary 2.7 (added during the review) | correct as stated |

## 13. Line map and what was not checked

**Line map**, v1 (commit `8e2d8e6`, 614 lines) → pre-revision (commit `76e3218`, 693 lines):

| passage | v1 | pre-revision |
|---|---|---|
| §0 table, row A ("iff") | 28 | 28 |
| §0 table, row A″ ("only around tilted baselines") | 30 | 30 |
| §0 table, row B ("is attained") | 31 | 32 |
| §0 table, row E | 34 | 35 |
| "In one sentence" | 36–39 | 37–40 |
| Lemma 2.3, "the science division's Lemma 1" | 122 | 123 |
| Theorem A, the (O2) sentence | 139–140 | 140–141 |
| its proof, "the form `(1−η)(1−2δ)` needs…" | 172 | 173 |
| Lemma 2.5 (iii) | 202 | 203 |
| Corollary A″, `λ₁/λ₀` | 286 | 287 |
| §2.4 (3) | 298–309 | 299–310 |
| "The flat mixture is unique" | 300–301 | 301–302 |
| §2.5 (new), "The flat mixture is the wrong tool…" | — | 317 |
| Corollary C (ii), halving | 405–406 | 449–450 |
| Proposition C′ (c), halving | 424–425 | 468–469 |
| "Reading" | 430–433 | 474–477 |
| §5 table, first row | 443 | 487 |
| §5.1 (new): Lemma 5.1; "no hiding family of this kind…" | — | 504; 528 |
| Theorem E, "`ε < ln(11/8)`" | 469 | 546 |
| its proof: "Conditionally on neither…"; the display with `1.55η₁` | 485–487; 497 | 562–564; 574 |
| §7 table: "+ the same with…"; "+ `e^{νn}` samples" | 523; 527 | 600; 605 |
| §9, "Strengthened: …" | 559–561 | 637–639 |
| §9 novelty table, row "Theorems C, C′, E" | 576 | 654 |
| §10 table: "the reductions … are short"; "every identity and inequality" | 596; 597 | 674; 675 |

**Not checked.**
* The upper-bound theorems of the theory report on which every "exponent exactly" rests (11.44,
  11.54, 11.58, 11.58a; and 11.59 except its closed form (b), which was *used* and agreed with an
  independent computation).  They are [P], refereed elsewhere.
* The Lean file was read, not compiled (by instruction); `p2_checks.py` and the harness block XXVIII
  with its mutations were not run; the claim "21 mutations, all caught" is unverified.
* The original texts of S1 and S2 (not in the repository).
* Prior art outside the programme (no network).
* `docs/phase2/MANUSCRIPT.md`, `docs/THEORY_REPORT.md` §11.34, `THY-MSG-0023`, `DEAD_ENDS.md` D71: only
  searched for the statements of §4.4.
* §5.1 beyond Lemma 5.1 and the union-of-cosets count (the table's entries, the closing heuristics);
  the remark (3) of §2.5 (marginalisation); site-dependent `κ_i`.
* The single-type exponents with a field at more than two parameter pairs; the flat family for
  references other than `Bernoulli(p)ⁿ`.
* Theorem E was checked by re-derivation and, for its sampling part, by Monte Carlo at `m = 2` on
  cubes of 13–15 sites — far from the regime `m = e^{νn}`; the evaluation part is a union bound and
  was not simulated.
* Anything written to the report after commit `e4991d7`; of that revision, only the changed passages
  listed in §11b, read once.
