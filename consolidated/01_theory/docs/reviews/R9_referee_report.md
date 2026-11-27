> **Repository note (added by the coordinator).**  Report of the independent referee R9 on
> workstream F (`docs/workstreams/F_REPORT.md`; brief: `docs/reviews/R9_brief.md`; the addendum
> with the coordinator's proof of Proposition 11.65(b), reviewed as "F10(b′)":
> `docs/reviews/R9_addendum_monotonicity.md`), as delivered.  `<session scratch>` is the
> session's scratch directory; the referee's scripts are in `experiments/reviews/R9/`
> (libraries `r9lib.py`, `r9prof.py`; run from that directory as in §4 of the report), their
> outputs in `experiments/reviews/R9/out/` and `rerun/`; the downloaded summary paper (`dl_az/`)
> and the Lean scratch copy are not in the repository.  What was done with the findings:
> theory report §11.20 (status paragraph; the repairs (M1), (M2) in the proof of Theorem
> 11.64; the minor findings at the places they concern), `docs/DEAD_ENDS.md` D47 (item 5), the
> errata note at the head of `F_REPORT.md`, and `docs/collaboration/messages/theory/THY-MSG-0008.md`.
> The repository files that the referee did not read because they appeared during the review
> (theory report §§11.20–11.21, `FieldShift.lean`, `GamePair.lean`) are: the integrated
> statements of the report it reviewed, the Lean file it compiled under its original name,
> and a machine-checked abstract theorem that no statement of §11.20 depends on.

# R9 — Referee report on workstream F: "algorithms without a hint when there is a known part (a field)"

Object reviewed: `<session scratch>/ws/F/REPORT.md` (830 lines; line numbers below refer to it), `ws/F/lean/WorkstreamF.lean`,
and, as context, `docs/THEORY_REPORT.md` §§11.10, 11.16, 11.18 (commit `4f822c5`), `docs/workstreams/A_REPORT.md` §§2.2–2.3,
`docs/reviews/R4_referee_report.md`, `docs/workstreams/K_REPORT.md` §§1–3.3, `docs/reviews/R7_referee_report.md`,
`proofs/Frontiers/HintRecursion.lean`, `NonAdaptive.lean`.  A late addendum by the coordinator
(`referee9/ADDENDUM_monotonicity.md`, a proof of the statement that F10(b) has only numerically) is reviewed as the extra
entry **F10(b′)**.

Everything of mine is in `<session scratch>/referee9/` (scripts `r9_*.py`, libraries `r9lib.py`, `r9prof.py`, outputs
`out_*.txt`, `rerun/`, Lean scratch copy in `lean/`, one downloaded PDF in `dl_az/`).  Nothing under `/home/user/MetricChain`
was modified (the repository itself moved from `4f822c5` to `823f5b2` through commits by others while I worked; I read
the context files at `4f822c5`; the working tree is clean at the end); no state-changing git command; no `lake build`;
no delegation; all Python under `ulimit -v 4000000`, one
process at a time, every run under ten minutes.  The author's code was not run and not reused; I read `run_all.sh`, three
of the author's outputs (`out_t18`, `out_t23`, `out_t24`) and one script (`t20_product_samplers.py`, only to explain a
numerical discrepancy, m4 below).

## 0. Summary

**Theorem F4 (non-adaptive exponent `θ_na`): proved.**  (a), (b), (c) are elementary and correct for every `n`; (d) is correct
given Theorem F6, and I find Theorem F6 proved (below).  Small gaps only, all closed.

**Theorem F9 (adaptive exponent `R^max`): lower bound proved (every `n`); upper bound proved with gaps.**  I could not break
it and I believe it.  The gaps are in the algorithmic part, not in the isoperimetry: (M1) the induction over the levels is
not written, and the intermediate claim that is written ("a family with exponent function at most `T_k + η`") is not what
the one-level theorem yields — the assembly needs left limits in the accuracy, exactly as in R7 §5 / the proof of Theorem
11.54, which applies verbatim; (M2) in Theorem F7 the sentence "good event, validity, width: verbatim" does not hold as written
for strong fields: the number of potential inner calls is `4K/min μ_H = 4K·Z_H·e^{c₁n_o}`, not `4K·2^{n_o}`, with
`c₁ = ln 2` when `|θ| ≤ u` (harmless) but `c₁ = ln(1+e^{|θ|−u}) > ln 2` when `|θ| > u`; with the unchanged inner failure
probability `δ/(2^{n+6}n³)` the union bound is then void whenever `c₁φ > ln 2` (`φ > 0.87` in the report's main example
`p = 0.1`, `u = 2`); one line repairs it.  With these two repairs the chain F1(a) + F5 + F6 + F7 + F8 + `iterates_lt_hint_add` ⇒ F9 is sound, at the
standard of one careful paper check; nothing of it except the abstract recursion and the shift identity is machine-checked.

**Theorem F6 (the converse tail lemma), the critical part: proved.**  I re-derived Lemma T, Lemma SL (every use of Sion,
the Gibbs and Donsker–Varadhan steps, the endpoint argument, `τ ≥ 1`, the window step) and Steps 1–6 line by line, found
no error, and only cosmetic gaps (a constant; conditions `n ≥ n₀(p,u)` that are absorbed in `ω_n`; the "equivalent form"
needs `θ > ω_n`).  Lemma SL was confirmed by my own primal minimisation over kernels (about 800 random laws, equality to
`10⁻¹²` at the generalised dip for accuracies of both signs, Nelder–Mead ascent over laws never above `R^max`); Lemma T and
the inequality of Step 5 exactly by enumeration (210 instances); the theorem itself on all subsets of `Q_3`, `Q_4`, by
annealing on `Q_5`, `Q_6`, and exactly on about 3 500 sets at `n = 80…240` from families the author did not test (unions of
2 and of 16 balls with different centres, lenses, half-spaces, slabs, ellipsoids and boxes without a centre) plus an
annealing over arbitrary profile masks: on these families the least `ω` for which the inequality of the theorem holds
is `≤ 0.47·ln n/n` and decreases with `n` (`0.025, 0.014, 0.009` at `n = 80, 160, 240` for `p = 0.2`, `u = 4`); on the small
cubes it decreases from `n = 3` to `n = 6` as well.  No counterexample.

