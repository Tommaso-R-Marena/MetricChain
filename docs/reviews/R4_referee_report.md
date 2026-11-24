# Referee report R4 — Workstream A, "the randomised exponent of `ln Z`: a two-measure isoperimetric problem"

Reviewed: `<session scratch>/ws/A/REPORT.md`
(629 lines), its scripts/outputs and `lean/WorkstreamA.lean`.
Referee's files: `<session scratch>/referee4/`
(scripts `r4_*.py`, outputs `r4_*_out.txt`; all code written from scratch, nothing imported from `ws/A`).
Nothing in the repository was modified.  Date: 2026-11-24.

Conventions as in the report: site `(S, π, s)`, `k = |S|`, `Lip = {φ : φ(a) − φ(b) ≤ s(a,b)}`,
`Λ(φ) = −ln E_π e^{−βφ}`, `g(φ;Q,t) = −(t/β)Λ(φ) − ln E_Q e^{−tφ}`, `G(Q,t) = max_{Lip} g`,
`R^gen(ε₁) = max_{0≤t≤β}[−ln val(K_t) − tε₁/β]`.

---

## 0. Summary

* **Theorem A(ii) (upper bound, universal sampler): I found no error and no gap.**  I re-derived every
  step (Lemma 0(b), Steps 1–7, Proposition 4(i)–(iii), Lemma 3(a)–(f), Lemma 5) by hand; the two exact
  finite-`n` identities on which Steps 2–5 rest, and the single-letter optimisation of Proposition 4, were
  confirmed with independent code (Section 3).  Two places are written too tersely (the passage from
  interior to boundary `Q` before Sion's theorem; the domain of the inner minimax) — both are repairable in
  one line each and are repaired in Section 2 (m4).  My verdict: **proved**, at the standard of a careful
  paper check by one referee; it is not machine-checked.
* **Proposition 2 / Theorem A(i), Lemma 1, Lemma 3, Theorem B(a)–(d), Corollary A1, Proposition 6: correct.**
  All numbers I recomputed agree with the report to the digits printed (Corollary A2 examples, thresholds,
  closed forms, `E_iid`, exact `FC` for `|Sⁿ| ≤ 16`, finite-`n` binomial tails).
* **No CRITICAL finding.**  Two MAJOR findings, both about what is *claimed around* the theorems, not about
  the theorems:
  * **M1.** The claim that Theorem A "is not a corollary of the known isoperimetric exponent for two fixed
    product measures" (Verdict (iv), §2.3 last paragraph, §2.7 item 6, §4) is unsupported, and in the sense
    that matters it is numerically refuted on the report's own examples: the black-box bound
    `B* = sup_α min_Q ψ_Q(α,(α+ε₁)/β)` — which the report says it "did not evaluate" — **equals `R^gen`**
    on the two biased binary sites I scanned in full (`0.154075`, `0.125830`; agreement within `3·10⁻⁶`),
    and `min_Q ψ_Q` has a local maximum equal to `R^gen` at the extremal `α*` in two further cases
    (`0.091752`, `0.081093`).  So on these
    sites the upper bound follows from Ahlswede–Zhang/Yu's fixed-measure theorem applied with a product
    reference law adapted to the measure exponent of the set.  What is new is the *evaluation* (Proposition 4,
    Lemma 3(c)) and the application, not the isoperimetric statement as such.
  * **M2.** The headline sentences ("the exact single-letter exponent is now known for every alphabet",
    "every binary product instance (… arbitrary additive residual …)", "sharp for every alphabet and every
    `n`") silently need: identical sites (same `π`, `s` at every site, i.e. a site-homogeneous additive
    instance), `ε_n/n → ε₁` with `ln(1/ε_n) = o(n)`, instance complexity (a hint, or `n(k−1)+1` extra
    evaluations on such instances), a hedged output, fixed `δ`.  Heterogeneous sites are "not written out"
    (§2.8) — nothing is proved for them.
* **Theorem B**: the inequality is right (exhaustively: equality `max_h[…] = nβγ(Q)` at the vertices of
  `Lip(Sⁿ)` for `|Sⁿ| ∈ {4, 8, 9}`).  The algorithmic conclusion is right **only for the hedged spot-check**
  (output `ln Z(g) + ε/2 − η`); the theorem does not say so.  With the unhedged spot-check it is false for
  `ε₁^thr < ε₁ < 2ε₁^thr`.  The constant hidden in "`O(ln(1/δ))`" is `≈ βs_max/(ε₁ − ε₁^thr)`.
* **Lean file**: compiles (`lake env lean`, 11.6 s, exit 0), 15 theorems, no `sorry`, axioms
  `propext, Classical.choice, Quot.sound`.  The statements say what the report says (Section 1, last rows).
* **Literature**: Ahlswede–Zhang read in full (3-page summary); Yu arXiv:2205.07596v3 read by me in the PDF
  text for the relevant parts (definition of `ψ`, Theorems 4, 5, 8, Assumption 3, Remark 5, proof §VI-A1).
  The report's attributions are accurate.  I found no prior statement of the free-second-measure/coupled-radius
  problem or of the matrix game; missing citation: Alon–Boppana–Spencer (1998).  My search was cut short
  (6 queries performed; then the shared search budget was exhausted).
* Referee by-product: the crossover of Corollary A2 has the closed form `u_c(k) = ln C(k−1, 2)` (two-line
  identity, Section 2, m9).

---

## 1. Verdict per statement

"hand" = re-derived line by line; "num" = independent numerics (Section 3); depth: low / moderate;
novelty: K known, R routine, N apparently new (within the limits of my literature check).

| statement | correct? | proof checked how | depth | novelty | remark |
|---|---|---|---|---|---|
| §2.0 reduction (profiles, `h_D`, `FC`, symmetrisation) | yes | hand | low | R | `𝒟_n(ε)` is upward closed and contains `supp h_D`, so it has the same hitting number as the family of difference sets |
| Lemma 0(a),(b) | yes | hand | low | R | (b): pigeonhole over `J = ⌈βH⌉` levels; needs `H > 0` |
| Lemma 1 (generalised dips) | yes | hand; Lean `genDip_admissible`, `genDip_effect` | low | R | precedent for "sublevel sets of additive Lipschitz functions are extremal": Alon–Boppana–Spencer 1998 (not cited) |
| Proposition 2 / Theorem A(i) (`FC_n(ε) ≥ e^{−tε/β} ρ_t(M)^{−n}`, every `n`) | yes | hand; ingredients in Lean | low | N (routine proof) | it is a random-covering bound for the source `M` on centres with distortion `σ_φ(a)`; valid for every finite `F ⊂ Lip` and every `t ≥ 0` |
| Lemma 3(a),(b),(d),(e),(f) | yes | hand; num (`r4_misc`: (b),(e),(f)) | low | R | (e): the optimal `M` of the rate–distortion form is the optimal column strategy of `K_{t*}` (KKT) — confirmed numerically |
| Lemma 3(c) (max over `Lip` at a vertex for `t ≤ β`) | yes | hand; num (1500 sites: 0 violations for `t ≤ β`, 518 for `t > β`) | low–moderate | N | strictness needs `0 < t < β` and full support of `π`; `Q` arbitrary.  Not needed for the *truth* of Theorem A (a net of `Lip` would do), only for the vertex form |
| Closed forms §2.2 (two-state; biased cube; flat `k`-state; thresholds) | yes | hand; num (`r4_check_numbers`, `r4_scan`: 40 random two-state sites, max dev. `5.6·10⁻⁸`) | low | R/N | ratio limit `k²/(4(k−1))` only for even `k` (odd `k`: `(k+1)/4`) |
| Proposition 4(i),(ii),(iii) (collapse to a matrix game) | yes | hand; num (`r4_prop4`: primal convex programmes, 800 random laws, `|V(tilted) − R^gen| ≤ 2·10⁻¹¹` in 20 cases; `r4_prop4_adv`: local ascent from 6 starts × 4 cases never exceeds `R^gen`) | moderate | N (technique K: Lagrange + Kantorovich + Gibbs, as in Yu's Thm 8) | two terse spots, see m4 |
| Lemma 5 (inherently typical subset, weighted, rounding-up quantiser) | yes | hand; num (`r4_lemma5_step5`: 90 (set, `m`) instances, identities to `4·10⁻¹⁶`) | low–moderate | variant of K | it is **not** the AYZ statement (other quantiser, gap `k/m` for all `m ≥ 1` instead of `log²m/m` for `m ≥ 2^{16|X|²}`, weighted); the report's own 8-line proof is complete, so Theorem A does not depend on the literature here |
| **Theorem A(ii)** (universal sampler, Steps 1–7) | **yes — no gap found** | hand (every step, Appendix A); num (Step 4 mean-cost constancy and Step 5 inequality exactly, 270 kernels; asymptotic falsification test with block-periodic sets, `r4_block`) | moderate | statement N; proof = AZ/Yu's with the reference law chosen after the set | see M1 for the relation to the fixed-measure theorem |
| Theorem A, "Consequently…" (instance complexity `= exp(nR^gen + o(n))`) | yes, with the hypotheses of M2 | hand | low | N | upper bound = hedged spot-check with hint; hint-free on homogeneous additive instances at `+n(k−1)+1` evaluations |
| Corollary A1 (two-state sites: `R^gen = R^rand`) | yes (given A) | hand; num | low | N | `0.027531, 0.154075, 0.188226` at `β = 1, 4, 40` reproduced |
| Corollary A2 (`|S| ≥ 3`: dips not extremal) | yes | num: every quoted number reproduced (Section 3); uses Proposition 2 only | low (high impact) | N | "false for `|S| ≥ 3`" means "fails in general": the flat ternary site is not a counterexample |
| Theorem B(a) two-measure tensorisation | yes | hand; Lean `twoMeasureBound_prod/_pow`; num exhaustive | low | K for `Q = π` (tensorisation of the Laplace functional over Lipschitz functions); trivial extension to `Q ≠ π` | tight: equality for additive `h` |
| Theorem B(b) sandwich | yes | hand | low | R | |
| Theorem B(c) hitting bound and bounded cost above `ε₁^thr` | inequality yes; algorithmic sentence needs "hedged" | hand; Lean `mass_ge_of_twoMeasureBound`, `product_mass_ge`; num | low | N (use) | see m1 |
| Theorem B(d) (`ε₁^thr ≥ ε₁^crit`, examples) | yes | hand; num (`0.119685` vs `0.094716`; `0.120115` vs `0.107374`; `R^gen(0.10) = 7.78·10⁻⁴`) | low | N | |
| Proposition 6 (product samplers) | yes | hand (Chernoff); num (`E_iid = 0.165519` vs `0.154075`; `0.131033` vs `0.125830`; equality on the uniform cube) | low | N | vertices and unrestricted `t` suffice here (checked on the whole segment); the *inference* drawn from it in Verdict (iv) is M1 |
| §2.7 item 4 (inf-convolution inequality tensorises) | yes | hand (one-site case and induction step) | low | K-type | numerics of `v4` not re-run |
| Lean `WorkstreamA.lean` vs report | consistent | ran; read all 15 statements | — | — | Lean's `γ` is the report's `βγ(Q)`; `π` not normalised; profiles of any sign; convention `h y − h x ≤ s x y` (evaluated point first) as in the report; not linked to `Admissible`/`QueryAlgorithm`; facts `0 ≤ h_D ≤ n s_max 1_D` and "`γ` = max over vertices" not formalised — all of which the report says |

---

## 2. Errors and gaps

### CRITICAL
None.

### MAJOR

**M1. "Not a corollary of the fixed-measure exponent" — unsupported, and numerically false in the relevant
sense.**
*Location:* Verdict (iv) ("so the result is not a corollary of the known isoperimetric exponent for two
fixed product measures (Yu 2024)"); §2.3 "What the proof is"; §2.7 item 6 ("gives the bound
`sup_α min_Q ψ_Q(α,(α+ε₁)/β)`, which lies between `R^gen` and `E_iid` …; I did not evaluate it, and it is
not needed"); §4 table, last row.
*What is wrong.*  Proposition 6 shows that no *single* product sampler is optimal.  That does not exclude
the obvious use of the known theorem: for a sensitive `D`, Lemma 0(b) gives `(A, r)` with
`βr ≥ nα_A + nε_{1,n}`; choose a product law `Q` *as a function of `α_A` only* (finitely many values of
`α` suffice by monotonicity of the exponent in `(α, τ)`), apply the fixed-measure theorem (Yu, Theorem 5,
Statement 2: bounded cost, Assumption 3 trivial on a finite alphabet with the discrete metric) to
`(P_X, P_Y, c) = (π, Q, c(x,y) = s(y,x))`, and dominate the finitely many `Qⁿ` by the type mixture.  This
gives the exponent `B* = sup_α min_Q ψ_Q(α,(α+ε₁)/β) ≥ R^gen`.
*What I computed* (`r4_blackbox_yu2.py`, `r4_blackbox_star.py`, `r4_blackbox_yu3.py`; dual formula
`ψ_Q(α,τ) = sup_{t≥0} inf_{η>0} [ηα − tτ + max_{φ∈Lip}(−ln E_Q e^{−tφ} + η ln E_π e^{−(t/η)φ})]`, which is
Yu's Theorem 8 with `f = −φ`, `g = φ`; cross-checked against a primal search over laws `P_{UX}`, `|U| = 2`,
in `r4_blackbox_primal.py`):

| site (two states, Hamming, zero residual) | `R^gen` | `E_iid` | `min_Q ψ_Q` at `0.90, 0.97, 1.00, 1.03, 1.10 × α*` | minimising `Q₀` at `α*` (`Q*₀`) |
|---|---|---|---|---|
| `e=.5, c=1, β=4`, `ε₁=0` | 0.154075 | 0.165519 | 0.153281, 0.154006, **0.154073**, 0.154008, 0.153343 | 0.76449 (0.76449) |
| `e=1.5, c=3, β=1`, `ε₁=0` | 0.125830 | 0.131033 | 0.125139, 0.125770, **0.125830**, 0.125772, 0.125202 | 0.73982 (0.73982) |
| `e=.5, c=1, β=4`, `ε₁=0.2` | 0.091752 | — | 0.091061, 0.091692, **0.091752**, 0.091693, 0.091107 | 0.75061 (0.75061) |
| `e=1, c=2, β=1`, `ε₁=0` | 0.081093 | — | 0.080632, 0.081053, **0.081092**, 0.081054, 0.080674 | 0.69471 (0.69471) |

(The values at `α*` lie `2·10⁻⁷`–`3·10⁻⁶` *below* `R^gen`, which is impossible in exact arithmetic because
`B* ≥ R^gen`; it is the discretisation of the supremum over `t`.  A finer evaluation at `(Q*, α*)` of the
first site gives `0.154075`.)  Full scans over `α` (15 and 13 values, first two sites) are unimodal and peak
at `α*` within the grid resolution (`α* = Σ_w M*(w) KL(μ_w‖π)`, the measure exponent of the extremal
generalised dip).  At `(Q*, α*)` the
supremum over `t` is attained at `t*` with `t/η = β`, i.e. the extremal dip of the report is also the worst
set for the fixed pair `(π, Q*)`.  Hence `B* = R^gen` on the first two sites (full scans), and `B(α)` has a
local maximum equal to `R^gen` at `α*` in the other two cases (only `0.9–1.1 α*` scanned): **the
fixed-measure theorem, used as a black box with an `α`-adapted reference law, yields the upper bound of
Theorem A(ii) there** (modulo the routine grid argument of (iii) below).
*What remains true.*  (i) The black box gives `B*`, a sup–min–sup–inf formula; that it equals a matrix game
on the Lipschitz vertices is the content of Proposition 4/Lemma 3 and is not in the literature I saw.
(ii) I have no proof that `B* = R^gen` in general (it is a minimax statement for a function convex in `Q`
but not concave in `t`); the report's direct proof does not need it.  (iii) Yu's theorem is pointwise in
`(α, τ, P_Y)`; the reduction needs the routine grid/monotonicity argument.
*Fix.*  Replace the claim by: "the proof is Ahlswede–Zhang's/Yu's with the product reference law chosen
after the set; used as a black box with a reference law depending on the measure exponent, the
fixed-measure theorem gives `sup_α min_Q ψ_Q(α,(α+ε₁)/β)`, which coincides with `R^gen` in the examples
computed; the new content is the evaluation of the exponent (Proposition 4, Lemma 3(c)), the lower bound and
the application."  Reclassify Theorem A(ii) from "[N]" to "new statement, known proof".

**M2. Scope of the headline sentences.**
*Location:* §1 first paragraph and items (i), (iii); title of §2.5; §6 item 2.
*What is proved* is a statement about **`n` identical sites**: one `π` and one quasi-metric `s` for all
sites, i.e. known part `Σ_i φ(x_i)`, residual `Σ_i γ(x_i)` with the *same* `γ`, additive envelope.  The
hypotheses that the summary leaves out:
1. identical sites (heterogeneous sites: only a conjectured formula, §2.8, "not written out"; so
   "every binary product instance (… arbitrary additive residual …)" must read "… every site-homogeneous
   additive residual");
2. the accuracy regime `ε_n/n → ε₁ ≥ 0` **and** `ln(1/ε_n) = o(n)` (stated in Theorem A, absent from the
   verdict; for exponentially small `ε` the formula is false, D35);
3. the quantity is the *instance* complexity: the matching upper bound is a spot-check that is given the
   instance as a hint; hint-free it costs `n(k−1)+1` more evaluations and only on homogeneous additive
   instances (so "`O(1)` random evaluations" above the threshold is `O(n)` evaluations without a hint);
4. the output must be hedged (m1);
5. `δ ∈ (0, ½)` fixed; algorithms = finite mixtures of `QueryAlgorithm`s;
6. "sharp for every `n`" means: `FC_n(nε₁) ≥ exp(nR^gen(ε₁))` for every `n` when `ε₁ < ε₁^thr`, and
   `FC_n(nε₁) ≤ βs_max/(ε₁ − ε₁^thr)` for every `n` when `ε₁ > ε₁^thr` — true; nothing at `ε₁ = ε₁^thr`,
   and the bound blows up at the threshold.
*Fix.*  State 1–5 in the verdict.  Downstream texts should say "additive instances with identical sites".

### MINOR

**m1. Theorem B(c): the hedge is missing from the statement.**  "`q = ½πⁿ + ½Q*ⁿ` with `O(ln(1/δ))` samples
is a correct spot-check" is true for the hedged spot-check of Theorem 11.22(e) and false for the unhedged
one when `ε₁^thr < ε₁ < 2ε₁^thr` (it would have to hit `𝒟_n(nε₁/2)`, which costs
`≥ exp(nR^gen(ε₁/2))`).  Precise statement: hint `g`, output `ln Z(f+g) + ε/2 − η` with
`0 < η < n(ε₁ − ε₁^thr)`, sampler `½πⁿ + ½Q*ⁿ`, `N = ⌈ln(1/δ)/p⌉`,
`p = ½ min{(ε₁ − ε₁^thr − η/n)/(βs_max), 1 − e^{−η}}`; it is `(ε/2, δ)`-correct on the whole admissible
class and makes `N` evaluations on `g`.  Raising alternatives beyond `ε − η` are hit by `Q*ⁿ` (B(c)),
lowering ones beyond `η` by `πⁿ` (Lemma 0(a)); alternatives of full support are detected by every sample
(`D = Sⁿ`); B(a) itself holds for profiles of any sign.  With `η = n(ε₁ − ε₁^thr)/2`, `N` is independent of
`n` but of order `βs_max/(ε₁ − ε₁^thr)`, not `O(ln(1/δ))` uniformly.

**m2. §2.0, "plus `O(ln(1/δ))` samples of `π` for bumps, `ε'` slightly smaller than `ε`."**  The two
requirements pull against each other: with hedge `η` the bumps cost `ln(1/δ)/(1 − e^{−η})`.  The choice
`η = min(1, ε/2)` of §2.3 is the right one; say so here.

**m3. Lemma 5 is labelled "[K: AYZ 1997]".**  The statement proved is a variant (see table).  Label it
"[P], variant of the inherently typical subset lemma".  The proof is correct as written; the only implicit
points are `Σ_b ⌈m p(b)⌉ < m + k` and that labels of prefixes outside `A` are arbitrary.

**m4. Proposition 4, two terse spots (no error).**
(a) "Slater's condition holds … for `Q` of full support, and the infimum over such `Q` equals the minimum
over all `Q` by convexity" proves `V = inf_{int} sup_t Φ(Q,t)`.  To reach `min_Q sup_t Φ` (the object Sion's
theorem treats) add: `Q ↦ sup_t Φ(Q,t)` is convex, lower semicontinuous and finite at interior points, so
its infimum over the interior equals its minimum over the simplex.
(b) "exchanging `min_ν` and `max_φ` (Sion)": restrict `ν` to `Δ(supp Q)` (elsewhere `KL = +∞`) and `φ` to
`Lip ∩ {φ(a₀) = 0}` (compact).  `Φ` is finite on the whole simplex because `𝒦(μ,Q,t) ≤ tW_s(Q,μ)`.

**m5. Corollary A2 / Verdict wording.**  "The main conjecture is false for alphabets of size ≥ 3" should be
"fails in general": it holds e.g. on the flat ternary site.  (In my own ensemble of 300 random three-state
sites strict inequality occurred in 199; the report's ensemble gave 135.)

**m6. Verdict (ii): "`R^gen/R^rand → k²/(4(k−1))`"** holds for even `k`; for odd `k` the limit is
`(k+1)/4` (`k = 5`: `1.497` at `u = 0.01`, not `1.5625`).  §2.2 has the parity caveat, the verdict does not.

**m7. §2.8 / Corollary A2, "as `β → ∞` the gap closes".**  True for the difference.  On the sharp site
`(0,2,2)` the *ratio* stays `≈ 1.20` while both exponents tend to `0` (`1.9·10⁻⁵` vs `2.3·10⁻⁵` at `β = 8`).

**m8. Missing citation.**  Alon–Boppana–Spencer, "An asymptotic isoperimetric inequality", GAFA 8 (1998):
concentration exponent of product metric probability spaces as `sup_λ[λτ − L_G(λ)]`, `L_G(λ)` the maximum
of `log E e^{λf}` over 1-Lipschitz mean-zero `f` on the base space.  It is the precedent for (i) extremal
sets = sublevel sets of additive Lipschitz functions, (ii) a Legendre formula with a maximum over the
Lipschitz polytope of the base space, (iii) Theorem B(a) for `Q = π`.  (Known to me through Yu's paper,
which I read; ABS itself not re-read.)  The brief listed it.

**m9. Corollary A2, crossovers (improvement).**  The printed values `1.10, 1.79, 2.30, 3.04, 4.65, 7.57` are
`u_c(k) = ln C(k−1, 2)`.  Proof of the crossing identity: at `e^u = (k−1)(k−2)/2` one has
`1/k + (1−1/k)e^{−u} = 1/(k−2)` and `2/k + (1−2/k)e^{−u} = 2/(k−1)`, hence `ρ₁ + ρ₂ = 1` and
`D(ρ₁‖1−1/k) − D(ρ₂‖1−2/k) = −ρ₁ρ₂u + ρ₂ρ₁u = 0`.  In particular `u_c(3) = 0` (why the flat ternary site
never is a counterexample) and `u_c(64) = 7.577` (the report prints `7.57`).  That this is the *last*
crossing is numerical (`r4_crossover_closed_form_out.txt`, `k ≤ 100`).

**m10. Remarks to Theorem A, hint-free variant.**  State that the number of samples is computed from the
explicit lower bound on the hitting probability furnished by the proof, and that the algorithm falls back
unless the interpolant has identical sites.  (The interpolant of an admissible residual is admissible for
every additive quasi-metric envelope, not only Hamming — I checked.)

**m11. Scripts vs text.**  Scripts use "sensitive iff `ln E e^{βh_D} ≥ ε`", the text "`> ε`" (immaterial
generically).  The table of §3 says "370 lines, compiles in 15 s": 369 lines, 11.6 s here.

**m12. Proposition 6.**  `E(Q)` is a lower bound on the exponent of the product sampler (the proposition
says `liminf ≥`), so `E_iid` is "at least", not "the" exponent of product samplers; immaterial for the
negative conclusion.

### Assessments requested in the brief

*Novelty and depth* are in the table of Section 1.  In one sentence: the every-`n` statements (Lemma 1,
Proposition 2, Theorem B) are elementary and solid; the asymptotic theorem is a correct assembly of known
techniques whose genuinely new ingredient is the collapse of Proposition 4 with the vertex reduction of
Lemma 3(c); the strongest *consequence* for the project (dips are not extremal; the threshold moves) needs
only the elementary parts.

*Are the summary sentences justified?*  "The exact single-letter exponent is now known for every alphabet":
yes for `n` identical sites at a site-homogeneous additive instance, accuracy `ε_n` with `ε_n/n → ε₁` and
`ln(1/ε_n) = o(n)`, as an instance complexity with a hint (M2), on the strength of a paper proof that I
checked.  "Sharp for every alphabet and every `n`": yes in the sense of M2 item 6, with the hedge of m1.

*Strongest remaining gap between what is proved and what is claimed.*
(1) Scope: identical sites only; the formula for sites of several types is a conjecture.
(2) Status: A(ii) is a paper proof checked by one referee; only the every-`n` parts are machine-checked.
(3) Precision: `FC_n = exp(nR^gen + o(n))` with `o(n)` of order `n^{1−1/(k+1)} log n` at best; polynomial
prefactors, the critical accuracy `ε₁ = ε₁^thr` and exponentially small accuracies are open.
(4) Novelty: the isoperimetric upper bound is closer to the literature than the report says (M1).

---

## 3. Independent numerical checks

All with my own code (`r4_core.py`: Lipschitz-polytope vertices by brute force over `k−1` tight constraints,
matrix games by LP/HiGHS, thresholds by LP; `r4_util.py`: exact vertex enumeration of `Lip(Sⁿ)` by
tight-spanning-structure search, cross-checked against brute force).

| script → output | what | sizes | result |
|---|---|---|---|
| `r4_check_numbers.py` | Corollaries A1/A2, Theorem B(d), closed forms | binary `e/c=½`, `β = 1, 4, 40`; uniform cube `u = .5, 1, 2, ln 16`; flat `k = 3…8` (all `2^k−2` vertices); `(0,0,2)`, `(0,2,2)`; crossovers `k ≤ 64` | `R^rand = R^gen = 0.027531, 0.154075, 0.188226`; `U_β = 0.364667, 0.630380, 0.693147`; thr `0.113668`, `Q* = (0.6137, 0.3863)`, `βγ(π) = 0.122459`; flat 4-state `0.028405` vs `0.029139`; flat 8-state `0.019364` vs `0.030929` (`u=1`, triples), `0.099414` vs `0.119862` (`u=2`, pairs); `(0,0,2)`: `0.024665` vs `0.029032`, thresholds `0.094716` vs `0.119685`, `R^gen(0.10) = 7.78·10⁻⁴`, optimal mix `0.493` dip + `0.507` pair-box; `(0,2,2)`: `0.016395` vs `0.020106`; flat 4-state thr `0.120115 = ln cosh ½` vs `0.107374`; game value = closed form `max_m D(ρ_m‖1−m/k)` in all cases — **all as in the report** |
| `r4_prop6.py` | Proposition 6 | 4 binary sites; vertices only and whole segment, `t ≤ 40β` | `E_iid = 0.165519` (`Q₀ = 0.7654`) vs `0.154075`; `0.131033` vs `0.125830`; `0.027570` vs `0.027531`; equality on the uniform cube; `M* = (0.665, 0.335)` |
| `r4_theoremB.py` | Theorem B(a),(c) exhaustively | all vertices of `Lip(Sⁿ)` for `(k,n) = (2,2), (2,3), (3,2)` (6; 38–53; 534–2238 vertices), 18 sites × 4 laws `Q`; all `2^N−2` sets for `N ≤ 9`; binary `n = 4`: all 65534 sets, 3 sites; 100000 polytope points for the vertex claim on `γ(Q)` | `max_h [ln E e^{βh} − βE_{Qⁿ}h] − nβγ(Q) ∈ [−9·10⁻¹¹, 2·10⁻¹⁰]` (rounding of vertex coordinates): the inequality holds and is tight; (c): no violation; vertex claim: 0 exceptions |
| `r4_thmB_fc_check_out.txt` | `FC_n(nε₁) ≤ βs_max/(ε₁−ε₁^thr)` against exact `FC` | 3 binary sites, `n = 2, 3, 4`, 3 accuracies | holds in 27/27 |
| `r4_prop4.py` | Proposition 4 by a primal convex programme (cvxpy/Clarabel; couplings + `Q`) | 10 sites (`k = 2, 3, 4`; Hamming, symmetric, asymmetric) × 2 accuracies; 800 random laws `P_{UX}`, `|U| ≤ 4` | (iii): `|V(tilted) − R^gen| ≤ 1.9·10⁻¹¹`; (i): `max(V − R^gen) = −3.8·10⁻⁸`; (ii): never violated |
| `r4_prop4_adv.py` | adversarial ascent on `V(P_{UX})` | 4 cases × 6 starts (tilted law, perturbations, other tilts, "dip + nothing") | all converge to `≤ R^gen` (excess `≤ 3.5·10⁻¹⁰`) |
| `r4_lemma5_step5.py` | Lemma 5 and Steps 4–5 exactly | 90 (set, `m`) instances (random, balls, threshold, constrained, parity sets; binary `n ≤ 10`, ternary `n ≤ 6`; `m = 1, 2, 4`), 3 kernels each | (2), (3) hold; `|I(X_I;V|U_I) − (α_Ã − α)| ≤ 4·10⁻¹⁶`; mean cost constant on `Ã` to `2·10⁻¹⁵`; `n⁻¹D(P_{X'ⁿ}‖Qⁿ) ≤ I(X';U) + α_Ã − α` in 270/270 (the correction is needed in 148) |
| `r4_block.py` | asymptotic falsification test of A(ii): exponent `min_Q b⁻¹ sup_t[…]` of block-periodic generalised dips against the universal sampler (tensorisation only gives `E_iid`) | binary: all sets `C ⊂ S^b`, `b ≤ 3`; 4136 of the 65534 sets for `b = 4`; additive vertex functions; 3000 random Lipschitz `Φ`; Nelder–Mead ascent; 3 sites, `ε₁ ∈ {0, 0.2}`.  Ternary `b ≤ 2`: all 510 sets, 2000 random `Φ`; 2 sites | no violation: `0.154070 ≤ 0.154075`; `0.088440 ≤ 0.091752`; `0.123925 ≤ 0.125830`; `0.051342 ≤ 0.066603`; ternary `(0,0,2)`: `0.028929 ≤ 0.029032` (and `> R^rand = 0.024665`); `0.009744 ≤ 0.009778`; `0.024572 ≤ 0.027858` |
| `r4_fc_bruteforce.py` | exact `FC`, `FC_dip`, `FC_box` by full enumeration of all subsets (no symmetry reduction, no MILP) | 17 instances, `|Sⁿ| ≤ 16` | identical to the report's values (`3, 4, 4.80556` vs `3, 2, 3.2`; uniform cube `n = 3`: `4` vs `2`; flat 4-ary `n = 2`: `4` vs `2.28571`; `(0,0,2)`, `ε = 0.1`, `n = 2`: `5.66667` vs `5`; …) |
| `r4_misc.py` | finite-`n` binomial tails; Lemma 3(b),(c),(e),(f) | `k = 8, 4`, `n ≤ 20000`; 8 rate–distortion programmes + 200 random `M`; 1500 + 60 random sites | `ln(N_box/N_dip) = 1.724, 11.345, 115.432, 231.697` and `14.761` as in the report; `R(M*) = R^gen`, random `M` never larger; (c): 0 violations for `t ≤ β`, 518 for `t > β` |
| `r4_scan.py` | two-state closed form; random ternary scan; `β → ∞` | 40 + 300 sites; 4 sites × 7 temperatures | see m5, m7 |
| `r4_blackbox_*.py` | M1 | 4 binary sites | table in M1 |
| `lean_run.txt` | `lake env lean …/WorkstreamA.lean` | — | exit 0, 9 `#print axioms`, standard axioms only |

Note on resources: an early version of the black-box script allocated ~2 GB arrays; I stopped it and
replaced it by a one-dimensional evaluator.  The remaining scripts are light.

---

## 4. Literature

**What I read.**
* Ahlswede–Zhang, "Asymptotical isoperimetric problem": the complete 3-page summary (Bielefeld PDF 149,
  pages rendered and read).  Theorem 1: `ξ_N(R,δ) = inf_{H(X|U)≥R} sup_{Eρ(X,Y)≤δ} H(Y|U)`,
  `ξ_N ≥ γ ≥ ξ_N − O(ln N / N^{1/|X|})`; cardinalities only (no probability measures); the lemma with
  `m ≥ 2^{16|X|²}`, loss `|X|(m+1)^{|X|} log(n+1)/n`, gap `log²m/m`, attributed to Ahlswede–Yang–Zhang 1997.
  The report quotes all of this correctly.  Venue confirmed from Yu's reference list (1999 IEEE Information
  Theory and Communications Workshop, pp. 85–87).
* Lei Yu, arXiv:2205.07596v3 (comments field: IEEE Trans. IT): abstract page (through the fetch tool's
  summariser), and — read by me in the PDF text — the passages on prior work, the definition (26) of `ψ`,
  Theorem 4 (`|W| ≤ 2`), Assumption 3, Theorem 5 (four statements), Remarks 4–5, the paragraph "Theorem 5
  generalizes Ahlswede and Zhang's result … also based on the inherently typical subset lemma", Theorems
  6–8 (statements; column extraction partly garbled), and the proof §VI-A1 (finite `X`: typical subset,
  uniform law on `Ã`, kernel concentrated on the cost ball, `−n⁻¹ log P_Y^n(A^t) ≤ n⁻¹D(Q_{Yⁿ}‖P_Y^n)`,
  chain rule).  Findings: two measures `P_X`, `P_Y` on possibly different spaces, general lower
  semicontinuous cost, enlargement `A^t = ∪_{x∈A}{y : c_n(x,y) ≤ t}`; for bounded cost under Assumption 3
  (trivial on finite alphabets) `limsup E₀ ≤ lim_{α'↓α} lim_{τ'↑τ} ψ`; under Assumption 1 (Example 1:
  countable alphabet, bounded cost) `liminf E₀ ≥ ψ` in the interior of the domain.  So the hypotheses the
  report could not verify are satisfied in its finite setting.  The report's descriptions of Theorems 4, 5,
  8 are accurate.
* Yu, arXiv:2510.04030 (v4, Feb 2026): abstract only (summariser).  It concerns product Riemannian manifolds
  and the boundary-measure profile; "conditional typical sets asymptotically optimal" is in the abstract.
* Ahlswede–Yang–Zhang 1997: **not read**; existence, bibliographic data and the role of the lemma only
  from a search-engine summary and from the two papers above.
* Gordon–Petrov (arXiv:1608.06848): search-engine summary only; the face-count formula
  `(n+m)!/(m!m!(n−m)!)` for `n+1` points gives `C(2k−2, k−1)` vertices, as the report says.
* Alon–Boppana–Spencer 1998: not read; as described in Yu's paper.

**(a) Do the cited results exist and say what is attributed to them?**  Yes for Ahlswede–Zhang and for
Yu's two papers (checked in the sources as described); for Ahlswede–Yang–Zhang and Gordon–Petrov I can
confirm existence and gist only at the level of summaries.

**(b) Is the main statement in that literature, or does it follow by a known reduction?**
I found no statement of the problem with a free (non-product) second measure and a radius coupled to the
measure of the set, and no matrix game over Lipschitz vertices.  But:
1. the report's proof of A(ii) *is* Yu's/Ahlswede–Zhang's proof: in §VI-A1 the product law `P_Y^n` enters
   only through `D(Q_{Yⁿ}‖P_Y^n)`, so it may be chosen after the set, and `min_Q D(Q_{Y|W}‖Q|Q_W) = I(Y;W)`;
   the type mixture dominating all product laws is standard;
2. even the published *theorem*, used as a black box with a reference law adapted to `α`, gives `R^gen` on
   the sites I computed (M1);
3. new, as far as I can tell: Proposition 4 (the coupling `βρ = α + ε₁` makes the two multipliers
   proportional and collapses the auxiliary variable to a game), Lemma 3(c), the binary corollary, the
   threshold `min_Q γ(Q)`, and the query-complexity application.

**Search log** (6 queries performed, a 7th refused because the shared search budget was exhausted, so
"no match" is weak evidence):
Ahlswede–Zhang title query; AYZ title query; Gordon–Petrov; a query for universal/arbitrary second
measures in isoperimetry (nothing relevant); Ingber–Weissman similarity identification (the AYZ lineage:
two fixed product measures, an auxiliary variable); a query combining enlargement, hitting, rate–distortion
and games (nothing relevant); an ABS query (not performed: budget).

---

## 5. Not checked

* Exact `FC` for `n = 5, 6` (the report's certified MILP runs); I verified `|Sⁿ| ≤ 16` only.
* `fc_orbit_binary.py` (two-block families to `n = 28`; integer sandwich to `n = 800`; the `√n` prefactor),
  `v10_sft_sets.py` (subshifts), `v4_tensor_ineq.py`, `v13`, `zero_temp.py` beyond my own table.
* Block test at `b = 4`: 4136 of the 65534 subsets (the report ran all).
* A proof that `B* = R^gen` in general (numerics on four binary cases only), the black-box bound on
  ternary sites, and the grid/monotonicity argument that turns Yu's pointwise theorem into the reduction of
  M1 (sketched, not written out).
* Heterogeneous sites; interacting known parts; polynomial prefactors; the point `ε₁ = ε₁^thr`.
* Lean: I ran the file and read the 15 statements; I did not audit the proofs beyond the kernel's check,
  nor the repository's new `GeneralisedDips.lean` and Theorems 11.27–11.28 (outside my brief).
* Full texts of Ahlswede–Yang–Zhang, Alon–Boppana–Spencer, Gordon–Petrov; Yu's §§III–V, VII and appendices.
* The hint-free "star + spot-check" statements: checked by argument, not numerically.

---

## Appendix A. Record of the check of Theorem A(ii)

*Lemma 0(b).*  `e^{βh} − 1 = ∫_0^h βe^{βρ}dρ`; the integral of `βe^{βρ}π(h>ρ)` over `[j/β, (j+1)/β)` is at
most `(e^{j+1} − e^j)π(h > j/β)`; one of `J` levels carries `η/J`.  `h(x) ≥ h(y) − s(x,y) > 0` for `h(y) > r ≥ s(x,y)`
gives `Γ_r(A) ⊂ supp h`.  ✓

*Step 1.*  `J = ⌈βn s_max⌉` depends on `n` only.  `j = 0`: `πⁿ(D) ≥ η/(eJ)`, subexponential because
`η ≥ ε_n` and `ln(1/ε_n) = o(n)`.  `j ≥ 1`: `βr ≥ nα_A + ln η − 1 − ln J`; `ε_{1,n} → ε₁` uses both
hypotheses on `ε_n`.  ✓

*Lemma 5.*  `u_i ≥ p_i·m/(m+k)` since `Σ_b ⌈mp(b)⌉ < m + k`; at most `(m+1)^k` labels, hence at most
`(n+1)^{k(m+1)^k}` joint types; for `x ∈ Ã`, `P_A(x) ≤ (1+k/m)ⁿ ∏ u_i(x_i)` gives
`α_A ≤ k/m + α − D(P_{X|U}‖U|P_U)`; chain rule under `πⁿ(·|Ã)` with `U_I` a function of `V = (I, X^{I−1})`
gives `α_Ã = α + I(X_I;V|U_I)`.  ✓ (and exactly, numerically)

*Step 2.*  `m_n → ∞` with `η_{m,n} = k/m + k(m+1)^k ln(n+1)/n → 0`, independent of `D`.  ✓

*Proposition 4(i).*  Kernels ↔ families `(ν_u)` with couplings; `I(X';U) = min_Q Σ P(u)KL(ν_u‖Q)`;
Lagrange duality at interior `Q` (Slater at `ν_u = μ_u`, `ρ > 0`); passage to the boundary (m4a); Sion on
`Δ(S) × [0,∞)` (`Φ` convex l.s.c. in `Q` as a partial minimum of a jointly convex l.s.c. function, concave
u.s.c. in `t` as a minimum of affine functions, finite); Kantorovich duality for a cost with triangle
inequality and zero diagonal (`ã(x') = min_x[s(x',x) − b(x)]` is in `Lip` and `b ≤ −ã`); inner Sion (m4b);
Gibbs principle twice; with `ρ = (α+ε₁)/β` the term `−(t/β)KL(μ_u‖π)` appears with exactly the weight that
turns `max_μ[−tE_μφ − (t/β)KL(μ‖π)]` into `−(t/β)Λ(φ)`; Lemma 3(d).  ✓
*(ii)* convexity of `ρ ↦ V` (mixing kernels; `I(X';U)` convex in `P_{X'|U}`), `V(0) ≤ I(X;U) ≤ α ≤ βρ*`.  ✓
*(iii)* for the tilted law every feasible kernel has `E σ_U(X') ≤ ε₁/β`; Lemma 3(e).  ✓

*Lemma 3(c).*  Face directions = functions constant on the components of the tight graph; along `1_C`:
`g' = t(Q_λ(C) − π_λ(C))`, `g'' = t(βVar_{π_λ} − tVar_{Q_λ})`; stationarity forces equal masses
`p ∈ (0,1)` (full support of `π`), then `g'' = t(β−t)p(1−p) > 0`: no maximum in the relative interior of a
face of positive dimension; `t = β` by continuity.  ✓

*Step 3.*  `(α+ε₁)/β − δ' ≤ (α_A + ε_{1,n})/β − δ ≤ r/n − δ` because `α ≤ α_A + η_{m,n}`.  ✓

*Step 4.*  Given `Xⁿ = x` the `X'_i` are independent by construction; the conditional mean of
`s_n(X'ⁿ, x)` is `n Σ_{u,a} P_{UX}(u,a) E_W[s(X',a)|a,u]`, the same for all `x ∈ Ã`; Hoeffding for
summands in `[0, s_max]`; the cost is measured to the generating `x ∈ Ã ⊂ A`, which is all that
`X'ⁿ ∈ Γ_r(Ã) ⊂ Γ_r(A) ⊂ D` needs; argument order (evaluated point first) agrees with Lemma 0(b), `W_s`
and `Lip`.  ✓

*Step 5.*  Chain rule against `Qⁿ`; `X'^{i−1} — X^{i−1} — X'_i` (the past outputs are generated from
`X^{i−1}` and independent noise); `(U_I, X_I, X'_I) ∼ P_{UX} × W`, so `P_{X'_I} = Q`; given `U_I`,
`V — X_I — X'_I`; (★).  ✓ (and exactly, numerically)

*Step 6.*  `d(p‖q) ≥ p ln(1/q) − ln 2`.  ✓   *Step 7.*  Product laws are constant on type classes; at most
`(n+1)^{k−1}` types; `q_n ≥ ½(n+1)^{−(k−1)}Qⁿ` pointwise.  ✓   *Uniformity.*  `m_n`, `δ_n`, `J`,
`ε_{1,n}` do not depend on `D`; Proposition 4(ii) and Lemma 5 hold with the same constants for all sets.  ✓

*Algorithmic statement.*  Output `ln Z(g) + ε_n/2 − ε'`, `ε' = min(1, ε_n/2)`: undetected alternatives
have `ln Z(g') − ln Z(g) ∈ [−ε', ε_n − ε']`; `(ε_n − ε')/n → ε₁` and `ln(1/(ε_n − ε')) = o(n)`, so A(ii)
applies to the level `ε_n − ε'`; bumps cost `1/(1 − e^{−ε'})`, subexponential.  ✓
