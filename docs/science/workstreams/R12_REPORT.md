# Workstream R12 — independent review of what the theory division asked us to review (THY-RES-0010 §9.2)

*Science division, review workstream R12, 2026-11-26.  Object: the theory branch at commit
`9408e33` (read-only export `…/scratchpad/thy_ro_9408e33/`, called `<EXP>` below).  Our own
tree at `d45ad56` when the work began (the coordinator has committed since; the files
used here — `QueryLowerBound.lean`, `CertificateAlgebra.lean`, workstream K, P3 — were read
as they stood).  Everything here was written by one reviewer working alone; the scripts,
logs and notes are in `experiments/science/ws_R12/`.  The kinds of checking are kept
apart throughout: **review** (re-derived on paper from the hypotheses), **replication**
(re-computed with code of my own, written from the statements before the theory
division's harness was opened), **re-run** (their code, unchanged), and **read only**;
"confirmed" is not used for anything only read.
Labels of COMMON.md rule 6: [V] machine-checked, [P] paper proof given here, [N] numerical
evidence, [K] known, [C] conjecture.  All statements are model-relative mathematics;
nothing here is a physical claim.*

**Headline.**  No critical finding.  The corrected Theorem 11.110(e) is right — and holds
without its hypothesis.  **Two major findings, both in sentences that the theory division
itself marked as a sketch or as quoted from memory:** Proposition 11.18e(b) (randomised
algorithms need the ball too)
is false as written — at `δ = 0.05` five random evaluations do what it says needs
`0.95·(n + 1)`, and the step that carries this is machine-checked here; and the
"necessary order" of Proposition 11.113(d) is wrong by a factor `e^Δ` (no consequence at our
`Δ = 0.06`).  The support-fraction claim is **true**: proved here by induction and found
exact in 128 exhaustive cases; for unequal alphabets the right constant is
`1/(product of the m − 1 largest alphabet sizes)`.  Our own adjacency lemma is false for
empty boxes, as they say; nothing of ours depended on it.

---

## 0. Verdict table

| # | statement | verdict | what was done | scripts / logs (`experiments/science/ws_R12/`) |
|---|---|---|---|---|
| 1 | Theorem 11.110(e), corrected two-sided display | **holds** as stated; holds also *without* the hypothesis "no single state can change `ln Z` by `ε`" if the check is done in two stages (§1, m2) | review (both ends re-derived); replication (exact packings by exhaustive DP, 720 + 1425 small boxes; closed forms up to `10⁷` states); re-run (XXIV.9; mutation "dips alone" caught); a copy of `BoxClass.lean` compiled here, 12 statements, standard axioms; four small additions of mine machine-checked (§3.7) | `r12_01_box.py`, `r12_01b_twostage.py`, `r12_07_harness_rerun.sh`, `r12_07b_mutations.sh`, `r12_08_lean_boxclass.sh`, `r12_09_lean_additions.sh` |
| 1a | the first version (dips alone) was false near the floor | **yes** — at the floor of a constant box the bump lower bound (45 at `ε = 0.02`) exceeds the upper end written with the dip packing (25.1) | replication | `r12_01_box.py` part B2 |
| 1b | reading "`Θ((Z(lo)/Z − 1)/ε + (1 − Z(hi)/Z)/ε)`" | right **for `ε ≲ 1`**, with the single-state hypothesis and an additive constant; for large `ε` the two ends differ by `≈ 4(e^{ε/2}+1)ln(1/δ)/(1−2δ)` and "`/ε`" is not the dependence (§1, m4) | review; replication | part B3 |
| 1c | (c): proportional case, `544`; without a hint `545`; general count `1088` | **hold**; exact failure of 544 samples `0.0379–0.0495 ≤ 0.05`; exact failure of the rule without a hint `≤ 0.9993·δ` (theirs: `0.994·δ` on a random grid) | review; replication; re-run | parts B1, C |
| 1d | (a), (c), (d), (f) as amended; Lean statements against the wording | no error; **the report omits `U > 0`, `V > 0`**, which the Lean statements have (§1, m1); (b): `q*` re-derived, the entropy count read only | review ((a), (c), (d), (f) and `q*`); Lean statements read in full | — |
| 2a | Proposition 11.18e: dimension `N_ball`, closure of the class, unisolvence of the ball for **every** anchor, part (a), "any unisolvent set does" | **hold** | review; replication (101 grid × order cases, every reference); re-run XI.20 | `r12_02_support.py` part 1 |
| 2b | Proposition 11.18e(b) (randomised, no hint: `(1 − δ)N_ball − o(1)`) | **false as written** (task of (a) with failure probability `δ`); unproved under the other reading (prescribed accuracy) — **major M1** | review (counter-algorithm with proof; its core on the cube machine-checked here, `affine_half_large`); replication (exact failure probability on the cube) | `r12_03_randomised.py`, `r12_09_lean_additions.sh` |
| 2c | Proposition 11.18e(c): support fraction `≥ k^{−(m−1)}` | **true** — proved (induction on the sites); exact in **128 exhaustive cases, 0 refutations** (17 larger cases: random search only, nothing found); for unequal alphabets the sharp constant is `1/Π(m − 1 largest k_i)` | review (proof); replication (brute force); re-run XI.20 (theirs is a spot test) | `r12_02_support.py` part 2, `r12_02b_support_search.py` |
| 3 | Proposition 11.113(a)–(c) | **hold** (one wording point: the *bracket* stays inside the deterministic one only after clipping) | review; replication (200 exact sandwiches; 400 000 simulated runs; exact binomial coverage); re-run XXIV.10 | `r12_04_sandwich.py` |
| 3d | Proposition 11.113(d): "this order is necessary", "the hint is worth `(e^Δ − 1)/ε`" | **wrong in its `Δ`-dependence** for `Δ ≳ 1` (factor `e^Δ`); right to first order in `Δ` — **major M2**, no consequence at `Δ = 0.0605` | review; replication | part 4 |
| 4 | Corollary 11.114(a)–(c), `BoxRatio.lean` | **hold**; the Lean statements are slightly more general than the wording (no disjointness needed in (a), (b)) and need `U_M, V_M > 0` | review; replication (252 small cases, exhaustive over subsets); re-run XXIV.8; Lean **read only** (cannot be compiled here) | `r12_06_ratio.py` |
| 4d | Corollary 11.114(d) and consequence (3) | (3) holds at the level of packing and hitting numbers; the bold display of (d) has the dip term only — the defect just removed from 11.110(e), here acknowledged in a parenthesis; the bump alternative for ratios is not in `BoxRatio.lean` (§1, m5) — machine-checked here | review; replication | parts 3, 4; `r12_09_lean_additions.sh` |
| 5 | `BarrierCertificate.lean`, Theorem 11.115(c)–(e) | the soundness statements say what a barrier certificate must mean; all small instances reproduced; **our lemma is false for empty boxes, their clause repairs it, nothing of ours used the false direction**; their copy of our file is ours up to the two changes they list | Lean **read only** (in full; cannot be compiled here); replication (instances and the adjacency lemma by brute force); `diff` | `r12_05_barrier.py` |
| 6 | Theorem 11.18d as written | says what is machine-checked, with three small exceptions; attribution incomplete for (b), (d); what is *not* machine-checked of P3's certificate is stated correctly (§1, m9) | Lean file **read** in full against the text (its core was compared with ours by the coordinator, SCI-MSG-0023 §2); re-run XI.19 | — |
| 7 | harness blocks XI.19, XI.20, XXIV.6–XXIV.10 | all `survived`; the quoted numbers come out (`85`; `0.994`; `544/545/1088`; 41 mutations of group XXIV, all caught; 56 of group XI, all caught) | re-run | `r12_07_harness_rerun.sh`, `r12_07b_mutations.sh` |

---

## 1. Findings by severity, with replacement texts

*How the line was drawn.*  **Major:** a mathematical claim that is false or unproved as
stated (two, both repairable; nothing else in their tree depends on either).  **Minor:**
a hypothesis that the Lean statement or the theorem itself carries and the wording drops,
a display that is incomplete where the text says so, wording, attribution, stale
sentences — and four sharpenings (m2, m3, m8 and the one-sided lemmas of m1) that are
additions rather than corrections.

### Critical

None.

### Major

**M1 — Proposition 11.18e(b) is false as written.**  Text: "For randomised algorithms
without a hint the same count holds in the worst case, `sup_g E|Q(g)| ≥ (1 − δ)·N_ball − o(1)`",
the task being that of (a): "returns a finite lower bound for `min(E₀ + g)` or a bracket of
finite width for `ln Z`, valid for every `g ∈ 𝒢`".

*Counter-algorithm* **[P; checked numerically, exactly on the cube]**.  Let `𝒢` be the class
with given order-`m` constants, so `g = h + R` with `h = I_{m−1}g` of order below `m` and
`|R| ≤ C := Σ_T c_T` (Theorem 11.18d).  Let `ρ` be the least support fraction of a non-zero
function of order below `m` (item 2c: `ρ = 1/Π(m − 1 largest k_i)`).  Then there is
`c = c(grid, m) > 0` with

    #{x : |h(x)| ≥ c·‖h‖_∞}  ≥  ρ·|X|        for every h of order below m

(on the unit sphere of the finite-dimensional space, the `⌈ρ|X|⌉`-th largest value of `|h|`
is continuous and positive, hence bounded below).  Draw `q = ⌈ln(1/δ)/−ln(1 − ρ)⌉`
configurations uniformly and independently, let `M = max_j |g(x^j)|` and
`B = (M + C)/c + C`.  With probability at least `1 − δ` some sample has `|h(x^j)| ≥ c‖h‖_∞`;
then `‖h‖_∞ ≤ (M + C)/c`, `‖g‖_∞ ≤ B`, and

    min E₀ − B  ≤  min(E₀ + g),            |ln Z(E₀ + g) − ln Z(E₀)|  ≤  B.

This is a finite lower bound and a bracket of finite width, valid with probability `1 − δ`
on **every** `g ∈ 𝒢`, without a hint, from `q ≤ ⌈k^{m−1} ln(1/δ)⌉` evaluations whatever the
number of sites.  *Explicit on the cube, `m = 2`:* `h = α + Σβ_i s_i` (`s_i = ±1`),
`‖h‖_∞ = |α| + Σ|β_i|`; the largest of these `n + 1` terms is at least `‖h‖_∞/(n + 1)`, and
pairing `s` with `s` flipped at that site (or with `−s`, if the term is `α`) shows that half
of the points have `|h|` at least that term: `c = 1/(n + 1)`, `ρ = ½`, `q = ⌈log₂(1/δ)⌉`.
This step is machine-checked here — **[V]** `ScienceR12.affine_half_large`
(`experiments/science/ws_R12/lean/R12Additions.lean`, standard axioms): for every affine
`h` on `{−1, 1}^n` and every point `s₀`, at least `2^{n−1}` points `s` have
`|h(s₀)| ≤ (n + 1)|h(s)|`.  The rest (`q` independent samples miss with probability at most
`2^{−q}`; the bound `B`) is two lines of paper.
*Explicit on the cube, any `m = d + 1`:* `c = 0.6/(N_ball·(3n)^d)`, `ρ = 2^{−d}` (take the
set `U*` maximising `|ĥ(U)|·(3n)^{|U|}`; on every sub-cube over the coordinates of `U*` the
top Walsh coefficient is within a factor `[0.6, 1.4]` of `ĥ(U*)`).

*Numbers* (`r12_03_randomised.py`): `n = 8, 12, 16` (`N_ball = 9, 13, 17`; the claimed bound
`(1 − δ)N_ball = 8.55, 12.35, 16.15` at `δ = 0.05`): `q = 5`; the exact fraction of bad points
is at most `0.5000` (attained) over 1080–1288 test functions and a hill-climbing adversary,
so the exact failure probability is at most `2⁻⁵ = 0.031`; end to end at `n = 12` with a
random known part and a remainder `|R| ≤ 0.7` the output was invalid in 2 of 20 000 runs.
For `d = 2, 3` at `n = 10`: least fraction of good points `0.2500`, `0.1250` — exactly `2^{−d}`
(cylinders) — and `q = 11`, `23` against `N_ball = 56`, `176`.

*Why the sketch fails.*  "The target keeps a spread that grows with the variance" is true,
and does not prevent a valid finite bound, because the bound may scale with the observed
values.  The deterministic argument of (a) works because the adversary chooses the hidden
direction after the evaluation set; a random set defeats every fixed direction with
probability `ρ` per point.

*What remains.*  The bound `B` is valid and useless (`c` is small): nothing here helps a
certificate of useful width.  For a bracket of **prescribed** width the count of (b) is
plausible and unproved: conditionally on a transcript with fewer evaluations the target
has atoms (the minimiser may lie where the unseen direction vanishes), so "the probability
of being right tends to zero" is not automatic.  (On the cube with `m = 2`: with one
coefficient unseen, guessing its sign is right with probability ½ under a symmetric
prior.  A proof would have to show that with `j` evaluations missing the probability of
being right is at most about `2^{−j}`, which does give `(1 − δ)N_ball − o(1)`; I have not
written this out, and for one site the bound `(1 − 2δ)N_ball` is just the packing bound at
a flat instance.)  Nothing else in the theory report uses
(b): `BLUEPRINT.md` Step 3b and the research log quote the deterministic statement only.
THY-RES-0010 §4 repeats (b).