No CRITICAL finding.  Two MAJOR (M1, M2: gaps in the written proof of F7/F9, both closed).  Minor: a remark that is false
as a general statement ("on the 4-cube the exact `Ξ_H` exceeds the family by a factor at most 2": `2.08` at `p = 0.2`,
`u = 4`); the table of Proposition F11(a) is inaccurate by up to 4 % (the maximum over centre types is at the constant
centres `m ∈ {0,1}`, outside the author's grid); Lemma T is a variant of, not the lemma of, Ahlswede–Yang–Zhang; some labels.
All single-letter formulas, the tables, the finite-`n` sums (`n ≤ 4000`) and the recursion were reproduced with my own code.
The coordinator's addendum **F10(b′)** is correct: **proved**.

## 1. Verdict per statement

"hand" = re-derived line by line; "num" = own numerics (§4).

| statement | verdict | how checked; remarks |
|---|---|---|
| **F1(a)** every-`n` lower bound `(1−2δ)e^{−tε+nF(γ,t)}` at `γ\|x\|` | **proved** | hand (it is Theorem 11.27(c) for this class: slack `u[a≠b]−γa+γb`, soft gap `Λ(b)+γb+ln Z_γ`, `β=1`; holds for every correct algorithm, hinted or not, `δ<½`); num: brute force `n=8` (`r9_t15`) |
| **F1(b)** hinted cost `e^{nR_γ+o(n)}` at `γ\|x\|` | known (Theorem A(ii) of workstream A, refereed in R4) | only the identification of the site (`π_γ`, quasi-metric slack for `\|γ\|≤u`, two states) checked; not re-refereed |
| **F2(a)** max–min form of `F` | **proved** | hand (Gibbs principle + minimax for `Σ_b M(b)G_b(Q)`, `G_b` finite and convex) |
| **F2(b)** closed form, cosh form, `F(γ,0)=F(γ,1)=0`, `F≤0` for `t≥1`, limit `t↓0` | **proved** | hand (2×2 value, monotone rows, the identity for `F(γ,1)`, `L^t`-norm monotonicity); num: LP game solver vs closed form `5·10⁻¹¹`, vs cosh form `5·10⁻¹⁵`, `max F` on `t∈[1,12]`: `7·10⁻¹⁵`, chord-gap limit `4·10⁻⁶` at `t=10⁻⁶` |
| **F2(c)** `R_γ`, `R_0 = max_m[h(m)−h((Λ_m+e)/u)]_+` (`e≥0`) | **proved** | hand; num: direct max–min over profiles `≤ 4·10⁻¹⁶` (closed form), `2·10⁻⁹` (general `γ`) |
| **F2(d)** max–min form of `R^max` (`e≥0`) | **proved** | hand (Sion in `(z,γ)`); num `2·10⁻⁹` |
| **F2(e)** `θ_na = max_m min{I : I^cone ≤ x} = max_τ (F*(τ)−τx)/(1−τ)`; `a = max_m I(z_c(m))` | **proved** | hand (Lagrangian with `τ=t/(1+t)`, thinning step); num: three forms agree to `10⁻⁹…10⁻¹⁵`; `a = −dF*/dt(1)` (the supremum over `τ<1` is a limit, not attained) `= max_m I(z_c(m))` to `10⁻⁹` |
| **F2(f)** sign of `∂_γF(0,t)`; `F*>F(0,·)`; `E>E_0`; `R^max>R_0` on `[0,E)` | **proved** | hand (formula for the derivative, convexity of `D`, variance comparison); num: formula `3·10⁻¹¹`, sign in 3000/3000 |
| **F3** shift identity | **proved**; Lean statement = paper statement for a two-letter `S` and interior profiles | compiled (`lake env lean`, 6 s, exit 0, axioms `propext, Classical.choice, Quot.sound`); see §5 |
| **F4(a)** quantiles are Lipschitz, `ψ^{tr,q}∈L_u`, `maxdens(D)≤q` | **proved** | hand (the coupling; "smallest value" handled); num: 400 random `(ψ,q)`, `n≤9`, 0 violations |
| **F4(b)** complexity `≍1/q` at accuracy `ε_n^{tr}(q)` | **proved** | hand: (i) meets the hypotheses of `nonadaptive_expected_queries_ge` (pairs `(ψ∘σ, ψ^{tr,q}∘σ)`, weights `1/n!`, cap `q`); (ii) Chernoff + Markov; num: simulation of both tails (`n=10`) |
| **F4(c)** truncated cones | **proved** | hand (hypergeometric shells log-concave, tilt, counting, constants); num: bound holds in 102/102 exact cases (`n≤2000`), far from tight |
| **F4(d)** upper bound | **proved** (given F6, which I find proved) | hand (`A(ψ^{tr})≥qT`, `t_κ≤e^{2u}(n+1)Tw_H(κ)`, `Φ_H⁺`, `μ_H(D)≤maxdens(D)`); finite-`n` sums approach `θ_na` |
| **F5** tail lemma relative to a reference | **proved** | hand (orientation `s₀(x,y)=ud+ψ₀(x)−ψ₀(y)`, `x` inside, `y` outside; `Ξ₀` nondecreasing); num: `Q_4`, exact `Ξ₀`, 12 references, 26 000 thresholds, no violation, equality attained |
| **F6, Lemma T** | **proved** (it is a variant of the AYZ lemma with its own complete proof; the label "known" is inaccurate) | hand; num: (2), (3), (4) exactly on 210 instances |
| **F6, Lemma SL** | **proved** | hand (§2, A); num (`r9_t3`, `t3b`, `t3c`) |
| **F6, Steps 1–6** | **proved**, with cosmetic gaps, all closed (m1) | hand; num (`r9_t6`, `t7`, `t8`, `t10`, `t16`) |
| **F7** one more level relative to a reference | **proved with gaps** — M2 (the union bound over inner calls for strong fields `\|θ\| > u` and for general references; closed), m6 | hand, with §11.18 and K_REPORT §2 next to me; not simulated by me |
| **F8** `HintPair θ_na R^max a h E` | **proved** | hand, field by field against `HintRecursion.lean`; num on grids |
| **F9** adaptive exponent `R^max` | lower bound **proved**; upper bound **proved with gaps** — M1, M2 (both closed) | hand; recursion iterated with own code |
| **F10(a)** | **proved** | F2(f) + F9 |
| **F10(b)** | numerical in the report; my numerics agree (no increase of `F*` in `\|θ\|` on my grid) | superseded by F10(b′) |
| **F10(b′)** (coordinator's addendum) | **proved** | hand, every step; num (`r9_t12`); four remarks at the end of the list of minor findings, §2 |
| **F10(c)** stratified bracket, instance-optimality at symmetric instances | **proved** (validity for every member of the class, the deterministic ratio, the lower bound, optimality up to `16(n+1)K/(1−2δ)` at the accuracy `ε − ln 3`); the sentence on the worst case ("exponent `θ_na` by the argument of F4(d)") is a sketch — gap m8, closed in outline only | hand (the three per-class events and their probabilities; `Tail` costs no evaluations; `D ≠ Q_n` because `t̂_κ` is a sampled value) |
| **F11** | sketch, as labelled; nothing false in the formulas, but the table of (a) is inaccurate (m4), and its conclusions are used elsewhere as facts (§3) | num for (a) only |
| **F12** | sketch, as labelled; nothing found false; not used elsewhere as proved | read only |

## 2. Errors and gaps, by severity

### CRITICAL
None.

### MAJOR

**M1. Theorem F9, upper bound: the induction over the levels is not written, and the step that is written is not what is
provable** (lines 494–500).  "By Theorem F7 with the reference `H` and induction, for every `k` and `η > 0` there is a family
with exponent function at most `T_k + η`."  Theorem F7 produces, for one tuple `(φ, β, g, η₀)`, procedures of the single
accuracy `gn + O(log n)`; a *family* (one procedure for every `(d, x, δ′)`, cost nonincreasing in `x` and `δ′`) has to be
assembled, and its exponent function at `ξ` is bounded by `R[T](g)` for `g < ξ` only, i.e. by `min(T, R[T])(ξ⁻) + η₀`.
Nothing shows that the `T_k` are continuous, so
the induction hypothesis must carry a left limit and the step needs the shift inequality
`R[T̃](g) ≤ R[T](g − ε) + ε + η` for `T̃ ≤ T(·⁻) + η`.  This is precisely gap M2 of referee report R7, and the report under
review repeats the compressed parenthesis that R7 objected to.
*Repair (closed).*  The induction written into the proof of Theorem 11.54 (Assembly / Shift / Induction, following R7 §5)
uses of the one-level theorem only: the accuracy `gd + O(log d)`, the cost exponent `τ + η₀` of (11.18.2) for a ladder of
finitely many rates fixed relative to the inner dimension, monotonicity of `θ_na`, and `T` nonincreasing.  Theorem F7 has
exactly this form (same `τ`, with the `θ_na` of this report), so the three steps apply verbatim; the base family is
enumeration (`T₁ ≡ ln 2`), and the final statement takes `g < ε₁` anyway, which is what makes the left limits harmless.
(Proposition E of K_REPORT is *not* directly applicable with `T₁ ≡ ln 2`: its corner case "`y_l ≥ u > ε*`, so
`T_k(y_l) ≤ θ_na(y_l) = 0`" uses the base family `θ_na`.)  The report should cite that induction and state the result as
"for every `g < ξ`: exponent at `ξ` at most `T_k(g) + kη′`".

**M2. Theorem F7: "Good event, validity, width: verbatim" does not hold as written when `c₁φ > ln 2`** (lines 434–440;
"Everything else … is unchanged").  In Theorem 11.52 the union bound over inner calls rests on the deterministic count
"`M ≤ 4K·2^{n_o}` always", on `K = ⌈24 ln(2^{n+6}n³/δ)⌉` and on the inner failure probability `δ/(2^{n+6}n³)`.  With a
reference, the count is `M ≤ 4K/min μ ≤ 4K·e^{c₁n_o}` (beyond `2K/min μ` points a level is populated or `Ξ(q) = 0`).  For `H`,
`−ln min_x μ_H(x) = n_o c₁ + ln Z_H` exactly, with `c₁ = ln 2` when `|θ| ≤ u` (the type `½` is in the window; then the only
new factor is `Z_H ≤ n_o+1` and the union bound survives) and `c₁ = ln(1+e^{|θ|−u}) > ln 2` when `|θ| > u` (test 17).  In
the second case — and for a general reference, for which the theorem is stated — the union bound with the unchanged
`δ′ = δ/(2^{n+6}n³)` is of order `e^{c₁n_o}2^{−n}` and is void as soon as `c₁φ > ln 2`: `φ > 0.87` for the report's main
example `p = 0.1`, `u = 2`; `φ > 0.55` for `p = 0.05`, `u = 2`; `φ > 0.19` for `p = 0.01`, `u = 1` (the outer fractions that the
recursion uses at small accuracies are large — R7 reports `0.63–0.99` on the cube).  The report adapts `J` (`c₁n` in place
of `n_o ln 2`) but not this.  The author's simulation (`t14`) cannot see it: the inner brackets are simulated and never fail.
*Repair (closed), either of:* (a) hand down the inner failure probability `δ·e^{−c₁n}/(2⁶n⁴)` and take
`K = ⌈24 ln(2⁶n³/δ)⌉` (the events (V2), (V3) are `O(n³)` binomial events at fixed thresholds: `J+1` levels, `O(c₁n)` values
of `M`, `J+2` values of `x`); the definition of an exponent function allows every failure probability `e^{−cd}`, and `K`
stays `O(n)`, so no exponent changes; or (b) keep the parameters and replace the union over potential calls by the union
over the calls actually made, whose number is at most the abort threshold (`≤ e^{n(τ+2η₀)+o(n)} < 2^n` for the parameters
of interest, `τ + 2η₀ < ln 2`): each call fails with conditional probability `≤ δ′` given the past.  The exponent `τ` is unaffected.
(By (b) the algorithm with the unchanged parameters is in fact still correct; it is the justification "verbatim" that fails.)

### MINOR

**m1. Theorem F6, cosmetic gaps (all closed).**
(i) Statement, "Equivalently …" (lines 316–317): the inverse form holds for `θ > ω_n` only (for `θ ≤ ω_n` it is void); its
uses (F4(d), F7) are on compact subsets of `θ > 0`, so nothing changes.
(ii) Step 3 (line 369): the constant is `[2(m+1)² + 3] ln(n+1)/n`, not `+1` (the `2 ln(n+1)/n` of Step 1 was dropped).
(iii) Step 4 and Step 6 need `n ≥ n₀(p,u)`: `θ_n = 3e^{−√n/(2u²)} < 1` (i.e. `n > 4u⁴ ln²3`: `n > 1236` for `u = 4`), and
`κ_∓ ∓ δ₁ ∈ (0,1)` for the constant `c = sup 1/(2κ(1−κ))` over a neighbourhood of the window.  For smaller `n` take
`ω_n = u`: then the statement is trivial (`Φ_H⁺(D) ≤ μ_H(D)e^{2un}` and `R^max(e−ω)+ω ≥ 2ω−e`).  So `ω_n → 0` exists, but
slowly: beyond `n₀` its leading term is `2/m = 2n^{−1/8}` (the report says the `o(n)` is "`n^{7/8}`-ish"; correct).
(iv) Uniformity in `e`: the only place is the factor `1/(1−θ_n)` on `R^max(B−2δ−α)`; for `e ≥ −c₁` this is `O(θ_n)`, and
for `e < n^{−1}ln min μ_H` the statement is trivial, as the report says.  Correct.
(v) `Φ_H⁺` versus `Φ_H`: the theorem is stated with `Φ_H⁺ ≥ Φ_H`; F4(d) uses `Φ_H⁺`, F7 uses `Ξ = max Φ_H ≤ max Φ_H⁺`.
Consistent.

**m2. Lemma T is labelled "[known; proof reproduced]"** (line 323).  The lemma of Ahlswede–Yang–Zhang as stated in the
Ahlswede–Zhang summary (which I read in full, §5) is for cardinalities, `m ≥ 2^{16|X|²}`, entropy gap `log²m/m`, loss
`|X|(m+1)^{|X|}log(n+1)/n`.  Lemma T is a weighted variant with a rounding-up quantiser, gap `2/m`, every `m ≥ 1`; its
eight-line proof is complete (I re-derived it; R4 had done the same for workstream A), so nothing depends on the
literature.  Label: "[proved here; variant of AYZ]".

**m3. Theorem F6, Remark (ii)** (lines 394–395): "On the 4-cube the exact `Ξ_H(q)` exceeds the best set of the family … by
a factor at most 2."  True in the nine cases the author computed (`u ≤ 2`; I reproduce `1.286`, `1.427`, `2.000`), false in
general: `2.080` at `p = 0.2`, `u = 4` (`q = 0.299`), with the same family (all balls with type-dependent radii around one
centre, all 16 centres).  A finite-`n` remark; no consequence.

**m4. Proposition F11(a), table** (lines 579–583).  For a product sampler the formula of the proposition is maximised at a
*constant* centre: objective `D(P_{X|S}‖r|P_S)` and constraint `D(P_{X|S}‖π_s|P_S) ≤ x` are both linear in `m` for fixed
conditional laws, hence `inner(m) ≤ m·φ₁(x) + (1−m)·φ₀(x) ≤ max(φ₀, φ₁)` with
`φ₀ = min{KL(y‖r) : KL(y‖η₀) ≤ x}`, `φ₁ = min{KL(z‖1−r) : KL(z‖η₁) ≤ x}`, and
`θ_na^{(r)}(x) = max(φ₀, φ₁)` in closed form.  The author's script maximises over `m ∈ [0.005, 0.995]` and stops the scan
over `r` early.  Correct values (`r9_t13b`): best single `r`: `0.1033` (`r = 0.185`), `0.0451` (`r = 0.170`), `0.0244`
(`r = 0.319`) against the printed `0.1046`, `0.0470`, `0.0247`; plain `π_f`: `0.2743`, `0.1430`, `0.0348` against `0.2729`,
`0.1420`, `0.0347`.  The qualitative statement (`θ_na^{(r)} > θ_na` for every `r`) survives, by a narrower margin
(`0.0244` against `0.0243` in the third row).  That the worst centres of a product sampler are the constant ones is
Proposition 6 of workstream A and should be said.

**m5. Theorem F4(d), line 277.**  "`nv` is the inf-convolution of `nKL(·‖p)` with `un|·|`": the minimum over `κ′` runs over
lattice types; rounding the continuous minimiser towards `p` costs at most `u` (the constant `e^{2u}` is generous).  No
error.

**m6. Theorem F7, lines 445–448.**  `Ξ` is a right-continuous step function, so the defining property of `q†` may fail at
`q = q†` itself; "a level that is left has `q_j > q†`" should read `≥`, and "`if q ≤ q†`" `<`.  The bounds `M_j^neg ≤ 4Je²M†`,
`M ≤ 8Je²M†` are unchanged.

**m7. Theorem F9, line 498.**  "`HintPair θ_na R^max (ln 2) h E` holds (… with the bound `a ≤ ln 2`)" is true but not
needed: in `iterates_lt_hint_add` the bound on `T₁` is a separate hypothesis (`∃ C`), so `HintPair θ_na R^max a h E` and
`T₁ ≡ ln 2` suffice.

**m8. Theorem F10(c), line 553, carries the label [proved] over a sketch.**  "In the worst case over `L_u` it has the
non-adaptive exponent `θ_na` (by the argument of Theorem F4(d), given Theorem F6)": the thresholds `t̂_κ` are sample
quantiles, not the exact quantiles for which F4(a) proves the Lipschitz property; one needs
`t_κ(2K/M) ≤ t̂_κ ≤ t_κ(K/(2M))` on the good event and then F4(d) with the two exact levels.  Routine, not written (closed in outline only).
Also "it has the hinted exponent of every symmetric instance" means: its cost is within `16(n+1)K/(1−2δ)` of the least
cost of any correct algorithm *at the accuracy `ε − ln 3`* — an exponent statement only where the hinted exponent of the
instance is continuous in the accuracy (true for additive instances).

**m9. Theorem F7, Remark (ii)** (lines 458–460).  "Here only its exponent is known": the proof of Theorem F6 gives an
explicit (if useless) `ω_n`, hence an explicit `Ξ̄ ≥ Ξ_H`; an upper bound suffices for validity and for the exponent
provided `Ξ̄(q) = 0` for `q < min μ` (termination), which costs nothing.

**m10. §7, item 2** (lines 767–768): "nothing at bounded accuracy (there the non-adaptive exponent is `a` …)".  Only the
lower bound `a` is proved at bounded accuracy (F4(b)(i), (c)); the upper bound from F4(d) is at accuracy `o(n)`, not `O(1)`.

**m11. Theorem F3 / Lean.**  The Lean theorem has the hypotheses `0 < x, y < 1`, `0 < κ < 1` (interior profiles of a
two-letter `S`); the boundary cases of "every joint law" follow by continuity and are not machine-checked.  Harmless.

**m12. Housekeeping.**  `out_run_all.log` records the tests up to `t18` only, while `run_all.sh` lists `t19`–`t24`: the log
is from an earlier version of the script (the later outputs exist).

**Remarks on the addendum F10(b′)** (no error): (1) in step (iii) the first-order condition is not needed if the
derivative in `θ` is taken at fixed total field `x` (then `∂_θ ln ρ_θ(x) = ∂_θ ln I_θ(x)` and the envelope theorem at the
interior nondegenerate maximum gives the displayed inequality directly); (2) step (i) should say why a critical point
exists (`ρ = 1` at both ends and `ρ` not constant) and that two local maxima would force a local minimum in between;
(3) strictness: the centre of `[P,Q]` is strictly to the right of `θ/2` because `γ* < 0` and `t > 0`, and `tanh` is strictly
increasing — this is what makes `dF*/dθ < 0` for `θ > 0`; (4) "Theorem 11.59(b)" does not exist at commit `4f822c5` (it is
Theorem F2(b) of the report).  The consequences for `R^max`, `E`, `θ_na`, `a` are immediate (monotone functionals of `F*`);
"the uniform cube is the hardest case" is conditional on Theorems F4 and F9.

### A. Record of the check of Theorem F6

*Setting.*  `v = max_{|γ|≤u} v_γ` is `KL(·‖p)` on `[κ_−, κ_+]` continued with slopes `±u` (the Legendre transform restricted
to `|γ| ≤ u`; numerically `2·10⁻⁹` against the maximum over `γ`); `π(x)w_H(x) = e^{−n[h+KL−v](κ_x)}`; `1 ≤ Z_H ≤ n+1`
(`Z_H ≥ E_π e^{nv_γ} = 1`; numerically `Z_H ≈ 16` at `n = 1000`, of order `√n`);
`μ_H(x)e^{s_H(x,y)} = π(x)e^{nv(κ_y)+ud(x,y)}/Z_H`.  ✓

*Lemma T.*  `Σ_b⌈mp(b)⌉ ≤ m+1`, so `p_i ≤ (1+2/m)u_i`; at most `(m+1)²` labels, `(n+1)^{2(m+1)²}` joint types; for `x ∈ C̃`,
`α_C ≤ 2/m + α − D(P_{X|U}‖U|P_U)`; chain rule under `π(·|C̃)` with `U_I` a function of `V = (I, X^{I−1})`:
`α_{C̃} = α + I(X_I;V|U_I)`; hence (4) with `η_{m,n} = 2/m + 2(m+1)²ln(n+1)/n`.  ✓

*Lemma SL.*  (1) `V = min{I(ν) : g(ν) ≤ 0}`, `I` (mutual information as a function of the channel) and `g` convex and
continuous on the compact convex `[0,1]^𝒰`, `g(μ) ≤ 0` because `B ≥ v(P_X)`.  (2) First Sion: `(ν,τ) ↦ I(ν)+τg(ν)` on
`[0,1]^𝒰 × [0,∞)`, convex continuous in `ν`, linear in `τ`; compactness is on the minimising side, so no Slater condition
is needed: `V = sup_{τ≥0} min_ν`.  (3) Second Sion, for fixed `τ`: convex in `ν`, concave in `γ` (`−ln(q+pe^{−γ})` is
concave), both sets compact: `min_ν max_γ = max_γ min_ν`.  (4) `τ ≥ 1`: `ν = μ` gives
`Ψ ≤ I(X;U) + τ(v_γ(P_X) − B) ≤ I(X;U) + v(P_X) − B ≤ α − B ≤ R^max(B−α)` (`v_γ(P_X) − B ≤ 0`, `v ≤ KL`, `R^max(e) ≥ −e`
because `F*(1) = 0`).  (5) `τ ≤ 1`: `I(ν) = min_Q ΣP(u)KL(ν_u‖Q)`; the minimisation separates over `u` for fixed `Q`;
third Sion in `(ν_u, φ)` (restrict `ν_u` to the support of `Q`; `φ(0) = 0`, `|φ(1)| ≤ u` compact); Gibbs principle;
Donsker–Varadhan against `π_γ` with `KL(μ_u‖π_γ) = KL(μ_u‖π) + γμ_u + ln Z_γ`; the terms `±τγμ_u` cancel and the terms
`τ ln Z_γ` cancel against `v_γ`; result `Ψ(τ,γ) ≤ min_Q max_ψ g_Q(ψ) − τ(B−α)`.  (6) Endpoint argument: `g_Q` is smooth on
`[γ−u, γ+u]` also for degenerate `Q`; at an interior critical point the two tilted laws agree at some `r ∈ (0,1)` (`π_γ`
has full support) and `g_Q″ = τ(1−τ)r(1−r) > 0`, so no interior maximum for `0 < τ < 1`; without a critical point `g_Q` is
monotone; `τ = 1` is covered by (4).  At the endpoints `ψ = u1[·≠b] − γ· + γb` and `g_Q = −ln Σ_a Q(a)K_τ^γ(a,b)`
(`E_{π_γ}e^{−u1[a≠b]+γa} = e^{−Λ(b)}/Z_γ`), so `min_Q max_ψ g_Q = F(γ,τ)` by the minimax theorem for matrix games.
(7) Window: thinning by an independent Bernoulli(`κ_+/κ′`) variable; `I` decreases (data processing), the distance grows
by at most `κ′−κ_+`, `v` decreases by exactly `u(κ′−κ_+)`.  ✓  (Sion is used three times and von Neumann once.)

*Steps 1–6.*  Step 1: `B(x)` is determined by the type and the distance of a minimiser, at most `(n+1)²` values;
`B − α_C ≥ e − 2ln(n+1)/n`; (∗) by definition.  Step 2: `v(P_X) ≤ B` from the `u`-Lipschitz property of `v`.  Step 3: ✓ with
the constant of m1(ii); `−e ≤ R^max(e)`.  Step 4: given `x ∈ C̃` the `X′_i` are independent; the means are `nP(X′≠X)` and
`nQ` because the joint type of `(u_i(x^{i−1}), x_i)` is `P_{UX}` for every `x ∈ C̃`; Hoeffding three times;
`v(κ_{X′}) + ud/n ≤ v(Q) + uδ₁ + uP(X′≠X) + uδ₁ ≤ B − δ`; membership in `D` by (∗) for the generating `x ∈ C̃ ⊂ C`.  Step 5:
`X′^{i−1} — X^{i−1} — X′_i` (the earlier outputs are functions of `X^{i−1}` and independent noise); `P_{X′_I} = Q`; given
`U_I`, `V — X_I — X′_I`; Lemma T(4).  Step 6: `d(a‖b) ≥ a ln(1/b) − ln 2`; `Qⁿ(y) ≤ e^{−nh(κ_y)}`; `Q` is in the window by
Lemma SL, so `KL − v ≤ cδ₁²` on `𝒯`; `Z_H ≤ n+1`.  Bookkeeping `B − α ≥ e − [2(m+1)²+2]ln(n+1)/n` ✓.  With `δ = n^{−1/4}`,
`m = ⌈n^{1/8}⌉` all error terms depend on `(n, p, u)` only.  ✓

*Is it in the literature?*  Not as a statement (§5).  The proof is the converse proof of Ahlswede–Zhang / Yu (§VI-A1 of
Yu's paper as described in R4) with the product reference law chosen after the set (`Q = P_{X′}`), restricted to a typical
set of that law — the restriction is what lets `μ_H` dominate `Qⁿ` — and with a budget that depends on the type of the exit
point.  It is not a black-box corollary of the fixed-measure theorem: the enlargement here is
`{y : ∃x∈C, v(κ_y) + ud(x,y)/n < B}`, i.e. an intersection over `γ` of additive-cost conditions that must hold for the same
`x`, not an enlargement for one additive cost.  For one fixed `Q` and the radius `n(B − v(Q))/u` the Hamming enlargement of
`C` contains points of other types, which need not lie in `D` (the budget depends on the type of the exit point); the
fixed-measure theorem bounds `Qⁿ` of the whole enlargement and says nothing about its part of type `≈ Q`, and giving up a
margin in the radius to make the wrong types negligible costs a constant in the exponent.  The restriction to the typical
set of `Q` is what Step 4 obtains from the independence of the `X′_i`; it is part of the proof, not of the black box.  New, as far as I can tell: the reference `H`, the
type-dependent budget, and the collapse of Lemma SL (`sup_{P_{UX}} V = max_γ R_γ`).

### B. Record of the check of Theorem F7 (against §11.18 and K_REPORT §2)

Decomposition `A = Z·E_μŴ`; `s₀ ≤ min Ŵ` and `max Ŵ ≤ s₀e^{2un}·max w_ref/min w_ref ≤ s₀e^{3un}` ✓; `J` ✓ (nothing is high
above `max Ŵ·e^b`; `ℓ ≤ max Ŵ`; `M_j^neg > 2K/min μ` once `j > 3un + b + c₁n_o − ln(Je)`, and the closure test precedes the
negligibility test in every pass, so the pass at which `M` first exceeds `2K/min μ` closes with `Ξ(q) = 0`).  Outer
sample i.i.d. from `μ`, thresholds functions of the reference query only: (V2), (V3) are binomial events ✓.  Validity:
lower end by Markov under `μ`; upper end by the layer cake (pointwise) and Lemma F5 with `D = {Ŵ > s_j}`, which needs
`μ(D) ≤ q < 1` — hence "no closure at `q = 1`" ✓.  Width: algebra, measure-free ✓.  `q†`, `M† = 2K/q†`: a level that is left
has `q_j ≥ q†` (m6); `M_j^neg ≤ 4Je²M†`, `M ≤ 8Je²M†` by the argument of Theorem 11.52 (negligible predecessor:
`M_{j−1} ≤ M†`; populated predecessor: `ℓ ≥ s_{j−1}e^{−b}q_{j−1}/4`, also when `q_{j−1} = 1`) ✓.  The hypothesis on `Ξ^{(d)}`
is used on the compact interval `θ ∈ [θ̂_na(x)+η, c₁]` only (never near `θ = 0`; beyond `c₁` the tail function vanishes),
with `x_n = (G−b)/n_o → (g−β)/φ` and the strict inequality `Ŝ(θ̂_na(x)+η) < x` ✓.  For `H`:
`Ŝ(θ) = θ + (R^max)^{−1}(θ)` by Theorem F6 and the uniform continuity of `(R^max)^{−1}` on compact subsets of `(0,∞)`;
`θ̂_na = θ_na` ✓.  Count of close points and cost: measure-free ✓ (a bracket of `W(a)` divided by the known `w_ref(a)` is a
bracket of `Ŵ(a)` of the same ratio).  Union bound over inner calls: ✗ as written when `c₁φ > ln 2` (M2).  The algorithm needs an upper
bound of `Ξ`, not `Ξ` itself (m9).

### C. Record of the check of Theorem F8 against `HintRecursion.lean`

`structure HintPair (θna θh : ℝ → ℝ) (a h E : ℝ)`: `h_pos : 0 < h` ✓ (`E > 0`); `a_pos` ✓; `na_le : ∀ x > 0, θna x ≤ a` ✓
(`θ_na ≤ R^max(e_c) = −e_c = a`); `na_cont : ∀ x > 0, ContinuousAt θna x` ✓ (`S : [e_c,∞) → [0,∞)` is an increasing
homeomorphism: convex, zero up to `e_c`, positive afterwards; `θ_na = 0` on `[E,∞)`, continuous at `E`);
`na_h : θna h = h` ✓ (`S(0) = h`); `ident : ∀ e ∈ (0,E), θna(e + θh e) = θh e` ✓ (by definition, `e > e_c`);
`hint_pos` ✓ (`R^max(e) = 0 ⟺ e ≥ E`); `hint_mono : ∀ 0 < e ≤ e′ < E, e + θh e ≤ e′ + θh e′` ✓ (slopes `≥ −1`);
`hint_lower : ∃ L, ∀ e ∈ (0,E), h − L·e ≤ θh e` ✓ with `L = 1`.  All fields quantify over `(0,E)` or `(0,∞)` only; `θna` is
used by `StepLE` at arbitrary positive arguments, where it is defined.  The hypotheses of `iterates_lt_hint_add` on the
sequence (`StepLE`, monotone in `k`, nonincreasing in the accuracy, nonnegative, `T₁` bounded) hold for
`T_{k+1} = min(T_k, R[T_k])`, `T₁ ≡ ln 2`, on paper (as in R7 §3.10).  Not formalised, as the report says.
Remark: the super-solution property `R[R^max] ≥ R^max` (no level below the lower bound) is automatic for any convex
nonincreasing `θ_h` with `θ_na := θ_h∘(id+θ_h)^{−1}`: with `e_o = S^{−1}((g−β)/φ)`, `γ = max(β, μ)`,
`φR^max(e_o) + (1−φ)R^max(γ/(1−φ)) ≥ R^max(φe_o + γ) ≥ R^max(g)`.  So "never below `R^max`" tests the code, not the theory;
what carries information is that the recursion built on `R_0` falls below (reproduced: `−3.1 %` of `a`).

## 3. Statements that say more than is proved

1. **Theorem F9, header and proof** ("upper bound: proved given Theorems F6, F7 … and the machine-checked
   `iterates_lt_hint_add`"): the chain also needs the induction over the levels with left limits (M1), which is not in
   the report, and the union bound of F7 as repaired (M2).  The Lean theorem is about an abstract pair; that the pair
   `(θ_na, R^max)` satisfies `HintPair` (F8) and that the exact recursion satisfies the hypotheses are paper statements
   (the report says the former in §7, item 8).
2. **Theorem F7**: "every step that changes is written out below" and "good event, validity, width: verbatim" — one step
   that changes (for `c₁ > ln 2`, i.e. `|θ| > u` in the case of `H`) is not written out (M2).
3. **Theorem F6, Remark (ii)**: "by a factor at most 2" (m3).
4. **Proposition F11 is a sketch, but its conclusions are used as facts** in §1 ("not from `π_f` and not from any single
   tilted product measure"), in Remark (i) after Theorem F7 ("the limit of the recursion is … strictly worse than
   `R^max`"), and in §5, items 3 and 4 ("false", "false too").  The lower bounds for product samplers are "not written
   out" and the numbers of the table are inaccurate (m4).  What is solid at the level of the formula of F11(a): the
   closed form `max(φ₀, φ₁)`, which is strictly above `θ_na` in the three rows I recomputed.  The statements about the
   nested scheme with the reference `0` (F11(b)) rest on Yu's theorem "read as a machine summary" and on numerics; I did
   not check them.
5. **Theorem F10(c)** carries **[proved]** over the sentence on the worst case (a sketch, m8), and "the hinted exponent of
   every symmetric instance" is an exponent statement only where that exponent is continuous in the accuracy.
6. **Lemma T "[known]"** (m2); **Theorem F3 "machine-checked"** — for interior profiles of a two-letter `S` (m11).
7. **§7, item 2**: "(there the non-adaptive exponent is `a` …)" — lower bound only (m10).
8. **§1 and §8**: "both decrease with `|θ|` ([numerical])" — correctly labelled numerical in the report; it is now a
   theorem (F10(b′)).  "`γ*θ < 0` in all computations (proved to first order)" — now proved for every `0 < t < 1`.
9. The exponent statements are all of the form `e^{n·(exponent)+o(n)}` with an `o(n)` that is of the typical-subset kind in
   every upper bound that uses Theorem F6 (F4(d), F7, F9, the worst case of F10(c)); the report says so (§5 item 8,
   §7 items 2–3).  The proof of F6 gives only the trivial `ω_n = u` for `n ≤ 4u⁴ln²3` and `ω_n` of order `n^{−1/8}` beyond; the
   evidence that the exponents are approached like `c·ln n/n` is numerical (the report's and mine).

## 4. My numerics (own code; nothing imported from `ws/F`)

Libraries: `r9lib.py` (single-letter quantities: `F` from the closed form, the cosh form and an LP game solver; `F*`,
`R^max`, `R_γ`, `E`, `a`, `S^{−1}`, `θ_na`; profile functionals and a grid+zoom minimiser), `r9prof.py` (exact finite-`n`
sums on unions of cells of a `G`-group profile grid: the slack to the complement is a separable `l₁` min-plus transform;
validated against brute force on the full cube, test 4).  All commands are run in `referee9/` as
`ulimit -v 4000000; python3 <script> [args]`; runtimes are wall-clock on the shared machine.

| # | command → output | runtime | what, sizes | outcome |
|---|---|---|---|---|
| 1 | `r9_t1_game.py` → `out_t1.txt` | 10 s | `F(γ,t)`: LP solver vs closed form vs cosh form, 4000 random `(p,u,γ,t)`, `t ≤ 3`, endpoints `γ = ±u` included; `F(γ,1)`; `F ≤ 0` on `t ∈ [1,12]`; `∂_γF(0,t)` (3000 points); `v`; `E`, `E_0`, `a` for 6 pairs | `5·10⁻¹¹`; `5·10⁻¹⁵`; `1·10⁻¹⁵`; `max F = 7·10⁻¹⁵`; derivative formula `3·10⁻¹¹`, sign `= sign(p−½)` 3000/3000; `E > E_0` for `p ≠ ½` (`0.2123` vs `0.2018` at `p=0.1,u=2`); `a = max_m I(z_c(m))` to `10⁻⁹` |
| 2 | `r9_t2_maxmin.py` → `out_t2.txt` | 4 min 3 s | `R_0`, `R_γ`, `R^max`, `θ_na` by direct max–min over profiles `(m;a,b)` (grid + zoom, no duality) vs the formulas from `F*`; closed form of `R_0`; identity `θ_na(e+R^max(e)) = R^max(e)` and the same with `R_0`; `p = ½`; 6 pairs × 5 accuracies | agreement to `10⁻⁵` (zoom error; two cases `1.6·10⁻⁴`, `2.9·10⁻⁴` at `p=½`, artefacts, see 2b); closed form `4·10⁻¹⁶`; identity `4·10⁻¹⁵`; with `R_0` it **fails** (`θ_na(e+R_0(e)) − R_0(e) = +0.0105` at `p=0.1,u=2,e=0`); `p=½`: §11.16 formulas to `5·10⁻¹³` |
| 2b | `r9_t2b_polish.py` → `out_t2b.txt` | 32 s | the same max–min forms with an SLSQP-polished inner minimiser, 13 cases (incl. the worst of test 2) | `≤ 2·10⁻⁹` |
| 2c | `r9_t2c_na_small.py` → `out_t2c.txt` | 46 s | `θ_na(x)` for `x < h`, i.e. where `S^{−1}(x) < 0` (the regime of negative accuracies of the pair, which F6/F7 use): direct max–min vs `R^max∘S^{−1}` vs the `τ`-form, 4 pairs × 4 values `x = 0.02h … 0.8h` | agreement to `1·10⁻⁷` |
| 3 | `r9_t3_SL.py 7` → `out_t3_seed7.txt` | 8 min 26 s | **Lemma SL** by primal minimisation over kernels: (a,b) 800 random laws, `\|𝒰\| ≤ 4`, `e = B−α` of both signs (SLSQP in split variables, `\|𝒰\|=2` also by brute-force grid); (c) the generalised dip `U = S ∼` Bernoulli(`m`), `X\|S ∼` cone law, maximised over `m`, 4 pairs × 5 accuracies (two negative); (d) crude random ascent | (a,b) `max(V − R^max) = 0` (attained only where both vanish); (c) `max_m V = R^max(e)` to `10⁻¹²` in 20/20, also for `e < 0`; (d) never positive |
| 3b | `r9_t3b_SLadv.py 41` → `out_t3b.txt` | 7 min 57 s | Nelder–Mead ascent over all laws with `\|𝒰\| = 2`, 3 pairs × 5 accuracies × 6 starts | supremum found `= 0` up to `+1.6·10⁻⁶` (solver error of the inner minimum, which is computed from above), always at the generalised dip |
| 3c | `r9_t3c_SLcheck.py` → `out_t3c.txt` | 2 min 37 s | the case with `+1.6·10⁻⁶`, inner minimum by 36-start SLSQP, 400 laws near the dip | `max(V − R^max) = −1.4·10⁻¹¹` |
| 4 | `r9_t4_validate.py` → `out_t4.txt` | 2 s | profile machinery vs brute force on the full cube: 354 (grouping, set, reference) cases, `n ≤ 11`, `G ≤ 4`; also: the deepest dip is in `L_u` and `A(ψ₀^D)/A(ψ₀) = 1 + Φ₀(D)` | `1.2·10⁻¹⁴` |
| 5 | `r9_t5_finite.py p u 0.3 1000,2000,4000` for `(p,u) = (0.1,2), (0.2,4), (0.3,1)` → `out_t5_*.txt` (`rerun/`) | ≈ 2 min each | exact finite-`n` exponents on density balls, 5 centre types: smallest `q` with a sensitive dip at `g=0`, at `γ*\|x\|`, at `H`; smallest `q` at which the truncated cone loses `ε` | table below |
| 6 | `r9_t6_small.py exh` → `out_t6_exh.txt` (or `exhA`, `exhB`) | 8 min 42 s | **all** subsets of `Q_3` (254) and `Q_4` (65 534), 9 pairs: exact `Ξ_H` vs the family of balls with type-dependent radii (134 / 1310 sets); least `ω(D)` | ratio `≤ 2.080` (m3); `max_D ω(D)`: `0.282 → 0.260`, `0.285 → 0.209`, `0.686 → 0.544`, `0.265 → 0.222`, `0.426 → 0.370` (`n = 3 → 4`), attained inside the family |
| 6b | `r9_t6_small.py f5` → `out_t6_f5.txt` | 2 s | **Lemma F5** on `Q_4` with the exact `Ξ₀` (all subsets), references `H`, `0`, two additive, 3 pairs; random members of `L_u` and fibre averages over a second block | 26 000 thresholds, `max (lhs−rhs)/rhs = 2·10⁻¹⁵`, equality attained |
| 6c | `r9_t6_small.py anneal` → `out_t6_anneal.txt` | 2 min 40 s | annealing over subsets of `Q_5` (5 pairs) and `Q_6` (3 pairs) for a large `ω(D)` | `0.246, 0.167, 0.408, 0.167, 0.253` (`n=5`); `0.207, 0.139, 0.315` (`n=6`): decreasing in `n` |
| 7 | `r9_t7_F6sets.py p u s N seed` → `out_t7_*.txt` (`rerun/`): `0.2 4.0 20 24 1`, `0.2 4.0 40 100 2`, `0.2 4.0 60 24 3`, `0.1 2.0 40 60 4`, `0.5 2.0 40 60 5` | 3 s, 2 min, 3 min, 75 s, 70 s | **Theorem F6 on sets the author did not test**, exactly, 4-group grids (`n = 4s`, two shapes of grouping): unions of two density balls with different centres, lenses, unions of two Hamming balls, unions of 16 balls (plain and type-dependent radii), half-spaces and slabs with random coefficients, ellipsoids and `l₁`-balls around fractional profiles, random unions of boxes; 3 494 sets | table below |
| 8 | `r9_t8_anneal.py 0.2 4.0 100 0.5 6000 1`, `… 40000 2`, `0.1 2.0 200 0.52 12000 3` → `out_t8_*.txt` | 20 s, 2 min, 88 s | annealing over **arbitrary** unions of profile classes around one centre (2-group grid), objective `ω(D)`, 5 starts | best found `0.451 ln n/n` against `0.448 ln n/n` for the best density ball (`n=100`); nothing better than the ball at `n=200` |
| 9 | `r9_t9_recursion.py 0.1 2.0 12` → `out_t9_p0.1_u2.txt` | 36 s | the level recursion with `(θ_na, R^max)`: super-solution property on 20 000 random `(φ,β,g)`; 12 levels from `T₁ = θ_na` and from `T₁ ≡ ln 2` (240 accuracies, 150 fractions, 20 tolerances, 48 values of `γ`); mutation with the pair of `g=0` | `min = +1.6·10⁻⁷ ≥ 0`; never below `R^max`; `T₁₂/a = 0.2971, 0.2831, 0.2368, …` against `R^max/a = 0.2934, 0.2818, 0.2367, …` (`max (T₁₂−R^max)/a = 0.004`); mutation falls `3.1 %` of `a` below `R^max` |
| 10 | `r9_t10_lemmaT.py` → `out_t10.txt` | 1 s | **Lemma T** and Steps 4–5 exactly by enumeration: 210 (set, `m`) instances (random, balls, parity, half-spaces, golden-mean sets; `n = 5…9`, random `p`, `m = 1, 2, 4`), 3 kernels each | (2), (3) hold; `\|I(X_I;V\|U_I) − (α_C̃ − α)\| ≤ 6·10⁻¹⁶`; conditional means of Step 4 to `4·10⁻¹⁵`; Step 5: `max[n⁻¹D(P_{X′ⁿ}‖Qⁿ) − I(X′;U) − (α_C̃ − α)] = 3·10⁻¹⁶` |
| 11 | `r9_t11_F4.py` → `out_t11.txt` | 10 s | F4(a) by brute force (400 `(ψ,q)`, `n ≤ 9`); F4(b)(ii) simulated (`n = 10`, 4 settings × 2000 runs); F4(c): exact `ln[A(cone)/A(truncated)]` against the bound, 102 cases, `n ≤ 2000` | 0 violations; 0 tail failures; bound holds 102/102 (exact value `= nF_m(θ) + (0.6…1.1) ln n`) |
| 12 | `r9_t12_addendum.py` → `out_t12.txt` | 42 s | **F10(b′)**, every step (see §2): ODE residual; unimodality; `∂_γF(0,t)` formula; monotone quotient; envelope formula vs finite differences of `F*`; the inequality of averages at `γ*` (1500 random `(θ,u,t)`); the lemma (3000 random odd concave-on-positives functions); consequences on a grid of 25 fields × 4 values of `u` | `1·10⁻⁷`; 0/2000; `5·10⁻¹¹`; 0; `4·10⁻⁹`; 0 violations (least margin `9·10⁻⁶`); 0; 0 |
| 13 | `r9_t13_table.py`, `r9_t13b_F11.py` → `out_t13.txt`, `out_t13b.txt` | 3 s, 1 s | the table of §3.7 (10 columns); the table of F11(a) | §3.7 reproduced to the printed digits (`≤ 5·10⁻⁴`); F11(a): m4 |
| 14 | `r9_t14_misc.py` → `out_t14.txt` | 5 min 2 s | `1 ≤ Z_H ≤ n+1`; the fields of `HintPair` on grids (6 pairs); the every-`n` lower bound at `γ*` vs `e^{nR_0}` | `Z_H ≈ 2.6, 5.9, 16.5` at `n = 10, 100, 1000` (`p=0.1,u=2`); slopes of `R^max` in `[−1,0]`, convex, `S` nondecreasing, `θ_na` continuous, `θ_na(h) = h`, `R^max(e) ≥ h − e`; item 14 of the brief below |
| 15 | `r9_t15_lowerbound.py` → `out_t15.txt` | 1 s | F1(a) by brute force, `n = 8`: 216 generalised dips at additive instances | each is in `L_u` and raises `ln A` by `≥ r`; coverage `≤ 0.79·e^{tr}val(K_t)ⁿ` |
| 17 | `r9_t17_minmu.py` → `out_t17.txt` | 1 s | the least point mass of `μ_H` (7 pairs, `n = 50, 400`) | `−ln min μ_H = n c₁ + ln Z_H` to 4 decimals, `c₁ = ln 2` for `\|θ\| ≤ u`, `ln(1+e^{\|θ\|−u})` otherwise (M2) |
| 16 | `r9_t16_ballconv.py 0.2 4.0` → `out_t16_p0.2_u4.txt` | 27 s | F6 on density balls at fixed `θ`, `n = 250…4000` | raw excess `e − (R^max)^{−1}(θ)` in units `ln n/n`: `1.77 → 1.28`, `1.35 → 0.95`, `0.91 → 0.53`, `0.75 → 0.30` |

**Finite-`n` exponents (test 5)**, `n⁻¹ln(1/q)`, `ε₁ = 0.3E`; the author's values in brackets where given:

| `(p,u)` | quantity | `n=1000` | `2000` | `4000` | claimed limit | excess at `n=4000` |
|---|---|---|---|---|---|---|
| `(0.1, 2)` | hint, `g=0` | .021964 [.021964] | .021034 [.020949] | .020339 [.020254] | `R_0 = .019497` | `0.41 ln n/n` |
| | hint, `γ* = −0.563` | .025517 [.025517] | .024553 [.024553] | .023996 [.023996] | `R^max = .023270` | `0.35 ln n/n` |
| | hint, `H` | .024697 [.024696] | .024057 [.024068] | .023722 [.023718] | `R^max = .023270` | `0.22 ln n/n` |
| | non-adaptive | .040673 [.040825] | .038776 [.038801] | .037648 [.037666] | `θ_na = .036246` | `0.68 ln n/n` |
| `(0.2, 4)` | `g=0` / `γ*` / `H` / non-adaptive | .088966 / .102958 / .101969 / .143927 | .088015 / .101809 / .101300 / .141920 | .087143 / .101133 / .100876 / .140782 | .086324 / .100321 / .100321 / .139401 | `0.39 / 0.39 / 0.27 / 0.67` |
| `(0.3, 1)` | `g=0` / `γ*` / `H` / non-adaptive | .014545 / .014415 / .013629 / .024462 | .013331 / .013482 / .013014 / .022473 | .012783 / .012932 / .012667 / .021349 | .012049 / .012209 / .012209 / .019941 | `0.35 / 0.35 / 0.22 / 0.68` |

So the three hinted quantities approach `R_0`, `R^max`, `R^max` and the non-adaptive one `θ_na`, from above, like
`(0.2…0.7)·ln n/n`.  (Small differences from the author's numbers in the first and fourth rows come from the choice of the
five centre types; independent code otherwise.)  *Item 14 of the brief:* at `(0.1, 2, 0.3E)` the every-`n` bound
`E|Q(γ*|x|)| ≥ (1−2δ)e^{n·0.023270}` (the pair `γ* = −0.5634`, `t* = 0.3166`; game value re-computed by LP) exceeds
`e^{nR_0} = e^{n·0.019497}` for `n > ln(1/(1−2δ))/(R^max − R_0) = 184` (`δ = ¼`); with the exact density-ball sums the
certified exponent at `γ*` is `.023996` at `n = 4000` against `.020339` for the best sensitive ball at `g = 0`
(a factor `e^{14.6}`).  For `(0.3, 1)` the two exponents differ by `1.6·10⁻⁴` only and the bound overtakes `e^{nR_0}` at
`n ≈ 4300`.

**Theorem F6 on multi-centre and centreless families (test 7).**  `ω(D)` = least `ω ≥ 0` with
`θ ≤ R^max(e−ω) + ω`, `θ = −n⁻¹ln μ_H(D)`, `e = n⁻¹ln Φ_H⁺(D)`; "raw" = `e − (R^max)^{−1}(θ)` over the sets with
`θ ≥ 3 ln n/n`.

| `(p,u)`, `n` | sets | largest `ω(D)` | in units `ln n/n` | where | largest raw |
|---|---|---|---|---|---|
| `(0.2,4)`, 80 | 303 | 0.0252 | 0.46 | single / union of two density balls | `+1.60 ln n/n` |
| `(0.2,4)`, 160 | 1287 | 0.0137 | 0.43 | the same | `+1.89 ln n/n` (at the smallest admitted `θ`) |
| `(0.2,4)`, 240 | 310 | 0.0091 | 0.40 | the same | `+2.03 ln n/n` (at the smallest admitted `θ`) |
| `(0.1,2)`, 160 | 810 | 0.0104 | 0.33 | a half-space | `+0.61 ln n/n` |
| `(0.5,2)`, 160 | 784 | 0.0149 | 0.47 | union of two Hamming balls | `+1.44 ln n/n` |

Unions of two balls gain nothing at the exponential scale over one ball; unions of 16 balls, lenses and all centreless
families (slabs, ellipsoids, boxes) are worse (`ω = 0` or raw strongly negative for most of them).  The growth of the
"largest raw" with `n` in the first three rows is an artefact of the cut `θ ≥ 3 ln n/n` (the inverse of `R^max` is steep at
small `θ`); at fixed `θ` the raw excess in units `ln n/n` decreases (test 16).

**What these numerics do and do not exercise.**  They test every single-letter identity of the report independently of
duality (tests 1–3), the two finite-`n` identities and the inequality on which Steps 2–5 of F6 rest (test 10), the
lemma F5 exactly (6b), and the theorem F6 on (i) all sets for `n ≤ 4`, (ii) sets found by local search for `n = 5, 6`,
(iii) sets that are invariant under a Young subgroup with at most four blocks for `n ≤ 240` and under two blocks for
`n ≤ 4000`.  They do **not** test F6 on sets without any symmetry at `n > 6` (e.g. unions of exponentially many balls
around a code, or random sets — which are not sensitive), and at `n ≤ 240` the slack `ln n/n ≈ 0.02–0.05` is of the size
of the smaller exponents, so only parameter pairs with large exponents (`u = 4`) have real power.  They do not test the
cost of the nested algorithm (F7/F9) at all: I did not simulate it.  Bugs of my own that were caught on the way and
are fixed in the files: an overflow in `ln(e^s−1)` (first run of test 5), a floating-point equality in test 11(a) (121
spurious "violations"), and an underflow of type densities below `10⁻³²³` in the ordering of density balls (first
version of test 16 and a few cases of test 11(c)); tests 5, 7, 8 were re-run with the corrected library (`rerun/`,
identical numbers).  Two inaccurate first attempts were replaced: the grid + zoom minimiser of test 2 (hence test 2b)
and a first check of F11(a) with a coarse inner grid (replaced by the closed form of test 13b).  No interval
arithmetic anywhere.

## 5. Lean and prior art

**Lean.**  `lake env lean <scratch>/ws/F/lean/WorkstreamF.lean` (no `lake build` running, checked with `pgrep`): exit 0,
6 s, `'WorkstreamF.shift_identity' depends on axioms: [propext, Classical.choice, Quot.sound]`; no `sorry`.  The four
statements are what the report says: `klBin_tilt` (`KL(x‖q₀e^{−u}/Z) = KL(x‖q₀) + ux + ln Z`, `0 < x, q₀ < 1`),
`cone_rate_eq` (`I^cone = J + uρ − Λ_m`), `sphere_rate_eq` (`J = I + KL(κ‖p)`), `shift_identity`
(`I^cone = I + KL(κ‖p) + uρ − Λ_m`) with `x = P(X=0|S=1)`, `y = P(X=1|S=0)`, `κ = m(1−x) + (1−m)y`,
`η₁ = (1−p)e^{−u}/(p+(1−p)e^{−u})`, `η₀ = pe^{−u}/(1−p+pe^{−u})`, `Λ(1) = −ln(p+(1−p)e^{−u})`, `Λ(0) = −ln(1−p+pe^{−u})`;
hypotheses `0 < x, y, p < 1`, `0 < κ < 1`; `m` unrestricted.  This is Theorem F3 for a binary centre letter and interior
profiles (m11).  `proofs/Frontiers/HintRecursion.lean` (scratch copy with `#print axioms`, `out_lean_hintrecursion.txt`):
exit 0, 19 s, standard axioms; `iterates_lt_hint_add` has the statement used in F9 (the bound on `T 0` is a separate
hypothesis `∃ C`); the fields of `HintPair` are listed in §2 C.  `NonAdaptive.lean`: `nonadaptive_expected_queries_ge`
read; its hypotheses (query sets `Q ω` independent of the residual, pairs of class members with `|Φ(g′_j) − Φ(g_j)| > ε`,
weights with cap `B`) are met by the pairs of F4(b)(i).

**Prior art** (25 Nov 2026; generic queries only; "not found" means not found at this depth).

| source | what it says, as far as I read | how read |
|---|---|---|
| R. Ahlswede, Z. Zhang, *Asymptotical isoperimetric problem* (3-page summary, Bielefeld server, item 149) | finite alphabets, general distortion, **cardinalities** (`G_n(M,d) = min{\|Γ_d(A)\| : \|A\| ≥ M}`); Theorem 1: `ξ_N(R,δ) ≥ γ(R,δ) ≥ ξ_N(R,δ) − O(ln N/N^{1/\|X\|})`, `ξ_N = inf_{H(X\|U)≥R} sup_{Eρ(X,Y)≤δ} H(Y\|U)`, `\|U\| = N`; the Inherently Typical Subset Lemma (`m ≥ 2^{16\|X\|²}`, gap `log²m/m`, loss `\|X\|(m+1)^{\|X\|}log(n+1)/n`), attributed to Ahlswede–Yang–Zhang 1997 | **read in full** (PDF fetched, text extracted with `pdftotext`; copy in `dl_az/`) |
| L. Yu, *Exact exponents for concentration and isoperimetry in product Polish spaces*, arXiv:2205.07596 v3 | two distributions `P_X`, `P_Y` on possibly different Polish spaces, additive cost, `E_0^{(n)}(α,τ) = −n⁻¹ log inf{P_Y^n(A^{nτ}) : P_X^n(A) ≥ e^{−nα}}`; `ψ(α,τ) = sup_{Q_{XW}: D(Q_{X\|W}‖P_X\|Q_W) ≤ α} inf_{Q_{Y\|XW}: E c ≤ τ} D(Q_{Y\|W}‖P_Y\|Q_W)` (eq. 35); Theorem 4: `\|W\| ≤ 2`; Theorem 5, four statements (upper bounds on `limsup E_0` under Assumption 3 and bounded cost, lower bound under Assumption 1); "generalizes Ahlswede and Zhang's result … also based on the inherently typical subset lemma" | abstract page and a machine summary of the arXiv HTML v3 (first 100 000 characters); hypotheses not checked in the text by me (R4 read the PDF text for workstream A) |
| B. Bollobás, I. Leader, *Isoperimetric inequalities and fractional set systems*, JCTA 56(1) (1991) 63–74 | `p`-biased product measure on `{0,1}ⁿ`; if a **down-set** `A` has probability at least a cumulative binomial sum, then `A(t)` has at least the corresponding larger sum; "This result generalises Harper's theorem" | abstract, through a machine summary of the repository record (formulas garbled there); paper not read |
| P. Mathé, E. Novak, *Simple Monte Carlo and the Metropolis algorithm*, J. Complexity 2007 (arXiv math/0611285) | integration against an unknown density; lower bound for all non-adaptive methods on a class with Lipschitz log-density (curse of dimension), adaptive Metropolis breaks it for log-concave densities | search-engine summary only |
| vertex isoperimetry in the Johnson graph (Christofides–Ellis–Keevash; Diego–Serra–Vena) | approximate / small-case vertex-isoperimetric inequalities inside one slice | search-engine summary only; listed because `μ_H` is uniform on slices — the neighbourhoods of F6 cross slices, so these do not apply |

*Assessment.*  The report's attributions to Bollobás–Leader, Ahlswede–Zhang/AYZ and Yu are accurate as far as these
readings go, with the correction m2.  Theorem F6 is not in these sources and is not a black-box corollary of the
fixed-measure theorem (§2 A, last paragraph); its proof is theirs, with the reference law chosen after the set.  Not
found at this depth (7 searches, 7 fetches of which 2 were refused by the servers): an isoperimetric statement for a mixture over types with a
type-dependent enlargement; the exponent `max_γ R_γ`; exact adaptive/non-adaptive exponents for integration against a
product measure over a Hamming–Lipschitz class.  This is "not found", not "new".

## 6. What I did not check

* Theorem F1(b) (Theorem A(ii) of workstream A) beyond the identification of the site; I relied on R4.
* The nested algorithm end to end: no simulation of F7 by me (the author's `t14` was neither run nor read beyond its
  output header); F7 and the induction of F9 are checked on paper only; the uniformity of the `o(n)` terms through `k`
  levels likewise.  The proof of Theorem 11.52 itself was read as far as needed to transpose it (R7 had re-derived it).
* Theorem F6 on sets without symmetry for `n > 6`; rates of convergence (`ω_n`) — nothing quantitative is proved and I
  did not try to improve it.
* Proposition F11: the lower-bound construction for product samplers, and all of (b) (the nested scheme with the
  reference `0`, Yu's theorem as its tail lemma).  Proposition F12: read only.
* The Lean proofs line by line (statements read, files compiled, axioms printed); `HintPair` for this pair is not
  formalised by anyone.
* The author's scripts (not run); the report's numerical claims were compared with my own code where I recomputed the
  same quantity (tables of §§3.7, 3.8, 4; `t18`), not otherwise (`t12` grid details, `t14`, `t15`, `t16`, `t19`, `t23`, `t24`).
* Prior art beyond abstracts and summaries, except the Ahlswede–Zhang summary (read in full).
* The repository files that appeared while I worked (theory report §§11.20–11.21, `proofs/Frontiers/FieldShift.lean`,
  `GamePair.lean`, `experiments/workstreams/F/`, the coordinator's check script for the addendum): outside my brief, not read.
* Floating point: all numerical statements are in double precision without interval arithmetic.

## Appendix: files in `referee9/`

`R9_report.md` (this file) · `r9lib.py`, `r9prof.py` (libraries) · `r9_t1_game.py`, `r9_t2_maxmin.py`, `r9_t2b_polish.py`,
`r9_t2c_na_small.py`, `r9_t3_SL.py`, `r9_t3b_SLadv.py`, `r9_t3c_SLcheck.py`, `r9_t4_validate.py`, `r9_t5_finite.py`,
`r9_t6_small.py`, `r9_t7_F6sets.py`, `r9_t8_anneal.py`, `r9_t9_recursion.py`, `r9_t10_lemmaT.py`, `r9_t11_F4.py`,
`r9_t12_addendum.py`, `r9_t13_table.py`, `r9_t13b_F11.py`, `r9_t14_misc.py`, `r9_t15_lowerbound.py`, `r9_t16_ballconv.py`, `r9_t17_minmu.py`
(tests; commands in §4) · `out_*.txt` (their outputs), `rerun/` (tests 5, 7, 8 once more with the final library) ·
`lean/HintRecursion_copy.lean`, `out_lean_hintrecursion.txt` · `dl_az/` (the Ahlswede–Zhang summary, PDF and extracted text) ·
`BRIEF.md`, `ADDENDUM_monotonicity.md` (inputs, not mine).
