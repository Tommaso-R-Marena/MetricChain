# Adversarial review of `HIERARCHY_REPORT.md`

*Reviewer: an independent AI session (subagent), 2026-11-28, following `HIERARCHY_review_brief.md`.
Reviewed file: `docs/phase2_hierarchy/HIERARCHY_REPORT.md` as of 02:43 UTC (50 242 bytes,
sha256 `9687866b…73adf7`).  `docs/THEORY_REPORT.md` was not read; of the archive only
`docs/workstreams/U_REPORT.md` §2 was read.  All code is my own (`experiments/phase2_hierarchy/review/`);
the author's scripts `h1_…`, `h3_…` were read, not imported.  No existing file was modified, no
state-changing git command was run, every run stayed under ten minutes on the local container.
Files that appeared in the repository while this review was running (`HIERARCHY_ADDENDUM.md`,
`h7`–`h12`, Lean files) are **not** covered.*

---

## 0. Verdict

| item | result |
|---|---|
| 1. Lemma B, facts (F1)–(F4), (R) | **No error found.**  Proof checked line by line; (F1)–(F4), (R) checked exactly; the lemma could not be refuted on about 6 000 exact extremal functions *with parity-dependent profiles* (largest excess `+0.89` nats against allowances of 36–146). |
| 2. Theorem H1, Algorithm R3 | **No error found.**  Proof checked; R3 implemented literally on real cubes (`n ≤ 20`): candidates, exact and statistical unbiasedness, exactness when all blocks are revealed, the path argument (with parity), the cost bound — all pass.  One overstatement in §0 (minor, m1). |
| 3. Lemma A2, Theorem H2 | **No error found.**  Both anchors and the case analysis are correct; `Ξ` is nonincreasing (strictly decreasing above its minimum `−φ₂Λ₁`); the use of Theorem 11.86 is legitimate.  The exact extremal hidden gain changes sign at `ϑ(φ₁)` and follows `n·min{Ξ, φ₂k(y¹)}` within about 2 nats. |
| 4. Corollary H4, Propositions G, C | Statements are what the proofs give, **but** (M1) the barrier is announced for more than Lemma B covers, and (M2, M3) Propositions G and C are proved only as non-strict inequalities, which do not by themselves support "no separation"/"cells do not help"; both gaps are closed below. |
| 5. §0, §8, §10 | Overstatements listed under M1, m1, m2, m3, m8. |

**Critical findings: none.  Major: 3.  Minor: 9.**

---

## 1. Findings

### Critical
None.

### Major

**M1. The barrier is stated for "any number of blocks" / "every member of every `BR_m`"; what is proved needs
`m ln n = o(n)` and blocks of size `≥ N_u`, and concerns one proof device only.**