*Replacement text for (b):*

> (b) *Randomised algorithms without a hint.*  What is asked decides.  A bound of
> unspecified width costs no more than with a hint: there is `c = c(k₁, …, k_n; m) > 0` such
> that every function of order below `m` is at least `c` times its maximum in absolute
> value on a fraction `ρ = 1/Π(m − 1 largest k_i)` of the configurations, so
> `⌈ln(1/δ)/−ln(1 − ρ)⌉` uniformly random evaluations give, with probability `1 − δ` on every
> `g ∈ 𝒢`, `‖g‖_∞ ≤ B := (max_j |g(x^j)| + C)/c + C` and hence a finite lower bound for the
> minimum and a finite bracket for `ln Z` — whatever the number of sites (the Scientific
> Discovery Division's review R12; `c = 1/(n + 1)`, `ρ = ½` on the cube for `m = 2`).  The
> count `N_ball` of (a) is therefore a statement about deterministic algorithms.  The
> bound is valid and useless.  For a bracket of prescribed width we conjecture
> `sup_g E|Q(g)| ≥ (1 − δ)N_ball − o(1)` **[C]**; a Gaussian prior alone does not prove it.

**M2 — Proposition 11.113(d): the "necessary order" and the value of the hint are wrong
by a factor `e^Δ`.**  Text: "without a hint `ln Z(E)` is certified within `ε` by about
`ln(2/δ)·(e^Δ − 1)²/(2ε²)` evaluations, and this order is necessary in the worst case over
the box … The hint is worth the factor `(e^Δ − 1)/ε`."  The count is sufficient.  It is not
necessary in its `Δ`-dependence.  Write `Z(E) = (Z(m₋) − Z(m₊))(c + w)`, `c = 1/(e^Δ − 1)`,
`w = E_q W`.  The plug-in estimate of (c) is off by more than `ε` in `ln Z` iff
`Ŵ − w > t₊ := (e^ε − 1)(c + w)` or `Ŵ − w < −t₋ := −(1 − e^{−ε})(c + w)`; by Hoeffding's
Theorem 1 in its Kullback–Leibler form **[K — from memory, standard]**, valid for every
`[0, 1]`-valued `W` of mean `w`,

    N_KL  =  ln(2/δ) · max_w  1/min( KL(w + t₊ ‖ w), KL(w − t₋ ‖ w) )   ≈   ln(2/δ)·(e^Δ − 1)²/(2 e^Δ ε²)

evaluations suffice **on every member of the box**, the maximum being at `w ≈ c/(1 + 2c)`
(where `Var W ≤ w(1 − w)` is largest relative to `(c + w)²`: `max_w w(1 − w)/(c + w)² =
1/(4c(1 + c))`) **[P]**.  A two-point argument (two-level members with means `w`, `w′`;
Bretagnolle–Huber, **[P-sketch; K from memory]**) gives a lower bound of the same order.
*Numbers* (`r12_04_sandwich.py` part 4, `δ = 0.05`):

| `Δ` | `ε` | count of (d) | `N_KL` (sufficient on every member) | ratio | `e^{−Δ}` | two-point lower bound |
|---|---|---|---|---|---|---|
| 0.0605 | 0.01 | 72 | 68 | 0.948 | 0.941 | 7 |
| 0.5 | 0.01 | 7 762 | 4 724 | 0.609 | 0.607 | 517 |
| 1 | 0.01 | 54 457 | 20 100 | 0.369 | 0.368 | 2 199 |
| 2 | 0.01 | 752 901 | 102 234 | 0.136 | 0.135 | 11 188 |
| 3 | 0.1 | 67 185 | 3 455 | 0.051 | 0.050 | 388 |
| 5 | 0.1 | 4 008 085 | 27 898 | 0.0070 | 0.0067 | 3 138 |

and the exact failure probability of the plug-in estimate with `N_KL` samples on two-level
members (binomial, 600 means) is at most `0.007` at `Δ = 1, 3, 5`.  (For a bracket rather
than a point estimate the same inequality is inverted, `{w : N·KL(Ŵ ‖ w) ≤ ln(2/δ)}` — a
valid interval for every `[0, 1]`-valued `W`, **[K — from memory]**; its width was not
computed here.)  So the worst-case order
without a hint is `(e^Δ − 1)²/(e^Δ ε²)`, and worst case against worst case the hint is worth
`(1 − e^{−Δ})/ε` — at most `1/ε`.  For a narrow sandwich both forms are `Δ/ε`: at the
`Δ = 0.0605` of our twenty-residue instance the correction is 5 %.

*Replacement text for (d):*

> (d) *Against a hint.*  With `Δ = ln Z(m₋) − ln Z(m₊)`: by (c), `ln(2/δ)(e^Δ − 1)²/(2ε²)`
> evaluations certify `ln Z(E)` within `ε` without a hint.  For a wide sandwich fewer do:
> Hoeffding's inequality in its Kullback–Leibler form gives the same estimate within `ε`
> on every member of the box from about `ln(2/δ)(e^Δ − 1)²/(2e^Δ ε²)` evaluations, and this
> order — `(e^Δ − 1)²/(e^Δ ε²)` — is necessary in the worst case over the box (a two-point
> argument; the Scientific Discovery Division's review R12).  With a hint, Theorem
> 11.110(e) gives at most the order `(e^Δ − 1)/ε`.  Worst case against worst case the hint
> is worth the factor `(1 − e^{−Δ})/ε`; `Δ/ε` for a narrow sandwich.

### Minor

**m1 — Theorem 11.110(c): the hypotheses `U > 0`, `V > 0` are missing from the text.**
`detect_ge`, `detect_ge_of_proportional`, `box_spotCheck_correct` and
`box_spotCheck_correct_of_proportional` all assume `0 < Σ dip` and `0 < Σ bump` (`hU`, `hV`);
without them `sampler` does not sum to one in Lean, and `p(η)` in the report has a zero
denominator.
The case excluded is the one the correction is about: **at** the floor (`U = 0`).  There
the right sampler is the bump half alone and the factor `½` disappears.  *Replacement:*
add "for `U, V > 0`; if one of them vanishes the sampler is the other half alone, and
`p(η)` is the corresponding term without the factor `½`".  Both one-sided statements are
machine-checked here on their definitions — **[V]** `ScienceR12.detect_ge_at_floor`,
`detect_ge_at_ceiling` (`lean/R12Additions.lean`) — and can be taken over as they are.

**m2 — Theorem 11.110(e): the hypothesis is not needed for the display** **[P; checked on
1425 small boxes]**.  Let `H` be the states that are heavy on their own (dip weight above
`(e^ε − 1)Z` or bump weight above `(1 − e^{−ε})Z`) and `R` the rest.  *Two-stage check:*
evaluate `H`; if all agree with the hint, spot-check `R` with the sampler of (c) restricted
to `R`, `N_R = ⌈ln(1/δ)·max(1, 2U_R/((e^{ε/2} − 1)Z), 2V_R/((1 − e^{−ε/2})Z))⌉`.  A member that
agrees with `r` on `H` and is off by more than `ε/2` differs from `r` on a subset of `R` of
dip weight at least `(e^{ε/2} − 1)Z` or bump weight at least `(1 − e^{−ε/2})Z`: correct.  On
`R` no state is heavy, the greedy packings apply to `R`, and `k ≥ |H| + max(k_R^{dip}, k_R^{bump})`;
so for `δ ≤ e^{−1/8}`

    (1 − 2δ)·k   ≤   min_alg E|Q(r)|   ≤   |H| + N_R   ≤   4 ln(1/δ)(e^{ε/2} + 1)(k + 1) + 1        at every instance.

In 1238 of 1425 random small boxes some state is heavy; the one-stage `N` of (c) exceeds
the right-hand side in 839 of them (and in none of the 187 without a heavy state), the
two-stage count in none (largest ratio `0.49`; worst exact miss probability `0.029`).  The hypothesis "no single state can change `ln Z`
by `ε`" is needed only for the closed form in `Z(lo)/Z`, `Z(hi)/Z`.

**m3 — Theorem 11.110(c): `2·max` can be a sum** **[V** `ScienceR12.detect_ge_weighted`,
`weighted_opt`**; checked on 720 small boxes]**.  With
the mixture weights `λ = A/(A + B)`, `1 − λ`, `A = (Z(lo)/Z − 1)/(e^{ε/2} − 1)`,
`B = (1 − Z(hi)/Z)/(1 − e^{−ε/2})`, instead of `½, ½`, the detection probability is
`1/(A + B)` and `N = ⌈ln(1/δ)·max(1, A + B)⌉ ≤ ⌈ln(1/δ)·max(1, 2A, 2B)⌉` — the displayed
quantity of (e) itself.  (Examples from the log: `313 → 195`, `1001 → 501`, `2764 → 1382`.)  In
the proportional case `max(A, B)` is better still, as they prove.

**m4 — the `Θ` reading.**  Where no single state is heavy, and for `ε ≤ 1`, with
`a = Z(lo)/Z − 1`, `b = 1 − Z(hi)/Z`:

    (1 − 2δ)·((a + b)/(6.9 ε) − 1)   ≤   cost   ≤   ln(1/δ)·(2.7 (a + b)/ε + 1) + 1        [P]

— a `Θ` with constants that depend on `δ` only, and an additive constant.  For large `ε`
this fails: the lower end is `≈ a/(2(e^ε − 1))`, the upper `≈ 2a ln(1/δ)/(e^{ε/2} − 1)`.  At
the centre of the constant box with `ρ₋ = 12` (closed forms, `10⁷` states): lower end over
`(a + b)/ε` falls from `0.79` (`ε = 0.1`) to `0.0024` (`ε = 8`), and upper over lower grows from
`7.4` to `187`.  The report's own sentence ("up to a factor that depends on `ε` and `δ` only
and an additive constant") is correct; the summary row of §0 and THY-RES-0010 §1 state the
`Θ` without the hypothesis, the additive constant or the restriction to bounded `ε`.
*Replacement for those places:* "for accuracies `ε ≲ 1`, at instances where no single state
can change `ln Z` by `ε`, and up to an additive constant".  Also the cases `U = V = 0` (a
degenerate box: cost 0) and `Z(lo) = Z` are covered only with m1.

**m5 — Corollary 11.114(d): the display has the dip term only.**  At the floor of both
macrostates `max_M (W_M(lo)/W_M − 1)/ε = 0`, while sets inside a macrostate with bump weight
above `(1 − e^{−ε})W_M`, raised to the ceiling, move the log-ratio by more than `ε` and force
`(1 − 2δ)` evaluations each: `10, 40, 200` disjoint sets at `ε = 0.2, 0.05, 0.01` in the
closed-form example (`r12_06_ratio.py` part 3).  The text says so in a parenthesis ("the
bumps enter as in Theorem 11.110(e)"), but `BoxRatio.lean` has no bump alternative, so that
half of the lower bound is on paper only in their library, and the bold sentence is the
one that was just corrected in Theorem 11.110(e).  The missing alternative is
machine-checked here on their definitions — **[V]** `ScienceR12.logRatio_bumpAlt_lt`,
`logRatio_bumpAlt_gt` (`lean/R12Additions.lean`); the packing statement then follows as
`ratio_expected_queries_ge` does.  In 130 of 252 small cases the packing of *all*
alternatives that move the ratio exceeds the packing of the alternatives the Lean theorem
uses.  *Replacement for the bold sentence:* "… is, up to a factor depending on `ε`, `δ` and
an additive constant, `max_M [(W_M(lo)/W_M(r) − 1)/ε + (1 − W_M(hi)/W_M(r))/ε]`; the second
term (at most `1/ε`) is the whole cost near the floor of a macrostate; its lower bound is
the analogue of `logZ_bumpAlt_gt` for one macrostate."

**m6 — Corollary 11.114, Lean against wording.**  `ratio_detect_ge` and
`ratio_spotCheck_correct` do not assume `A`, `B` disjoint (the proof never uses it; the
report states disjointness); they do assume `U_A, V_A, U_B, V_B > 0`, which the report omits
(as in m1); the module docstring of `BoxRatio.lean` calls the result "Corollary 11.113".

**m7 — Proposition 11.113(c): "a bracket that never leaves the deterministic one".**  True
of the point estimate.  The bracket `estimate ± half-width` leaves `[Z(m₊), Z(m₋)]` whenever
`Ŵ` is within the half-width of 0 or 1 — in 47 % of 20 000 runs at `N = 20` on one random
instance — unless it is intersected with the deterministic bracket, which is always valid.
*Replacement:* "a bracket which, intersected with the deterministic one, …".

**m8 — Proposition 11.18e(c): unequal alphabets.**  As stated ("`k` states at every site")
the bound is right and attained.  With sites of different sizes the sharp bound is
`1/(product of the m − 1 largest k_i)`; `k_max^{−(m−1)}` is valid and not attained (20 of the
exhaustive cases, e.g. `(2, 2, 3)`, `m = 3`: `1/6` against `1/9`).  The harness tests the
claim on one cylinder and four random sparse combinations per case, equal alphabets only.
The proof is in §2.2.

**m9 — Theorem 11.18d as written.**  (i) The italic attribution names parts (a) and (c) as
ours.  Part (b) — anchored constants suffice — is the "Consequently" of our Proposition 1
(P3_REPORT §2.1) and the docstring of `AnchoredRemainder.lean` says so; part (d) in its
site-penalty form is the bracketed option of our Theorem 5 (P3_REPORT §2.5).  (ii) "with
equality for the set of all sites" in (c) is not a Lean statement (it is trivial, and
tested in XI.19) although the theorem is labelled [V] as a whole.  (iii) "For two states
per site the two kinds of constants coincide" is a one-line paper argument and [N]
(`equal_binary = 154`), not [V].  (iv) The remark that the identity holds with "after the
last site of `T`" follows from the Lean theorem applied to the reversed order — correct.
(v) The file has 17 declarations; the index of §9 and THY-RES-0010 count 16
(`mem_sitesBefore`).  (vi) THY-RES-0010 §2: "strictly smaller for 85 sets with three or
four [states]" — the harness computes constants for grids with two or three states only,
so all 85 are three-state sets; the report's own sentence ("for three or more the anchored
ones can be strictly smaller") is fine.  What is *not* machine-checked of our certificate
— chain rule, term-by-term bound with enclosures, the closed form, the banding — is stated
correctly in all four places where the report mentions it; in the limitations bullet of §8
the sentence "The certificates are probabilistic" follows the description of our
certificate and should not be read as applying to its deterministic bracket.

**m10 — Theorem 11.115(d).**  `Dom.adjacent_iff` and `cutCheck_boxAdjacent_iff` need at
least one site (`hn : 0 < n`); the text does not say so.  (With no site `SingleSite` is
false and `Adjacent` true.)  "The two ends of a single-site move" includes the null move:
`SingleSite` is "differ in at most one site".

**m11 — places where the correction has not arrived** (not in the list we were asked to
review; found while checking THY-RES-0010's "the bump term is in the theorem, the summary
rows, the README and the blueprint").  (i) `docs/BLUEPRINT.md` §6.4, "Rules that follow
(1)" (line 476): "The ceiling and the number of states do not enter" — the sentence of
the first version, just below the corrected display.  (ii) The same display, "no algorithm of
any kind does better than `(1 − 2δ)·max(⌊(Z(lo)/Z − 1)/(2(e^ε − 1))⌋, ⌊(1 − Z(hi)/Z)/(2(1 − e^{−ε}))⌋)`
evaluations — verified", has lost the hypothesis that no single state is heavy; without it
the line is false (all the dip weight on one state, no bumps: one evaluation suffices,
whatever `Z(lo)/Z`), and what is machine-checked is the packing statement, not the greedy
floors.  (iii) Three sentences still say that ratios of macrostate weights are not
covered — theory report §8 (line 1276: "neither minima nor ratios of macrostate weights
are covered"), §11.30 (line 9381: "not differences of macrostates — for which §11.28 gives
the range but not the cost") and `BLUEPRINT.md` §6.4 rule (5) (line 491) — next to
Corollary 11.114, which covers them in a box class.

---

## 2. What was re-derived

### 2.1 Theorem 11.110 [review]

Notation `z = Z(r)/Z₀`, `a = U/z`, `b = V/z`.

* **(d), greedy packing.**  If no point has dip weight above `t = (e^ε − 1)z`, fill bins
  until the sum exceeds `t`: every bin weighs at most `2t`, the last incomplete one at most
  `t`, so `U ≤ 2tk + t` and `k ≥ ⌈U/(2t) − ½⌉ ≥ ⌊a/(2(e^ε − 1))⌋`.  The same with bumps and
  `(1 − e^{−ε})z`.  The lower bound `(1 − 2δ)k` is `expected_queries_ge_packing` with unit
  weights and capacity one (read in `QueryLowerBound.lean`, unchanged since our base).
* **(e), upper end.**  `N = ⌈ln(1/δ)M⌉`, `M = max(1, 2a/(e^{ε/2} − 1), 2b/(1 − e^{−ε/2}))`.  From
  the two floors, `a < 2(e^ε − 1)(k + 1)` and `b < 2(1 − e^{−ε})(k + 1)`; hence
  `2a/(e^{ε/2} − 1) < 4(e^{ε/2} + 1)(k + 1)` and `2b/(1 − e^{−ε/2}) < 4(1 + e^{−ε/2})(k + 1)`, and
  `N ≤ 4 ln(1/δ)(e^{ε/2} + 1)(k + 1) + 1`.  ✓.  (`k` may be the largest *mixed* packing number,
  as in the report, or the larger of the two, as in THY-RES-0010: both ends hold for
  either; the mixed number exceeds the larger of the two in 108 of 720 small cases.)
* **What the first version got wrong.**  The old display (export of `24a3c27`, line 8881)
  was a true pair of inequalities — its upper end contained `1/(1 − e^{−ε/2})`.  False were
  the sentences after it: "the two bounds differ by a factor that depends on `ε` and `δ`
  only" (at the floor the lower end was 0) and "`Θ((e^{ρ₋} − 1)/ε)` … the ceiling `ρ₊` … absent".
  The correction describes this accurately.
* **(c).**  `1/p = max(1, 2·max(a/(e^η − 1), b/(1 − e^{−η})))`; `(1 − p)^N ≤ e^{−pN} ≤ δ`.
  Proportional case: both halves of the sampler are one distribution and
  `q(D) = dip(D)/U = bump(D)/V`.  Arithmetic: `(e³ − 1)/(e^{0.1} − 1)·ln 20 = 543.6`.
* **The rule without a hint.**  A wrong output at level `v` forces
  `1 − s > (e^η − 1)/(e^{ρ₋+v} − 1)` (too low) or `1 − s > (1 − e^{−η})/(1 − e^{−(ρ₊−v)}) ≥ 1 − e^{−η}`
  (too high); the rule stops at `v` with probability `s^{N(v)}`; so the failure is at most
  `Σ_v s_v(1 − q(v))^{N(v)−1} ≤ δ`.  ✓.
* **(a).**  `L(w)` is the maximum over `p` of `ln(1 − p + pe^w) − pw`, at `p* = 1/w − 1/(e^w − 1)`;
  the form with the mean known has `p = a/w` because the two-point law with mean zero on
  `{−a, b}` puts mass `a/(a + b)` on `b`.  `L(3.7) = 1.4604`.  **(b)**: `q*` re-derived from
  `1 + q(e^{ρ₋} − 1) ≤ e^ε(1 − q(1 − e^{−ρ₊}))`; the count `e^{S(π)(1+o(1))}` read only.
  **(f)**: Chebyshev step and monotonicity of `W` in `b` re-derived; `W(3.7, 0.036²) =
  3.38·10⁻³`; the inequality itself is machine-checked on our side (workstream L4,
  SCI-MSG-0023 — not re-checked here).
* **Lean statements against the wording.**  `logZ_bumpAlt_gt`: nonnegative weights, one
  positive weight, bump weight of `D` above `(1 − e^{−ε})Z`; conclusion `ε < |Δ ln Z|`; no box
  hypothesis is needed and none is stated.  `box_expected_queries_ge_mixed`: a finite
  mixture of `QueryAlgorithm`s (a class larger than decision trees), correct within `ε/2`
  with probability `1 − δ` on every member of the **full** box; pairwise disjoint sets, each
  dip-heavy or bump-heavy with strict inequalities; conclusion `(1 − 2δ)·#sets ≤ E|Q(r)|`.
  `detect_ge_of_proportional`: `bump = κ·dip` pointwise, `U, V > 0`; conclusion without the
  `½`.  `box_spotCheck_correct_of_proportional`: any class inside the box, `(1 − p)^N ≤ δ`.
  Nothing is added to the report's wording and one thing is missing from it: `U, V > 0` (m1).
  The step from `(1 − p)^N ≤ δ` to `N = ⌈ln(1/δ)/p⌉` is on paper (one line).

### 2.2 Proposition 11.18e [review]

* **Dimension.**  `ℝ^X = ⊕_U W_U`, `W_U` the functions of the sites of `U` that vanish when
  any of them is at the reference; `dim W_U = Π_{i∈U}(k_i − 1)`; the functions of order below
  `m` are `⊕_{|U|<m} W_U`.  **Unisolvence** of the ball around any reference: the anchored
  interpolant reproduces a function of order below `m` from its ball values and is itself
  of order below `m`.  **Closure:** mixed differences of order `m` of such functions vanish.
* **(a).**  On `Q(g)` with `|Q(g)| < N_ball` the evaluation map restricted to the
  `N_ball`-dimensional space has a kernel; `g + th` is indistinguishable from `g` for every
  `t`; the minimum goes to `−∞` and `ln Z` to `+∞`.  ✓ for adaptive algorithms, on every
  input.  **"Any unisolvent set does":** `g = I_{m−1}g + R`, `|R| ≤ C`; the values of `g` on a
  unisolvent `Q` determine `I_{m−1}g` up to `‖Λ_Q‖·C` (`Λ_Q` the interpolation operator of
  `Q`), so a finite bound follows — of a quality set by the Lebesgue constant of `Q`, which
  for the ball is explicit (the remainder identity).  ✓.
* **(c), the support lemma — proof [P].**  *Claim: a non-zero function `f` of order at most
  `d` on `Π[k_i]` is non-zero on at least the fraction `1/Π(d largest k_i)`.*  Induction on
  the number of sites; `d = 0` and one site are clear.  Let `f_s = f(·, x_n = s)`.  If no
  slice vanishes identically, each is a non-zero function of order at most `d` on the other
  sites and the bound for fewer sites is no smaller.  If some slice `f_{s₀} ≡ 0`, then every
  `f_s = f_s − f_{s₀}` has order at most `d − 1` (the difference kills the terms without
  `x_n`), one of them is non-zero, and the fraction is at least
  `(1/k_n)·1/Π(d − 1 largest of the others) ≥ 1/Π(d largest)`.  Attained by the indicator of
  a cylinder on the `d` largest sites.  ∎  The hinted count `⌈k^{m−1} ln(1/δ)⌉` follows.
* **(b).**  See M1.

### 2.3 Proposition 11.113 [review]

(a) `Σ_x q(x)W(x) = (Z(E) − Z(m₊))/(Z(m₋) − Z(m₊))`, the states with `m₋ = m₊` contributing
nothing.  (b) `π_{m₋}(x)(1 − e^{−(m₊ − m₋)}) = (e^{−m₋} − e^{−m₊})/Z(m₋)`; total `1 − Z(m₊)/Z(m₋)`.
(c) Hoeffding for `[0, 1]`; `2√(ln(2/δ)/(2N)) = √(2 ln(2/δ)/N)`.  Plain sampling: the variable
`e^{−(E − m₋)}` has range `max d`, and `(Z(m₋) − Z(m₊))/Z(m₋) = E_{π_{m₋}} d`: ratio of
half-widths `E d/max d`.  ✓.  The illustration: `√(2 ln 40/50 000) = 0.01215`, times
`e^{0.0605} − 1 = 0.06237`, is `7.58·10⁻⁴` in `Z/Z(m₊)`, an upper bound in nats; `4.89·10⁻³` at
`N = 1200`.  ✓.  (d): see M2.

### 2.4 Corollary 11.114 [review]

`ratio_core` is a linear programme with two vertices: minimise `αx + βy` over
`x + Ey ≥ E − 1`, `x, y ≥ 0` (`x = d_A/Z_A`, `y = b_B/Z_B`, `E = e^η`): the minimum is
`min(α(E − 1), β(1 − 1/E))` — "one macrostate alone moves".  The mass of the difference set
under the mixture is at least `¼(d_A/U_A + b_B/V_B)`, whence `½ min(p_A, p_B)`.  ✓.
(3): `Z(lo)/Z = Σ_M (W_M/Z)·W_M(lo)/W_M` and the same for `Z(hi)/Z`; more is true — a set
heavy for `ln Z` at level `ε` contains a set heavy for the ratio at level `ε` (if
`dip(D) > (e^ε − 1)(W_A + W_B)` then `dip_M(D ∩ M) > (e^ε − 1)W_M` for one `M`), so the packing
and fractional hitting numbers of the ratio dominate those of `ln Z` **[P]**.  The literal
sentence "the ratio costs at least as much as `ln Z`" is true in this sense (lower bound
against lower bound, spot check against spot check), not as a statement about the two
optimal costs.  Example: `e⁸ − 1 = 2979.96`; `10⁻⁶·2979.96 + (1 − 10⁻⁶)(e^{0.1} − 1) = 0.10815`.  ✓.
The last sentence (part (f) per macrostate): the first-order estimate errs by `K_A − K_B ∈
[−W(b_B, σ_B²), W(b_A, σ_A²)]`.  ✓.

### 2.5 Theorem 11.115(c)–(e) [review of the argument; Lean read only]

`cutCheck_sound`: the first step of the walk that leaves the union `S` of the inside
leaves lands in some leaf (the leaves cover the root box); not an inside leaf; not an
outside leaf, because the two ends of the step lie in an inside and an outside box and the
adjacency test holds for such a pair; hence a wall leaf, on which the kernel certifies
`L`.  Only "neighbours ⇒ test" is used.  The residual version returns **one** configuration
for all residuals (`∃ j, ∀ g`), and for the lower class; the height statement needs the
anchor value from above only.  This is what a barrier certificate must mean.

| Lean statement (read, not compiled) | what it says | wording of Theorem 11.115 | |
|---|---|---|---|
| `bverify_sound` | `bverify c I a b L = true` ⇒ for every `p`, `m` with `IsWalk SingleSite p m`, `p 0 = a`, `p m = b`: `∃ j ≤ m, L ≤ I.energy (p j)` (exact rationals; `SingleSite` = differ in at most one site) | (c) "every walk of single-site moves from `a` to `b` visits a configuration of energy at least `L`" | the same |
| `bverifyR_sound` | `∃ j ≤ m, ∀ g, ResidualLowerClass P g → L ≤ E₀(p j) + g(p j)` | (c) "of true energy at least `L` for every residual of the class" | Lean is stronger: one configuration for all residuals, and anchor values need only be lower bounds |
| `bverifyR_trap_height` | for an anchor `(a, v)` of the problem and a walk from `a`: `∃ j ≤ m, ∀ g, ResidualClass P g → L − (E₀(a) + v) ≤ (E₀ + g)(p j) − (E₀ + g)(p 0)` | (c) "the barrier is at least `L − (E₀(a) + v_a)` above an anchor `a` with evaluated value `v_a`" | the same |
| `bverifyRTop_sound` | acceptance ⇒ the published data are satisfiable (some residual is in the class) and the walk statement holds | not worded separately | adds the consistency check; nothing claimed beyond it |
| `bverifyOn_sound` | the same for walks whose steps move one site along a relation `G i` (Boolean, not assumed symmetric) | (e) | the same |
| `Dom.adjacent_iff` | for `n > 0`: `D.Adjacent D′ ⟺ ∃ x ∈ D, y ∈ D′, SingleSite x y` | (d) "iff both are non-empty and at most one site has disjoint domains" | the same, up to `n > 0` (m10) |
| `cutCheck_boxAdjacent_iff` | for `n > 0`: the cut check accepts ⟺ every wall leaf passes and no pair `x`, `y` with `SingleSite x y` lies in an inside and an outside leaf | (d) "the second check rejects exactly the trees with a move from an inside box to an outside box" | the same |

The library lemmas these rest on (`verify_sound`, `verify_sound_real`, `verifyR_sound_lower`,
`ResidualClass`, `ResidualLowerClass`, `RProblem.Consistent`) are in
`proofs/CertificateAlgebra.lean`, which is byte-identical in our tree and in the export.

---

## 3. Replication: my numbers next to theirs

All scripts were written from the statements before `<EXP>/experiments/falsify_conjectures.py`
was opened (it was opened at 03:37, after `r12_01`–`r12_06` had been written; see NOTES.md).

### 3.1 Box classes (`r12_01_box.py`, `r12_01b_twostage.py`)

| quantity | mine | theirs |
|---|---|---|
| packings | **exact** (DP over all subsets), `n = 6, 8, 10`, 720 cases; fractional hitting numbers by LP | greedy, 30 000 states, 12 cases (XXIV.9) |
| violations of: greedy floors; `detect_ge`; spot-check failure `≤ δ`; (e) upper end where no single state is heavy | **0** of 720 | 0 |
| exact detection probability / `p(η)` | min `1.0008`, max `379` | "between `p` and `2p`" holds for their linear relaxation; the exact value can be far above |
| worst exact failure of the spot check | `0.0496` (`δ = 0.05`) | — |
| centre of `[−3, 3]`, `ε = 0.2`, `δ = 0.05` | proportional `544`, general `1088`; exact failure of 544 samples `0.0379…0.0495`; `k = 83…86`; `(1 − 2δ)k = 74.7…77.4 ≤ 544 ≤ 2120…2196` | `544`, `1088` |
| rule without a hint | `N(0) = 545`; exact failure: two-level sup `0.9993·δ` (`v ≈ 2.998`), three-level random `0.9887·δ` | `545`; `worst_failure = 0.9942` (re-run) |
| floor of the constant box, `ε = 0.02` | `k_dip = 0`, `k_bump = 50`, `(1 − 2δ)k_bump = 45 > 25.1` | mutation `XXIV.9 M2` caught (re-run) |
| two-stage check (m2) | 1425 cases, 0 above the bound | — |

Monte Carlo of the spot check on one instance: miss frequency `0.00338` in 200 000 runs
against the exact `0.00312`.

### 3.2 The support lemma (`r12_02_support.py`)

Two exhaustive methods, both exact.  *Primal:* every maximal zero set contains `N_ball − 1`
independent points and, by the transitivity of state relabellings, may be taken to contain
the origin; for every `(N_ball − 2)`-subset of the other points the integer null vector is
computed by cofactors and its zeros are counted in integer arithmetic.  *Dual:* a non-zero
function of order at most `d` supported in `S` exists iff the principal submatrix
`(I − Π)[S, S]` of the complementary projector is singular; all `S` of size `s* − 1` through
the origin are tested (least eigenvalues found: `0.03–0.38`, against a threshold `10⁻¹¹`).

| | |
|---|---|
| grids | all 6 two-site and 10 three-site grids over `{2, 3, 4}`; 15 four-site grids; `(2,2,2,2,2)`, `(2,2,2,2,3)`; every order `d = 0, …, n` |
| cases done exhaustively | **128**; refutations of `s* = Π(n − d smallest k_i)`: **0** |
| largest | `(2,3,3,3)`, `d = 1`: 22 957 480 hyperplane candidates; `(2,2,3,4)`, `d = 1`: 10 737 573; `(2,2,2,2,3)`, `d = 2`: 10 737 573 principal minors |
| unequal alphabets | in 20 cases the least fraction is strictly above `k_max^{−(m−1)}` |
| **not done exhaustively** (17, too large) | `d = 1` on `(3,4,4)`, `(4,4,4)`, `(2,2,4,4)`, `(2,3,3,4)`, `(2,3,4,4)`; `d = 1` and `d = 2` on `(2,4,4,4)`, `(3,3,3,3)`, `(3,3,3,4)`, `(3,3,4,4)`, `(3,4,4,4)`, `(4,4,4,4)` — for these the proof of §2.2 stands, and a falsification attempt (`r12_02b_support_search.py`: random sparse integer combinations, hill climbing, sums and differences of two cylinders; 4 858 700 candidates in exact integer arithmetic) found **no support below `s*`** and attained `s*` in all 17 — evidence [N], not a proof |
| dimension and unisolvence | 101 grid × order cases: the span has dimension `N_ball` and the ball around **every** reference is unisolvent; the ball is one of many unisolvent sets (58 of the 70 four-subsets of the 3-cube for `d = 1`) |
| theirs (XI.20, re-run) | `cases = 106`, `thinnest = 1`; a spot test (one cylinder and four random sparse combinations per case; equal alphabets) |

### 3.3 The sandwich (`r12_04_sandwich.py`)

200 random sandwiches with 20–400 states and four width profiles: identity (a) to
`4·10⁻¹⁶`; rate and law of (b) exact; `E d/max d ≤ 1` always, median `0.012` when the sandwich
is wide only where the lower model is rare (the regime of our instance) and `0.19–0.50`
otherwise.  Coverage of the bracket (c): `1.0000` in 400 000 simulated runs (theirs: 1 miss
in 8000); exact for two-level `W`: least `0.99175` (at `N = 10`).  Bias: at most `2.5` standard
errors of the simulation.  Their `gain = 0.04442`.

### 3.4 Ratios (`r12_06_ratio.py`)

`ratio_core`: 0 violations in 111 300 random instances.  252 small cases, exhaustive over
subsets: exact detection probability over `½ min(p_A, p_B)`: min `1.25`, median `5.7`
(theirs: `closest = 1.002`); worst exact failure of the spot check `0.0228`;
`k(ln Z) ≤ k(ratio)` and `τ*(ln Z) ≤ τ*(ratio)` in every case.

### 3.5 Barrier instances (`r12_05_barrier.py`)

| instance | mine (own code, exact rationals) | Lean statement |
|---|---|---|
| `ferro` | barrier `111 ↔ 000` = `7/2` | `ferro_barrier_exact` |
| `maze` | energy table = the closed form; `E(0000) = E(1111) = 0`; barrier `1`; basin `{0000, 1000, 1100}`; `mazeCut` accepted by my own implementation of the three checks (adjacency decided by enumerating moves), its region is that basin, and `1 + 1/1000` is rejected | `maze_barrier_exact`, `maze_verified` |
| `maze`, box cuts | all 15 boxes around `0000` without `1111`, and the 15 around `1111`: the best bound a box cut certifies is `0`, the trivial one | `maze_boxCut_start_le`, `maze_boxCut_target_le` |
| `scan` | `5/2` with nearest-state moves, `0` with unrestricted moves; `scanCut` accepted on the product graph, rejected on the Hamming graph | `scan_barrier_exact`, `scan_hamming_rejected` |
| `ferroResidual` | the residual `g(x) = −(number of ones in x)/4` lies in the class and gives height exactly `13/4`: the bound is attained | `ferroWellR_trap` |
| empty leaf | accepted with the clause and with move enumeration; rejected with the literal criterion | `ferroEmptyLeaf_verified`, `ferroEmptyLeaf_literal_rejected` |

### 3.6 Re-runs (their code)

`r12_07_harness_rerun.sh`: the seven blocks in full mode, default seed, `-I -B`: all
`survived`, exit 0, at most 2.1 s each.  Statistics printed: XI.19 `identities = 14444`,
`strictly_smaller = 85`, `equal_binary = 154`, `sandwiches = 2796`; XI.20 `cases = 106`,
`thinnest = 1`; XXIV.6 `laws = 1599`; XXIV.7 `cube_sharp = 0.9995`; XXIV.8 `alternatives = 1775`,
`closest = 1.002`; XXIV.9 `near_floor = 4`, `members = 1200`, `worst_failure = 0.9942`;
XXIV.10 `runs = 8000`, `misses = 1`.  (THY-RES-0010 §1 quotes "attained to `0.3 %` at the
additive instance with `u = 0.05`" for XXIV.7; the harness prints only the best ratio,
`0.9995`; from the closed form in the block's own description,
`D_p/n = [ln cosh(pu/2) − p ln cosh(u/2)]/(p − 1)` against `(p − 1)u²/8 + L(u)`, the
deficits at `u = 0.05` are `0.047 %`, `0.071 %`, `0.217 %` for `p = 1.5, 2, 4` — my arithmetic
(`r12_10_arithmetic.py`); the quoted figure comes out.)  `r12_07b_mutations.sh`: their mutation driver, group
XXIV: **41 mutations, 41 caught**, 11 baselines as expected (the report says "with 41
mutations"); `XXIV.9 M2` — "the two-sided statement with the packing number of the dips
alone (the first version of the theorem)" — is caught.  Group XI: **56 mutations, 56
caught**, 21 baselines as expected, among them the four of XI.19 and the four of XI.20.
(The driver writes one scratch copy of the harness; its temporary directory was pointed
into this workstream's directory and removed afterwards.)
`r12_08_lean_boxclass.sh`: a copy of `BoxClass.lean` (first 513 lines identical to the
export, twelve `#print axioms` lines appended) compiles against **our** tree, whose
`QueryLowerBound.lean` is byte-identical to theirs: exit 0, 31.6 s; all twelve statements
depend on `propext`, `Classical.choice`, `Quot.sound` only.

### 3.7 Machine-checked here (`lean/R12Additions.lean`, `r12_09_lean_additions.sh`)

A file of my own (505 lines, imports Mathlib only, namespace `ScienceR12`, not part of
any library; their definitions `Box`, `Zw`, `dip`, `bump`, `bumpAlt`, `restr`, `logRatio`
and five of their lemmas are copied into it, with their proofs, because `BoxClass.lean`
and `BoxRatio.lean` are not modules of our tree).  `lake env lean`: exit 0, 9 s, no
warning, no `sorry`; each of the seven statements below depends on `propext`,
`Classical.choice`, `Quot.sound` only.

| declaration | statement | used in |
|---|---|---|
| `detect_ge_at_floor`, `detect_ge_at_ceiling` | if the total dip (bump) weight at `r` is zero, a member whose `ln Z` differs by more than `η ≥ 0` differs from `r` on a set of mass at least `(1 − e^{−η})Z/V` under `bump/V` (at least `(e^η − 1)Z/U` under `dip/U`) | m1 |
| `detect_ge_weighted` | the sampler `λ·dip/U + (1 − λ)·bump/V`, `0 ≤ λ ≤ 1`, detects with probability at least `min(λ(e^η − 1)Z/U, (1 − λ)(1 − e^{−η})Z/V)` | m3 |
| `weighted_opt` | at `λ = A/(A + B)` both terms are `1/(A + B)` | m3 |
| `logRatio_bumpAlt_lt`, `logRatio_bumpAlt_gt` | raising to the ceiling on a set that avoids one macrostate, with bump weight above `(1 − e^{−ε})` times the weight of the other, moves `ln(Z_A/Z_B)` by more than `ε` | m5 |
| `affine_half_large` | an affine function on `{−1, 1}^n` is at least `1/(n + 1)` of its value at any given point, in absolute value, on at least half of the points | M1 |

---

## 4. The barrier certificates against our formats; our own lemma

**What our texts claimed.**  SK_REPORT §2.5, check (2): "two boxes `D, D′` are adjacent iff
`#{i : D_i ∩ D′_i = ∅} ≤ 1`"; §7, T1: "The only new lemma is 'two boxes contain a pair of
configurations that differ in at most one site iff at most one coordinate has disjoint
domains'"; SCI-MSG-0005 §5 and §7 (K-T1), the same.

**Is it false?**  Yes, in the direction "criterion ⇒ neighbours", and only for empty
boxes.  By brute force over **all** ordered pairs of boxes with arbitrary domains (the
empty one included) on nine grids from `(n, k) = (1, 1)` to `(4, 2)` and `(2, 4)` (up to 65 536
pairs): "neighbours ⇒ criterion" never fails; "criterion ⇒ neighbours" fails
`3, 7, 15, 6, 98, 1110, 1029, 10850, 9604` times and **never when both boxes are non-empty**;
with their non-emptiness clause the equivalence holds in every pair (their
`Dom.adjacent_iff`, for at least one site).  Their witness (`∅ × {0}` against `{0} × {0}`)
is one of these.  The coordinator has already put a head note on SCI-MSG-0005 and a
linked correction in SCI-RES-0011 §4, which leaves to this workstream the question:

**Did anything of ours use the false direction?**  No.  Checked: (1) the soundness
statements of SK_REPORT §2.5 and §2.8 use "neighbours ⇒ criterion" only; (2) "the format
is complete (full tree)": the leaves of the full tree are single configurations, where the
criterion is exact; (3) the cost `O(ℓ²nk)` is unaffected; (4) the numerics T11
(`t11_cut_size.py`) grow boxes around enumerated wall points and never use the criterion;
(5) our Lean file contains no adjacency lemma — the tree checker was "specified, not
formalised".  The only effect of the literal criterion is a **false rejection** of a valid
certificate that has an empty leaf; their `ferroEmptyLeaf_literal_rejected` shows one and
my own checker reproduces it.  An empty leaf needs their `split` node (a list disjoint
from the current domain) or a root box with an empty domain: in our own format — `branch`
nodes only, with the kernel's convention of one child per state of the *current* domain,
below the full box — every leaf box is non-empty, so on our trees the literal test would
have been exact.  The lemma as we stated it, for arbitrary boxes, is false all the same.

**Their format against ours.**  Three differences.  (i) The clause, above.  (ii) A `split`
node (`split i T yes no`: the states of site `i` listed in `T`, and the others); our
`branch` is kept; soundness needs only that the leaves cover the root box
(`CutTree.leaves_cover`), and they also prove that the leaves partition it.  (iii) The
checker is generic in the wall kernel and the move graph, so the residual version and the
site-graph version come from the same proof; on a site-graph product their `AdjacentOn`
("some site has an edge between the two domains and every other site shares a state")
agrees with our "the one disjoint coordinate has a `G_i`-edge" on leaves, which are
disjoint.  Their statements are those we asked for in K-T1, and stronger in two places:
one configuration serves all residuals, and the lower class suffices.

**The copy of our file.**  `diff` of `experiments/science/ws_K/KineticsCertificates.lean`
(639 lines, SHA-256 `fc9c7f28e5ad5fec806c8d80…`, identical at `25626db`, `a841cb4` and our
head) against `<EXP>/proofs/Frontiers/KineticsCertificates.lean` (612 lines): exactly two
hunks — lines 32–33 (the sentence that the file is not part of the library, and the check
command) replaced by a nine-line provenance paragraph; lines 606–639 (a blank line, a
heading and the 32 `#print axioms` commands) removed.  Nothing else.  The hash they quote
is ours.

---

## 5. What each item means for our certified free energy (SCI-MSG-0020)

*Theorem 11.110(e).*  Our sandwich is a box with floor `m₋` and ceiling `m₊`, and it is
narrow: `Δ = 0.0605`, so both cost numbers are at most `e^Δ − 1 = 0.062`.  Arithmetic on our
reported numbers, not a run (`δ = 0.05`; `r12_10_arithmetic.py`): to verify a claimed energy function inside the
sandwich to a bracket of width `5·10⁻³` nats takes at most
`ln 20·2·0.0624/(e^{0.0025} − 1) ≈ 150` evaluations at any instance, and at least
`(1 − 2δ)·6 ≈ 5` at an instance near the ceiling `m₊` — against 1200 without a hint
(Proposition 11.113) and the 50 000 we used.  A hint in this sense is a complete candidate
energy table, which we do not have; the numbers are a benchmark.
*Proposition 11.18e.*  The 87 441 evaluations of the ball (`Σ_{j<5} C(20, j)2^j`) cannot be
undercut by any deterministic certificate on the class "order-5 constants given, lower
orders free", nor — for a bracket of useful width — plausibly by a randomised one; M1 shows
only that a useless bound is cheap.  The ways out are those the proposition names: bounds
on the lower-order terms known in advance (which for us would have to be certified, e.g.
the decay of `d_U` with distance along the chain), a lower order, or another expansion.
*Proposition 11.113.*  Parts (a)–(c) are right and are the sampler our sandwich calls for;
the predicted width `7.6·10⁻⁴` from 50 000 evaluations is correct arithmetic, and the
bracket must be clipped to the deterministic one (m7).  M2 changes nothing at our `Δ`.
*Corollary 11.114.*  For a ratio of two macrostates of our instance the sandwich
restricted to each macrostate is again a sandwich; the cost is set by each macrostate's
own width and not by its weight, provided `π_{m₋}` can be sampled conditionally on the
macrostate — which the transfer matrix does for macrostates defined by the states of a
few residues.  *Theorem 11.115.*  Nothing of ours changes.  Applied to `m₋` (pairwise,
banded), their tree checker would certify that every walk from `a` to `b` visits `E ≥ L`,
and a height `L − E(a)` above an evaluated `a`: a certified trap statement for the real
energy, given the sandwich.  Not done.  *Theorem 11.18d.*  The machine-checked core of the
certificate, twice (theirs and ours); the rest of the chain is on paper.

---

## 6. Requests to the theory division (can be sent as they stand)

* **R12-T1 (Proposition 11.18e(b)).**  Replace part (b) by the text of M1, or withdraw it:
  as written it is false — on the cube with `m = 2`, `⌈log₂(1/δ)⌉` uniformly random
  evaluations return a valid finite lower bound for the minimum and a valid finite bracket
  for `ln Z` with probability `1 − δ` on every member of the class, against `N_ball = n + 1`.
  Proof and exact numbers: R12_REPORT §1 M1, `r12_03_randomised.py`.  If the statement meant
  is for a bracket of prescribed width, say so and mark it [C].  The same sentence is in
  THY-RES-0010 §4.
* **R12-T2 (Proposition 11.113(d)).**  Replace by the text of M2: the order
  `(e^Δ − 1)²/ε²` is sufficient and not necessary; the worst-case order without a hint is
  `(e^Δ − 1)²/(e^Δ ε²)` and the hint is worth `(1 − e^{−Δ})/ε`.  Table: R12_REPORT §1 M2.
* **R12-T3 (Theorem 11.110).**  (i) State `U, V > 0` in (c) and the one-sided sampler when
  one of them vanishes; the two lemmas for that case — exactly where the correction
  applies, at the floor — are machine-checked on your definitions in
  `experiments/science/ws_R12/lean/R12Additions.lean` (`detect_ge_at_floor`,
  `detect_ge_at_ceiling`) and are yours to take.  (ii) The hypothesis of (e) can be dropped
  from the display by the two-stage check of m2.  (iii) With the mixture weights of m3 the
  sample size is `⌈ln(1/δ)·max(1, A + B)⌉` (`detect_ge_weighted`, `weighted_opt`, same
  file).  (iv) Qualify the `Θ` in the summary row and in THY-RES-0010 §1 as in m4.
  (v) `BLUEPRINT.md` §6.4: restore the hypothesis in the lower-bound line and remove "The
  ceiling and the number of states do not enter" (m11).
* **R12-T4 (Corollary 11.114).**  Give (d) both terms, as in m5, and add the bump
  alternative for one macrostate to `BoxRatio.lean` (raising to the ceiling on a set inside
  `A` that avoids `B`, with bump weight above `(1 − e^{−ε})W_A`, lowers the log-ratio by more
  than `ε`): `logRatio_bumpAlt_lt`, `logRatio_bumpAlt_gt` in our `R12Additions.lean` are
  stated on your definitions and compile.  Correct the docstring ("Corollary 11.113"); say
  that (a), (b) need `U_M, V_M > 0` and do not need disjointness; remove the three sentences
  that still say ratios are not covered (m11).
* **R12-T5 (Proposition 11.18e(c)).**  State the bound for unequal alphabets,
  `1/Π(m − 1 largest k_i)`, with the proof of §2.2; it was found exact in 128 exhaustive
  cases (`r12_02_support.py`).
* **R12-T6 (wording).**  Theorem 11.18d: attribute (b) and (d) as in m9(i); mark the
  equality clause of (c) and the two-state coincidence as on paper.  Proposition 11.113(c):
  "intersected with the deterministic bracket" (m7).  Theorem 11.115(d): "on at least one
  site" (m10).  THY-RES-0010 §2: the 85 sets are three-state sets (m9(vi)).

---

## 7. How to re-run

From `/home/user/MetricChain/experiments/science/ws_R12/`, with
`export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`; one command per script; every log cited
here contains the script's last line (`R12_…_DONE`), followed for the Python scripts by
the three lines of `time`; no log of an interrupted run is cited.

| command | log | wall time | what |
|---|---|---|---|
| `python3 -B r12_01_box.py` | `logs/r12_01_box.log` | 15.6 s | box classes: exact packings, spot check, centre, floor, rule without a hint |
| `python3 -B r12_01b_twostage.py` | `logs/r12_01b_twostage.log` | 1.9 s | the two-stage check (m2) |
| `python3 -B r12_02_support.py` | `logs/r12_02_support.log` | 8 min 41 s | dimension, unisolvence, support lemma by brute force |
| `python3 -B r12_02b_support_search.py` | `logs/r12_02b_support_search.log` | 1 min 20 s | the 17 large cases of the support lemma: falsification attempt |
| `python3 -B r12_03_randomised.py` | `logs/r12_03_randomised.log` | 20.7 s | counter-algorithm to 11.18e(b); hinted refutation (c) |
| `python3 -B r12_04_sandwich.py` | `logs/r12_04_sandwich.log` | 18.4 s | Proposition 11.113 |
| `python3 -B r12_05_barrier.py` | `logs/r12_05_barrier.log` | 0.6 s | adjacency lemma; barrier instances |
| `python3 -B r12_06_ratio.py` | `logs/r12_06_ratio.log` | 8.6 s | Corollary 11.114 |
| `bash r12_07_harness_rerun.sh` | `logs/r12_07_harness_rerun.log` | 8 s | their harness, seven blocks |
| `bash r12_07b_mutations.sh` | `logs/r12_07b_mutations.log` | 39 s + 3 min 2 s | their mutation driver, groups XXIV and XI |
| `bash r12_08_lean_boxclass.sh` | `logs/r12_08_lean_boxclass.log` | 31.6 s | `lake env lean` on a copy of `BoxClass.lean` |
| `bash r12_09_lean_additions.sh` | `logs/r12_09_lean_additions.log` | 9 s | `lake env lean` on `lean/R12Additions.lean` (my own statements) |
| `python3 -B r12_10_arithmetic.py` | `logs/r12_10_arithmetic.log` | 0.02 s | the arithmetic quoted in §2 and §5 (`L(3.7)`, `544/1088/545`, the "0.3 %", our sandwich, `87 441`) |

Python 3.13 with numpy and scipy; seeds fixed in the scripts.  The Lean copy is
`lean/BoxClass_copy_9408e33.lean`.  No `lake build`, no git command that changes state, no
file written outside `experiments/science/ws_R12/` and this report.

---

## 8. Not checked

* **Lean.**  `BoxRatio.lean` and `BarrierCertificate.lean` were read in full and **not
  compiled** (their imports are not modules of our tree); `AnchoredRemainder.lean` was read
  and not compiled by me (the coordinator did).  No proof term was inspected beyond
  reading; the audit of the whole library at `9408e33` is a separate job.  Of my own
  proposals, the two-stage check (m2), the explicit `Θ` constants (m4), the support lemma
  (§2.2), the cube constant for `m > 2` and the `KL` count of M2 are **on paper** (with the
  numerical checks stated); only the seven statements of §3.7 are machine-checked.
* **Support lemma:** 17 grid × order cases too large for exhaustive search (listed in
  §3.2); for them the proof stands, with a random search that found nothing.
* **Proposition 11.18e(b)** under the reading "bracket of prescribed width": neither
  proved nor refuted.  The constant `c(grid, m)` of M1 is explicit only on the cube; for
  three and four states its existence is by compactness and it was not computed.
* **Proposition 11.113(d):** the lower bound of order `(e^Δ − 1)²/(e^Δ ε²)` is a two-point
  sketch for algorithms that evaluate at points drawn from a fine-grained `q`; I did not
  write it out for adaptive algorithms in the query model.  Hoeffding's Theorem 1 in
  Kullback–Leibler form is quoted from memory (no source opened).
* **Theorem 11.110(b):** the count `e^{S(π)(1+o(1))}`; **(f)**: nothing beyond the Chebyshev
  step (the inequality is machine-checked on our side).  Corollary 11.111 and Proposition
  11.112 were not under review (of XXIV.7 only the quoted "0.3 %" was checked, §3.6).
  The sentence of Theorem 11.18d(d) that relates the case `m = 3` to Theorem 11.18a was
  not checked.
* **Theorem 11.115:** parts (a), (b), (f) are our own statements and were not re-reviewed;
  the weight-domain paragraph (K-T2) was not examined; no certificate was produced for an
  instance of ours.
* **Mutation tests:** only the groups XXIV and XI of their driver were run, in its quick
  mode, as the driver does; the mutations themselves were not reviewed.
* The true optimal cost `min_alg E|Q(r)|` was not computed for any instance; it is
  bracketed by packing and hitting numbers throughout.
* No prior-art search was made (not asked); nothing is claimed new.

---

## 9. Own errors

* `r12_04_sandwich.py` crashed in its first run (part 4 formatted `None` when `Δ < ε` makes
  the deterministic bracket sufficient).  Fixed; re-run; the log of the crashed run was
  overwritten and is not cited.
* The first entry of NOTES.md gives guessed clock times ("03:10–03:30"); the machine clock
  read 03:12 when that reading was finished.  Corrected in the notes; later times are from
  `date -u`.
* In `r12_01_box.py` the flag `single` is `True` when a single state **is** heavy (the
  hypothesis of (e) fails); the summary line prints the count of cases in which the
  hypothesis holds (138 of 720).  The naming is confusing; the numbers are right.
* The first version of `r12_01b_twostage.py` printed, untested, that the 839 cases in which
  the one-stage `N` exceeds the bound all have a heavy single state.  The script now counts
  the exceptions (0) and was re-run; all other numbers are unchanged.  The log cited is of
  the re-run.
* A first draft of m4 said that the README displays the `Θ` formula; it does not (it
  states the result in words).  Corrected before the report was finished.
* The Lean file of §3.7 compiled at the first attempt; a second version used the
  deprecated tactic `push_neg` (three warnings), replaced by `push Not`; the log cited is
  of the final file.

---

## Coordinator's note (2026-11-26, before publication as SCI-REV-0013)

1. **Read in full by the coordinator**, and the two sentences under review read in the
   theory report at `9408e33` (Proposition 11.18e, lines 2390–2420; Proposition 11.113(d)):
   they are quoted correctly, with their own labels ("(b) P-sketch"; "[K] … from memory").
2. **M1 re-derived and recomputed** (`experiments/science/pi_inference/r12_adoption_check.py`,
   written from the statement; none of the workstream's code imported).  The pairing
   argument on the cube is three lines and is right.  By exact enumeration on 3 834 affine
   functions (`n = 4 … 14`; random, sparse heavy-tailed, extremal and near-tied) the least
   fraction of points with `|h| ≥ ‖h‖_∞/(n + 1)` is exactly `0.5`.  End to end at `δ = 0.05`,
   `q = 5`: on the extremal member `h = 1 + s₁` the algorithm fails with probability exactly
   `2⁻⁵ = 0.031`; on random members with a remainder `|R| ≤ 0.7`: 9, 0, 0 invalid bounds in
   20 000 runs at `n = 8, 12, 16` (the claimed lower bound there: 8.55, 12.35, 16.15
   evaluations).
3. **M2 derived independently before the report was read** (research log, cycle 48): with
   `Z = Z₊(1 + aw)`, `a = e^Δ − 1`, relative accuracy `ε` and `Var W ≤ w(1 − w)`, the worst mean
   is `w = 1/(a + 2)` and the count is `2 ln(2/δ) sinh²(Δ/2)/ε² = ln(2/δ)(e^Δ − 1)²/(2e^Δε²)` — the
   workstream's `N_KL`.  Exact binomial failure of the plug-in estimate on two-level members
   with that many samples: at most `0.0073` for `Δ = 0.06 … 5`; with a quarter of it
   `0.18–0.23`, with a sixteenth `0.53–0.65`.  So for this estimator the necessary number is
   within a factor four of `N_KL`, and the count of (d) is too large by `e^Δ`.  (The lower
   bound for *all* algorithms is a sketch in the report, as it says.)
4. **Compiled by the coordinator:** `ws_R12/lean/R12Additions.lean` (510 lines — the report
   says 505; sha256 `ef6481c4…a8afc495`) with `lake env lean`: exit 0, 9 s, no `sorry`, `admit`,
   `native_decide`, `axiom`, `unsafe`; the seven statements depend on `propext`,
   `Classical.choice`, `Quot.sound`.  `affine_half_large` read: it says what §3.7 says.
5. **Re-run from a clean copy:** `r12_03_randomised.py`, `r12_04_sandwich.py` — outputs
   identical to the cited logs except the line with the elapsed time.
6. **Not checked by the coordinator:** the support lemma's exhaustive search (the proof by
   induction in §2.2 was read and is right); the box-class replication; the ratio and
   barrier replications; the re-runs of the theory division's harness and mutation driver;
   the reading of `BoxRatio.lean` and `BarrierCertificate.lean`.  The theory division's
   whole audit at `9408e33`, which builds those two files, passes on this machine
   (`INDEPENDENT_VALIDATION.md` §1.7).