*Place.*  §0, table row "Barrier" ("for any `u`, any number of blocks, any split … Lemma B applies to every
member of every `BR_m`"); §6, Corollary H4, last sentence ("every slope, every number of blocks, every split,
every profile"); §8 "Evidence" ("every hard family that the known technique can analyse").

*Reason.*  Lemma B assumes `n_j ≥ N_u` for every block and loses `m(u + 5 ln(n+1))`; the conclusion of H4 is
`A(F_D)/A(F_S) ≤ 1 + (n+1)^m e^{m(u+5L) − (Θ − nh)}`, which is empty as soon as `m ln n` is not `o(n)`.  This is
not a technicality.  With singleton blocks `BR_n = L_u` exactly (every `ψ ∈ L_u` is `ψ_{F,s}` with
`F = ψ(· ⊕ s)`), and with blocks of bounded size the class is of the same nature; a hard three-round family
living on `≳ n/ln n` blocks is excluded by nothing in the report (R3 itself costs `(n+1)^m` there, Remark (3) of
§4 says so).  Secondly, H4 is a statement about Lemma 11.85 (= Lemma U2), in which batch `t` is *handed* the
centres — hence also the blocks — of all earlier levels.  A hiding argument for a hidden partition in which an
earlier batch cannot target shells (the report's own open problem 1) is not an instance, so "no argument that
hides centres of a block-radial energy" (§0) is too wide.

*Repair.*  State H4 and the §0 row as: "for every fixed `m` (more generally `m ln n = o(n)`), blocks of size
`≥ N_u`, every `θ > h`, and every application of Lemma 11.85 with `p_t ≤ e^{−nθ+o(n)}`:
`|ln A(F_D) − ln A(F_S)| ≤ ln(1 + (n+1)^m e^{m(u+5L) − (Θ−nh)}) → 0`, `Θ = nθ − o(n)`."  Under these hypotheses
the deduction is correct; I checked it against Lemma U2: `p_t ≤ e^{−nθ+o(n)}` *forces* `𝒲_t ⊇ V_{<t}(nθ − o(n))`
(a single type outside `𝒲_t` contributes its conditional probability to `p_t`), so (H1), (H2) hold for `r ≥ 3`;
the types where the twins differ lie outside `V_{P∪Q}(Θ)`; and the other direction follows because `F_S = F_D`
on the `𝒲_t`.  The corollary's "`≤ O(log n)`" should read "`→ 0`": that is what the proof gives and what "there
is no gap" needs at bounded accuracy.

**M2. Proposition G gives only "`≤ M`"; the conclusion drawn from it needs a strict margin for `θ > ¼`, which
the report has only numerically.**

*Place.*  §7.1, statement and last lines of the proof ("So `G₀ ≥ 0`"), then "*What this says* … no flag …
separates three or more rounds from `h`"; §0 row "Beyond blocks (i)".

*Reason.*  In an exponent-level model, "hidden mass exponent `≤` visible mass exponent" does not exclude a gap
(equal exponents allow any sub-exponential ratio).  The case `y* ≤ b` has the margin `1 − 2√θ`; the case
`y* > b` is reduced to `θ = ¼` by monotonicity and ends with `G₀ ≥ 0`, i.e. with no margin.  The sentence
"for `θ > ¼` the minimum of the bracket is `2√θ − 1`" is [N] only.  (The algebra itself is right: the anchor is
in `D`, `b ≥ θ/ρ`, the bracket is nondecreasing in `θ` on `[¼, ρ²]`, the expansion, `c₀`, `c₂`, the
factorisation `16ρ⁴(4c₀ − c₂²) = −(2ρ−1)³(16ρ³−8ρ²−6ρ−1)` and the sign of the cubic on `[½, cos(π/8)]` were
verified symbolically and on grids, `r5_propG_propC.py G`.)

*Repair (closed).*  With `s = 2√θ ≥ 1`, `Δ = sΔ′`, `ρ = sρ′` (`ρ′ ≥ ½`) and `R = √(Δ′² + (ρ′−½)²)`:

    Δ² + 2θΔ/ρ + ρ² − 2√(Δ² + (ρ−√θ)²)  =  s²·G₀(Δ′, ρ′) + 2s(s−1)·R .

Both terms are `≥ 0`.  If `R ≥ 1/16` the second is `≥ s(s−1)/8`; if `R < 1/16` then `G₀ ≥ ρ′² − 2R ≥ ⅛` and the
first is `≥ s²/8`.  Hence the bracket is `≥ s(s−1)/8 = √θ(2√θ−1)/4`; the first case has the margin `2√θ − 1`
(`θ ≤ 1`) or `θ` (`θ > 1`), both larger.  So for every `θ > ¼` every type with `|Y*_r| ≥ √θ` has exponent
`≤ M − √θ(2√θ−1)/4` (numerically the sharp margin is `2√θ − 1` for `θ ≤ 1`, as the report says).
The identity was checked numerically (error `6·10⁻¹⁴`), and so was the bound: on grids the minimum of the
bracket is `2√θ − 1` for `θ ≤ 1` and `θ` for `θ > 1`, at least `2.5` times `s(s−1)/8` (`r5b_margins_check.py`).  Two side remarks: `G₀` vanishes not only at
`(Δ, ρ) = (0, 1)` but also at `(½, ½)`; and "levels of any dimension" is not what is written (levels are
scalars) — the proof does extend verbatim with `y, q, w` replaced by norms and the anchor taken radially.

**M3. Proposition C: one sub-case of the proof has no margin for `θ > h`, so "cells do not help" does not
follow from the proof as written.**

*Place.*  §7.2, proof, case "*If `x ≤ R`*" when `T` is not relaxed (`r_T(y) ≤ θ − x − r_Q(e)`); the sentence
"So the dilution `R` … is paid back exactly"; §0 row "Beyond blocks (ii)".

*Reason.*  The two cases are correct as inequalities (checked on 198 711 random hidden types: the anchors are
in the required regions, the bound is never positive, `r5_propG_propC.py C1`).  But in the sub-case named above
the bound is `m_vis − r_T(y) − Σ_{P∪Q} φ_j g_j` with `g_j = f(y_j)` for `y_j ≥ κ` and `k(y_j)` otherwise, and this
is `m_vis` exactly — for *every* `θ` — at `y_j = p_u` on a group `G ⊂ P ∪ Q` with `φ_G a > θ`, `y_j = ½`
elsewhere, `R > θ` (9 100 such random instances with `θ > h`).  The other three sub-cases have the margin
`θ − h`.  As in M2, equality of exponents does not exclude a gap.

*Repair (closed).*  Let `δ = θ − h > 0` and `ζ ∈ [p_u, κ)` with `f(ζ) = min{a, h + δ/2}`.  If `r_T(y) ≥ δ/4` the
report's bound already has the margin `δ/4`.  Otherwise take the anchor `e′_j = max(y_j, ζ)` on `P ∪ Q`,
`e′_T = y_T`: `r(e′) ≤ h + 3δ/4 < θ`, so `e′ ∈ 𝒲₁` and `U_D(e′) = U(e′_P, ½, ½) ≤ m_vis + (r_P(e′) − R)₊`.
`R < r_P(e′) ≤ h + δ/2` is impossible (then `y ∉ 𝒲₃` would force `r_T(y) > θ − R > δ/2`).  So the cap is `m_vis`
and

    U_D(y) − r(y) ≤ m_vis − r_T(y) − Σ_{P∪Q: y_j ≥ ζ} φ_j f(y_j) − Σ_{P∪Q: y_j < ζ} φ_j [k(y_j) + u(κ − ζ)] .

Since `r(y) > θ` and `r_T(y) < δ/4`, either the first sum is `≥ h/2` or the blocks with `y_j < ζ` have weight
`≥ h/(2 ln 2)`.  Hence for `θ > h`:  `max_{y∉𝒲₃}[U_D(y) − r(y)] ≤ m_vis − min{δ/4, h/2, u(κ−ζ)h/(2 ln 2)}`.
(Checked on 54 155 random hidden types of this sub-case: the new anchor is always in `𝒲₁` with cap `m_vis`, and
the margin is never below the claimed one, `r5b_margins_check.py`.)
*Independent numerical confirmation at finite slope* (the author's check is in the small-slope limit only):
on grids, with my own shortest-path code, the true extremal hidden gain of the cell model is at most
`D(θ)` plus one grid step, `D(θ) = u f⁻¹(θ) − Λ₁ ≤ h − θ` being the plain-dip value (so: at most one grid step
at `θ = h`, and about `D(θ) < 0` at `θ = 1.2h, 1.6h`, attained for `R ≳ θ`), in all 432 parameter sets, 354 of
which have hidden types (`u = 1, 4`; nine block/role patterns; `R/θ` from 0 to 50), `r5_propG_propC.py C2`.

### Minor

**m1. §0, row H1: "every partition into `m` blocks".**  Theorem H1 requires all blocks `≥ N_u`.  Easy repair:
enumerate the `≤ 2^{mN_u}` patterns of the small blocks and run R3 on each restriction (block-radial on the
large blocks, same three rounds, constant factor), or keep the hypothesis in §0.

**m2. Corollary H3, last sentence, and §0/§10 "exactly three levels".**  For a fixed class there may be only
two levels: by Theorem H2 itself `c_2 = h` whenever `min(φ₁, φ₂) ≥ 1 − h/a`, which the equal split satisfies as
soon as `h/a ≥ ½` (`u ≳ 6.1`; I get `c_2/h = 1.000` at `u = 8, 12`, `φ₁ = ½`).  For `m ≥ 3` the value
`c_2(BR_m)` is not determined (§5, [C]), and for large `u` with equal blocks no grouping gives a threshold above
`h`.  Correct as "for splits with `min φ < 1 − h/a`" or "supremum over splits".

**m3. §3 "Exact check" and §0 row Lemma B.**  The author's 124 cases (a) contain no parity-dependent profile and
(b) all use `Θ = θnh`, `θ/h ≤ 1.3`, which is *below* the lemma's own hypothesis `Θ ≥ nh + 2mL` at these sizes
(they test a stronger statement, which is fine but should be said).  My exact extremal functions reproduce the
author's table to `5·10⁻⁴` nats on the 39 rows compared, and parity raises the excess by at most `0.16` nats.

**m4. §6 table, fifth digits.**  `θ₂*(2) = 0.12918` (report: `0.12916`), `θ₂*(4) = 0.29415` (report: `0.29417`);
`θ₂*/a` at `u = 2` is `0.39408` (report: `0.3940`); at `u = 0.05` I get `0.3461` (report: `0.3460`).  The other
printed digits of `θ₂*/a` and all best `φ₁` are reproduced.

**m5. §1 "their cost is a deterministic number".**  The number of evaluations of R3/R2 depends on `S₁, S₂`; only
the bound `3(n+1)^{m+1}M` is deterministic.

**m6. Corollary H4 wording** — "`≤ O(log n)`" should be "`→ 0`" (see M1).

**m7. §8, item 7 ("holds verbatim … `γ(e) ≤ γ(y) + n·t(κ)/n`").**  Typo, and the list is incomplete: the proof of
Lemma B also uses the reflection symmetry and unimodality of `t`, `t(w) = O(L)` at near-typical radii of *both*
parities, and jumps of `t` of size `≤ L`.

**m8. §10 "complete finite-`n` proof" of H1; Theorem H2(b).**  Lemma B is finite-`n` with explicit constants; H1
is asymptotic with an unspecified `n₀(u, m, η, ε, δ)` and fixed `m`.  H2(b) inherits `δ < ½` and `n₁ = ⌊φ₁n⌋`
from Theorem 11.86; for "`n_j/n → φ_j`" one needs its `n₀` locally uniform in `φ₁` (plausible, not stated).

**m9. §5, paragraph [C]: "the same proof gives `c_2(BR_m) ≥` …".**  This is a lower bound and comes from
Theorem 11.86 applied to grouped blocks, not from the proof of Theorem H2(a).

---

## 2. What was checked, item by item

### 2.1 Lemma B and the facts of §1 (priority 1)

*Paper check.*  Every step was redone by hand: `k = f + uρ − Λ₁`, `Λ₁ = a + up_u`; (F1) from
`e^{nH}/(n+1) ≤ C(n,d) ≤ e^{nH}`; (F2); (F3) and its threshold `d+1 ≤ (n+1)p_u`; (F4) including
`k_j ≤ d_j* − 1` for `n_j ≥ N_u`; (R); the reflection (parity classes go to parity classes, also for odd `n_j`);
`t_j(e_j) ≤ t_j(k_j) ≤ n_jh + L`; `T(·)` nonincreasing, left-continuous, jumps `≤ |T|L` (several blocks may jump
together, each by `ln((n_j−d)/(d+1)) ≤ ln n_j`); `T(κ) ≤ nφ_Th + mL ≤ Θ₂` (uses `Θ ≥ nh + 2mL`); in case (ii)
`inf{τ: T(τ) ≤ Θ₂}` is not attained, lies in `[0, κ)`, and `Θ₂ − mL < t_T(e) ≤ Θ₂`; `e, e′ ∈ V_P(Θ)`,
`e′, e″ ∈ V_∅(Θ)`; the parities of `w_j` are exactly what (H1), (H2) require; `t_j(w_j) ≤ ln 3`; the Lipschitz
step; the three kinds of terms; the sum `m(u+3L)` and the final `m(u+5L)`.  All correct.  (In case (i) the proof
even gives `m(u+3L)`.)

*Numerics.*
* `r1_facts.py`: (F1)–(F4), (R), `t_j(w_j) ≤ ln 3`, jumps `≤ L`, `t_j(k_j) ≤ n_jh + L`, exactly, every `d`, twelve
  slopes `0.05 … 20`, block sizes `N_u … 2500` (all sizes up to 400): **0 violations** (with `L = ln(n_j+1)`,
  the harder version).  Smallest slack in (F2) `0.78`, in (R) `5.2` nats.
* `r2_lemmaB.py`: for given blocks, roles, `u`, `Θ` the **pointwise largest** `−F` under exactly (adm), (H1),
  (H2) *in the parity version* and `ν₀ ≤ 0` is a shortest-path distance (classes of (H1)/(H2) contracted, edges
  of length `u`, a source at height `t(d)` over `V_∅(Θ)`); validated against a linear programme on 24 tiny
  instances (deviation `9·10⁻¹⁶`).  Lemma B is equivalent to
  `X := max_y[ν*(y) − nφ_Ph + min{t_T(y), Θ − n(1−φ_P)h}] ≤ m(u+5L)`.
  - 4 464 cases at small sizes (all `3^m` role patterns, `m = 2, 3, 4`, block sizes `N_u`, `N_u+1`, `2N_u+1`, …,
    odd and even, `u = 1, 2, 4, 8`, `Θ = nh + 2mL + {0, 0.5, 1.5, 4}·nh`): largest `X = +0.893`; `X − m(u+5L) ≤ −35.9`.
  - 1 113 further cases (`u = 0.25, 0.5, 3, 12`; five blocks): largest `X = +0.863`.
  - scaling at fixed proportions, `Θ = ρ·nh + 2mL`, `ρ ∈ {1, 1.15, 1.3, 2}`: two blocks `n = 500 … 4000`
    (`u = 1, 4`), three blocks `n = 90 … 360`, four blocks `n = 84, 168`: `X ≤ +0.19` everywhere and does **not**
    grow with `n`; in these runs the hidden types satisfy `ν* ≤ ν₀ − (Θ − nh) − 1.7` or better (at `n = 4000`,
    `u = 4`: an extra `−44` to `−953` nats).
  - outside the hypothesis (`Θ = nh` exactly, the author's range): largest `X = +4.99` (`u = 4`, a plain dip at the
    critical budget) — the author's `+4.95` reproduced; the hypothesis `Θ ≥ nh + 2mL` was not needed in any case.
  Observation, not an error: the lemma is far from sharp — the true hidden exponent is about `D(θ)`, not `h − θ`.

### 2.2 Theorem H1 and Algorithm R3 (priority 2)

*Paper check.*  Reveal step (two values, `c^j ∈ {s^j, s̄^j}`); cost `≤ 3(n+1)^{m+1}M`; unbiasedness for any
candidates; `E₁, E₂` (`M·P ≥ e^{ηn/4}`, union over `≤ (n+1)^m` types, conditioning on round 1 for `E₂`); `E₃`
(Chernoff `2e^{−δ²μ/3}`, `δ = ε/8`); `E₄` (conditional Markov); the path argument (order "decreasing blocks
first", unimodality gives cost `≤ max(t(d), t(d′))` for every intermediate type and midpoint, midpoints have the
moving coordinate in `[1, n_j−1]`), also for round 2 in `V_{S₁}(Θ)`; the roles `P = S₁`, `Q = S₂∖S₁`; `A_bad ≤ β_nA`;
the bracket; `Θ ≥ nh + 2mL` for large `n`.  All correct.

*Literal implementation* (`r3_R3_real_cube.py`; energy tables on all `2^n` points, `n = 14 … 20`, blocks
`(10,10), (8,12), (7,7,6), (9,5), (6,6,6), (11,9)`, random non-consecutive known partition, hidden centre; ten
profiles each: random cone envelopes, separable random walks, 2-periodic in every block, cone + 2-periodic,
flat with a dip at a rare type, radial dip, "block 2 visible only deep inside block 1", symmetric cones, parity
of the sum + rare dip, constant):
* T0, exhaustive over every point and block: 44 151 962 revealing (point, block) pairs, always exactly two
  values, candidate always the centre or its antipode.  T1, inside R3: 2 804 475 revealing points, 0 failures.
* T2a, exact unbiasedness identity for the realised `(S₂, candidates)` and for arbitrary wrong candidates:
  1 056 cases, `|E/A − 1| ≤ 2.5·10⁻¹²`.  T2b, statistical (small cubes so that no rare event is missing): 67
  cells × 500 runs, `M = 1, 2, 5`: rms `z = 1.00`, one cell at `|z| = 3.6` (heavy-tailed); re-run with 20 000 runs
  and three seeds (`r3b_unbiased_recheck.py`): `|z| ≤ 2.83` over 18 cells.
* T3: 28 194 runs with all blocks revealed, `|Â/A − 1| ≤ 5·10⁻¹⁵`.
* T4, path argument: with `Θ₁` the largest budget for which `E₁` holds for the realised sample, "`F` sees only `S₁`
  on `V_∅(Θ₁)`" held in all 4 686 samples (292 non-trivial: an unrevealed block and `≥ 20` visible types); the same
  for round 2 (253 non-trivial).  Without the parity qualifier the statement fails 180 and 171 times — the
  parities are indeed needed.
* T5: evaluations `≤ 3(n+1)^{m+1}M` in all 54 186 runs.

### 2.3 Lemma A2 and Theorem H2 (priority 3)

*Paper check.*  (A1): `t(e) ≤ Θ`; `e₂ > y₂`; `(e₁, w₂) ∈ V_∅(Θ) ∩ V_{1}(Θ)`; both brackets; the cases `z = ½`, odd
`n_j`.  (A2): `e ∈ V_{1}(Θ)`, `γ₂(⌈p_un₂⌉) ≤ n₂Λ₁ + u + L`, `y₂/n₂ < y¹ ≤ p_u`, monotonicity of `k` on `[0, p_u]`.
Theorem H2(a): the four cases of `S₁`, `Mp_d ≥ e^{ηn/4}`, the dichotomy from `ϑ = min{φ₂a, root}`.  `Ξ` is
nonincreasing because the feasible set grows with `θ`, and strictly decreasing wherever `Ξ > −φ₂Λ₁`, in
particular near its root; `Ξ(h, φ₁) > 0` by strict convexity of `f`.  The report's `Ξ` (constraint "`≤ θ`") agrees
with the archive's (constraint "`= θ`", `θ < φ₂ ln 2`).  Use of Theorem 11.86: the twins are block-radial on
the given two blocks, Lemma U2 only uses the randomness of the centres (the algorithm may know the blocks), so
the bound holds on `BR_2`; exchanging the blocks gives `ϑ(φ₂)`.  All correct (remarks m8, m9).

*Numerics* (`r4_lemmaA2_H2.py`).  Part A: own evaluation of `Ξ`, its root and `θ₂*` at eight slopes (m4);
`Ξ` nonincreasing on all grids, `Ξ(h, φ₁) > 0`.  Part B: exact extremal function of Lemma A2 (parity version),
168 cases (`u = 1, 2, 4`; `φ₁ = 0.3, 0.5, 0.641, 0.8`; `n = 800, 3200`; `θ` from `h` to `3h`): **0 violations** of
(A1), (A2); the extremal hidden gain `H` changes sign at `θ = ϑ(φ₁)` (`|H| ≤ 2` nats there) and equals
`n·min{Ξ, φ₂k(y¹)}` within `2.3` nats wherever the latter is defined (e.g. `u = 2`, `φ₁ = 0.3`, `n = 3200`, `θ = h`:
`71.2` against `70.6`; at `θ = 1.2h`: `−43.8` against `−44.4`).  This confirms the upper bound and, from the other
side, the archive's gap formula.

### 2.4 Corollary H4, Propositions G, C (priority 4)

See M1–M3.  H4: deduction from Lemma B and Lemma U2 checked on paper.  G: algebra checked symbolically and on
grids; 400 000 random instances of the whole chain (anchor in `D`, distance formula, bound `≤ 0`).  C: both
cases checked on random instances; statement checked on grids at finite slope.

### 2.5 §0, §8, §10 (priority 5)

Overstatements: M1 (barrier), M2/M3 (rows "Beyond blocks"), m1, m2, m3, m8.  The paragraph "What is not
established" in §0 and the hedging in §10 are accurate.

---

## 3. What I did **not** check

* `docs/THEORY_REPORT.md` and everything quoted from it: Theorems 11.25, 11.44/11.45 (taken as given), the proof
  of Theorem 11.86 beyond a reading of U_REPORT §2.2 and the numerical corroboration in 2.3.
* §2 of the report (re-derivation, exact finite-`n` twins, Lean builds), §9, the prior-art paragraph of §10 (the
  arXiv numbers were not looked up).
* The simulation table of §6: the script `h3_…` was read (a faithful type-level emulation of R1–R3 with
  Poisson counts; the table agrees with its output file) but not re-run or re-implemented.
* The modelling steps of §7 (the passage to the small-slope limit model; the accounting of cells; "for two
  rounds the same model gives `0.346a` for every body") — only the stated inequalities were checked.
* Lemma B numerically beyond `n = 4000` (two blocks), `360` (three), `168` (four), `≈ 55` (five), or for `m ≥ 6`;
  Theorem H1 end-to-end at the theorem's `M` (it is asymptotic).
* The files added to the repository during the review (addendum, `h7`–`h12`, Lean files).

---

## 4. Scripts and outputs (`experiments/phase2_hierarchy/review/`, outputs in `out/`)

| command | what | time |
|---|---|---|
| `python3 r1_facts.py` | (F1)–(F4), (R), exact | 7 s |
| `python3 r2_lemmaB.py selftest` | shortest-path construction against an LP | 1 s |
| `python3 r2_lemmaB.py small 1 2 4 8` | Lemma B, 4 464 cases, parity version | 110 s |
| `python3 r2_lemmaB.py scale2 1` / `scale2 4` / `scale3` / `scale4` | scaling in `n` | 351 / 80 / 99 / 24 s |
| `python3 r2_lemmaB.py outside` | `Θ = θnh` (outside the hypothesis), with and without parity | 115 s |
| `python3 r2c_lemmaB_more.py 0.25` / `0.5 3 12` | further slopes, five blocks | 82 / 64 s |
| `python3 r2b_compare_author_output.py` | author's table against exact extremal values | < 10 min |
| `python3 r3_R3_real_cube.py` | R3 literally on real cubes, tests T0–T5 | 337 s |
| `python3 r3b_unbiased_recheck.py` | unbiasedness, 20 000 runs per cell | < 10 min |
| `python3 r4_lemmaA2_H2.py A` / `B` | `Ξ`, thresholds / Lemma A2 extremal | 496 / 336 s |
| `python3 r4b_theta2_precise.py` | `θ₂*` at `u = 2, 4` to six digits | < 1 min |
| `python3 r5_propG_propC.py G` / `C1` / `C2` | Propositions G and C | 12 / 33 / 16 s |
| `python3 r5b_margins_check.py` | the two repairs of M2 and M3, numerically | < 1 min |

`out/r2_lemmaB_scale2_u1_bothparities_partial.txt` is an earlier parameterisation of `scale2` that my own
timeout cut after 51 of 56 lines; its completed lines are valid and agree with the later runs.
